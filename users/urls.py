from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    UserRegistrationView,
    PostCreateView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    ReportCreateView,
    CalendarView,
    CalendarDetailView,
    CalendarCreateView,
    CalendarUpdateView,
    CalendarDeleteView
)
from . import views


app_name = 'users'

urlpatterns = [
    path('accounts/cabinet/new/', views.PostCreateView.as_view(), name='post-create'),
    path('accounts/cabinet/blog/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('', views.home, name='home'),
    path('report_main/', views.report_main_page, name='report_main_page'),
    path('accounts/register/', UserRegistrationView.as_view(), name='register'),
    path('accounts/report/', ReportCreateView.as_view(template_name='report/report.html'), name='report'),
    path('accounts/report_list/<int:pk>/', views.report_list, name='report-list'),
    path('accounts/report_list_sorted_by_month/<int:month_number>', views.report_list_sorted_by_month, name='report-list-sorted-by-month'),
    path('accounts/report_list_by_area/', views.report_list_by_area, name='report_list_by_area'),
    path('accounts/report_list_by_month/', views.report_list_by_month, name='report_list_by_month'),
    path('accounts/cabinet/', views.profile, name='cabinet'),
    path('accounts/cabinet/blog/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('accounts/cabinet/blog/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('accounts/cabinet/blog/', views.blog, name='blog'),
    path('accounts/cabinet/countries/', views.countries, name='countries'),
    path('accounts/cabinet/cities/<int:pk>/', views.cities, name='cities'),
    path('accounts/cabinet/address/<int:pk>/', views.address, name='address'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('accounts/cabinet/post_page/', views.post_page, name='post-page'),
    path('accounts/cabinet/youtube/', views.youtube, name='youtube'),
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('calendar/<int:pk>/update', CalendarUpdateView.as_view(), name='calendar_update_form'),
    path('calendar/<int:pk>/delete', CalendarDeleteView.as_view(), name='calendar_delete'),
    path('calendar/<int:pk>/', CalendarDetailView.as_view(), name='calendar-details'),
    path('calendar/new/', CalendarCreateView.as_view(), name='calendar-form')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

