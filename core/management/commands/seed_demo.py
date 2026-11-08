from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from core.models import Category, Profession, Group, News


class Command(BaseCommand):
    help = 'Заполняет БД демо-данными и создаёт пользователя admin/admin123'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Создан пользователь admin / admin123'))
        else:
            self.stdout.write('Пользователь admin уже существует')

        categories_data = [
            ('Новая подготовка', 'novaya-podgotovka', 0),
            ('Повышение квалификации', 'povyshenie-kvalifikacii', 1),
            ('Повышение квалификации без присвоения разряда', 'bez-razryada', 2),
            ('Курсы целевого назначения', 'celevye-kursy', 3),
        ]
        categories = []
        for name, slug, order in categories_data:
            cat, _ = Category.objects.get_or_create(
                slug=slug, defaults={'name': name, 'order': order}
            )
            categories.append(cat)

        professions_data = [
            (0, 'Слесарь по контрольно-измерительным приборам и автоматике',
             'slesar-kipia', 'Обслуживание и ремонт КИПиА.'),
            (0, 'Оператор по добыче нефти, газа и газового конденсата',
             'operator-dobychi', 'Добыча нефти и газа.'),
            (0, 'Слесарь по эксплуатации и ремонту газового оборудования',
             'slesar-gazovogo-oborudovaniya', 'Ремонт газового оборудования.'),
            (0, 'Бурильщик капитального ремонта скважин',
             'burilshchik-krs', 'Капитальный ремонт скважин.'),
            (0, 'Оператор по исследованию скважин',
             'operator-issledovaniya', 'Исследование скважин.'),
            (0, 'Стропальщик', 'stropalshchik', 'Стропальные работы.'),
            (1, 'Слесарь-ремонтник (по ремонту нефтепромыслового оборудования)',
             'slesar-remontnik', 'Ремонт нефтепромыслового оборудования.'),
            (2, 'Оператор обезвоживающей и обессоливающей установки',
             'operator-obezvozhivaniya', 'Подготовка нефти.'),
            (2, 'Сливщик-разливщик', 'slivshchik-razlivshchik', 'Слив и налив нефтепродуктов.'),
            (2, 'Обходчик линейный', 'obkhodchik-lineynyy', 'Обход трубопроводов.'),
            (2, 'Помощник бурильщика капитального ремонта скважин',
             'pomoshchnik-burilshchika', 'Помощь бурильщику КРС.'),
            (3, 'Контроль скважины. Управление скважиной при газонефтеводопроявлениях',
             'kontrol-skvazhiny', 'Газонефтеводопроявления.'),
            (3, 'Безопасные методы и приёмы выполнения работ при воздействии вредных и (или) опасных производственных факторов',
             'bezopasnye-metody', 'Охрана труда.'),
            (3, 'Охрана труда. Обучение по оказанию первой помощи пострадавшим',
             'pervaya-pomoshch', 'Первая помощь.'),
            (3, 'Безопасные методы и приёмы выполнения работ повышенной опасности',
             'raboty-povyshennoy-opasnosti', 'Работы повышенной опасности.'),
            (3, 'Персонал, обслуживающий сосуды, работающие под давлением',
             'sosudy-pod-davleniem', 'Сосуды под давлением.'),
            (3, 'Безопасное проведение газоопасных работ на опасных производственных объектах',
             'gazoopasnye-raboty', 'Газоопасные работы.'),
            (3, 'Дополнительное обучение рабочих основных профессий, обслуживающих оборудование, работающее на газообразном топливе',
             'gazoobraznoe-toplivo', 'Газообразное топливо.'),
        ]
        professions = []
        for cat_idx, name, slug, desc in professions_data:
            prof, _ = Profession.objects.get_or_create(
                slug=slug,
                defaults={
                    'category': categories[cat_idx],
                    'name': name,
                    'description': desc,
                    'published': True,
                },
            )
            professions.append(prof)

        today = date.today()
        for i, prof in enumerate(professions):
            Group.objects.get_or_create(
                profession=prof, category=prof.category,
                start_date=today + timedelta(days=10 + i),
                exam_date=today + timedelta(days=40 + i),
                defaults={'note': '', 'published': True},
            )

        news_data = [
            ('Открыт набор на ноябрь 2026 года', 'otkryt-nabor-noyabr-2026',
             'УКЦ «Карьера» открывает набор групп на ноябрь 2026 года. '
             'Подробное расписание — на главной странице сайта.'),
            ('Новые программы обучения по охране труда', 'novye-programmy-okhrana-truda',
             'Разработаны новые программы по охране труда и первой помощи. Запись открыта.'),
            ('Обновлён график экзаменов', 'obnovlen-grafik-ekzamenov',
             'Проверьте актуальные даты экзаменов в разделе «Набор групп».'),
        ]
        for title, slug, text in news_data:
            News.objects.get_or_create(
                slug=slug, defaults={'title': title, 'text': text, 'published': True}
            )

        self.stdout.write(self.style.SUCCESS('Демо-данные загружены'))