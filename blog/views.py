from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Article, NewsletterSubscription, Category, User

posts = [
    {
        'author': 'Ameh Sunday S.',
        'tittle': 'Blog Post',
        'content': 'This is my first blog post',
        'date_posted': '25th June, 2023',
    },
    {
        'author': 'Daniel John',
        'tittle': 'Blog Post 2',
        'content': 'This is my second blog post',
        'date_posted': '30th June, 2023',
    }
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'tittle': "About Page"})

# Create your views here.






def signup(request):
    if request.method == 'POST':
        # Process sign-up form data
        email = request.POST['email']
        password = request.POST['password']
        # Create a new user
        user = User.objects.create_user(username=email, email=email, password=password)
        user.is_active = False  # Email verification required
        user.save()
        # Send verification email
        # ... (implement email sending logic)
        messages.success(request, 'Please check your email to verify your account.')
        return redirect('signup')
    return render(request, 'signup.html')


def verify_email(request, token):
    # Verify email and activate user account
    # ... (implement email verification logic)
    user = User.objects.get(token=token)
    user.is_verified = True
    user.save()
    messages.success(request, 'Your email has been verified. Please log in.')
    return redirect('login')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_verified:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials or email not verified.')
    return render(request, 'login.html')


@login_required
def dashboard(request):
    user = request.user
    articles = Article.objects.filter(author__user=user)
    return render(request, 'dashboard.html', {'articles': articles})


@login_required
def create_article(request):
    if request.method == 'POST':
        # Process article creation form data
        title = request.POST['title']
        content = request.POST['content']
        category_id = request.POST['category']
        author = request.user.author
        category = Category.objects.get(id=category_id)
        article = Article(title=title, content=content, category=category, author=author)
        article.save()
        return redirect('dashboard')
    categories = Category.objects.all()
    return render(request, 'create_article.html', {'categories': categories})


@login_required
def update_article(request, article_id):
    article = Article.objects.get(id=article_id)
    if request.method == 'POST':
        # Process article update form data
        article.title = request.POST['title']
        article.content = request.POST['content']
        article.category = Category.objects.get(id=request.POST['category'])
        article



