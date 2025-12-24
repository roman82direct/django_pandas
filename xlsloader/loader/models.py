from django.db import models


class CommonFields(models.Model):
    articul = models.CharField('art', unique=True, max_length=7)
    title = models.CharField('title', max_length=64)
    description = models.CharField('description', max_length=128)
    created_at = models.DateTimeField('created', auto_now_add=True)
    updated_at = models.DateTimeField('updated', auto_now=True)

    class Meta:
        abstract = True
        ordering = ('articul')

    def __str__(self):
        return self.title


class Group(CommonFields):
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class MainCategory(CommonFields):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Основная категория'
        verbose_name_plural = 'Основные категории'
        default_related_name = 'maincategories'


class SecondCategory(CommonFields):
    maincategory = models.ForeignKey(MainCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Категория 2-го уровня'
        verbose_name_plural = 'Категории 2-го уровня'
        default_related_name = 'secondcategories'
