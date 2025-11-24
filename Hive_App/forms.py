from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile, NewsletterSubscription, CustomUser,News, ComicSeries, ComicChapter, ComicPage,Entrepreneur, Blog

# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # تأكد من استيراد النموذج الصحيح

class UserRegistrationForm(UserCreationForm):
    # إضافة الحقول الإضافية
    full_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    age = forms.IntegerField(
        required=True,
        min_value=16,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    university = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    college = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    major = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 
                 'full_name', 'age', 'university', 'college', 
                 'major', 'phone_number']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # استخدم CustomUser بدلاً من User
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # إذا كنت تريد حفظ الاسم الكامل في الحقول المضمنة
        user.first_name = self.cleaned_data['full_name']
        if commit:
            user.save()
        return user

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email for updates'
            })
        }

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'image', 'publish_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter news title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Enter news content'
            }),
            'publish_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

class ComicSeriesForm(forms.ModelForm):
    class Meta:
        model = ComicSeries
        fields = ['title', 'description', 'cover_image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter series title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter series description'
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

class ComicChapterForm(forms.ModelForm):
    class Meta:
        model = ComicChapter
        fields = ['series', 'title', 'chapter_number', 'description']
        widgets = {
            'series': forms.Select(attrs={
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter chapter title'
            }),
            'chapter_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter chapter description (optional)'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['series'].queryset = ComicSeries.objects.all()

class ComicPageForm(forms.ModelForm):
    class Meta:
        model = ComicPage
        fields = ['chapter', 'image', 'page_number']
        widgets = {
            'chapter': forms.Select(attrs={
                'class': 'form-control'
            }),
            'page_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['chapter'].queryset = ComicChapter.objects.all()

class MultipleImageInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleImageField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleImageInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class BulkComicPagesForm(forms.Form):
    chapter = forms.ModelChoiceField(
        queryset=ComicChapter.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    images = MultipleImageField(
        label='Select multiple pages',
        help_text='Hold Ctrl/Cmd to select multiple images'
    )

    def clean_images(self):
        images = self.cleaned_data.get('images')
        if not images:
            raise ValidationError('Please select at least one image')
        return images
    
# forms.py


class EntrepreneurForm(forms.ModelForm):
    class Meta:
        model = Entrepreneur
        fields = ['name', 'company', 'position', 'linkedin_url', 'profile_image', 'bio', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/username'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['entrepreneur', 'title', 'featured_image', 'content', 'publish_date', 'is_published']
        widgets = {
            'entrepreneur': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'publish_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }