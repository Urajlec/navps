from .models import SiteContent
import re

def get_site_content():
    """Получить весь контент сайта в виде словаря"""
    contents = SiteContent.objects.all()
    content_dict = {}
    
    # Заполняем значениями из базы
    for item in contents:
        content_dict[item.key] = item.content
    
    # Устанавливаем значения по умолчанию, если в базе их нет
    defaults = {
        'greeting_title': 'Привет, я Егор',
        'greeting_subtitle': 'Профессиональный фотограф с 15 летним опытом',
        'about_paragraph1': 'Специализируюсь на предметной, бизнес-портретной и студийной съёмке.',
        'about_paragraph2': 'В работе использую профессиональную технику и индивидуальный подход к каждому клиенту.',
        'projects_count': '114',
        'clients_count': '368',
        'experience_years': '15',
        # Дефолтные ссылки для соцсетей
        'social_max_url': '#',
        'social_vk_url': '#',
        'social_telegram_url': '#',
        'social_whatsapp_url': '#',
    }
    
    # Объединяем значения из базы с дефолтными
    for key, value in defaults.items():
        if key not in content_dict:
            content_dict[key] = value
    
    # Преобразуем ссылки для использования в шаблоне
    return process_social_links(content_dict)


def process_social_links(content_dict):
    """Преобразует сырые данные в готовые ссылки"""
    processed = content_dict.copy()
    
    # WhatsApp: номер → ссылка
    whatsapp = processed.get('social_whatsapp_url', '#')
    if whatsapp != '#':
        phone = re.sub(r'\D', '', whatsapp)
        if phone:
            if phone.startswith('8') and len(phone) == 11:
                phone = '7' + phone[1:]
            processed['social_whatsapp_url'] = f'https://wa.me/{phone}'
        else:
            processed['social_whatsapp_url'] = '#'
    
    # VK: ID/никнейм → ссылка
    vk = processed.get('social_vk_url', '#')
    if vk != '#':
        if vk.startswith('http'):
            processed['social_vk_url'] = vk
        else:
            vk_clean = vk.strip().lstrip('@')
            if vk_clean:
                if vk_clean.isdigit():
                    processed['social_vk_url'] = f'https://vk.com/id{vk_clean}'
                else:
                    processed['social_vk_url'] = f'https://vk.com/{vk_clean}'
            else:
                processed['social_vk_url'] = '#'
    
    # Telegram: @username или username → ссылка
    telegram = processed.get('social_telegram_url', '#')
    if telegram != '#':
        telegram_clean = telegram.strip().lstrip('@')
        if telegram_clean:
            processed['social_telegram_url'] = f'https://t.me/{telegram_clean}'
        else:
            processed['social_telegram_url'] = '#'
    
    # MAX: оставляем как есть или добавляем https://
    max_link = processed.get('social_max_url', '#')
    if max_link != '#':
        if max_link.startswith('http'):
            processed['social_max_url'] = max_link
        elif max_link:
            processed['social_max_url'] = f'https://{max_link}'
        else:
            processed['social_max_url'] = '#'
    
    return processed

# УДАЛИТЬ ВСЁ ЧТО НИЖЕ (если есть функции про ContactInfo)