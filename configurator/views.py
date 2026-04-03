from decimal import Decimal

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from my_site_app.models import Case, Cooler, GPU, Motherboard, PowerSupply, Processor, RAM, Storage
from my_site_register.permissions import get_logged_in_user

from .models import PCConfiguration


TAX_RATE = Decimal("0.01")
SESSION_CART_KEY = "cart_items"
SESSION_GUEST_CONFIGS_KEY = "guest_configurations"
PSU_TIERS = [450, 550, 650, 750, 850, 1000, 1200, 1500]


def _selected_id(request, key):
    value = request.POST.get(key) or request.GET.get(key)
    try:
        return int(value) if value else None
    except (TypeError, ValueError):
        return None


def _build_from_request(request):
    processor = Processor.objects.filter(pk=_selected_id(request, "processor")).first()
    gpu = GPU.objects.filter(pk=_selected_id(request, "gpu")).first()
    motherboard = Motherboard.objects.filter(pk=_selected_id(request, "motherboard")).first()
    ram = RAM.objects.filter(pk=_selected_id(request, "ram")).first()
    cooler = Cooler.objects.filter(pk=_selected_id(request, "cooler")).first()
    power_supply = PowerSupply.objects.filter(pk=_selected_id(request, "power_supply")).first()
    case = Case.objects.filter(pk=_selected_id(request, "case")).first()
    storage = Storage.objects.filter(pk=_selected_id(request, "storage")).first()
    return {
        "processor": processor,
        "gpu": gpu,
        "motherboard": motherboard,
        "ram": ram,
        "cooler": cooler,
        "power_supply": power_supply,
        "case": case,
        "storage": storage,
    }


def _recommended_psu(total_power):
    required = int(Decimal(total_power) * Decimal("1.25"))
    for tier in PSU_TIERS:
        if tier >= required:
            return tier
    return 1500


def _price_as_decimal(value):
    return Decimal(str(value or 0))


def _cooler_type_label(cooler):
    return "Liquid Cooling" if cooler.cooler_type == "AIO" else "Air Cooler"


def _calc_preview(build):
    total_power = 0
    total_price = Decimal("0")

    if build["processor"]:
        total_power += int(build["processor"].tdp_max or 0)
        total_price += _price_as_decimal(build["processor"].price)
    if build["gpu"]:
        total_power += int(build["gpu"].power_consumption or 0)
        total_price += _price_as_decimal(build["gpu"].price)
    if build["motherboard"]:
        total_power += int(build["motherboard"].power_consumption or 0)
        total_price += _price_as_decimal(build["motherboard"].price)
    if build["ram"]:
        total_power += int((build["ram"].power_per_module or 0) * (build["ram"].modules or 1))
        total_price += _price_as_decimal(build["ram"].price)
    if build["cooler"]:
        total_power += int(build["cooler"].tdp_capacity or 0)
        total_price += _price_as_decimal(build["cooler"].price)
    if build["storage"]:
        total_power += int(build["storage"].power_consumption or 0)
        total_price += _price_as_decimal(build["storage"].price)
    if build["power_supply"]:
        total_price += _price_as_decimal(build["power_supply"].price)
    if build["case"]:
        total_price += _price_as_decimal(build["case"].price)

    recommended_psu = _recommended_psu(total_power)
    issues = []
    if build["processor"] and build["motherboard"]:
        if build["processor"].socket != build["motherboard"].socket:
            issues.append(f"Socket incompatibility: CPU {build['processor'].socket} != MB {build['motherboard'].socket}")
    if build["ram"] and build["motherboard"]:
        if build["ram"].memory_type != build["motherboard"].ram_type:
            issues.append(f"RAM incompatibility: RAM {build['ram'].memory_type} != MB {build['motherboard'].ram_type}")
    if build["processor"] and build["cooler"]:
        if not build["cooler"].supports_socket(build["processor"].socket):
            issues.append(
                f"Cooler socket mismatch: {build['cooler'].name} does not support {build['processor'].socket}"
            )
        if build["processor"].tdp_max > build["cooler"].tdp_capacity:
            issues.append(
                f"Cooling capacity issue detected: {build['cooler'].name} is rated for {build['cooler'].tdp_capacity}W, "
                f"but {build['processor'].name} can reach {build['processor'].tdp_max}W. "
                f"AI recommendation: choose a cooler with at least {build['processor'].tdp_max}W TDP support."
            )
    if build["power_supply"] and build["power_supply"].wattage < recommended_psu:
        issues.append(f"Insufficient PSU power: {build['power_supply'].wattage}W < {recommended_psu}W")
    if build["gpu"] and build["case"] and build["gpu"].length > build["case"].max_gpu_length:
        issues.append(f"GPU won't fit in case: {build['gpu'].length}mm > {build['case'].max_gpu_length}mm")
    if build["cooler"] and build["case"]:
        if build["cooler"].cooler_type == "AIO" and build["cooler"].radiator_length_mm:
            if build["cooler"].radiator_length_mm > build["case"].max_gpu_length:
                issues.append(
                    f"Case clearance risk detected: {build['cooler'].radiator_length_mm}mm AIO radiator exceeds "
                    f"the case limit of {build['case'].max_gpu_length}mm. "
                    f"AI recommendation: choose a shorter AIO or a larger case."
                )
        elif build["cooler"].height_mm and build["cooler"].height_mm > build["case"].max_cpu_cooler_height:
            issues.append(
                f"Cooler too tall: {build['cooler'].height_mm}mm > {build['case'].max_cpu_cooler_height}mm allowed height"
            )

    tax = total_price * TAX_RATE
    grand_total = total_price + tax

    return {
        "issues": issues,
        "total_power": total_power,
        "recommended_psu": recommended_psu,
        "max_power": 1200,
        "power_percent": min((total_power / 1200) * 100, 100),
        "total_price": total_price,
        "tax": tax,
        "grand_total": grand_total,
    }


def _image_url(obj):
    if getattr(obj, "image", None):
        try:
            return obj.image.url
        except ValueError:
            return ""
    return ""


def _component_payload():
    return {
        "processor": [
            {
                "id": x.id,
                "name": x.name,
                "price": float(x.price),
                "image": _image_url(x),
                "subtitle": f"{x.socket} / {x.cores}C {x.threads}T",
                "power": int(x.tdp_max or 0),
                "socket": x.socket,
                "tdp_max": int(x.tdp_max or 0),
            }
            for x in Processor.objects.all()
        ],
        "gpu": [
            {
                "id": x.id,
                "name": x.name,
                "price": float(x.price),
                "image": _image_url(x),
                "subtitle": f"{x.vram}GB {x.vram_type}",
                "power": int(x.power_consumption or 0),
            }
            for x in GPU.objects.all()
        ],
        "motherboard": [
            {
                "id": x.id,
                "name": x.name,
                "price": float(x.price),
                "image": _image_url(x),
                "subtitle": f"{x.socket} / {x.get_form_factor_display()}",
                "power": int(x.power_consumption or 0),
                "socket": x.socket,
                "ram_type": x.ram_type,
            }
            for x in Motherboard.objects.all()
        ],
        "ram": [
            {
                "id": x.id,
                "name": x.name,
                "price": float(x.price),
                "image": _image_url(x),
                "subtitle": f"{x.total_capacity}GB {x.memory_type}",
                "power": int((x.power_per_module or 0) * (x.modules or 1)),
                "memory_type": x.memory_type,
            }
            for x in RAM.objects.all()
        ],
        "cooler": [
            {
                "id": x.id,
                "name": x.name,
                "price": float(x.price),
                "image": _image_url(x),
                "subtitle": f"{_cooler_type_label(x)} / TDP {x.tdp_capacity} W",
                "power": int(x.tdp_capacity or 0),
                "cooler_type": x.cooler_type,
                "supported_sockets": x.supported_sockets_list,
                "tdp_capacity": int(x.tdp_capacity or 0),
                "height_mm": int(x.height_mm or 0),
                "radiator_length_mm": int(x.radiator_length_mm or 0),
            }
            for x in Cooler.objects.all()
        ],
        "storage": [
            {
                "id": x.id,
                "name": x.name,
                "price": float(x.price),
                "image": _image_url(x),
                "subtitle": f"{x.capacity}GB {x.storage_type}",
                "power": int(x.power_consumption or 0),
            }
            for x in Storage.objects.all()
        ],
        "power_supply": [
            {
                "id": x.id,
                "name": x.name,
                "price": float(x.price),
                "image": _image_url(x),
                "subtitle": f"{x.wattage}W {x.get_efficiency_display()}",
                "power": 0,
                "wattage": int(x.wattage or 0),
            }
            for x in PowerSupply.objects.all()
        ],
        "case": [
            {
                "id": x.id,
                "name": x.name,
                "price": float(x.price),
                "image": _image_url(x),
                "subtitle": f"{x.get_form_factor_display()} / {x.max_gpu_length}mm GPU",
                "power": 0,
                "max_gpu_length": int(x.max_gpu_length or 0),
                "max_cpu_cooler_height": int(x.max_cpu_cooler_height or 0),
            }
            for x in Case.objects.all()
        ],
    }


def _add_to_session_cart(request, item):
    cart = request.session.get(SESSION_CART_KEY, [])
    for existing in cart:
        if existing["id"] == item["id"]:
            existing["quantity"] += 1
            request.session[SESSION_CART_KEY] = cart
            return
    cart.append({**item, "quantity": 1})
    request.session[SESSION_CART_KEY] = cart


def _configuration_queryset_for(request):
    user = get_logged_in_user(request)
    if user:
        return PCConfiguration.objects.filter(user=user)

    guest_ids = request.session.get(SESSION_GUEST_CONFIGS_KEY, [])
    return PCConfiguration.objects.filter(pk__in=guest_ids)


