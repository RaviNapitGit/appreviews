from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.home, name='home'),
    path('apps/<int:pk>/', views.app_detail, name='app_detail'),
    path('apps/<int:pk>/review/new/', views.review_create, name='review_create'),
    path('supervisor/queue/', views.supervisor_queue, name='supervisor_queue'),
    path('supervisor/reviews/<int:pk>/approve/', views.approve_review, name='approve_review'),
    path('supervisor/reviews/<int:pk>/reject/', views.reject_review, name='reject_review'),
    path('search/', views.search_results, name='search_results'),
    path('api/suggest/', views.api_suggest, name='api_suggest'),
]
