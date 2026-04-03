from django.core.management.base import BaseCommand
from my_site_app.models import Processor, GPU, RAM, Motherboard, Storage, PowerSupply, Case, Cooler, Laptop
from faker import Faker
import random

fake = Faker()


class Command(BaseCommand):
    help = 'Populate database with test data'

    def add_arguments(self, parser):
        parser.add_argument('--processors', type=int, default=10, help='Number of processors to create')
        parser.add_argument('--gpus', type=int, default=10, help='Number of GPUs to create')
        parser.add_argument('--ram', type=int, default=10, help='Number of RAM modules to create')
        parser.add_argument('--motherboards', type=int, default=10, help='Number of motherboards to create')
        parser.add_argument('--storage', type=int, default=10, help='Number of storage devices to create')
        parser.add_argument('--psu', type=int, default=10, help='Number of power supplies to create')
        parser.add_argument('--cases', type=int, default=10, help='Number of cases to create')
        parser.add_argument('--coolers', type=int, default=10, help='Number of coolers to create')
        parser.add_argument('--laptops', type=int, default=10, help='Number of laptops to create')
        parser.add_argument('--clear', action='store_true', help='Clear existing data before creating new')
        parser.add_argument('--all', type=int, help='Create N of each type')

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Processor.objects.all().delete()
            GPU.objects.all().delete()
            RAM.objects.all().delete()
            Motherboard.objects.all().delete()
            Storage.objects.all().delete()
            PowerSupply.objects.all().delete()
            Case.objects.all().delete()
            Cooler.objects.all().delete()
            Laptop.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✓ Data cleared'))

        if options['all']:
            count = options['all']
            options['processors'] = count
            options['gpus'] = count
            options['ram'] = count
            options['motherboards'] = count
            options['storage'] = count
            options['psu'] = count
            options['cases'] = count
            options['coolers'] = count
            options['laptops'] = count

        self.stdout.write(self.style.SUCCESS('\nCreating test data...'))
        self.stdout.write('━' * 50)

        # Create processors
        self.create_processors(options['processors'])
        
        # Create GPUs
        self.create_gpus(options['gpus'])
        
        # Create RAM
        self.create_ram(options['ram'])
        
        # Create Motherboards
        self.create_motherboards(options['motherboards'])
        
        # Create Storage
        self.create_storage(options['storage'])
        
        # Create Power Supplies
        self.create_power_supplies(options['psu'])
        
        # Create Cases
        self.create_cases(options['cases'])

        # Create Coolers
        self.create_coolers(options['coolers'])
        
        # Create Laptops
        self.create_laptops(options['laptops'])

        total = sum([
            options['processors'], options['gpus'], options['ram'],
            options['motherboards'], options['storage'], options['psu'],
            options['cases'], options['coolers'], options['laptops']
        ])

        self.stdout.write('━' * 50)
        self.stdout.write(self.style.SUCCESS(f'\n✓ Total: {total} products created successfully!\n'))

    def create_processors(self, count):
        intel_series = ['Core i5-13400', 'Core i5-13600K', 'Core i7-13700K', 'Core i9-13900K', 'Core i9-13900KS']
        amd_series = ['Ryzen 5 7600X', 'Ryzen 7 7700X', 'Ryzen 7 7800X3D', 'Ryzen 9 7900X', 'Ryzen 9 7950X']
        
        for i in range(count):
            is_intel = random.choice([True, False])
            
            if is_intel:
                manufacturer = 'Intel'
                name = random.choice(intel_series)
                socket = 'LGA1700'
            else:
                manufacturer = 'AMD'
                name = random.choice(amd_series)
                socket = 'AM5'
            
            cores = random.choice([6, 8, 12, 16, 24])
            threads = cores * 2
            base_clock = round(random.uniform(3.0, 4.5), 1)
            boost_clock = round(base_clock + random.uniform(0.8, 1.5), 1)
            tdp_base = random.choice([65, 95, 105, 125])
            tdp_max = tdp_base + random.randint(50, 125)
            price = round(random.uniform(150, 700), 2)
            stock = 0 if random.random() < 0.2 else random.randint(5, 50)
            
            Processor.objects.create(
                name=name,
                manufacturer=manufacturer,
                socket=socket,
                cores=cores,
                threads=threads,
                base_clock=base_clock,
                boost_clock=boost_clock,
                tdp_base=tdp_base,
                tdp_max=tdp_max,
                description=f"High-performance {manufacturer} processor with {cores} cores and {threads} threads. Perfect for gaming and productivity.",
                price=price,
                stock=stock
            )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {count} Processors'))

    def create_gpus(self, count):
        nvidia_chips = ['RTX 4090', 'RTX 4080', 'RTX 4070 Ti', 'RTX 4070', 'RTX 4060 Ti']
        amd_chips = ['RX 7900 XTX', 'RX 7900 XT', 'RX 7800 XT', 'RX 7700 XT', 'RX 7600']
        brands = ['ASUS', 'MSI', 'Gigabyte', 'EVGA', 'Zotac']
        
        for i in range(count):
            is_nvidia = random.choice([True, True, False])  # 66% NVIDIA
            
            if is_nvidia:
                manufacturer_base = 'NVIDIA'
                chipset = random.choice(nvidia_chips)
                vram_type = 'GDDR6X' if '4090' in chipset or '4080' in chipset else 'GDDR6'
            else:
                manufacturer_base = 'AMD'
                chipset = random.choice(amd_chips)
                vram_type = 'GDDR6'
            
            brand = random.choice(brands)
            manufacturer = f"{brand} {manufacturer_base}"
            
            vram = random.choice([8, 12, 16, 24])
            power = random.randint(200, 450)
            recommended_psu = power + random.randint(200, 350)
            pcie_slots = random.choice([2, 3])
            length = random.randint(280, 350)
            price = round(random.uniform(300, 1800), 2)
            stock = 0 if random.random() < 0.2 else random.randint(3, 30)
            
            GPU.objects.create(
                name=f"{brand} {chipset}",
                manufacturer=manufacturer,
                chipset=chipset,
                vram=vram,
                vram_type=vram_type,
                power_consumption=power,
                recommended_psu=recommended_psu,
                pcie_slots=pcie_slots,
                length=length,
                description=f"Powerful graphics card featuring {vram}GB {vram_type} memory. Ideal for 4K gaming and content creation.",
                price=price,
                stock=stock
            )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {count} GPUs'))

    def create_ram(self, count):
        manufacturers = ['Corsair', 'G.Skill', 'Kingston', 'Crucial', 'TeamGroup']
        series = ['Vengeance', 'Trident Z', 'Fury', 'Ballistix', 'Elite']
        
        for i in range(count):
            manufacturer = random.choice(manufacturers)
            series_name = random.choice(series)
            memory_type = random.choice(['DDR4', 'DDR5'])
            capacity = random.choice([8, 16, 32])
            modules = random.choice([1, 2, 4])
            
            if memory_type == 'DDR4':
                speed = random.choice([3200, 3600])
            else:
                speed = random.choice([4800, 5200, 5600, 6000, 6400])
            
            price = round(capacity * modules * (0.8 if memory_type == 'DDR4' else 1.2) * random.uniform(2, 4), 2)
            stock = 0 if random.random() < 0.2 else random.randint(10, 100)
            
            RAM.objects.create(
                name=f"{series_name} {memory_type} {speed}MHz",
                manufacturer=manufacturer,
                memory_type=memory_type,
                capacity=capacity,
                modules=modules,
                speed=speed,
                power_per_module=5,
                description=f"High-speed {memory_type} memory kit with {capacity}GB per module. Total capacity: {capacity * modules}GB.",
                price=price,
                stock=stock
            )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {count} RAM modules'))

    def create_motherboards(self, count):
        manufacturers = ['ASUS', 'MSI', 'Gigabyte', 'ASRock']
        intel_chipsets = ['Z790', 'B760', 'H610']
        amd_chipsets = ['X670', 'B650', 'A620']
        
        for i in range(count):
            manufacturer = random.choice(manufacturers)
            is_intel = random.choice([True, False])
            
            if is_intel:
                socket = 'LGA1700'
                chipset = random.choice(intel_chipsets)
            else:
                socket = 'AM5'
                chipset = random.choice(amd_chipsets)
            
            form_factor = random.choice(['ATX', 'ATX', 'MICRO_ATX', 'MINI_ITX'])
            ram_type = random.choice(['DDR4', 'DDR5'])
            ram_slots = 4 if form_factor in ['ATX', 'MICRO_ATX'] else 2
            max_ram = 128 if form_factor == 'ATX' else 64
            m2_slots = random.randint(2, 4)
            sata_ports = random.randint(4, 8)
            pcie_x16_slots = random.randint(1, 3)
            
            price = round(random.uniform(100, 600), 2)
            stock = 0 if random.random() < 0.2 else random.randint(5, 40)
            
            Motherboard.objects.create(
                name=f"{manufacturer} {chipset} {form_factor}",
                manufacturer=manufacturer,
                socket=socket,
                chipset=chipset,
                form_factor=form_factor,
                ram_type=ram_type,
                ram_slots=ram_slots,
                max_ram=max_ram,
                m2_slots=m2_slots,
                sata_ports=sata_ports,
                pcie_x16_slots=pcie_x16_slots,
                power_consumption=80,
                description=f"{form_factor} motherboard with {chipset} chipset. Supports {ram_type} memory up to {max_ram}GB.",
                price=price,
                stock=stock
            )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {count} Motherboards'))

    def create_storage(self, count):
        manufacturers = ['Samsung', 'WD', 'Crucial', 'Kingston', 'Seagate']
        
        for i in range(count):
            manufacturer = random.choice(manufacturers)
            storage_type = random.choice(['NVME', 'NVME', 'SATA_SSD', 'HDD'])
            capacity = random.choice([256, 512, 1000, 2000, 4000])
            
            if storage_type == 'NVME':
                read_speed = random.randint(3500, 7000)
                write_speed = random.randint(3000, 6000)
                power = random.randint(5, 8)
                series = '980 PRO' if manufacturer == 'Samsung' else 'Black SN850'
            elif storage_type == 'SATA_SSD':
                read_speed = random.randint(500, 550)
                write_speed = random.randint(450, 520)
                power = random.randint(3, 5)
                series = '870 EVO' if manufacturer == 'Samsung' else 'Blue'
            else:  # HDD
                read_speed = random.randint(150, 200)
                write_speed = random.randint(120, 180)
                power = random.randint(6, 10)
                series = 'BarraCuda'
            
            price = round(capacity * (0.15 if storage_type == 'NVME' else 0.08 if storage_type == 'SATA_SSD' else 0.03), 2)
            stock = 0 if random.random() < 0.2 else random.randint(10, 80)
            
            Storage.objects.create(
                name=f"{manufacturer} {series} {capacity}GB",
                manufacturer=manufacturer,
                storage_type=storage_type,
                capacity=capacity,
                read_speed=read_speed,
                write_speed=write_speed,
                power_consumption=power,
                description=f"Fast and reliable {storage_type.replace('_', ' ')} with {capacity}GB capacity. Read speeds up to {read_speed}MB/s.",
                price=price,
                stock=stock
            )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {count} Storage devices'))

    def create_power_supplies(self, count):
        manufacturers = ['Corsair', 'EVGA', 'Seasonic', 'Thermaltake', 'Cooler Master']
        
        for i in range(count):
            manufacturer = random.choice(manufacturers)
            wattage = random.choice([450, 550, 650, 750, 850, 1000, 1200])
            efficiency = random.choice(['80PLUS', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'TITANIUM'])
            modular = random.choice([True, False])
            
            price = round(wattage * (0.08 if efficiency in ['80PLUS', 'BRONZE'] else 0.12 if efficiency in ['SILVER', 'GOLD'] else 0.15), 2)
            stock = 0 if random.random() < 0.2 else random.randint(5, 50)
            
            PowerSupply.objects.create(
                name=f"{manufacturer} {wattage}W {'Modular' if modular else 'Non-Modular'}",
                manufacturer=manufacturer,
                wattage=wattage,
                efficiency=efficiency,
                modular=modular,
                description=f"{wattage}W power supply with {efficiency.replace('_', ' ')} certification. {'Fully modular' if modular else 'Non-modular'} design.",
                price=price,
                stock=stock
            )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {count} Power Supplies'))

    def create_cases(self, count):
        manufacturers = ['Lian Li', 'NZXT', 'Corsair', 'Fractal Design', 'Cooler Master']
        
        for i in range(count):
            manufacturer = random.choice(manufacturers)
            form_factor = random.choice(['ATX', 'ATX', 'MICRO_ATX', 'MINI_ITX'])
            max_gpu_length = random.randint(300, 400)
            max_cpu_cooler_height = random.randint(150, 180)
            fan_slots = random.randint(6, 10)
            included_fans = random.randint(0, 4)
            
            price = round(random.uniform(50, 250), 2)
            stock = 0 if random.random() < 0.2 else random.randint(5, 30)
            
            Case.objects.create(
                name=f"{manufacturer} {form_factor} Case",
                manufacturer=manufacturer,
                form_factor=form_factor,
                max_gpu_length=max_gpu_length,
                max_cpu_cooler_height=max_cpu_cooler_height,
                fan_slots=fan_slots,
                included_fans=included_fans,
                description=f"Premium {form_factor} case with support for GPUs up to {max_gpu_length}mm. Includes {included_fans} fans.",
                price=price,
                stock=stock
            )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {count} Cases'))

    def create_coolers(self, count):
        manufacturers = ['Noctua', 'DeepCool', 'Corsair', 'Arctic', 'Cooler Master']
        socket_sets = ['AM5, LGA1700', 'AM4, AM5, LGA1700', 'LGA1700', 'AM5']

        for i in range(count):
            manufacturer = random.choice(manufacturers)
            cooler_type = random.choice(['AIR', 'AIR', 'AIO'])
            tdp_capacity = random.choice([150, 180, 220, 250, 280, 320])
            supported_sockets = random.choice(socket_sets)
            stock = 0 if random.random() < 0.2 else random.randint(5, 35)
            price = round(random.uniform(45, 220), 2)

            if cooler_type == 'AIO':
                height_mm = None
                radiator_length_mm = random.choice([240, 280, 360])
                name = f"{manufacturer} {radiator_length_mm}mm Liquid Cooling"
                description = (
                    f"{manufacturer} liquid cooling with a {radiator_length_mm} mm radiator "
                    f"and support for CPUs up to {tdp_capacity}W TDP."
                )
            else:
                height_mm = random.choice([145, 155, 165, 170])
                radiator_length_mm = None
                name = f"{manufacturer} Air Cooler"
                description = (
                    f"{manufacturer} air cooler with a height of {height_mm} mm "
                    f"and support for CPUs up to {tdp_capacity}W TDP."
                )

            Cooler.objects.create(
                name=name,
                manufacturer=manufacturer,
                cooler_type=cooler_type,
                supported_sockets=supported_sockets,
                tdp_capacity=tdp_capacity,
                height_mm=height_mm,
                radiator_length_mm=radiator_length_mm,
                description=description,
                price=price,
                stock=stock
            )

        self.stdout.write(self.style.SUCCESS(f'✓ Created {count} Coolers'))

    def create_laptops(self, count):
        manufacturers = ['Dell', 'HP', 'Lenovo', 'ASUS', 'MSI', 'Acer']
        
        for i in range(count):
            manufacturer = random.choice(manufacturers)
            category = random.choice(['GAMING', 'OFFICE', 'ULTRABOOK', 'WORKSTATION'])
            
            if category == 'GAMING':
                processor_name = random.choice(['Intel Core i7-13700H', 'Intel Core i9-13900HX', 'AMD Ryzen 7 7840HS', 'AMD Ryzen 9 7940HS'])
                gpu_name = random.choice(['NVIDIA RTX 4060', 'NVIDIA RTX 4070', 'NVIDIA RTX 4080', 'AMD RX 7600M'])
                ram_size = random.choice([16, 32, 64])
                screen_refresh_rate = random.choice([144, 165, 240])
                price_base = 1200
            elif category == 'OFFICE':
                processor_name = random.choice(['Intel Core i5-1335U', 'Intel Core i7-1355U', 'AMD Ryzen 5 7530U'])
                gpu_name = 'Integrated Graphics'
                ram_size = random.choice([8, 16])
                screen_refresh_rate = 60
                price_base = 600
            elif category == 'ULTRABOOK':
                processor_name = random.choice(['Intel Core i5-1340P', 'Intel Core i7-1360P', 'AMD Ryzen 7 7840U'])
                gpu_name = 'Integrated Graphics'
                ram_size = random.choice([16, 32])
                screen_refresh_rate = 60
                price_base = 900
            else:  # WORKSTATION
                processor_name = random.choice(['Intel Core i9-13950HX', 'AMD Ryzen 9 7945HX'])
                gpu_name = random.choice(['NVIDIA RTX 4000 Ada', 'NVIDIA RTX 5000 Ada'])
                ram_size = random.choice([32, 64])
                screen_refresh_rate = 60
                price_base = 2000
            
            ram_type = random.choice(['DDR4', 'DDR5'])
            storage_size = random.choice([512, 1000, 2000])
            storage_type = 'NVMe SSD'
            screen_size = random.choice([13.3, 14.0, 15.6, 17.3])
            screen_resolution = random.choice(['1920x1080', '2560x1440', '3840x2160'])
            weight = round(random.uniform(1.2, 3.5), 1)
            battery_capacity = random.randint(50, 99)
            power_consumption = random.choice([65, 90, 120, 180, 230, 330])
            
            price = round(price_base + (ram_size * 10) + (storage_size * 0.1) + random.uniform(-200, 300), 2)
            stock = 0 if random.random() < 0.2 else random.randint(3, 20)
            
            Laptop.objects.create(
                name=f"{manufacturer} {category.title()} Laptop",
                manufacturer=manufacturer,
                category=category,
                processor_name=processor_name,
                gpu_name=gpu_name,
                ram_size=ram_size,
                ram_type=ram_type,
                storage_size=storage_size,
                storage_type=storage_type,
                screen_size=screen_size,
                screen_resolution=screen_resolution,
                screen_refresh_rate=screen_refresh_rate,
                weight=weight,
                battery_capacity=battery_capacity,
                power_consumption=power_consumption,
                description=f"{category.title()} laptop with {processor_name} and {gpu_name}. Features {screen_size}\" display with {screen_refresh_rate}Hz refresh rate.",
                price=price,
                stock=stock
            )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {count} Laptops'))
