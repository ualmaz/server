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
from .models import User, Post, Country, Report, Area
from .forms import PostForm, UserCreationModelForm, UserUpdateForm, ProfileUpdateForm, ReportForm

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
    template_name = 'users/report.html'



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


@login_required
def report_view(request, pk):
    report = Report.objects.filter(pk=pk)
    patron = User.objects.filter(username='ualmaz')
    author = Report.objects.get(pk=pk).author

    context = {
        'report': report,
        'patron': patron,
        'author': author,

    }

    return render(request, 'users/report_view.html', context)

@login_required
def report_list(request):
    areas = Report.objects.all().distinct('area')
    # ordering = ['-date_posted']

    context = {
        'areas':areas
    }
    return render(request, 'users/report_list.html', context)


@login_required
def report_list_by_month(request):
    month = Report.objects.distinct('month')
    ordering = ['date_posted']

    context = {
        'month': month
    }

    return render(request, 'users/report_list_by_month.html', context)


def report_countries(request, pk):
    countries = Report.objects.filter(id=pk)

    context = {
        'countries':countries
    }
    return render(request, 'users/report_countries.html', context)

def report_month(request, pk):
    month = Report.objects.filter('month')


    context = {
        'month': month
    }
    return render(request, 'users/report_month.html', context)

def post_page(request):
    posts = Post.objects.filter(author=request.user)

    context = {
        'posts': posts
    }

    return render(request, 'users/post_page.html', context)
