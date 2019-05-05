from django.urls import include, path
from .views import UserRegistrationView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView, ReportCreateView
from . import views


app_name = 'users'

urlpatterns = [
    path('accounts/cabinet/new/', views.PostCreateView.as_view(), name='post-create'),
    path('accounts/cabinet/blog/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('', views.home, name='home'),
    path('accounts/register/', UserRegistrationView.as_view(), name='register'),
    path('accounts/report/', ReportCreateView.as_view(), name='report'),
    path('accounts/report_view/<int:pk>/', views.report_view, name='report_view'),
    path('accounts/report_list/', views.report_list, name='report_list'),
    path('accounts/report_countries/<int:pk>', views.report_countries, name='report_countries'),
    path('accounts/report_list_by_month/', views.report_list_by_month, name='report_list_by_month'),
    path('accounts/report_month/<int:pk>/', views.report_month, name='report_month'),
    path('accounts/cabinet/', views.profile, name='cabinet'),
    path('accounts/cabinet/blog/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('accounts/cabinet/blog/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('accounts/cabinet/blog/', views.blog, name='blog'),
    path('accounts/cabinet/countries/', views.countries, name='countries'),
    path('accounts/cabinet/cities/<int:pk>/', views.cities, name='cities'),
    path('accounts/cabinet/address/<int:pk>/', views.address, name='address'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('accounts/cabinet/post_page/', views.post_page, name='post-page'),




]
