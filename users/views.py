from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.core import mail
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import User, Post, Country, Report, Area, Calendar
from .forms import PostForm, UserCreationModelForm, UserUpdateForm, ProfileUpdateForm, ReportForm, CalendarForm
from django.http import HttpResponseRedirect
from django.conf import settings

class UserRegistrationView(SuccessMessageMixin, CreateView):
    form_class = UserCreationModelForm
    model = User
    success_url = reverse_lazy('login')
    success_message = "Account for %(first_name)s was created successfully. You will get email notification when admin will activate your account!"
    template_name = 'users/registration.html'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data)

class PostDetailView(DetailView):
    model = Post


class PostListView(ListView):
    model = Post
    context_object_name = 'people'


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('users:cabinet')


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('users:cabinet')

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'report/report.html'



@login_required
def cabinet(request):
    profile = Profile.objects.all()

    context = {
        'profile': profile,

    }
    return render(request, 'users/user_detail.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        uform = UserUpdateForm(request.POST, instance=request.user)
        pform = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        posts = Post.objects.filter(author=request.user)

        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('users:cabinet')
    else:
        uform = UserUpdateForm(instance=request.user)
        pform = ProfileUpdateForm()
        posts = Post.objects.filter(author=request.user)

    context = {
        'uform': uform,
        'pform': pform,
        'posts': posts
    }

    return render(request, 'users/user_detail.html', context)

@login_required
def blog(request):

    context = {
        'posts': Post.objects.filter(author=request.user)
    }
    return render(request, 'users/post_detail.html', context)


def countries(request):
    country = Post.objects.all().order_by('country').distinct('country')
    context = {
        'posts': country
    }
    return render(request, 'users/countries.html', context)



def cities(request, pk):
    country = Post.objects.get(id=pk).country
    cities = Post.objects.filter(country=country).distinct('city')
    access_challenge_country = Country.objects.filter(access_challenge = True)

    context = {
        'cities':cities,
        'country':country,
        'access_challenge_country': access_challenge_country

    }

    return render(request, 'users/cities.html', context)

def address(request, pk):
    user = User.objects.all()
    city = Post.objects.get(id=pk).city
    address = Post.objects.filter(city=city)

    context = {
        'user': user,
        'address': address,
        'city': city,
    }

    return render(request, 'users/address.html', context)

def home(request):
        country = Post.objects.all().order_by('country__name').distinct('country__name')
        west_eu = Post.objects.filter(area__name__icontains='Western').distinct('country')
        east_eu = Post.objects.filter(area__name__icontains='Eastern').distinct('country')
        north_eu = Post.objects.filter(area__name__icontains='NORTHERN').distinct('country')
        middle_e = Post.objects.filter(area__name__icontains='Middle').distinct('country')
        africa = Post.objects.filter(area__name__icontains='Africa').distinct('country')
        baltic = Post.objects.filter(area__name__icontains='Baltic').distinct('country')


        context = {
            'country': country,
            'west_eu': west_eu,
            'east_eu': east_eu,
            'north_eu': north_eu,
            'middle_e': middle_e,
            'africa': africa,
            'baltic': baltic,
        }

        return render(request, 'registration/home.html', context)


def load_cities(request):
    area_id = request.GET.get('area')
    countries = Country.objects.filter(area_id=area_id).order_by('name')
    return render(request, 'users/city_dropdown_list_options.html', {'countries': countries})


# #Report views
class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'report/report.html'


@login_required
def report_main_page(request):
    return render(request, 'report/report_main_page.html')


@login_required
def report_list(request, pk):
    area_id = Report.objects.get(pk=pk).area
    report = Report.objects.filter(area_id=area_id)

    context = {
        'report': report,
        'area_id': area_id
    }
    return render(request, 'report/report_list.html', context)


@login_required
def report_list_sorted_by_month(request, month_number):
    filtered_reports = Report.objects.filter(month__month=month_number)
    reports_dates = Report.objects.dates('month', 'month')

    context = {
        'reports': filtered_reports,
        'title': reports_dates
    }
    return render(request, 'report/report_list_sorted_by_month.html', context)


@login_required
def report_list_by_area(request):
    report = Report.objects.all().distinct('area')
    context = {
        'report': report
    }
    return render(request, 'report/report_list_by_area.html', context)


@login_required
def report_list_by_month(request):
    reports_dates = Report.objects.dates('month', 'month')
    context = {
        'reports_dates': reports_dates
    }
    return render(request, 'report/report_list_by_month.html', context)


def post_page(request):
    posts = Post.objects.filter(author=request.user)

    context = {
        'posts': posts
    }

    return render(request, 'users/post_page.html', context)

def youtube(request):
    return render(request, 'users/youtube.html')


class CalendarView(ListView):
    model = Calendar
    form_class = CalendarForm
    template_name = 'calendar/calendar.html'
    context_object_name = 'calendar'
    ordering = ['-id']


class CalendarDetailView(DetailView):
    model = Calendar
    ordering = ['-id']

class CalendarCreateView(CreateView):
    model = Calendar
    form_class = CalendarForm
    template_name = 'calendar/calendar_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CalendarUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Calendar
    # form_class = CalendarUpdateForm
    template_name = 'calendar/calendar_update_form.html'
    fields = ['title', 'link', 'date_posted', 'date_from']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        calendar = self.get_object()
        if self.request.user == calendar.author:
            return True
        return False

class CalendarDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Calendar
    template_name = 'calendar/calendar_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        calendar = self.get_object()
        if self.request.user == calendar.author:
            return True
        return False