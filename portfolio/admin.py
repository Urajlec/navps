from django.contrib import admin
from .models import Category, Photo

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ['name', 'order', 'created_at']
    
    # Редактируемые поля прямо в списке
    list_editable = ['order']
    
    # Поля для поиска
    search_fields = ['name', 'description']
    
    # Настройки для русской админки
    list_display_links = ['name']  # Ссылка на редактирование
    list_filter = ['created_at']  # Фильтры
    ordering = ['order', 'name']  # Сортировка по умолчанию
    
    # Русские названия для интерфейса
    list_per_page = 20  # Элементов на страницу
    
    # Можно добавить description для полей, если нужно
    def get_queryset(self, request):
        """Оптимизация запросов"""
        return super().get_queryset(request).select_related()


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ['title', 'category', 'uploaded_at', 'is_featured']
    
    # Редактируемые поля прямо в списке
    list_editable = ['is_featured']
    
    # Фильтры справа
    list_filter = ['category', 'is_featured', 'uploaded_at']
    
    # Поля для поиска
    search_fields = ['title', 'description']
    
    # Настройки для русской админки
    list_display_links = ['title']  # Ссылка на редактирование
    date_hierarchy = 'uploaded_at'  # Навигация по датам
    ordering = ['-uploaded_at']  # Сортировка по умолчанию (новые сверху)
    
    # Русские названия для интерфейса
    list_per_page = 30  # Элементов на страницу
    
    # Оптимизация запросов (предзагрузка категорий)
    def get_queryset(self, request):
        """Оптимизация запросов - предзагрузка категорий"""
        return super().get_queryset(request).select_related('category')