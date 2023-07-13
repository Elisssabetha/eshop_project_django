from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    product_name = models.CharField(max_length=250, verbose_name='Название продукта')
    product_description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='products/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена', **NULLABLE)
    date_of_creation = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name='Дата создания')
    last_modified_date = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'{self.product_name} - {self.price}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Category(models.Model):
    category_name = models.CharField(max_length=100, verbose_name='Категории')
    category_description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.category_name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
