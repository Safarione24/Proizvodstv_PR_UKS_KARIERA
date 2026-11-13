from datetime import date, timedelta
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Category, Profession, Group, News, Application, Photo, Review, FAQ

def home(request):
    today = date.today()
    groups = (Group.objects.filter(published=True, exam_date__gte=today)
              .select_related('profession', 'category').order_by('start_date', 'exam_date'))
    
    cat_slug = request.GET.get('category')
    if cat_slug:
        groups = groups.filter(category__slug=cat_slug)

    q = request.GET.get('q', '').strip()
    if q:
        groups = groups.filter(profession__name__icontains=q)

    by_date = {}
    for g in groups:
        by_date.setdefault(g.start_date, []).append(g)

    soon_exam = (Group.objects.filter(published=True, exam_date__gte=today, exam_date__lte=today + timedelta(days=7))
                 .select_related('profession').order_by('exam_date'))

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
        'vision_mode': request.session.get('vision_mode', False),
    })

def professions(request):
    qs = (Profession.objects.filter(published=True)
          .select_related('category').order_by('category__order', 'name'))
    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(name__icontains=q)
    return render(request, 'core/profession_list.html', {
        'professions': qs, 
        'q': q,
        'vision_mode': request.session.get('vision_mode', False),
    })

def profession_detail(request, slug):
    profession = get_object_or_404(Profession, slug=slug, published=True)
    groups = (Group.objects.filter(profession=profession, published=True, exam_date__gte=date.today())
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
        'vision_mode': request.session.get('vision_mode', False),
    })

def self_prep(request):
    faqs = FAQ.objects.filter(published=True)
    return render(request, 'core/self_prep.html', {
        'faqs': faqs,
        'vision_mode': request.session.get('vision_mode', False),
    })

def about(request):
    photos = Photo.objects.filter(published=True)
    return render(request, 'core/about.html', {
        'photos': photos,
        'vision_mode': request.session.get('vision_mode', False),
    })

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        message_text = request.POST.get('message', '').strip()
        
        if name and email and message_text:
            Application.objects.create(
                name=name,
                phone=phone,
                comment=f"Email: {email}\n\n{message_text}"
            )
            messages.success(request, 'Спасибо! Ваше сообщение отправлено.')
            return redirect('contacts')
        else:
            messages.error(request, 'Заполните обязательные поля.')
    
    return render(request, 'core/contacts.html', {
        'vision_mode': request.session.get('vision_mode', False),
    })

# ВКЛЮЧЕНИЕ / ВЫКЛЮЧЕНИЕ РЕЖИМА СЛАБОВИДЯЩИХ
def toggle_vision(request):
    current_mode = request.session.get('vision_mode', False)
    request.session['vision_mode'] = not current_mode
    # Возвращаем пользователя на ту страницу, с которой он пришел
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def news_list(request):
    return render(request, 'core/news_list.html', {
        'news': News.objects.filter(published=True),
        'vision_mode': request.session.get('vision_mode', False),
    })

def news_detail(request, slug):
    item = get_object_or_404(News, slug=slug, published=True)
    return render(request, 'core/news_detail.html', {
        'item': item,
        'vision_mode': request.session.get('vision_mode', False),
    })

def documents(request):
    return render(request, 'core/documents.html', {
        'vision_mode': request.session.get('vision_mode', False),
    })

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