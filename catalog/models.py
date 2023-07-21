from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название продукта')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='products/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена', **NULLABLE)
    date_of_creation = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name='Дата создания')
    last_modified_date = models.DateTimeField(auto_now=False, auto_now_add=False,
                                              verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'{self.name} - {self.price}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Category(models.Model):
    category = models.CharField(max_length=100, verbose_name='Категории')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.category}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, verbose_name='Slug')
    content = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='blog_preview/', **NULLABLE, verbose_name='Превью (изображение)')
    created_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Признак публикации')
    views_count = models.PositiveIntegerField(default=0, editable=False, verbose_name='Количество просмотров')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
