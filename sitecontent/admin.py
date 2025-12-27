from django.contrib import admin
from .models import SiteContent

@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ['key_display', 'content_preview', 'processed_content_preview', 'updated_at']
    list_filter = ['key']
    search_fields = ['content', 'description']
    readonly_fields = ['updated_at']  # ← УБРАЛИ 'help_text' отсюда
    
    fieldsets = [
        ('Основная информация', {
            'fields': ['key', 'description', 'content'],
            'description': '''
                <h3>Подсказки для заполнения:</h3>
                <ul>
                    <li><strong>WhatsApp:</strong> просто номер телефона (79991234567 или 89991234567)</li>
                    <li><strong>VK:</strong> ID или никнейм (durov или 123456)</li>
                    <li><strong>Telegram:</strong> @username или просто username</li>
                    <strong>MAX:</strong> адрес (max.example.com)</li>
                </ul>
            '''
        }),
        ('Системная информация', {
            'fields': ['updated_at'],
            'classes': ['collapse']
        }),
    ]
    
    def key_display(self, obj):
        return obj.get_key_display()
    key_display.short_description = "Тип контента"
    
    def content_preview(self, obj):
        """Превью оригинального содержимого"""
        if len(obj.content) > 30:
            return obj.content[:30] + "..."
        return obj.content
    content_preview.short_description = "Введённое значение"
    
    def processed_content_preview(self, obj):
        """Превью обработанной ссылки"""
        from .utils import process_social_links
        processed = process_social_links({obj.key: obj.content})
        link = processed.get(obj.key, '#')
        
        if link == '#':
            return 'Не настроено'
        if len(link) > 40:
            return link[:40] + "..."
        return link
    processed_content_preview.short_description = "Будет ссылкой"