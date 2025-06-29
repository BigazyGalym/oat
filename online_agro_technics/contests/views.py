from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import Contest, ContestEntry
from .forms import ContestForm, ContestEntryForm
from accounts.models import Profile

def is_admin(user):
    return user.profile.is_admin

def contest_list(request):
    contests = Contest.objects.filter(is_active=True, end_date__gt=timezone.now()).order_by('-start_date')
    return render(request, 'contests/contest_list.html', {'contests': contests})

def contest_detail(request, contest_id):
    contest = get_object_or_404(Contest, id=contest_id, is_active=True)
    entries = contest.entries.all().order_by('-created_at')
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Конкурсқа қатысу үшін кіріңіз.')
            return redirect('accounts:login')
        form = ContestEntryForm(request.POST)
        if form.is_valid():
            if contest.end_date < timezone.now():
                messages.error(request, 'Конкурс аяқталды.')
                return redirect('contests:contest_detail', contest_id=contest.id)
            entry = form.save(commit=False)
            entry.contest = contest
            entry.user = request.user
            entry.save()
            messages.success(request, 'Жұмысыңыз қабылданды.')
            return redirect('contests:contest_detail', contest_id=contest.id)
    else:
        form = ContestEntryForm()
    return render(request, 'contests/contest_detail.html', {'contest': contest, 'entries': entries, 'form': form})

@login_required
@user_passes_test(is_admin, login_url='/accounts/login/')
def create_contest(request):
    if request.method == 'POST':
        form = ContestForm(request.POST)
        if form.is_valid():
            contest = form.save()
            messages.success(request, 'Конкурс сәтті құрылды.')
            return redirect('contests:contest_list')
    else:
        form = ContestForm()
    return render(request, 'contests/create_contest.html', {'form': form})