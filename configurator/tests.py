from django.test import TestCase
from django.urls import reverse

from configurator.models import PCConfiguration
from configurator.views import _calc_preview
from my_site_app.models import Case, Cooler, Processor


class CoolerCompatibilityTests(TestCase):
    def create_processor(self, name="Ryzen 7 Test", socket="AM5", tdp_max=180):
        return Processor.objects.create(
            name=name,
            manufacturer="AMD",
            socket=socket,
            cores=8,
            threads=16,
            base_clock=4.2,
            boost_clock=5.0,
            tdp_base=120,
            tdp_max=tdp_max,
            description="Test processor",
            price=299.99,
            stock=10,
        )

    def create_cooler(
        self,
        name="Test Cooler",
        cooler_type="AIR",
        tdp_capacity=220,
        supported_sockets="AM5, LGA1700",
        height_mm=155,
        radiator_length_mm=None,
    ):
        return Cooler.objects.create(
            name=name,
            manufacturer="Cooler Master",
            cooler_type=cooler_type,
            supported_sockets=supported_sockets,
            tdp_capacity=tdp_capacity,
            height_mm=height_mm,
            radiator_length_mm=radiator_length_mm,
            description="Test cooler",
            price=79.99,
            stock=8,
        )

    def create_case(self, name="Test Case", max_gpu_length=320, max_cpu_cooler_height=165):
        return Case.objects.create(
            name=name,
            manufacturer="NZXT",
            form_factor="ATX",
            max_gpu_length=max_gpu_length,
            max_cpu_cooler_height=max_cpu_cooler_height,
            fan_slots=6,
            included_fans=2,
            description="Test case",
            price=109.99,
            stock=6,
        )

    def test_pc_configuration_marks_weak_cooler_as_issue(self):
        processor = self.create_processor(tdp_max=253)
        cooler = self.create_cooler(tdp_capacity=180)

        config = PCConfiguration.objects.create(name="Hot Build", processor=processor, cooler=cooler)

        issues = config.check_compatibility()

        self.assertTrue(any("AI-анализ охлаждения" in issue for issue in issues))

    def test_preview_detects_aio_radiator_longer_than_case(self):
        processor = self.create_processor()
        cooler = self.create_cooler(
            name="360 AIO",
            cooler_type="AIO",
            height_mm=None,
            radiator_length_mm=360,
        )
        build_case = self.create_case(max_gpu_length=330)

        preview = _calc_preview(
            {
                "processor": processor,
                "gpu": None,
                "motherboard": None,
                "ram": None,
                "cooler": cooler,
                "power_supply": None,
                "case": build_case,
                "storage": None,
            }
        )

        self.assertEqual(preview["total_power"], processor.tdp_max + cooler.tdp_capacity)
        self.assertTrue(any("Радиатор СЖО слишком длинный" in issue for issue in preview["issues"]))

    def test_save_configuration_persists_selected_cooler(self):
        processor = self.create_processor()
        cooler = self.create_cooler()

        response = self.client.post(
            reverse("save_configuration"),
            {
                "config_name": "My cooled build",
                "processor": processor.pk,
                "cooler": cooler.pk,
            },
        )

        self.assertEqual(response.status_code, 302)
        config = PCConfiguration.objects.get(name="My cooled build")
        self.assertEqual(config.cooler, cooler)
