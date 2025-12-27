from django.db import models
from django.core.exceptions import ValidationError
import re

class SiteContent(models.Model):
    """Модель для хранения текстового контента сайта"""
    CONTENT_TYPES = [
        ('greeting_title', 'Приветствие в заголовке'),
        ('greeting_subtitle', 'Подзаголовок приветствия'),
        ('about_paragraph1', 'Первый абзац "Обо мне"'),
        ('about_paragraph2', 'Второй абзац "Обо мне"'),
        ('projects_count', 'Количество проектов (цифра)'),
        ('clients_count', 'Количество клиентов (цифра)'),
        ('experience_years', 'Лет опыта (цифра)'),
        # Ссылки на социальные сети
        ('social_max_url', 'Ссылка на MAX'),
        ('social_vk_url', 'Ссылка на VK'),
        ('social_telegram_url', 'Ссылка на Telegram'),
        ('social_whatsapp_url', 'Ссылка на WhatsApp'),
    ]
    
    key = models.CharField(
        max_length=50,
        choices=CONTENT_TYPES,
        unique=True,
        verbose_name="Тип контента"
    )
    content = models.TextField(verbose_name="Содержимое")
    description = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Описание (для администратора)"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    
    class Meta:
        verbose_name = "Контент сайта"
        verbose_name_plural = "Контент сайта"
        ordering = ['key']
    
    def __str__(self):
        return f"{self.get_key_display()}"
    
    def clean(self):
        """Валидация и преобразование ссылок"""
        super().clean()
        
        if self.key == 'social_whatsapp_url':
            # Очищаем номер от всего кроме цифр
            phone = re.sub(r'\D', '', self.content)
            
            if not phone:
                raise ValidationError({'content': 'Введите номер телефона для WhatsApp'})
            
            if len(phone) < 10:
                raise ValidationError({'content': 'Номер телефона слишком короткий'})
            
            # Если номер в формате 8..., меняем на 7
            if phone.startswith('8') and len(phone) == 11:
                phone = '7' + phone[1:]
            
            # Сохраняем оригинальный номер, но для использования преобразуем
            self.content = phone  # Сохраняем очищенный номер
            
        elif self.key == 'social_vk_url':
            # Для VK: может быть ID, короткое имя или полная ссылка
            vk_value = self.content.strip()
            
            if not vk_value:
                raise ValidationError({'content': 'Введите ID пользователя VK'})
            
            # Если это уже ссылка, оставляем как есть
            if vk_value.startswith('http'):
                # Проверяем что это vk.com
                if 'vk.com' not in vk_value:
                    raise ValidationError({'content': 'Неверная ссылка VK. Должна быть на vk.com'})
                # Сохраняем как есть
            else:
                # Это ID или короткое имя
                # Сохраняем как есть, обработка будет в utils
                pass
    
    def save(self, *args, **kwargs):
        self.clean()  # Вызываем валидацию перед сохранением
        super().save(*args, **kwargs)


# sitecontent/models.py - добавляем после SiteContent
class ContactInfo(models.Model):
    """Модель для хранения контактной информации"""
    CONTACT_TYPES = [
        ('phone', 'Телефон'),
        ('email', 'Email'),
        ('address', 'Адрес'),
        ('work_hours', 'Часы работы'),
        ('instagram', 'Instagram'),
        ('whatsapp', 'WhatsApp (только номер)'),
        ('telegram', 'Telegram (@username)'),
        ('vk', 'VK (ID или ник)'),
    ]
    
    contact_type = models.CharField(
        max_length=20,
        choices=CONTACT_TYPES,
        unique=True,
        verbose_name="Тип контакта"
    )
    value = models.CharField(max_length=200, verbose_name="Значение")
    description = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Описание"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    
    class Meta:
        verbose_name = "Контактная информация"
        verbose_name_plural = "Контактные данные"
        ordering = ['order', 'contact_type']
    
    def __str__(self):
        return f"{self.get_contact_type_display()}: {self.value}"