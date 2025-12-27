from django.core.management.base import BaseCommand
from sitecontent.models import SiteContent

class Command(BaseCommand):
    help = 'Создание начального контента сайта'

    def handle(self, *args, **kwargs):
        initial_content = [
            {
                'key': 'greeting_title',
                'content': 'Привет, я Егор',
                'description': 'Приветствие в заголовке блока "О фотографе"'
            },
            {
                'key': 'greeting_subtitle',
                'content': 'Профессиональный фотограф с 15 летним опытом',
                'description': 'Подзаголовок приветствия'
            },
            {
                'key': 'about_paragraph1',
                'content': 'Специализируюсь на предметной, бизнес-портретной и студийной съёмке.',
                'description': 'Первый абзац текста "Обо мне"'
            },
            {
                'key': 'about_paragraph2',
                'content': 'В работе использую профессиональную технику и индивидуальный подход к каждому клиенту.',
                'description': 'Второй абзац текста "Обо мне"'
            },
            {
                'key': 'projects_count',
                'content': '114',
                'description': 'Количество проектов (цифра в статистике)'
            },
            {
                'key': 'clients_count',
                'content': '368',
                'description': 'Количество клиентов (цифра в статистике)'
            },
            {
                'key': 'experience_years',
                'content': '15',
                'description': 'Лет опыта (цифра в статистике)'
            },
        ]
        
        for item in initial_content:
            SiteContent.objects.update_or_create(
                key=item['key'],
                defaults={
                    'content': item['content'],
                    'description': item['description']
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Начальный контент успешно создан!'))