class ConfiguratorView(View):
    def get(self, request):
        loaded = None
        load_id = request.GET.get("load")
        if load_id:
            loaded = _configuration_queryset_for(request).filter(pk=load_id).first()

        initial = {
            "processor": loaded.processor if loaded else None,
            "gpu": loaded.gpu if loaded else None,
            "motherboard": loaded.motherboard if loaded else None,
            "ram": loaded.ram if loaded else None,
            "cooler": loaded.cooler if loaded else None,
            "power_supply": loaded.power_supply if loaded else None,
            "case": loaded.case if loaded else None,
            "storage": loaded.storage_devices.first() if loaded else None,
        }
        preview = _calc_preview(initial)
        context = {
            "processors": Processor.objects.all(),
            "gpus": GPU.objects.all(),
            "motherboards": Motherboard.objects.all(),
            "ram_modules": RAM.objects.all(),
            "coolers": Cooler.objects.all(),
            "storages": Storage.objects.all(),
            "power_supplies": PowerSupply.objects.all(),
            "cases": Case.objects.all(),
            "selected": initial,
            "config_name": loaded.name if loaded else "My Gaming Build",
            "preview": preview,
            "saved_configurations": _configuration_queryset_for(request)[:20],
            "loaded_id": loaded.pk if loaded else None,
            "component_payload": _component_payload(),
        }
        return render(request, "configurator/configurator.html", context)

    def post(self, request):
        selected = _build_from_request(request)
        preview = _calc_preview(selected)
        context = {
            "processors": Processor.objects.all(),
            "gpus": GPU.objects.all(),
            "motherboards": Motherboard.objects.all(),
            "ram_modules": RAM.objects.all(),
            "coolers": Cooler.objects.all(),
            "storages": Storage.objects.all(),
            "power_supplies": PowerSupply.objects.all(),
            "cases": Case.objects.all(),
            "selected": selected,
            "config_name": request.POST.get("config_name", "My Gaming Build"),
            "preview": preview,
            "saved_configurations": _configuration_queryset_for(request)[:20],
            "loaded_id": None,
            "component_payload": _component_payload(),
        }
        return render(request, "configurator/configurator.html", context)


class SaveConfigurationView(View):
    def post(self, request):
        selected = _build_from_request(request)
        cfg = PCConfiguration.objects.create(
            user=get_logged_in_user(request),
            name=(request.POST.get("config_name") or "My Build").strip()[:200],
            processor=selected["processor"],
            gpu=selected["gpu"],
            motherboard=selected["motherboard"],
            ram=selected["ram"],
            cooler=selected["cooler"],
            power_supply=selected["power_supply"],
            case=selected["case"],
        )
        if selected["storage"]:
            cfg.storage_devices.set([selected["storage"]])

        if not get_logged_in_user(request):
            guest = request.session.get(SESSION_GUEST_CONFIGS_KEY, [])
            if cfg.pk not in guest:
                guest.append(cfg.pk)
                request.session[SESSION_GUEST_CONFIGS_KEY] = guest

        messages.success(request, "Configuration saved.")
        return redirect("saved_configurations")


class AddCurrentBuildToCartView(View):
    def post(self, request):
        selected = _build_from_request(request)
        for component in selected.values():
            if not component:
                continue
            image = component.image.url if getattr(component, "image", None) else ""
            _add_to_session_cart(
                request,
                {
                    "id": f"{component._meta.model_name}-{component.pk}",
                    "name": component.name,
                    "price": float(component.price),
                    "image": image,
                    "category": "PC Build",
                },
            )
        messages.success(request, "Build added to cart.")
        return redirect("configurator")


class SavedConfigurationsView(View):
    def get(self, request):
        return render(
            request,
            "configurator/saved_configurations.html",
            {"configurations": _configuration_queryset_for(request)},
        )


class AddSavedConfigurationToCartView(View):
    def post(self, request, pk):
        cfg = get_object_or_404(_configuration_queryset_for(request), pk=pk)
        components = [
            cfg.processor,
            cfg.gpu,
            cfg.motherboard,
            cfg.ram,
            cfg.cooler,
            cfg.power_supply,
            cfg.case,
            *list(cfg.storage_devices.all()),
        ]
        for component in components:
            if not component:
                continue
            image = component.image.url if getattr(component, "image", None) else ""
            _add_to_session_cart(
                request,
                {
                    "id": f"{cfg.pk}-{component._meta.model_name}-{component.pk}",
                    "name": component.name,
                    "price": float(component.price),
                    "image": image,
                    "category": "Saved Build",
                },
            )
        messages.success(request, "Saved configuration added to cart.")
        return redirect("saved_configurations")


class DeleteSavedConfigurationView(View):
    def post(self, request, pk):
        cfg = get_object_or_404(_configuration_queryset_for(request), pk=pk)
        cfg.delete()
        messages.success(request, "Configuration deleted.")
        return redirect("saved_configurations")
