from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    
    
    def create_user(self, email, password=None, **extra_fields):
        """إنشاء وتخزين مستخدم عادي بالبريد الإلكتروني"""
        if not email:
            raise ValueError(_('You should use an email'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """إنشاء وتخزين مستخدم superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    """نموذج المستخدم المخصص باستخدام البريد الإلكتروني"""
    username = None
    email = models.EmailField(_('email address'), unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    university = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class News(models.Model):  # تأكد من أن الاسم News وليس news
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news/')
    publish_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    def is_recent(self):
        return (timezone.now() - self.publish_date).days <= 30

class ComicSeries(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='comics/covers/')
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class ComicChapter(models.Model):
    series = models.ForeignKey(ComicSeries, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    chapter_number = models.IntegerField()
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['chapter_number']
    
    def __str__(self):
        return f"{self.series.title} - Chapter {self.chapter_number}"

class ComicPage(models.Model):
    chapter = models.ForeignKey(ComicChapter, on_delete=models.CASCADE, related_name='pages')
    image = models.ImageField(upload_to='comics/pages/')
    page_number = models.IntegerField()
    
    class Meta:
        ordering = ['page_number']
    
    def __str__(self):
        return f"{self.chapter} - Page {self.page_number}"

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email
    

class Entrepreneur(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    linkedin_url = models.URLField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='entrepreneurs/profile/')
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.position} at {self.company}"
    
    class Meta:
        ordering = ['-created_date']
        verbose_name = "Entrepreneur"
        verbose_name_plural = "Entrepreneurs"

class Blog(models.Model):
    entrepreneur = models.ForeignKey(Entrepreneur, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=200)
    featured_image = models.ImageField(upload_to='blogs/featured/')
    content = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-publish_date']
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
