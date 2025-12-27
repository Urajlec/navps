from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Название категории"))
    description = models.TextField(verbose_name=_("Описание категории"))
    cover_image = models.ImageField(
        upload_to='category_covers/',
        verbose_name=_("Обложка категории"),
        blank=True,
        null=True
    )
    order = models.IntegerField(default=0, verbose_name=_("Порядок отображения"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    
    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Photo(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Название фотографии"))
    description = models.TextField(verbose_name=_("Описание фотографии"), blank=True)
    image = models.ImageField(upload_to='photos/', verbose_name=_("Изображение"))
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name=_("Категория")
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата загрузки"))
    is_featured = models.BooleanField(default=False, verbose_name=_("Избранное (показать на главной)"))
    
    class Meta:
        verbose_name = _("Фотография")
        verbose_name_plural = _("Фотографии")
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.title