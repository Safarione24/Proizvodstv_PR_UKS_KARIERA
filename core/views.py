from datetime import date

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from .models import Profession, Group, News


def home(request):
    today = date.today()
    groups = (Group.objects
              .filter(published=True, exam_date__gte=today)
              .select_related('profession', 'category')
              .order_by('start_date', 'exam_date'))
    by_date = {}
    for g in groups:
        by_date.setdefault(g.start_date, []).append(g)
    latest_news = News.objects.filter(published=True)[:3]
    return render(request, 'core/home.html', {
        'by_date': sorted(by_date.items()),
        'latest_news': latest_news,
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
    return render(request, 'core/profession_detail.html', {
        'profession': profession, 'groups': groups,
    })


def news_list(request):
    return render(request, 'core/news_list.html', {
        'news': News.objects.filter(published=True),
    })


def news_detail(request, slug):
    item = get_object_or_404(News, slug=slug, published=True)
    return render(request, 'core/news_detail.html', {'item': item})


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