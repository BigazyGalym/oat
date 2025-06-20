from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from accounts.views import custom_logout
import logging

logger = logging.getLogger('django')

def home(request):
    logger.debug("Accessing home view")
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    return TemplateView.as_view(template_name='home.html')(request)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
    path('', home, name='home'),
    path('forum/', include('forum.urls')),
    path('bookings/', include('bookings.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)