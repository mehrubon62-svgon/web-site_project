import json
import random
import urllib.parse
import urllib.request
from urllib.error import URLError, HTTPError

from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from my_site_app.models import Case, Cooler, GPU, Laptop, Motherboard, PowerSupply, Processor, ProductImage, RAM, Storage


def _open_url(url, timeout=25):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X) BuildBoxSeeder/1.0",
            "Accept": "*/*",
        },
    )
    return urllib.request.urlopen(req, timeout=timeout)


def _download_image(image_url):
    try:
        with _open_url(image_url, timeout=25) as image_resp:
            image_bytes = image_resp.read()
    except (URLError, HTTPError):
        return None, None

    ext = image_url.split(".")[-1].lower().split("?")[0]
    if ext not in {"jpg", "jpeg", "png", "webp"}:
        ext = "jpg"
    return image_bytes, ext


def _fetch_from_wikimedia_commons(query):
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": 5,
            "srnamespace": 6,
            "format": "json",
        }
    )
    search_url = f"https://commons.wikimedia.org/w/api.php?{params}"
    try:
        with _open_url(search_url, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (URLError, HTTPError):
        return None, None

    results = (data.get("query") or {}).get("search") or []
    for result in results:
        title = result.get("title", "")
        if not title.startswith("File:"):
            continue
        file_name = title[len("File:"):]
        file_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{urllib.parse.quote(file_name)}"
        image_bytes, ext = _download_image(file_url)
        if image_bytes:
            return image_bytes, ext
    return None, None


def _fetch_from_wikipedia_page_image(query):
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "generator": "search",
            "gsrsearch": query,
            "gsrlimit": 1,
            "prop": "pageimages",
            "piprop": "original",
            "format": "json",
        }
    )
    url = f"https://en.wikipedia.org/w/api.php?{params}"
    try:
        with _open_url(url, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (URLError, HTTPError):
        return None, None

    pages = (data.get("query") or {}).get("pages") or {}
    if not pages:
        return None, None
    page = next(iter(pages.values()))
    original = page.get("original") or {}
    image_url = original.get("source")
    if not image_url:
        return None, None
    return _download_image(image_url)


def _attach_image_if_missing(obj, query):
    if obj.image:
        return

    try_queries = [
        query,
        f"{query} product photo",
        f"{query} hardware",
    ]

    image_bytes = None
    ext = None
    for q in try_queries:
        image_bytes, ext = _fetch_from_wikimedia_commons(q)
        if image_bytes:
            break
        image_bytes, ext = _fetch_from_wikipedia_page_image(q)
        if image_bytes:
            break

    if not image_bytes:
        return
    filename = f"{obj.__class__.__name__.lower()}_{obj.pk}.{ext}"
    obj.image.save(filename, ContentFile(image_bytes), save=True)


def _attach_gallery_images(obj, query, count=3):
    content_type = ContentType.objects.get_for_model(obj.__class__)
    if ProductImage.objects.filter(content_type=content_type, object_id=obj.pk).exists():
        return

    queries = [
        query,
        f"{query} product photo",
        f"{query} pc hardware closeup",
        f"{obj.__class__.__name__} computer component",
    ]
    seen = set()
    order = 1
    for q in queries:
        if order > count:
            break
        for fetcher in (_fetch_from_wikimedia_commons, _fetch_from_wikipedia_page_image):
            image_bytes, ext = fetcher(q)
            if not image_bytes:
                continue
            key = hash(image_bytes[:64])
            if key in seen:
                continue
            seen.add(key)
            img = ProductImage(
                content_type=content_type,
                object_id=obj.pk,
                order=order,
                is_main=(order == 1),
            )
            img.image.save(
                f"{obj.__class__.__name__.lower()}_{obj.pk}_gallery_{order}.{ext}",
                ContentFile(image_bytes),
                save=True,
            )
            order += 1
            if order > count:
                break


class Command(BaseCommand):
    help = "Seed catalog with real component models and download photos from Wikimedia Commons."

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true", help="Clear existing products first")

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(self.style.WARNING("Clearing existing products..."))
            Processor.objects.all().delete()
            GPU.objects.all().delete()
            RAM.objects.all().delete()
            Motherboard.objects.all().delete()
            Storage.objects.all().delete()
            PowerSupply.objects.all().delete()
            Case.objects.all().delete()
            Cooler.objects.all().delete()
            Laptop.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Done."))

        processors = [
            ("Intel Core i5-13600K", "Intel", "LGA1700", 14, 20, 3.5, 5.1, 125, 181, 299.99),
            ("Intel Core i7-14700K", "Intel", "LGA1700", 20, 28, 3.4, 5.6, 125, 253, 409.99),
            ("AMD Ryzen 5 7600X", "AMD", "AM5", 6, 12, 4.7, 5.3, 105, 142, 229.99),
            ("AMD Ryzen 7 7800X3D", "AMD", "AM5", 8, 16, 4.2, 5.0, 120, 162, 379.99),
        ]
        for name, manufacturer, socket, cores, threads, base, boost, tdp_b, tdp_m, price in processors:
            obj, _ = Processor.objects.get_or_create(
                name=name,
                defaults={
                    "manufacturer": manufacturer,
                    "socket": socket,
                    "cores": cores,
                    "threads": threads,
                    "base_clock": base,
                    "boost_clock": boost,
                    "tdp_base": tdp_b,
                    "tdp_max": tdp_m,
                    "description": f"{name} desktop processor.",
                    "price": price,
                    "stock": random.randint(8, 35),
                },
            )
            _attach_image_if_missing(obj, name)
            _attach_gallery_images(obj, name)

        gpus = [
            ("NVIDIA GeForce RTX 4070 Super", "NVIDIA", "RTX 4070 Super", 12, "GDDR6X", 220, 650, 2, 300, 599.99),
            ("NVIDIA GeForce RTX 4080 Super", "NVIDIA", "RTX 4080 Super", 16, "GDDR6X", 320, 750, 3, 320, 999.99),
            ("AMD Radeon RX 7800 XT", "AMD", "RX 7800 XT", 16, "GDDR6", 263, 700, 2, 300, 499.99),
            ("AMD Radeon RX 7900 XTX", "AMD", "RX 7900 XTX", 24, "GDDR6", 355, 850, 3, 330, 949.99),
        ]
        for name, manufacturer, chipset, vram, vram_type, pwr, psu, slots, length, price in gpus:
            obj, _ = GPU.objects.get_or_create(
                name=name,
                defaults={
                    "manufacturer": manufacturer,
                    "chipset": chipset,
                    "vram": vram,
                    "vram_type": vram_type,
                    "power_consumption": pwr,
                    "recommended_psu": psu,
                    "pcie_slots": slots,
                    "length": length,
                    "description": f"{name} graphics card.",
                    "price": price,
                    "stock": random.randint(4, 20),
                },
            )
            _attach_image_if_missing(obj, name)
            _attach_gallery_images(obj, name)

        ram_items = [
            ("Corsair Vengeance DDR5 6000", "Corsair", "DDR5", 16, 2, 6000, 129.99),
            ("G.Skill Trident Z5 DDR5 6400", "G.Skill", "DDR5", 16, 2, 6400, 149.99),
            ("Kingston Fury Beast DDR4 3600", "Kingston", "DDR4", 16, 2, 3600, 89.99),
        ]
        for name, manufacturer, mem_type, cap, mods, speed, price in ram_items:
            obj, _ = RAM.objects.get_or_create(
                name=name,
                defaults={
                    "manufacturer": manufacturer,
                    "memory_type": mem_type,
                    "capacity": cap,
                    "modules": mods,
                    "speed": speed,
                    "power_per_module": 5,
                    "description": f"{name} memory kit.",
                    "price": price,
                    "stock": random.randint(10, 40),
                },
            )
            _attach_image_if_missing(obj, f"{name} RAM")
            _attach_gallery_images(obj, f"{name} RAM")

        boards = [
            ("ASUS ROG Strix B650E-F", "ASUS", "AM5", "B650", "ATX", "DDR5", 299.99),
            ("MSI MAG B760 Tomahawk", "MSI", "LGA1700", "B760", "ATX", "DDR5", 219.99),
        ]
        for name, manufacturer, socket, chipset, form, ram_type, price in boards:
            obj, _ = Motherboard.objects.get_or_create(
                name=name,
                defaults={
                    "manufacturer": manufacturer,
                    "socket": socket,
                    "chipset": chipset,
                    "form_factor": form,
                    "ram_type": ram_type,
                    "ram_slots": 4,
                    "max_ram": 128,
                    "m2_slots": 3,
                    "sata_ports": 6,
                    "pcie_x16_slots": 2,
                    "power_consumption": 80,
                    "description": f"{name} motherboard.",
                    "price": price,
                    "stock": random.randint(6, 25),
                },
            )
            _attach_image_if_missing(obj, f"{name} motherboard")
            _attach_gallery_images(obj, f"{name} motherboard")

        storages = [
            ("Samsung 990 PRO 1000GB", "Samsung", "NVME", 1000, 7450, 6900, 8, 129.99),
            ("WD Black SN850X 2000GB", "WD", "NVME", 2000, 7300, 6600, 8, 179.99),
            ("Crucial MX500 1000GB", "Crucial", "SATA_SSD", 1000, 560, 510, 4, 74.99),
        ]
        for name, manufacturer, s_type, cap, read_s, write_s, pwr, price in storages:
            obj, _ = Storage.objects.get_or_create(
                name=name,
                defaults={
                    "manufacturer": manufacturer,
                    "storage_type": s_type,
                    "capacity": cap,
                    "read_speed": read_s,
                    "write_speed": write_s,
                    "power_consumption": pwr,
                    "description": f"{name} storage drive.",
                    "price": price,
                    "stock": random.randint(12, 45),
                },
            )
            _attach_image_if_missing(obj, f"{name} SSD")
            _attach_gallery_images(obj, f"{name} SSD")

        psus = [
            ("Corsair RM750e", "Corsair", 750, "GOLD", True, 109.99),
            ("Seasonic Focus GX-850", "Seasonic", 850, "GOLD", True, 139.99),
        ]
        for name, manufacturer, watt, eff, modular, price in psus:
            obj, _ = PowerSupply.objects.get_or_create(
                name=name,
                defaults={
                    "manufacturer": manufacturer,
                    "wattage": watt,
                    "efficiency": eff,
                    "modular": modular,
                    "description": f"{name} power supply.",
                    "price": price,
                    "stock": random.randint(7, 30),
                },
            )
            _attach_image_if_missing(obj, f"{name} power supply")
            _attach_gallery_images(obj, f"{name} power supply")

        cases = [
            ("NZXT H7 Flow", "NZXT", "ATX", 400, 185, 7, 3, 129.99),
            ("Corsair 4000D Airflow", "Corsair", "ATX", 360, 170, 6, 2, 104.99),
        ]
        for name, manufacturer, form, gpu_len, cpu_h, fan_slots, included, price in cases:
            obj, _ = Case.objects.get_or_create(
                name=name,
                defaults={
                    "manufacturer": manufacturer,
                    "form_factor": form,
                    "max_gpu_length": gpu_len,
                    "max_cpu_cooler_height": cpu_h,
                    "fan_slots": fan_slots,
                    "included_fans": included,
                    "description": f"{name} PC case.",
                    "price": price,
                    "stock": random.randint(9, 35),
                },
            )
            _attach_image_if_missing(obj, f"{name} computer case")
            _attach_gallery_images(obj, f"{name} computer case")

        coolers = [
            ("Noctua NH-D15", "Noctua", "AIR", "AM5, LGA1700", 220, 165, None, 109.99),
            ("DeepCool AK620", "DeepCool", "AIR", "AM5, LGA1700", 260, 160, None, 64.99),
            ("Arctic Liquid Freezer III 360", "Arctic", "AIO", "AM5, LGA1700", 320, None, 360, 139.99),
        ]
        for name, manufacturer, cooler_type, sockets, tdp_capacity, height_mm, radiator_length_mm, price in coolers:
            obj, _ = Cooler.objects.get_or_create(
                name=name,
                defaults={
                    "manufacturer": manufacturer,
                    "cooler_type": cooler_type,
                    "supported_sockets": sockets,
                    "tdp_capacity": tdp_capacity,
                    "height_mm": height_mm,
                    "radiator_length_mm": radiator_length_mm,
                    "description": f"{name} кулер для процессора.",
                    "price": price,
                    "stock": random.randint(6, 25),
                },
            )
            _attach_image_if_missing(obj, f"{name} cpu cooler")
            _attach_gallery_images(obj, f"{name} cpu cooler")

        laptops = [
            ("ASUS ROG Zephyrus G16", "ASUS", "GAMING", "Intel Core Ultra 9", "RTX 4070", 16, "DDR5", 1000, "NVMe SSD", 16.0, "2560x1600", 240, 1.9, 90, 180, 1899.99),
            ("Lenovo Legion 5 Pro", "Lenovo", "GAMING", "Ryzen 7 8845HS", "RTX 4060", 16, "DDR5", 1000, "NVMe SSD", 16.0, "2560x1600", 165, 2.5, 80, 170, 1499.99),
        ]
        for (
            name, manufacturer, category, cpu, gpu, ram_size, ram_type, storage_size, storage_type,
            screen_size, resolution, hz, weight, battery, power, price
        ) in laptops:
            obj, _ = Laptop.objects.get_or_create(
                name=name,
                defaults={
                    "manufacturer": manufacturer,
                    "category": category,
                    "processor_name": cpu,
                    "gpu_name": gpu,
                    "ram_size": ram_size,
                    "ram_type": ram_type,
                    "storage_size": storage_size,
                    "storage_type": storage_type,
                    "screen_size": screen_size,
                    "screen_resolution": resolution,
                    "screen_refresh_rate": hz,
                    "weight": weight,
                    "battery_capacity": battery,
                    "power_consumption": power,
                    "description": f"{name} laptop.",
                    "price": price,
                    "stock": random.randint(3, 16),
                },
            )
            _attach_image_if_missing(obj, name)
            _attach_gallery_images(obj, name)

        self.stdout.write(self.style.SUCCESS("Seed complete: real model names + attempted real photos from Wikimedia Commons."))
