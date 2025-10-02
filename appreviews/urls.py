from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    # auth: login, logout, password reset (uses templates at registration/)
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('reviews.urls')),
    path('', RedirectView.as_view(pattern_name='reviews:home', permanent=False)),
]
