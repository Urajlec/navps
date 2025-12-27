from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Category, Photo
from .forms import PhotoUploadForm
from sitecontent.utils import get_site_content


def index(request):
    """Главная страница"""
    categories = Category.objects.prefetch_related('photos').all()
    featured_photos = Photo.objects.filter(is_featured=True)[:5]
    
    # Получаем контент из базы данных
    site_content = get_site_content()
    
    context = {
        'categories': categories,
        'featured_photos': featured_photos,
        'content': site_content,
    }
    return render(request, 'portfolio/index.html', context)


def category_detail(request, category_id):
    """Детальная страница категории"""
    category = get_object_or_404(Category, id=category_id)
    photos = category.photos.all()
    
    # Получаем контент
    site_content = get_site_content()
    
    context = {
        'category': category,
        'photos': photos,
        'content': site_content,
    }
    return render(request, 'portfolio/category_detail.html', context)


@login_required
@permission_required('portfolio.add_photo', raise_exception=True)
def add_photo(request):
    """Добавление новой фотографии"""
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            messages.success(request, f'Фотография "{photo.title}" успешно добавлена!')
            return redirect('category_detail', category_id=photo.category.id)
    else:
        form = PhotoUploadForm()
    
    site_content = get_site_content()
    
    context = {
        'form': form,
        'content': site_content,
    }
    return render(request, 'portfolio/add_photo.html', context)


@login_required
@permission_required('portfolio.add_photo', raise_exception=True)
def add_photo_to_category(request, category_id):
    """Добавление фотографии в конкретную категорию"""
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.category = category
            photo.save()
            messages.success(request, f'Фотография "{photo.title}" успешно добавлена в категорию "{category.name}"!')
            return redirect('category_detail', category_id=category.id)
    else:
        # Устанавливаем категорию по умолчанию
        form = PhotoUploadForm(initial={'category': category})
    
    site_content = get_site_content()
    
    context = {
        'form': form,
        'category': category,
        'content': site_content,
    }
    return render(request, 'portfolio/add_photo.html', context)