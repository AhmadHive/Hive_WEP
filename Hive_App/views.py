from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import UserProfile, News, ComicSeries, ComicChapter, ComicPage
from .forms import UserRegistrationForm, NewsletterForm, NewsForm, ComicSeriesForm, ComicChapterForm, ComicPageForm, BulkComicPagesForm
import json
from datetime import timedelta
import csv
from .models import Entrepreneur, Blog
from .forms import EntrepreneurForm, BlogForm
from django.db.models import Sum
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def home(request):
    # استخدم News.objects بدلاً من news.objects
    recent_news = News.objects.all().order_by('-publish_date')[:5]  # آخر 5 أخبار
    newsletter_form = NewsletterForm()
    
    if request.method == 'POST' and 'newsletter_email' in request.POST:
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            newsletter_form.save()
            messages.success(request, 'Successfully subscribed to newsletter!')
    
    context = {
        'recent_news': recent_news,
        'newsletter_form': newsletter_form,
    }
    return render(request, 'home.html', context)

def comics(request):
    series_list = ComicSeries.objects.all()
    return render(request, 'comics.html', {'series_list': series_list})

def comic_chapter(request, series_id, chapter_number):
    series = get_object_or_404(ComicSeries, id=series_id)
    chapter = get_object_or_404(ComicChapter, series=series, chapter_number=chapter_number)
    pages = chapter.pages.all().order_by('page_number')
    
    return render(request, 'comic_chapter.html', {
        'series': series,
        'chapter': chapter,
        'pages': pages,
    })

def news(request):
    news_list = News.objects.all().order_by('-publish_date')
    return render(request, 'news.html', {'news_list': news_list})

def news_detail(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    return render(request, 'news_detail.html', {'news_item': news_item})

from django.http import JsonResponse
import json

from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        print("POST data:", request.POST)
        
        form = UserRegistrationForm(request.POST)
        print("Form is valid:", form.is_valid())
        
        if form.is_valid():
            # حفظ مستخدم Django
            user = form.save()
            
            # إنشاء UserProfile
            user_profile = UserProfile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                age=form.cleaned_data['age'],
                university=form.cleaned_data['university'],
                college=form.cleaned_data['college'],
                major=form.cleaned_data['major'],
                phone_number=form.cleaned_data['phone_number'],
                email=form.cleaned_data['email']
            )
            
            # 🔥 **هذا هو الجزء المهم: تسجيل الدخول تلقائياً**
            # الطريقة 1: استخدام login مباشرة
            login(request, user)
            
            # أو الطريقة 2: المصادقة أولاً ثم تسجيل الدخول
            # user = authenticate(email=user.email, password=form.cleaned_data['password1'])
            # if user is not None:
            #     login(request, user)
            
            print("User logged in successfully")
            messages.success(request, 'Account created successfully! Welcome to Hive!')
            return redirect('home')
        else:
            print("Form errors:", form.errors)
            return render(request, 'register.html', {'form': form})
    
    else:
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})
    
    
def is_superuser(user):
    return user.is_superuser


def custom_login(request):  # اسم مختلف تماماً
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        # استخدام النموذج العادي مع تعديلات بسيطة
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # استخدام login العادي
            messages.success(request, f'Welcome back, {user.email}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'login.html')

@user_passes_test(is_superuser)
@login_required
def admin_panel(request):
    today = timezone.now().date()
    now = timezone.now()
    yesterday = today - timedelta(days=1)
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # آخر 24 ساعة
    last_24_hours = now - timedelta(hours=24)
    
    # الإحصائيات الرئيسية
    total_users = UserProfile.objects.count()
    total_news = News.objects.count()
    total_comics = ComicChapter.objects.count()
    total_series = ComicSeries.objects.count()
    
    # الإحصائيات اليومية (آخر 24 ساعة)
    users_today = UserProfile.objects.filter(join_date__gte=last_24_hours).count()
    news_today = News.objects.filter(publish_date__gte=last_24_hours).count()
    comics_today = ComicChapter.objects.filter(created_date__gte=last_24_hours).count()
    
    # الإحصائيات الأمس
    users_yesterday = UserProfile.objects.filter(
        join_date__date=yesterday
    ).count()
    news_yesterday = News.objects.filter(
        publish_date__date=yesterday
    ).count()
    comics_yesterday = ComicChapter.objects.filter(
        created_date__date=yesterday
    ).count()
    
    # الإحصائيات الأسبوعية
    users_week = UserProfile.objects.filter(join_date__date__gte=week_ago).count()
    news_week = News.objects.filter(publish_date__date__gte=week_ago).count()
    comics_week = ComicChapter.objects.filter(created_date__date__gte=week_ago).count()
    
    # الإحصائيات الشهرية
    users_month = UserProfile.objects.filter(join_date__date__gte=month_ago).count()
    news_month = News.objects.filter(publish_date__date__gte=month_ago).count()
    comics_month = ComicChapter.objects.filter(created_date__date__gte=month_ago).count()
    
    # حساب النسبة المئوية للتغير
    def calculate_change(current, previous):
        if previous == 0:
            return 100 if current > 0 else 0
        return round(((current - previous) / previous) * 100, 1)
    
    users_change = calculate_change(users_today, users_yesterday)
    news_change = calculate_change(news_today, news_yesterday)
    comics_change = calculate_change(comics_today, comics_yesterday)
    
    context = {
        'total_users': total_users,
        'total_news': total_news,
        'total_comics': total_comics,
        'total_series': total_series,
        'users_today': users_today,
        'news_today': news_today,
        'comics_today': comics_today,
        'users_yesterday': users_yesterday,
        'news_yesterday': news_yesterday,
        'comics_yesterday': comics_yesterday,
        'users_week': users_week,
        'news_week': news_week,
        'comics_week': comics_week,
        'users_month': users_month,
        'news_month': news_month,
        'comics_month': comics_month,
        'users_change': users_change,
        'news_change': news_change,
        'comics_change': comics_change,
    }
    
    return render(request, 'admin_panel.html', context)
# إدارة الأخبار
@user_passes_test(is_superuser)
@login_required
def news_management(request):
    news_list = News.objects.all().order_by('-publish_date')
    return render(request, 'admin/news_management.html', {'news_list': news_list})

@user_passes_test(is_superuser)
@login_required
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news_item = form.save(commit=False)
            news_item.author = request.user
            news_item.save()
            messages.success(request, 'News added successfully!')
            return redirect('news_management')
    else:
        form = NewsForm(initial={'publish_date': timezone.now()})
    
    return render(request, 'admin/add_news.html', {'form': form})

@user_passes_test(is_superuser)
@login_required
def edit_news(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'News updated successfully!')
            return redirect('news_management')
    else:
        form = NewsForm(instance=news_item)
    
    return render(request, 'admin/edit_news.html', {'form': form, 'news_item': news_item})

@user_passes_test(is_superuser)
@login_required
def delete_news(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    
    if request.method == 'POST':
        news_item.delete()
        messages.success(request, 'News deleted successfully!')
        return redirect('news_management')
    
    return render(request, 'admin/delete_news.html', {'news_item': news_item})

# إدارة الكوميكس
@user_passes_test(is_superuser)
@login_required
def comics_management(request):
    series_list = ComicSeries.objects.all()
    total_chapters = ComicChapter.objects.count()
    total_pages = ComicPage.objects.count()
    latest_series = series_list.first().title if series_list.exists() else "None"
    
    context = {
        'series_list': series_list,
        'total_chapters': total_chapters,
        'total_pages': total_pages,
        'latest_series': latest_series,
    }
    return render(request, 'admin/comics_management.html', context)

@user_passes_test(is_superuser)
@login_required
def add_comic_series(request):
    if request.method == 'POST':
        form = ComicSeriesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comic series added successfully!')
            return redirect('comics_management')
    else:
        form = ComicSeriesForm()
    
    return render(request, 'admin/add_comic_series.html', {'form': form})

@user_passes_test(is_superuser)
@login_required
def edit_comic_series(request, series_id):
    series = get_object_or_404(ComicSeries, id=series_id)
    
    if request.method == 'POST':
        form = ComicSeriesForm(request.POST, request.FILES, instance=series)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comic series updated successfully!')
            return redirect('comics_management')
    else:
        form = ComicSeriesForm(instance=series)
    
    return render(request, 'admin/edit_comic_series.html', {'form': form, 'series': series})

@user_passes_test(is_superuser)
@login_required
def delete_comic_series(request, series_id):
    series = get_object_or_404(ComicSeries, id=series_id)
    
    if request.method == 'POST':
        series.delete()
        messages.success(request, 'Comic series deleted successfully!')
        return redirect('comics_management')
    
    return render(request, 'admin/delete_comic_series.html', {'series': series})

@user_passes_test(is_superuser)
@login_required
def chapter_management(request, series_id):
    series = get_object_or_404(ComicSeries, id=series_id)
    chapters = series.chapters.all().order_by('chapter_number')
    
    return render(request, 'admin/chapter_management.html', {
        'series': series,
        'chapters': chapters
    })

@user_passes_test(is_superuser)
@login_required
def add_chapter(request, series_id):
    series = get_object_or_404(ComicSeries, id=series_id)
    
    if request.method == 'POST':
        try:
            # الحصول على البيانات من النموذج
            title = request.POST.get('title', '').strip()
            chapter_number = request.POST.get('chapter_number', '1').strip()
            description = request.POST.get('description', '').strip()
            
            # التحقق من البيانات
            if not title:
                messages.error(request, 'يجب إدخال عنوان الفصل')
                return render(request, 'admin/add_chapter.html', {'series': series})
            
            try:
                chapter_number = int(chapter_number)
                if chapter_number < 1:
                    messages.error(request, 'رقم الفصل يجب أن يكون 1 أو أكثر')
                    return render(request, 'admin/add_chapter.html', {'series': series})
            except ValueError:
                messages.error(request, 'رقم الفصل يجب أن يكون رقماً صحيحاً')
                return render(request, 'admin/add_chapter.html', {'series': series})
            
            # التحقق من عدم وجود فصل بنفس الرقم
            existing_chapter = ComicChapter.objects.filter(
                series=series, 
                chapter_number=chapter_number
            ).first()
            
            if existing_chapter:
                messages.error(request, f'يوجد بالفعل فصل برقم {chapter_number}')
                return render(request, 'admin/add_chapter.html', {'series': series})
            
            # إنشاء الفصل
            chapter = ComicChapter.objects.create(
                series=series,
                title=title,
                chapter_number=chapter_number,
                description=description
            )
            
            messages.success(request, f'تم إضافة الفصل "{title}" بنجاح!')
            return redirect('chapter_management', series_id=series_id)
            
        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء إضافة الفصل: {str(e)}')
    
    else:
        # اقترح الرقم التالي للفصل
        last_chapter = series.chapters.order_by('-chapter_number').first()
        next_chapter_number = last_chapter.chapter_number + 1 if last_chapter else 1
        
        context = {
            'series': series,
            'next_chapter_number': next_chapter_number
        }
        return render(request, 'admin/add_chapter.html', context)
    
@user_passes_test(is_superuser)
@login_required
def edit_chapter(request, chapter_id):
    chapter = get_object_or_404(ComicChapter, id=chapter_id)
    
    if request.method == 'POST':
        form = ComicChapterForm(request.POST, instance=chapter)
        if form.is_valid():
            form.save()
            messages.success(request, 'Chapter updated successfully!')
            return redirect('chapter_management', series_id=chapter.series.id)
    else:
        form = ComicChapterForm(instance=chapter)
    
    return render(request, 'admin/edit_chapter.html', {
        'form': form,
        'chapter': chapter
    })

@user_passes_test(is_superuser)
@login_required
def delete_chapter(request, chapter_id):
    chapter = get_object_or_404(ComicChapter, id=chapter_id)
    series_id = chapter.series.id
    
    if request.method == 'POST':
        chapter.delete()
        messages.success(request, 'Chapter deleted successfully!')
        return redirect('chapter_management', series_id=series_id)
    
    return render(request, 'admin/delete_chapter.html', {'chapter': chapter})

@user_passes_test(is_superuser)
@login_required
def page_management(request, chapter_id):
    chapter = get_object_or_404(ComicChapter, id=chapter_id)
    pages = chapter.pages.all().order_by('page_number')
    
    return render(request, 'admin/page_management.html', {
        'chapter': chapter,
        'pages': pages
    })

@user_passes_test(is_superuser)
@login_required
def add_page(request, chapter_id):
    chapter = get_object_or_404(ComicChapter, id=chapter_id)
    
    if request.method == 'POST':
        try:
            # الحصول على البيانات من النموذج
            page_number = request.POST.get('page_number', '1').strip()
            image = request.FILES.get('image')
            
            # التحقق من البيانات
            if not image:
                messages.error(request, 'يجب اختيار صورة للصفحة')
                return redirect('add_page', chapter_id=chapter_id)
            
            try:
                page_number = int(page_number)
                if page_number < 1:
                    messages.error(request, 'رقم الصفحة يجب أن يكون 1 أو أكثر')
                    return redirect('add_page', chapter_id=chapter_id)
            except ValueError:
                messages.error(request, 'رقم الصفحة يجب أن يكون رقماً صحيحاً')
                return redirect('add_page', chapter_id=chapter_id)
            
            # التحقق من عدم وجود صفحة بنفس الرقم
            existing_page = ComicPage.objects.filter(
                chapter=chapter, 
                page_number=page_number
            ).first()
            
            if existing_page:
                messages.error(request, f'يوجد بالفعل صفحة برقم {page_number} في هذا الفصل')
                return redirect('add_page', chapter_id=chapter_id)
            
            # إنشاء الصفحة
            page = ComicPage.objects.create(
                chapter=chapter,
                page_number=page_number,
                image=image
            )
            
            messages.success(request, f'تم إضافة الصفحة {page_number} بنجاح!')
            return redirect('page_management', chapter_id=chapter_id)
            
        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء إضافة الصفحة: {str(e)}')
    
    else:
        # اقترح الرقم التالي للصفحة
        last_page = chapter.pages.order_by('-page_number').first()
        next_page_number = last_page.page_number + 1 if last_page else 1
        
        context = {
            'chapter': chapter,
            'next_page_number': next_page_number
        }
        return render(request, 'admin/add_page.html', context)

@user_passes_test(is_superuser)
@login_required
def bulk_add_pages(request, chapter_id):
    chapter = get_object_or_404(ComicChapter, id=chapter_id)
    
    if request.method == 'POST':
        form = BulkComicPagesForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('images')
            last_page = chapter.pages.order_by('-page_number').first()
            next_page_number = last_page.page_number + 1 if last_page else 1
            
            for i, image in enumerate(images):
                ComicPage.objects.create(
                    chapter=chapter,
                    image=image,
                    page_number=next_page_number + i
                )
            
            messages.success(request, f'{len(images)} pages added successfully!')
            return redirect('page_management', chapter_id=chapter_id)
    else:
        form = BulkComicPagesForm(initial={'chapter': chapter})
    
    return render(request, 'admin/bulk_add_pages.html', {
        'form': form,
        'chapter': chapter
    })

@user_passes_test(is_superuser)
@login_required
def edit_page(request, page_id):
    page = get_object_or_404(ComicPage, id=page_id)
    
    if request.method == 'POST':
        form = ComicPageForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            form.save()
            messages.success(request, 'Page updated successfully!')
            return redirect('page_management', chapter_id=page.chapter.id)
    else:
        form = ComicPageForm(instance=page)
    
    return render(request, 'admin/edit_page.html', {
        'form': form,
        'page': page
    })

@user_passes_test(is_superuser)
@login_required
def delete_page(request, page_id):
    page = get_object_or_404(ComicPage, id=page_id)
    chapter_id = page.chapter.id
    
    if request.method == 'POST':
        page.delete()
        messages.success(request, 'Page deleted successfully!')
        return redirect('page_management', chapter_id=chapter_id)
    
    return render(request, 'admin/delete_page.html', {'page': page})

@user_passes_test(is_superuser)
@login_required
def reorder_pages(request, chapter_id):
    chapter = get_object_or_404(ComicChapter, id=chapter_id)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            page_order = data.get('page_order', [])
            
            for order_data in page_order:
                page = ComicPage.objects.get(id=order_data['id'])
                page.page_number = order_data['order']
                page.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    pages = chapter.pages.all().order_by('page_number')
    return render(request, 'admin/reorder_pages.html', {
        'chapter': chapter,
        'pages': pages
    })

# إحصائيات API
@user_passes_test(is_superuser)
@login_required
def stats_api(request):
    if request.method == 'GET':
        period = request.GET.get('period', 'week')
        
        now = timezone.now()
        today = now.date()
        
        if period == 'today':
            # آخر 24 ساعة
            start_datetime = now - timedelta(hours=24)
            return get_hourly_data(start_datetime, now)
        elif period == 'week':
            start_date = today - timedelta(days=7)
        elif period == 'month':
            start_date = today - timedelta(days=30)
        elif period == 'year':
            start_date = today - timedelta(days=365)
        else:
            start_date = today - timedelta(days=7)
        
        return get_daily_data(start_date, today)

def get_hourly_data(start_datetime, end_datetime):
    """الحصول على بيانات كل ساعة"""
    # بيانات المستخدمين كل ساعة
    user_data = []
    for hour in range(24):
        hour_start = start_datetime.replace(hour=hour, minute=0, second=0, microsecond=0)
        hour_end = hour_start + timedelta(hours=1)
        
        count = UserProfile.objects.filter(
            join_date__gte=hour_start,
            join_date__lt=hour_end
        ).count()
        
        user_data.append({
            'hour': hour,
            'count': count,
            'time': f"{hour:02d}:00"
        })
    
    # بيانات الأخبار كل ساعة
    news_data = []
    for hour in range(24):
        hour_start = start_datetime.replace(hour=hour, minute=0, second=0, microsecond=0)
        hour_end = hour_start + timedelta(hours=1)
        
        count = News.objects.filter(
            publish_date__gte=hour_start,
            publish_date__lt=hour_end
        ).count()
        
        news_data.append({
            'hour': hour,
            'count': count,
            'time': f"{hour:02d}:00"
        })
    
    # بيانات الكوميكس كل ساعة
    comic_data = []
    for hour in range(24):
        hour_start = start_datetime.replace(hour=hour, minute=0, second=0, microsecond=0)
        hour_end = hour_start + timedelta(hours=1)
        
        count = ComicChapter.objects.filter(
            created_date__gte=hour_start,
            created_date__lt=hour_end
        ).count()
        
        comic_data.append({
            'hour': hour,
            'count': count,
            'time': f"{hour:02d}:00"
        })
    
    return JsonResponse({
        'type': 'hourly',
        'users': user_data,
        'news': news_data,
        'comics': comic_data
    })

def get_daily_data(start_date, end_date):
    """الحصول على بيانات كل يوم"""
    # بيانات المستخدمين كل يوم
    user_data = []
    current_date = start_date
    while current_date <= end_date:
        next_date = current_date + timedelta(days=1)
        
        count = UserProfile.objects.filter(
            join_date__date__gte=current_date,
            join_date__date__lt=next_date
        ).count()
        
        user_data.append({
            'date': current_date.isoformat(),
            'count': count
        })
        current_date = next_date
    
    # بيانات الأخبار كل يوم
    news_data = []
    current_date = start_date
    while current_date <= end_date:
        next_date = current_date + timedelta(days=1)
        
        count = News.objects.filter(
            publish_date__date__gte=current_date,
            publish_date__date__lt=next_date
        ).count()
        
        news_data.append({
            'date': current_date.isoformat(),
            'count': count
        })
        current_date = next_date
    
    # بيانات الكوميكس كل يوم
    comic_data = []
    current_date = start_date
    while current_date <= end_date:
        next_date = current_date + timedelta(days=1)
        
        count = ComicChapter.objects.filter(
            created_date__date__gte=current_date,
            created_date__date__lt=next_date
        ).count()
        
        comic_data.append({
            'date': current_date.isoformat(),
            'count': count
        })
        current_date = next_date
    
    return JsonResponse({
        'type': 'daily',
        'users': user_data,
        'news': news_data,
        'comics': comic_data
    })

def profile(request, student_id):
    try:
        student = UserProfile.objects.get(id=student_id)
        return render(request, 'profile.html', {'student': student})
    except UserProfile.DoesNotExist:
        # عرض صفحة جميلة بدلاً من 404
        return render(request, 'profile_not_found.html', {'student_id': student_id})
@user_passes_test(is_superuser)
@login_required
def export_users_to_excel(request):
    """تصدير بيانات الأعضاء إلى Excel باستخدام CSV"""
    # إنشاء الاستجابة
    response = HttpResponse(content_type='text/csv')
    filename = f"hive_members_{timezone.now().strftime('%Y%m%d_%H%M%S')}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # إنشاء كاتب CSV
    writer = csv.writer(response)
    
    # كتابة العنوان والمعلومات
    writer.writerow(['Hive Community - Members Export'])
    writer.writerow([f'Generated on: {timezone.now().strftime("%Y-%m-%d at %H:%M:%S")}'])
    writer.writerow([f'Total members: {UserProfile.objects.count()}'])
    writer.writerow([])  # سطر فارغ
    
    # كتابة عناوين الأعمدة
    headers = [
        'Member ID', 'Username', 'Full Name', 'Email Address',
        'Age', 'University', 'College', 'Major',
        'Phone Number', 'Join Date'
    ]
    writer.writerow(headers)
    
    # جلب بيانات الأعضاء
    users = UserProfile.objects.select_related('user').all().order_by('-join_date')
    
    # كتابة بيانات كل عضو
    for user in users:
        writer.writerow([
            user.id,
            user.user.username,
            user.full_name,
            user.email,
            user.age,
            user.university,
            user.college,
            user.major,
            user.phone_number,
            user.join_date.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    # إضافة ملخص
    writer.writerow([])
    writer.writerow(['Summary:'])
    writer.writerow([f'Total members exported: {len(users)}'])
    writer.writerow([f'Newest member: {users[0].full_name if users else "N/A"}'])
    writer.writerow([f'Export completed: {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}'])
    
    return response

@user_passes_test(is_superuser)
@login_required
def entrepreneurs_management(request):
    entrepreneurs = Entrepreneur.objects.all().order_by('-created_date')
    return render(request, 'admin/entrepreneurs_management.html', {'entrepreneurs': entrepreneurs})

@user_passes_test(is_superuser)
@login_required
def add_entrepreneur(request):
    if request.method == 'POST':
        form = EntrepreneurForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entrepreneur added successfully!')
            return redirect('entrepreneurs_management')
    else:
        form = EntrepreneurForm()
    
    return render(request, 'admin/add_entrepreneur.html', {'form': form})

@user_passes_test(is_superuser)
@login_required
def edit_entrepreneur(request, entrepreneur_id):
    entrepreneur = get_object_or_404(Entrepreneur, id=entrepreneur_id)
    
    if request.method == 'POST':
        form = EntrepreneurForm(request.POST, request.FILES, instance=entrepreneur)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entrepreneur updated successfully!')
            return redirect('entrepreneurs_management')
    else:
        form = EntrepreneurForm(instance=entrepreneur)
    
    return render(request, 'admin/edit_entrepreneur.html', {'form': form, 'entrepreneur': entrepreneur})

@user_passes_test(is_superuser)
@login_required
def delete_entrepreneur(request, entrepreneur_id):
    entrepreneur = get_object_or_404(Entrepreneur, id=entrepreneur_id)
    
    if request.method == 'POST':
        entrepreneur.delete()
        messages.success(request, 'Entrepreneur deleted successfully!')
        return redirect('entrepreneurs_management')
    
    return render(request, 'admin/delete_entrepreneur.html', {'entrepreneur': entrepreneur})

# إدارة الـ Blogs
@user_passes_test(is_superuser)
@login_required
def blogs_management(request):
    blogs = Blog.objects.all().select_related('entrepreneur').order_by('-publish_date')
    return render(request, 'admin/blogs_management.html', {'blogs': blogs})

@user_passes_test(is_superuser)
@login_required
def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog added successfully!')
            return redirect('blogs_management')
    else:
        form = BlogForm(initial={'publish_date': timezone.now()})
    
    return render(request, 'admin/add_blog.html', {'form': form})

@user_passes_test(is_superuser)
@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog updated successfully!')
            return redirect('blogs_management')
    else:
        form = BlogForm(instance=blog)
    
    return render(request, 'admin/edit_blog.html', {'form': form, 'blog': blog})

@user_passes_test(is_superuser)
@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    
    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'Blog deleted successfully!')
        return redirect('blogs_management')
    
    return render(request, 'admin/delete_blog.html', {'blog': blog})

# الصفحات العامة (يمكن للجميع الوصول)

def blog_list(request):
    blogs = Blog.objects.filter(is_published=True).select_related('entrepreneur').order_by('-publish_date')
    
    context = {
        'blogs': blogs,
    }
    
    return render(request, 'blogs/blogs_list.html', context)

@login_required
def entrepreneur_profile(request, entrepreneur_id):
    entrepreneur = get_object_or_404(Entrepreneur, id=entrepreneur_id)
    blogs = Blog.objects.filter(entrepreneur=entrepreneur, is_published=True).order_by('-publish_date')
    
    # حساب إحصائيات إضافية
    blogs_count = blogs.count()
    
    # حساب إجمالي المشاهدات بطريقة آمنة
    total_views = 0
    try:
        # تحقق مما إذا كان الحقل موجوداً قبل استخدامه
        if 'views' in [f.name for f in Blog._meta.get_fields()]:
            total_views = blogs.aggregate(total_views=Sum('views'))['total_views'] or 0
    except:
        total_views = 0
    
    context = {
        'entrepreneur': entrepreneur,
        'blogs': blogs,
        'blogs_count': blogs_count,
        'total_views': total_views,
    }
    
    return render(request, 'entrepreneur_profile.html', context)

@login_required
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, is_published=True)
    
    # زيادة عدد المشاهدات إذا كان الحقل موجوداً
    try:
        if hasattr(blog, 'views') and blog.views is not None:
            blog.views += 1
            blog.save()
    except:
        pass  # تجاهل الخطأ إذا لم يكن الحقل موجوداً
    
    # المدونات ذات الصلة (نفس رائد الأعمال)
    related_blogs = Blog.objects.filter(
        entrepreneur=blog.entrepreneur,
        is_published=True
    ).exclude(id=blog.id).order_by('-publish_date')[:3]
    
    # مدونات مقترحة (من رواد أعمال آخرين)
    suggested_blogs = Blog.objects.filter(
        is_published=True
    ).exclude(
        entrepreneur=blog.entrepreneur
    ).exclude(
        id=blog.id
    ).order_by('-publish_date')[:3]
    
    context = {
        'blog': blog,
        'related_blogs': related_blogs,
        'suggested_blogs': suggested_blogs,
    }
    
    return render(request, 'blogs/blog_detail.html', context)