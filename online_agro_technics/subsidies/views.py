from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SubsidyInquiry
from .forms import SubsidyInquiryForm

def subsidies_info(request):
    return render(request, 'subsidies/subsidies_info.html')

@login_required
def submit_inquiry(request):
    if request.method == 'POST':
        form = SubsidyInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.user = request.user
            inquiry.save()
            messages.success(request, 'Сұрауыңыз қабылданды.')
            return redirect('subsidies:subsidies_info')
    else:
        form = SubsidyInquiryForm()
    return render(request, 'subsidies/submit_inquiry.html', {'form': form})