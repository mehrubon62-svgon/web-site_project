(function () {
    const STORAGE_KEY = 'buildbox-language';
    const SUPPORTED_LANGUAGES = new Set(['en', 'ru']);
    const originalTextNodes = new WeakMap();
    const originalAttributes = new WeakMap();
    let mutationObserver = null;
    const monthMapRu = {
        Jan: 'янв',
        Feb: 'фев',
        Mar: 'мар',
        Apr: 'апр',
        May: 'мая',
        Jun: 'июн',
        Jul: 'июл',
        Aug: 'авг',
        Sep: 'сен',
        Oct: 'окт',
        Nov: 'ноя',
        Dec: 'дек',
    };

    function translateKnownValue(text) {
        return Object.prototype.hasOwnProperty.call(exactRu, text) ? exactRu[text] : text;
    }

    const exactRu = {
        'Language': 'Язык',
        'Home': 'Главная',
        'Explore': 'Каталог',
        'Components': 'Комплектующие',
        'Laptops': 'Ноутбуки',
        'Laptop': 'Ноутбук',
        'Configurator': 'Конфигуратор',
        'My Profile': 'Мой профиль',
        'My Configurations': 'Мои конфигурации',
        'Order History': 'История заказов',
        'Change Password': 'Изменить пароль',
        'Log Out': 'Выйти',
        'Sign In': 'Войти',
        'Register': 'Регистрация',
        'Sign In / Register': 'Войти / Регистрация',
        'Search products...': 'Поиск товаров...',
        'Quick Links': 'Быстрые ссылки',
        'Browse Components': 'Каталог комплектующих',
        'PC Configurator': 'Конфигуратор ПК',
        'About Us': 'О нас',
        'Contact': 'Контакты',
        'Contact Us': 'Связаться с нами',
        'Shipping Information': 'Информация о доставке',
        'Returns & Refunds': 'Возврат и возмещение',
        'FAQ': 'Частые вопросы',
        'Track Order': 'Отследить заказ',
        'Support Center': 'Центр поддержки',
        'Privacy Policy': 'Политика конфиденциальности',
        'Terms of Service': 'Условия использования',
        'Build your dream PC with confidence. Expert guidance and best prices.': 'Соберите ПК мечты уверенно. Экспертные подсказки и лучшие цены.',
        'Online': 'Онлайн',
        'Dock': 'Закрепить',
        'Clear': 'Очистить',
        'Close chat': 'Закрыть чат',
        'Toggle AI chat': 'Открыть AI-чат',
        'Resize chat': 'Изменить размер чата',
        'Ask about PC builds...': 'Спросите о сборках ПК...',
        "Hi! I'm BuildBox AI, your PC consultant. Tell me your budget and task.": 'Привет! Я BuildBox AI, ваш консультант по ПК. Напишите бюджет и задачу.',
        'Chat is temporarily unavailable. Please try again.': 'Чат временно недоступен. Попробуйте еще раз.',
        'I could not process your message.': 'Я не смог обработать ваше сообщение.',
        'Network error. Please try again.': 'Ошибка сети. Попробуйте еще раз.',
        'Chat history deleted. Start a new conversation anytime.': 'История чата удалена. Можете начать новый диалог в любой момент.',
        'Could not delete chat history. Please retry.': 'Не удалось удалить историю чата. Попробуйте еще раз.',
        'Build Your': 'Собери свой',
        'Dream PC': 'ПК мечты',
        'Configure, customize, and create the perfect computer with our intelligent compatibility system and expert guidance.': 'Настраивайте, комбинируйте и собирайте идеальный компьютер с нашей умной системой совместимости и экспертными подсказками.',
        'Start Building': 'Начать сборку',
        'Why Choose BuildBox?': 'Почему BuildBox?',
        'Everything you need to build the perfect PC': 'Все, что нужно для идеальной сборки ПК',
        'Compatibility Check': 'Проверка совместимости',
        'Automatic verification ensures all components work perfectly together before you buy.': 'Автоматическая проверка гарантирует, что все комплектующие идеально подходят друг к другу еще до покупки.',
        'Power Calculator': 'Калькулятор мощности',
        'Smart PSU recommendation based on your exact component selection and power needs.': 'Умная рекомендация блока питания на основе выбранных комплектующих и требуемой мощности.',
        'Best Prices': 'Лучшие цены',
        'Competitive pricing with real-time tracking to make sure you always get the best deal.': 'Конкурентные цены и отслеживание в реальном времени, чтобы вы всегда получали лучшее предложение.',
        'Popular Components': 'Популярные комплектующие',
        'View All →': 'Смотреть все →',
        'Ready to Build?': 'Готовы к сборке?',
        'Join thousands who built their dream PC with BuildBox': 'Присоединяйтесь к тысячам людей, которые собрали ПК мечты с BuildBox',
        'Get Started Now': 'Начать сейчас',
        'Continue Browsing': 'Продолжить просмотр',
        'Mixed picks from PC components only': 'Подборка только из комплектующих для ПК',
        'Back Home': 'Назад на главную',
        'All categories': 'Все категории',
        'Min price': 'Мин. цена',
        'Max price': 'Макс. цена',
        'Sort': 'Сортировка',
        'Price: Low to High': 'Цена: по возрастанию',
        'Price: High to Low': 'Цена: по убыванию',
        'Name: A-Z': 'Название: A-Z',
        'Apply Filters': 'Применить фильтры',
        'Reset': 'Сбросить',
        'View →': 'Открыть →',
        'No items for showcase yet.': 'Пока нет товаров для показа.',
        'Filters': 'Фильтры',
        'Clear All': 'Сбросить все',
        'No products found': 'Товары не найдены',
        'Clear filters': 'Сбросить фильтры',
        'Search by Name': 'Поиск по названию',
        'Manufacturer': 'Производитель',
        'Price ($)': 'Цена ($)',
        'Min': 'Мин',
        'Max': 'Макс',
        'In Stock Only': 'Только в наличии',
        'Memory Type': 'Тип памяти',
        'Form Factor': 'Форм-фактор',
        'Category': 'Категория',
        'Gaming': 'Игровой',
        'Office': 'Офисный',
        'Ultrabook': 'Ультрабук',
        'Workstation': 'Рабочая станция',
        'GAMING': 'Игровой',
        'OFFICE': 'Офисный',
        'ULTRABOOK': 'Ультрабук',
        'WORKSTATION': 'Рабочая станция',
        'Processors': 'Процессоры',
        'Graphics Cards': 'Видеокарты',
        'Memory (RAM)': 'Оперативная память (RAM)',
        'Motherboards': 'Материнские платы',
        'Storage': 'Накопители',
        'Power Supplies': 'Блоки питания',
        'Cases': 'Корпуса',
        'In Stock': 'В наличии',
        'Out of Stock': 'Нет в наличии',
        'Add to Cart': 'В корзину',
        'View Details': 'Подробнее',
        'Continue Shopping': 'Продолжить покупки',
        'Shopping Cart': 'Корзина',
        'Cart': 'Корзина',
        'Your cart is empty': 'Ваша корзина пуста',
        'Add some components or build a custom PC to get started.': 'Добавьте комплектующие или соберите кастомный ПК, чтобы начать.',
        'Build a PC': 'Собрать ПК',
        'each': 'за шт.',
        '← Continue Shopping': '← Продолжить покупки',
        'Clear Cart': 'Очистить корзину',
        'Order Summary': 'Сводка заказа',
        'Subtotal': 'Подытог',
        'Shipping': 'Доставка',
        'Free': 'Бесплатно',
        'Tax (1%)': 'Налог (1%)',
        'Promocode': 'Промокод',
        'Not applied': 'Не применен',
        'Quantity': 'Количество',
        '1 use per user': '1 использование на пользователя',
        'Total': 'Итого',
        'Have a promo code?': 'Есть промокод?',
        'Enter code': 'Введите код',
        'Apply': 'Применить',
        'Proceed to Checkout': 'Перейти к оформлению',
        'Checkout': 'Оформление заказа',
        'Processing your order...': 'Обрабатываем ваш заказ...',
        'Payment': 'Оплата',
        'Review': 'Проверка',
        'Full Name *': 'Полное имя *',
        'Email *': 'Email *',
        'Phone': 'Телефон',
        'Address Line 1 *': 'Адрес, строка 1 *',
        'Address Line 2 (optional)': 'Адрес, строка 2 (необязательно)',
        'City *': 'Город *',
        'Select city': 'Выберите город',
        'Dushanbe': 'Душанбе',
        'Khujand': 'Худжанд',
        'Bokhtar': 'Бохтар',
        'Kulob': 'Куляб',
        'Panjakent': 'Пенджикент',
        'Tursunzoda': 'Турсунзаде',
        'Hisor': 'Гиссар',
        'Istaravshan': 'Истаравшан',
        'Isfara': 'Исфара',
        'Vahdat': 'Вахдат',
        'Postal Code *': 'Почтовый индекс *',
        'Country *': 'Страна *',
        'Tajikistan': 'Таджикистан',
        'Save address for future orders': 'Сохранить адрес для будущих заказов',
        'Continue to Payment →': 'Перейти к оплате →',
        'Payment Method': 'Способ оплаты',
        'Credit/Debit Card': 'Банковская карта',
        'Cash on Delivery': 'Оплата при получении',
        'Card Number': 'Номер карты',
        'Cardholder Name': 'Имя владельца карты',
        'Expiration (MM/YY)': 'Срок действия (ММ/ГГ)',
        'CVV': 'CVV',
        'Save card for future purchases': 'Сохранить карту для будущих покупок',
        '← Back': '← Назад',
        'Continue →': 'Продолжить →',
        'Review Your Order': 'Проверьте ваш заказ',
        'Shipping Address': 'Адрес доставки',
        'Edit': 'Изменить',
        'Not provided': 'Не указано',
        'Order Notes (optional)': 'Комментарий к заказу (необязательно)',
        'Special instructions for your order...': 'Особые инструкции к вашему заказу...',
        'I agree to the': 'Я принимаю',
        'and': 'и',
        'I agree to the Terms of Service and Privacy Policy': 'Я принимаю Условия использования и Политику конфиденциальности',
        'Secure checkout': 'Безопасное оформление заказа',
        'My Wishlist': 'Мое избранное',
        'Remove': 'Удалить',
        'Your wishlist is empty.': 'Ваше избранное пусто.',
        'Browse Products': 'Смотреть товары',
        'My Configurations': 'Мои конфигурации',
        'Create New': 'Создать новую',
        'Issues': 'Есть проблемы',
        'Compatible': 'Совместимо',
        'CPU:': 'CPU:',
        'GPU:': 'GPU:',
        'MB:': 'MB:',
        'RAM:': 'RAM:',
        'PSU:': 'PSU:',
        'Delete': 'Удалить',
        'No configurations yet': 'Пока нет конфигураций',
        'Create first build': 'Создать первую сборку',
        'Build Your PC': 'Соберите свой ПК',
        "Select components and we'll check compatibility for you": 'Выберите комплектующие, а мы проверим их совместимость',
        'Saved Builds': 'Сохраненные сборки',
        'BUILD NAME': 'НАЗВАНИЕ СБОРКИ',
        'Your Build': 'Ваша сборка',
        'Compatibility': 'Совместимость',
        'Add components to check compatibility': 'Добавьте комплектующие для проверки совместимости',
        'Power Consumption': 'Потребление энергии',
        'estimated': 'оценочно',
        'Recommended PSU:': 'Рекомендуемый БП:',
        'Price Summary': 'Сводка цен',
        'Add Build to Cart': 'Добавить сборку в корзину',
        'Save Configuration': 'Сохранить конфигурацию',
        'Search...': 'Поиск...',
        'Prev': 'Назад',
        'Next': 'Далее',
        '✓ All components compatible': '✓ Все компоненты совместимы',
        'Processor': 'Процессор',
        'GPU': 'Видеокарта',
        'Graphics Card': 'Видеокарта',
        'Motherboard': 'Материнская плата',
        'RAM': 'ОЗУ',
        'Power Supply': 'Блок питания',
        'Case': 'Корпус',
        'ATX': 'ATX',
        'Micro-ATX': 'Микро-ATX',
        'Mini-ITX': 'Мини-ITX',
        'E-ATX': 'E-ATX',
        'MICRO_ATX': 'Микро-ATX',
        'MINI_ITX': 'Мини-ITX',
        'E_ATX': 'E-ATX',
        'NVMe SSD': 'NVMe SSD',
        'SATA SSD': 'SATA SSD',
        'HDD': 'HDD',
        'NVME': 'NVMe SSD',
        'SATA_SSD': 'SATA SSD',
        '80 Plus': '80 Plus',
        '80 Plus Bronze': '80 Plus Bronze',
        '80 Plus Silver': '80 Plus Silver',
        '80 Plus Gold': '80 Plus Gold',
        '80 Plus Platinum': '80 Plus Platinum',
        '80 Plus Titanium': '80 Plus Titanium',
        'Select': 'Выбрать',
        'Select Processor': 'Выберите процессор',
        'Select Graphics Card': 'Выберите видеокарту',
        'Select Motherboard': 'Выберите материнскую плату',
        'Select RAM': 'Выберите оперативную память',
        'Select Storage': 'Выберите накопитель',
        'Select Power Supply': 'Выберите блок питания',
        'Select Case': 'Выберите корпус',
        'Click to choose': 'Нажмите, чтобы выбрать',
        'Change': 'Изменить',
        'No Processor': 'Процессор не выбран',
        'No Graphics Card': 'Видеокарта не выбрана',
        'No Motherboard': 'Материнская плата не выбрана',
        'No RAM': 'Оперативная память не выбрана',
        'No Storage': 'Накопитель не выбран',
        'No Power Supply': 'Блок питания не выбран',
        'No Case': 'Корпус не выбран',
        'Order History': 'История заказов',
        'Delivered': 'Доставлен',
        'Shipped': 'Отправлен',
        'Processing': 'Обрабатывается',
        'Cancelled': 'Отменен',
        'Pending': 'В ожидании',
        'Placed on': 'Оформлен',
        'Updated': 'Обновлен',
        'Order note': 'Комментарий к заказу',
        'No orders yet': 'Пока нет заказов',
        'Your placed orders will appear here.': 'Здесь появятся ваши оформленные заказы.',
        'Start Shopping': 'Начать покупки',
        'Manage your BuildBox profile information.': 'Управляйте данными своего профиля BuildBox.',
        'Bio': 'О себе',
        'Edit Profile': 'Редактировать профиль',
        'Update your avatar and bio.': 'Обновите аватар и описание профиля.',
        'First Name': 'Имя',
        'Last Name': 'Фамилия',
        'Nickname (Username)': 'Никнейм (Username)',
        'Avatar': 'Аватар',
        'Your first name': 'Ваше имя',
        'Your last name': 'Ваша фамилия',
        'Your unique nickname': 'Ваш уникальный никнейм',
        'Tell others something about yourself': 'Расскажите немного о себе',
        'Up to 500 characters.': 'До 500 символов.',
        'Save Changes': 'Сохранить изменения',
        'Cancel': 'Отмена',
        'Welcome Back': 'С возвращением',
        'Sign in to your account': 'Войдите в свой аккаунт',
        'Username': 'Имя пользователя',
        'Enter your username': 'Введите имя пользователя',
        'Password': 'Пароль',
        'Enter your password': 'Введите пароль',
        'Remember me': 'Запомнить меня',
        'Forgot password?': 'Забыли пароль?',
        "Don't have an account?": 'Нет аккаунта?',
        'Sign up': 'Зарегистрироваться',
        'Create Account': 'Создать аккаунт',
        'Join BuildBox today': 'Присоединяйтесь к BuildBox уже сегодня',
        'Choose a username': 'Придумайте имя пользователя',
        'Email': 'Email',
        'Enter your email': 'Введите email',
        'Create a password': 'Создайте пароль',
        'Confirm Password': 'Подтвердите пароль',
        'Confirm your password': 'Подтвердите пароль',
        'Already have an account?': 'Уже есть аккаунт?',
        'Update your password': 'Обновите свой пароль',
        'Current Password': 'Текущий пароль',
        'Enter current password': 'Введите текущий пароль',
        'New Password': 'Новый пароль',
        'Enter new password': 'Введите новый пароль',
        'Confirm New Password': 'Подтвердите новый пароль',
        'Confirm new password': 'Подтвердите новый пароль',
        'At least 8 characters': 'Минимум 8 символов',
        'Mix of letters and numbers': 'Смешайте буквы и цифры',
        'Update Password': 'Обновить пароль',
        'Back to home': 'Назад на главную',
        'Forgot Password': 'Забыли пароль',
        'Enter your email to reset password': 'Введите email для сброса пароля',
        'Email Address': 'Email адрес',
        'Enter your email address': 'Введите ваш email адрес',
        'Send Reset Link': 'Отправить ссылку для сброса',
        'Back to login': 'Назад ко входу',
        'Reset Password': 'Сброс пароля',
        'Enter your new password': 'Введите новый пароль',
        'Check Your Email': 'Проверьте почту',
        "We've sent a confirmation email to your address. Please check your inbox and click the confirmation link to activate your account.": 'Мы отправили письмо с подтверждением на ваш адрес. Проверьте входящие и перейдите по ссылке, чтобы активировать аккаунт.',
        "Didn't receive the email?": 'Не получили письмо?',
        'Check your spam folder or make sure you entered the correct email address during registration.': 'Проверьте папку спам или убедитесь, что при регистрации вы указали правильный email.',
        'Back to Login': 'Назад ко входу',
        'Weak password': 'Слабый пароль',
        'Fair password': 'Нормальный пароль',
        'Good password': 'Хороший пароль',
        '✓ Passwords match': '✓ Пароли совпадают',
        '✗ Passwords do not match': '✗ Пароли не совпадают',
        'BuildBox AI for This Product': 'BuildBox AI для этого товара',
        'Check compatibility with your build.': 'Проверьте совместимость с вашей сборкой.',
        'Open Configurator →': 'Открыть конфигуратор →',
        'Qty:': 'Кол-во:',
        'Remove from Wishlist': 'Убрать из избранного',
        'Add to Wishlist': 'Добавить в избранное',
        'Description': 'Описание',
        'Specifications': 'Характеристики',
        'Rating': 'Рейтинг',
        'Reviews': 'Отзывы',
        'Edit your review': 'Редактировать отзыв',
        'Add your review': 'Добавить отзыв',
        'Write your thoughts...': 'Поделитесь своим мнением...',
        'Save': 'Сохранить',
        'My Gaming Build': 'Моя игровая сборка',
        'My Build': 'Моя сборка',
        'Configuration saved.': 'Конфигурация сохранена.',
        'Build added to cart.': 'Сборка добавлена в корзину.',
        'Please': 'Пожалуйста',
        'sign in': 'войдите',
        'Please sign in to leave a review.': 'Пожалуйста, войдите, чтобы оставить отзыв.',
        'Reply': 'Ответить',
        'Add a reply...': 'Добавить ответ...',
        'Post': 'Отправить',
        'No reviews yet': 'Пока нет отзывов',
        'Be the first to post one.': 'Станьте первым, кто оставит отзыв.',
        'Cores': 'Ядра',
        'Threads': 'Потоки',
        'Socket': 'Сокет',
        'Base Clock': 'Базовая частота',
        'Boost Clock': 'Boost частота',
        'TDP Base': 'Базовый TDP',
        'TDP Max': 'Макс. TDP',
        'Chipset': 'Чипсет',
        'VRAM': 'Видеопамять',
        'VRAM Type': 'Тип видеопамяти',
        'Recommended PSU': 'Рекомендуемый БП',
        'Length': 'Длина',
        'Capacity': 'Объем',
        'Speed': 'Скорость',
        'RAM Type': 'Тип RAM',
        'RAM Slots': 'Слоты RAM',
        'Max RAM': 'Макс. RAM',
        'Storage Type': 'Тип накопителя',
        'Read Speed': 'Скорость чтения',
        'Write Speed': 'Скорость записи',
        'Wattage': 'Мощность',
        'Efficiency': 'Эффективность',
        'Modular': 'Модульный',
        'Yes': 'Да',
        'No': 'Нет',
        'Max GPU Length': 'Макс. длина GPU',
        'Resolution': 'Разрешение',
        'Screen Size': 'Размер экрана',
        'Weight': 'Вес',
        'I am BuildBox AI for this product page. Ask me about specs, compatibility, performance, or usage of this item.': 'Я BuildBox AI для этой страницы товара. Спрашивайте о характеристиках, совместимости, производительности или использовании этого товара.',
        'Product assistant is unavailable right now.': 'Помощник по товару сейчас недоступен.',
        'I can only answer about this product.': 'Я могу отвечать только про этот товар.',
        'Chat reset. Ask anything about this product.': 'Чат сброшен. Спросите что угодно об этом товаре.',
        'Could not clear chat.': 'Не удалось очистить чат.',
        'Out of stock': 'Нет в наличии',
        'Welcome Back': 'С возвращением',
        'BuildBox - Build Your Dream PC': 'BuildBox - ПК твоей мечты',
        'Explore All - BuildBox': 'Каталог - BuildBox',
        'Shopping Cart - BuildBox': 'Корзина - BuildBox',
        'Checkout - BuildBox': 'Оформление заказа - BuildBox',
        'Configurator - BuildBox': 'Конфигуратор - BuildBox',
        'My Configurations - BuildBox': 'Мои конфигурации - BuildBox',
        'Change Password - BuildBox': 'Изменить пароль - BuildBox',
        'Forgot Password - BuildBox': 'Забыли пароль - BuildBox',
        'Reset Password - BuildBox': 'Сброс пароля - BuildBox',
        'e.g. Core i9, Ryzen 9': 'напр. Core i9, Ryzen 9',
        'e.g. RTX 4090, RX 7900': 'напр. RTX 4090, RX 7900',
        'e.g. RTX 4090': 'напр. RTX 4090',
        'e.g. Vengeance, Trident': 'напр. Vengeance, Trident',
        'e.g. Vengeance': 'напр. Vengeance',
        'e.g. H510, Meshify': 'напр. H510, Meshify',
        'e.g. H510': 'напр. H510',
        'e.g. XPS, ThinkPad': 'напр. XPS, ThinkPad',
        'e.g. XPS': 'напр. XPS',
        'Muhammad Ali': 'Мухаммад Али',
        'you@example.com': 'you@example.com',
        '+992 90 000 00 00': '+992 90 000 00 00',
        'Rudaki Avenue 10': 'проспект Рудаки 10',
        'Apartment, office, floor': 'Квартира, офис, этаж',
        '734000': '734000',
        'Gaming PC Setup': 'Игровая сборка ПК',
        '123 Tech Street, Silicon Valley, CA': '123 Tech Street, Silicon Valley, CA',
    };

    const keyedMessages = {
        language_changed: {
            en: 'Language changed',
            ru: 'Язык изменен',
        },
        wishlist_update_failed: {
            en: 'Failed to update wishlist. Please try again.',
            ru: 'Не удалось обновить избранное. Попробуйте еще раз.',
        },
        review_save_failed: {
            en: 'Failed to save review.',
            ru: 'Не удалось сохранить отзыв.',
        },
        review_save_network_error: {
            en: 'Network error while saving review.',
            ru: 'Ошибка сети при сохранении отзыва.',
        },
        reply_post_failed: {
            en: 'Failed to post reply.',
            ru: 'Не удалось отправить ответ.',
        },
        reply_ui_update_failed: {
            en: 'Reply was saved, but UI update failed. Please open Reviews tab again.',
            ru: 'Ответ сохранился, но интерфейс не обновился. Откройте раздел отзывов еще раз.',
        },
        reply_post_network_error: {
            en: 'Network error while posting reply.',
            ru: 'Ошибка сети при отправке ответа.',
        },
        review_delete_failed: {
            en: 'Failed to delete review.',
            ru: 'Не удалось удалить отзыв.',
        },
        reply_delete_failed: {
            en: 'Failed to delete reply.',
            ru: 'Не удалось удалить ответ.',
        },
        unknown_error: {
            en: 'unknown error',
            ru: 'неизвестная ошибка',
        },
    };

    function pluralRu(count, one, few, many) {
        const mod10 = count % 10;
        const mod100 = count % 100;
        if (mod10 === 1 && mod100 !== 11) return one;
        if (mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14)) return few;
        return many;
    }

    function interpolate(template, params) {
        return String(template).replace(/\{(\w+)\}/g, function (_, key) {
            return Object.prototype.hasOwnProperty.call(params, key) ? params[key] : '';
        });
    }

    function getStoredLanguage() {
        const saved = localStorage.getItem(STORAGE_KEY);
        return SUPPORTED_LANGUAGES.has(saved) ? saved : 'en';
    }

    let currentLanguage = getStoredLanguage();
    let originalTitle = document.title;

    function translateDateString(text) {
        const match = text.match(/^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{1,2}), (\d{4})(?: (\d{2}:\d{2}))?$/);
        if (!match) return text;
        const month = monthMapRu[match[1]] || match[1];
        return match[4] ? `${match[2]} ${month} ${match[3]} ${match[4]}` : `${match[2]} ${month} ${match[3]}`;
    }

    function translatePattern(text) {
        const patterns = [
            {
                regex: /^(\d+)\s+products$/,
                transform: (m) => `${m[1]} ${pluralRu(Number(m[1]), 'товар', 'товара', 'товаров')}`,
            },
            {
                regex: /^(\d+)\s+saved items$/,
                transform: (m) => `${m[1]} ${pluralRu(Number(m[1]), 'товар в избранном', 'товара в избранном', 'товаров в избранном')}`,
            },
            {
                regex: /^(\d+)\s+saved builds$/,
                transform: (m) => `${m[1]} ${pluralRu(Number(m[1]), 'сохраненная сборка', 'сохраненные сборки', 'сохраненных сборок')}`,
            },
            {
                regex: /^([0-9]+(?:\.[0-9]+)?) GB$/,
                transform: (m) => `${m[1]} ГБ`,
            },
            {
                regex: /^([0-9]+(?:\.[0-9]+)?) GB x(\d+)$/,
                transform: (m) => `${m[1]} ГБ x${m[2]}`,
            },
            {
                regex: /^([0-9]+(?:\.[0-9]+)?) W$/,
                transform: (m) => `${m[1]} Вт`,
            },
            {
                regex: /^([0-9]+(?:\.[0-9]+)?) MHz$/,
                transform: (m) => `${m[1]} МГц`,
            },
            {
                regex: /^([0-9]+(?:\.[0-9]+)?) GHz$/,
                transform: (m) => `${m[1]} ГГц`,
            },
            {
                regex: /^([0-9]+(?:\.[0-9]+)?) mm$/,
                transform: (m) => `${m[1]} мм`,
            },
            {
                regex: /^([0-9]+(?:\.[0-9]+)?) kg$/,
                transform: (m) => `${m[1]} кг`,
            },
            {
                regex: /^\((\d+)\s+items\)$/,
                transform: (m) => `(${m[1]} ${pluralRu(Number(m[1]), 'товар', 'товара', 'товаров')})`,
            },
            {
                regex: /^([0-9]+(?:\.[0-9]+)?)\/5 \((\d+) reviews\)$/,
                transform: (m) => `${m[1]}/5 (${m[2]} ${pluralRu(Number(m[2]), 'отзыв', 'отзыва', 'отзывов')})`,
            },
            {
                regex: /^([0-9]+(?:\.[0-9]+)?)\/5$/,
                transform: (m) => `${m[1]}/5`,
            },
            {
                regex: /^In Stock \((\d+) available\)$/,
                transform: (m) => `В наличии (${m[1]} доступно)`,
            },
            {
                regex: /^Add \$([0-9]+(?:\.[0-9]+)?) more to unlock free shipping\.$/,
                transform: (m) => `Добавьте еще $${m[1]}, чтобы получить бесплатную доставку.`,
            },
            {
                regex: /^Promo discount \((\d+)%\)$/,
                transform: (m) => `Скидка по промокоду (${m[1]}%)`,
            },
            {
                regex: /^Qty:\s*(\d+)$/,
                transform: (m) => `Кол-во: ${m[1]}`,
            },
            {
                regex: /^Order Items \((\d+)\)$/,
                transform: (m) => `Товары в заказе (${m[1]})`,
            },
            {
                regex: /^Page (\d+) \/ (\d+)$/,
                transform: (m) => `Страница ${m[1]} / ${m[2]}`,
            },
            {
                regex: /^(?:•\s*)?Socket mismatch: CPU (.+) \/ MB (.+)$/,
                transform: (m) => `Несовпадение сокета: CPU ${m[1]} / MB ${m[2]}`,
            },
            {
                regex: /^(?:•\s*)?(?:⚠️\s*)?Socket incompatibility: CPU (.+) != MB (.+)$/,
                transform: (m) => `Несовместимость сокета: CPU ${m[1]} != MB ${m[2]}`,
            },
            {
                regex: /^(?:•\s*)?RAM mismatch: (.+) RAM with (.+) motherboard$/,
                transform: (m) => `Несовместимость RAM: память ${m[1]} с материнской платой ${m[2]}`,
            },
            {
                regex: /^(?:•\s*)?(?:⚠️\s*)?RAM incompatibility: RAM (.+) != MB (.+)$/,
                transform: (m) => `Несовместимость RAM: память ${m[1]} != MB ${m[2]}`,
            },
            {
                regex: /^(?:•\s*)?PSU too weak: (\d+)W selected, (\d+)W recommended$/,
                transform: (m) => `Слишком слабый БП: выбрано ${m[1]}W, рекомендуется ${m[2]}W`,
            },
            {
                regex: /^(?:•\s*)?(?:⚠️\s*)?Insufficient PSU power: (\d+)W < (\d+)W(?: \(recommended\))?$/,
                transform: (m) => `Недостаточная мощность БП: ${m[1]}W < ${m[2]}W`,
            },
            {
                regex: /^(?:•\s*)?❌ CRITICAL: PSU too weak! (\d+)W < (\d+)W \(minimum\)$/,
                transform: (m) => `❌ КРИТИЧНО: БП слишком слабый! ${m[1]}W < ${m[2]}W (минимум)`,
            },
            {
                regex: /^(?:•\s*)?(?:⚠️\s*)?GPU won't fit in case: (\d+)mm > (\d+)mm$/,
                transform: (m) => `Видеокарта не помещается в корпус: ${m[1]} мм > ${m[2]} мм`,
            },
            {
                regex: /^(?:•\s*)?(?:⚠️\s*)?Motherboard (.+) won't fit in (.+) case$/,
                transform: (m) => `Материнская плата ${m[1]} не помещается в корпус ${m[2]}`,
            },
            {
                regex: /^(\d+)\s+repl(?:y|ies)$/,
                transform: (m) => `${m[1]} ${pluralRu(Number(m[1]), 'ответ', 'ответа', 'ответов')}`,
            },
            {
                regex: /^Max:\s*(\d+)$/,
                transform: (m) => `Макс: ${m[1]}`,
            },
            {
                regex: /^Answers only about (.+)$/,
                transform: (m) => `Отвечает только про ${m[1]}`,
            },
            {
                regex: /^Place Order [—-] \$(.+)$/,
                transform: (m) => `Оформить заказ — $${m[1]}`,
            },
            {
                regex: /^© (\d{4}) BuildBox\. All rights reserved\.$/,
                transform: (m) => `© ${m[1]} BuildBox. Все права защищены.`,
            },
            {
                regex: /^Placed on (.+)$/,
                transform: (m) => `Оформлен ${m[1]}`,
            },
            {
                regex: /^• (\d+) Cores \/ (\d+) Threads$/,
                transform: (m) => `• ${m[1]} ядер / ${m[2]} потоков`,
            },
            {
                regex: /^• ([0-9.]+)GHz Boost Clock$/,
                transform: (m) => `• Boost ${m[1]} ГГц`,
            },
            {
                regex: /^• (\d+)\s*MB\/s Read$/,
                transform: (m) => `• Чтение ${m[1]} МБ/с`,
            },
            {
                regex: /^• (\d+)\s*MB\/s Write$/,
                transform: (m) => `• Запись ${m[1]} МБ/с`,
            },
            {
                regex: /^• (ATX|Micro-ATX|Mini-ITX|E-ATX|MICRO_ATX|MINI_ITX|E_ATX)$/,
                transform: (m) => `• ${translateKnownValue(m[1])}`,
            },
            {
                regex: /^• (ATX|Micro-ATX|Mini-ITX|E-ATX|MICRO_ATX|MINI_ITX|E_ATX) • (DDR4|DDR5)$/,
                transform: (m) => `• ${translateKnownValue(m[1])} • ${translateKnownValue(m[2])}`,
            },
            {
                regex: /^• (\d+)GB ([A-Za-z0-9]+)$/,
                transform: (m) => `• ${m[1]} ГБ ${m[2]}`,
            },
            {
                regex: /^• (\d+)W TDP$/,
                transform: (m) => `• TDP ${m[1]} Вт`,
            },
            {
                regex: /^• Max GPU: (\d+)mm$/,
                transform: (m) => `• Макс. GPU: ${m[1]} мм`,
            },
            {
                regex: /^• (\d+)W$/,
                transform: (m) => `• ${m[1]} Вт`,
            },
            {
                regex: /^• (.+) • Modular$/,
                transform: (m) => `• ${translateKnownValue(m[1])} • Модульный`,
            },
            {
                regex: /^• (\d+)GB RAM • (\d+)GB (.+)$/,
                transform: (m) => `• ${m[1]} ГБ ОЗУ • ${m[2]} ГБ ${translateKnownValue(m[3])}`,
            },
            {
                regex: /^([0-9]+(?:\.[0-9]+)?)GB (DDR4|DDR5|GDDR6|GDDR6X)$/,
                transform: (m) => `${m[1]} ГБ ${translateKnownValue(m[2])}`,
            },
            {
                regex: /^([0-9]+(?:\.[0-9]+)?)GB (NVMe SSD|SATA SSD|HDD)$/,
                transform: (m) => `${m[1]} ГБ ${translateKnownValue(m[2])}`,
            },
            {
                regex: /^([0-9]+(?:\.[0-9]+)?)W (80 Plus(?: Bronze| Silver| Gold| Platinum| Titanium)?)$/,
                transform: (m) => `${m[1]} Вт ${translateKnownValue(m[2])}`,
            },
            {
                regex: /^(.+?) \/ (ATX|Micro-ATX|Mini-ITX|E-ATX|MICRO_ATX|MINI_ITX|E_ATX)$/,
                transform: (m) => `${m[1]} / ${translateKnownValue(m[2])}`,
            },
            {
                regex: /^(ATX|Micro-ATX|Mini-ITX|E-ATX|MICRO_ATX|MINI_ITX|E_ATX) \/ (\d+)mm GPU$/,
                transform: (m) => `${translateKnownValue(m[1])} / ${m[2]} мм GPU`,
            },
        ];

        for (const pattern of patterns) {
            const match = text.match(pattern.regex);
            if (match) return pattern.transform(match);
        }

        return text;
    }

    function translateCore(text, lang) {
        if (!text || lang === 'en') return text;
        if (Object.prototype.hasOwnProperty.call(exactRu, text)) {
            return exactRu[text];
        }
        const dateTranslation = translateDateString(text);
        if (dateTranslation !== text) return dateTranslation;
        return translatePattern(text);
    }

    function translateLoose(text, lang = currentLanguage) {
        if (typeof text !== 'string') return text;
        if (lang === 'en') return text;
        const match = text.match(/^(\s*)([\s\S]*?)(\s*)$/);
        if (!match) return translateCore(text, lang);
        const translated = translateCore(match[2], lang);
        return `${match[1]}${translated}${match[3]}`;
    }

    function isKnownRenderedValue(source, currentValue) {
        if (!source) return false;
        if (currentValue === source) return true;
        for (const lang of SUPPORTED_LANGUAGES) {
            if (lang === 'en') continue;
            if (currentValue === translateLoose(source, lang)) {
                return true;
            }
        }
        return false;
    }

    function t(key, params, langOverride) {
        const lang = SUPPORTED_LANGUAGES.has(langOverride) ? langOverride : currentLanguage;
        const bundle = keyedMessages[key];
        if (!bundle) return key;
        const template = bundle[lang] || bundle.en || key;
        return interpolate(template, params || {});
    }

    function shouldSkipNode(node) {
        const parent = node.parentElement;
        if (!parent) return true;
        if (parent.closest('[data-i18n-skip]')) return true;
        const tag = parent.tagName;
        return tag === 'SCRIPT' || tag === 'STYLE' || tag === 'NOSCRIPT' || tag === 'TEXTAREA';
    }

    function syncTextNode(node) {
        if (!node || node.nodeType !== Node.TEXT_NODE) return;
        const currentValue = node.textContent;
        if (!currentValue || !currentValue.trim() || shouldSkipNode(node)) return;

        const storedOriginal = originalTextNodes.get(node);
        if (!storedOriginal || !isKnownRenderedValue(storedOriginal, currentValue)) {
            originalTextNodes.set(node, currentValue);
        }

        const source = originalTextNodes.get(node);
        const nextValue = currentLanguage === 'en' ? source : translateLoose(source, currentLanguage);
        if (currentValue !== nextValue) {
            node.textContent = nextValue;
        }
    }

    function syncAttribute(element, attrName) {
        const currentValue = element.getAttribute(attrName);
        if (!currentValue || !currentValue.trim()) return;
        const stored = originalAttributes.get(element) || {};
        if (!stored[attrName] || !isKnownRenderedValue(stored[attrName], currentValue)) {
            stored[attrName] = currentValue;
            originalAttributes.set(element, stored);
        }
        const nextValue = currentLanguage === 'en' ? stored[attrName] : translateLoose(stored[attrName], currentLanguage);
        if (currentValue !== nextValue) {
            element.setAttribute(attrName, nextValue);
        }
    }

    function syncElementAttributes(element) {
        if (!(element instanceof Element) || element.closest('[data-i18n-skip]')) return;
        ['placeholder', 'title', 'aria-label'].forEach(function (attrName) {
            if (element.hasAttribute(attrName)) {
                syncAttribute(element, attrName);
            }
        });
        if (element.tagName === 'INPUT') {
            const type = (element.getAttribute('type') || '').toLowerCase();
            if (type === 'button' || type === 'submit' || type === 'reset' || element.hasAttribute('data-i18n-value')) {
                syncAttribute(element, 'value');
            }
        }
    }

    function walkAndTranslate(root) {
        if (!root) return;
        if (root.nodeType === Node.TEXT_NODE) {
            syncTextNode(root);
            return;
        }
        if (root.nodeType !== Node.ELEMENT_NODE && root.nodeType !== Node.DOCUMENT_FRAGMENT_NODE) return;

        if (root.nodeType === Node.ELEMENT_NODE) {
            syncElementAttributes(root);
        }

        const textWalker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
        while (textWalker.nextNode()) {
            syncTextNode(textWalker.currentNode);
        }

        if (root.querySelectorAll) {
            root.querySelectorAll('[placeholder],[title],[aria-label],[data-i18n-value],input[type="button"],input[type="submit"],input[type="reset"]').forEach(syncElementAttributes);
        }
    }

    function syncDocumentTitle() {
        const nextTitle = currentLanguage === 'en' ? originalTitle : translateLoose(originalTitle, currentLanguage);
        if (document.title === nextTitle) return;
        document.title = nextTitle;
    }

    function observeDocument() {
        if (!mutationObserver || !document.body) return;
        mutationObserver.observe(document.body, {
            childList: true,
            subtree: true,
            characterData: true,
            attributes: true,
            attributeFilter: ['placeholder', 'title', 'aria-label', 'value'],
        });
    }

    function withObserverPaused(callback) {
        if (!mutationObserver) {
            callback();
            return;
        }

        mutationObserver.disconnect();
        try {
            callback();
        } finally {
            observeDocument();
        }
    }

    function ensureToastContainer() {
        let container = document.getElementById('language-toast-container');
        if (container) return container;
        container = document.createElement('div');
        container.id = 'language-toast-container';
        container.className = 'fixed top-5 right-5 z-[100] flex flex-col gap-2 pointer-events-none';
        document.body.appendChild(container);
        return container;
    }

    function showToast(message) {
        const container = ensureToastContainer();
        const toast = document.createElement('div');
        toast.className = 'pointer-events-auto min-w-[220px] max-w-[320px] rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 px-4 py-3 text-sm font-medium text-gray-900 dark:text-white shadow-lg opacity-0 translate-y-2 transition-all duration-300';
        toast.textContent = message;
        container.appendChild(toast);

        requestAnimationFrame(function () {
            toast.classList.remove('opacity-0', 'translate-y-2');
        });

        setTimeout(function () {
            toast.classList.add('opacity-0', 'translate-y-2');
            setTimeout(function () {
                toast.remove();
            }, 280);
        }, 2200);
    }

    function updateSwitchers() {
        document.querySelectorAll('[data-lang-btn]').forEach(function (button) {
            const isActive = button.getAttribute('data-lang-btn') === currentLanguage;
            button.classList.toggle('bg-accent', isActive);
            button.classList.toggle('text-gray-900', isActive);
            button.classList.toggle('border-accent', isActive);
            button.classList.toggle('bg-transparent', !isActive);
            button.classList.toggle('text-gray-600', !isActive);
            button.classList.toggle('dark:text-gray-300', !isActive);
            button.classList.toggle('border-gray-300', !isActive);
            button.classList.toggle('dark:border-gray-600', !isActive);
        });
    }

    function applyLanguage(lang) {
        currentLanguage = SUPPORTED_LANGUAGES.has(lang) ? lang : 'en';
        localStorage.setItem(STORAGE_KEY, currentLanguage);
        document.documentElement.lang = currentLanguage;
        withObserverPaused(function () {
            walkAndTranslate(document.body);
            syncDocumentTitle();
            updateSwitchers();
        });
        document.dispatchEvent(new CustomEvent('buildbox:languagechange', { detail: { language: currentLanguage } }));
    }

    function setLanguage(lang, options) {
        const silent = options && options.silent;
        if (!SUPPORTED_LANGUAGES.has(lang)) return;
        applyLanguage(lang);
        if (!silent) {
            showToast(t('language_changed'));
        }
    }

    function bindSwitchers() {
        document.querySelectorAll('[data-lang-btn]').forEach(function (button) {
            button.addEventListener('click', function () {
                const lang = button.getAttribute('data-lang-btn');
                if (lang && lang !== currentLanguage) {
                    setLanguage(lang);
                }
            });
        });
    }

    function startObserver() {
        mutationObserver = new MutationObserver(function (mutations) {
            mutations.forEach(function (mutation) {
                if (mutation.type === 'characterData') {
                    syncTextNode(mutation.target);
                    return;
                }
                if (mutation.type === 'attributes' && mutation.target instanceof Element) {
                    syncElementAttributes(mutation.target);
                    return;
                }
                mutation.addedNodes.forEach(function (node) {
                    walkAndTranslate(node);
                });
            });
        });
        observeDocument();
    }

    function init() {
        originalTitle = document.title;
        ensureToastContainer();
        bindSwitchers();
        applyLanguage(currentLanguage);
        startObserver();
    }

    window.BuildBoxI18n = {
        getLanguage: function () {
            return currentLanguage;
        },
        setLanguage: setLanguage,
        applyLanguage: applyLanguage,
        t: t,
        translateText: function (text, lang) {
            return translateLoose(text, lang || currentLanguage);
        },
        showToast: showToast,
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init, { once: true });
    } else {
        init();
    }
})();
