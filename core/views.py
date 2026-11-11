from datetime import date, timedelta

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Category, Profession, Group, News, Application, Photo, Review, FAQ


def home(request):
    today = date.today()
    groups = (Group.objects
              .filter(published=True, exam_date__gte=today)
              .select_related('profession', 'category')
              .order_by('start_date', 'exam_date'))
    
    # Фильтр по категориям
    cat_slug = request.GET.get('category')
    if cat_slug:
        groups = groups.filter(category__slug=cat_slug)

    # Поиск по названию профессии
    q = request.GET.get('q', '').strip()
    if q:
        groups = groups.filter(profession__name__icontains=q)

    by_date = {}
    for g in groups:
        by_date.setdefault(g.start_date, []).append(g)

    # Скоро экзамен (ближайшие 7 дней)
    soon_exam = (Group.objects
                 .filter(published=True, exam_date__gte=today, exam_date__lte=today + timedelta(days=7))
                 .select_related('profession')
                 .order_by('exam_date'))

    categories = Category.objects.all()
    latest_news = News.objects.filter(published=True)[:3]
    photos = Photo.objects.filter(published=True)[:6]
    reviews = Review.objects.filter(published=True)[:3]
    faqs = FAQ.objects.filter(published=True)

    return render(request, 'core/home.html', {
        'by_date': sorted(by_date.items()),
        'soon_exam': soon_exam,
        'categories': categories,
        'selected_category': cat_slug,
        'q': q,
        'latest_news': latest_news,
        'photos': photos,
        'reviews': reviews,
        'faqs': faqs,
    })


def professions(request):
    qs = (Profession.objects.filter(published=True)
          .select_related('category')
          .order_by('category__order', 'name'))
    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(name__icontains=q)
    return render(request, 'core/profession_list.html', {'professions': qs, 'q': q})


def profession_detail(request, slug):
    profession = get_object_or_404(Profession, slug=slug, published=True)
    groups = (Group.objects
              .filter(profession=profession, published=True, exam_date__gte=date.today())
              .order_by('start_date'))

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        if name and phone:
            Application.objects.create(
                name=name, phone=phone, profession=profession,
                comment=request.POST.get('comment', '').strip()
            )
            messages.success(request, 'Спасибо! Ваша заявка принята. Мы свяжемся с вами.')
            return redirect('profession_detail', slug=slug)
        else:
            messages.error(request, 'Заполните имя и телефон.')

    return render(request, 'core/profession_detail.html', {
        'profession': profession,
        'groups': groups,
    })


def news_list(request):
    return render(request, 'core/news_list.html', {
        'news': News.objects.filter(published=True),
    })


def news_detail(request, slug):
    item = get_object_or_404(News, slug=slug, published=True)
    return render(request, 'core/news_detail.html', {'item': item})


def documents(request):
    return render(request, 'core/documents.html')


# ---------- JSON API ----------

def api_groups(request):
    today = date.today()
    data = [{
        'profession': g.profession.name,
        'profession_slug': g.profession.slug,
        'category': g.category.name,
        'start_date': str(g.start_date),
        'exam_date': str(g.exam_date),
        'note': g.note,
    } for g in Group.objects.filter(published=True, exam_date__gte=today)
        .select_related('profession', 'category').order_by('start_date')]
    return JsonResponse(data, safe=False)


def api_professions(request):
    data = [{
        'name': p.name, 'slug': p.slug, 'category': p.category.name,
        'description': p.description, 'url': p.get_absolute_url(),
    } for p in Profession.objects.filter(published=True).select_related('category')]
    return JsonResponse(data, safe=False)


def api_news(request):
    data = [{
        'title': n.title, 'slug': n.slug, 'text': n.text,
        'created_at': n.created_at.isoformat(),
    } for n in News.objects.filter(published=True)]
    return JsonResponse(data, safe=False)