from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('add-photo/', views.add_photo, name='add_photo'),
    path('category/<int:category_id>/add-photo/', views.add_photo_to_category, name='add_photo_to_category'),
]

# Для работы с медиафайлами в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)