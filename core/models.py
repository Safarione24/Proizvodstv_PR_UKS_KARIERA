from datetime import date

from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField(unique=True)
    order = models.PositiveSmallIntegerField('Порядок сортировки', default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Категория обучения'
        verbose_name_plural = 'Категории обучения'

    def __str__(self):
        return self.name


class Profession(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 related_name='professions', verbose_name='Категория')
    name = models.CharField('Название', max_length=300)
    slug = models.SlugField(unique=True)
    description = models.TextField('Описание', blank=True)
    published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        ordering = ['category__order', 'name']
        verbose_name = 'Профессия'
        verbose_name_plural = 'Профессии'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('profession_detail', kwargs={'slug': self.slug})


class Group(models.Model):
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE,
                                   related_name='groups', verbose_name='Профессия')
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 related_name='groups', verbose_name='Категория')
    start_date = models.DateField('Дата начала занятий')
    exam_date = models.DateField('Дата экзамена')
    note = models.CharField('Примечание', max_length=300, blank=True)
    published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        ordering = ['start_date', 'exam_date']
        verbose_name = 'Группа (набор)'
        verbose_name_plural = 'Группы (наборы)'

    def __str__(self):
        return '%s — старт %s' % (self.profession.name, self.start_date.strftime('%d.%m.%Y'))

    @property
    def is_past(self):
        return self.exam_date < date.today()


class News(models.Model):
    title = models.CharField('Заголовок', max_length=300)
    slug = models.SlugField(unique=True)
    text = models.TextField('Текст')
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)
    published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})


# --- НОВЫЕ МОДЕЛИ ---

class Application(models.Model):
    """Заявка на обучение"""
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('processed', 'Обработана'),
        ('rejected', 'Отклонена'),
    ]
    name = models.CharField('Имя', max_length=200)
    phone = models.CharField('Телефон', max_length=50)
    profession = models.ForeignKey(Profession, on_delete=models.SET_NULL,
                                   null=True, blank=True, verbose_name='Профессия')
    comment = models.TextField('Комментарий', blank=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField('Дата заявки', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'{self.name} — {self.phone}'


class Photo(models.Model):
    """Фото галереи (пока заглушки)"""
    title = models.CharField('Подпись', max_length=200, blank=True)
    image = models.ImageField('Изображение', upload_to='gallery/')
    order = models.PositiveSmallIntegerField('Порядок', default=0)
    published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Фото галереи'
        verbose_name_plural = 'Галерея'


class Review(models.Model):
    """Отзыв выпускника"""
    name = models.CharField('Имя', max_length=200)
    profession = models.ForeignKey(Profession, on_delete=models.SET_NULL,
                                   null=True, blank=True, verbose_name='Профессия')
    text = models.TextField('Текст отзыва')
    rating = models.PositiveSmallIntegerField('Оценка (1-5)', default=5)
    published = models.BooleanField('Опубликовано', default=True)
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class FAQ(models.Model):
    """Частые вопросы"""
    question = models.CharField('Вопрос', max_length=500)
    answer = models.TextField('Ответ')
    order = models.PositiveSmallIntegerField('Порядок', default=0)
    published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'

    def __str__(self):
        return self.question