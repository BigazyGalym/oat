from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ForumPost, ForumComment
from .forms import ForumPostForm, ForumCommentForm

def forum_list(request):
    posts = ForumPost.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'forum/forum_list.html', {'posts': posts})

def forum_post_detail(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id, is_active=True)
    comments = post.comments.all().order_by('created_at')
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Пікір қосу үшін кіріңіз.')
            return redirect('accounts:login')
        form = ForumCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Пікір қосылды.')
            return redirect('forum:post_detail', post_id=post.id)
    else:
        form = ForumCommentForm()
    return render(request, 'forum/post_detail.html', {'post': post, 'comments': comments, 'form': form})

@login_required
def create_forum_post(request):
    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Жазба сәтті құрылды.')
            return redirect('forum:forum_list')
    else:
        form = ForumPostForm()
    return render(request, 'forum/create_post.html', {'form': form})