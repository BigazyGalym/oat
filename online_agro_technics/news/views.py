from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import News
from .forms import NewsForm
from accounts.models import Profile

def is_admin(user):
    return user.profile.is_admin

def news_list(request):
    news = News.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'news/news_list.html', {'news': news})

def news_detail(request, news_id):
    news = get_object_or_404(News, id=news_id, is_active=True)
    return render(request, 'news/news_detail.html', {'news': news})

@login_required
@user_passes_test(is_admin, login_url='/accounts/login/')
def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, 'Жаңалық сәтті құрылды.')
            return redirect('news:news_list')
    else:
        form = NewsForm()
    return render(request, 'news/create_news.html', {'form': form})