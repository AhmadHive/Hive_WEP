from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('comics/', views.comics, name='comics'),
    path('comics/<int:series_id>/<int:chapter_number>/', views.comic_chapter, name='comic_chapter'),
    path('news/', views.news, name='news'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('register/', views.register, name='register'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('profile/<int:student_id>/', views.profile, name='profile'),
    path('login/', views.custom_login, name='login'),


    
    # إدارة الأخبار
    path('admin-panel/news/', views.news_management, name='news_management'),
    path('admin-panel/news/add/', views.add_news, name='add_news'),
    path('admin-panel/news/edit/<int:news_id>/', views.edit_news, name='edit_news'),
    path('admin-panel/news/delete/<int:news_id>/', views.delete_news, name='delete_news'),
    path('admin/export-users/', views.export_users_to_excel, name='export_users'),
    
    # إدارة الكوميكس
    path('admin-panel/comics/', views.comics_management, name='comics_management'),
    path('admin-panel/comics/add-series/', views.add_comic_series, name='add_comic_series'),
    path('admin-panel/comics/edit-series/<int:series_id>/', views.edit_comic_series, name='edit_comic_series'),
    path('admin-panel/comics/delete-series/<int:series_id>/', views.delete_comic_series, name='delete_comic_series'),
    path('admin-panel/comics/series/<int:series_id>/chapters/', views.chapter_management, name='chapter_management'),
    path('admin-panel/comics/series/<int:series_id>/chapters/add/', views.add_chapter, name='add_chapter'),
    path('admin-panel/comics/chapters/edit/<int:chapter_id>/', views.edit_chapter, name='edit_chapter'),
    path('admin-panel/comics/chapters/delete/<int:chapter_id>/', views.delete_chapter, name='delete_chapter'),
    path('admin-panel/comics/chapters/<int:chapter_id>/pages/', views.page_management, name='page_management'),
    path('admin-panel/comics/chapters/<int:chapter_id>/pages/add/', views.add_page, name='add_page'),
    path('admin-panel/comics/chapters/<int:chapter_id>/pages/bulk-add/', views.bulk_add_pages, name='bulk_add_pages'),
    path('admin-panel/comics/pages/edit/<int:page_id>/', views.edit_page, name='edit_page'),
    path('admin-panel/comics/pages/delete/<int:page_id>/', views.delete_page, name='delete_page'),
    path('admin-panel/comics/chapters/<int:chapter_id>/reorder-pages/', views.reorder_pages, name='reorder_pages'),
    
    # API للإحصائيات
    path('admin-panel/stats/api/', views.stats_api, name='stats_api'),
    path('admin/entrepreneurs/', views.entrepreneurs_management, name='entrepreneurs_management'),
    path('admin/entrepreneurs/add/', views.add_entrepreneur, name='add_entrepreneur'),
    path('admin/entrepreneurs/edit/<int:entrepreneur_id>/', views.edit_entrepreneur, name='edit_entrepreneur'),
    path('admin/entrepreneurs/delete/<int:entrepreneur_id>/', views.delete_entrepreneur, name='delete_entrepreneur'),
    
    # إدارة الـ Blogs (للسوبر يوزر فقط)
    path('admin/blogs/', views.blogs_management, name='blogs_management'),
    path('admin/blogs/add/', views.add_blog, name='add_blog'),
    path('admin/blogs/edit/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    path('admin/blogs/delete/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    
    # الصفحات العامة
    path('blogs/', views.blog_list, name='blogs_list'),  # غيرت من blogs_list إلى blog_list
    path('blogs/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('entrepreneur/<int:entrepreneur_id>/', views.entrepreneur_profile, name='entrepreneur_profile'),
]