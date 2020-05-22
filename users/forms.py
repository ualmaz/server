from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Post, User, Country, Profile, Report, Calendar

class UserCreationModelForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'country', 'city', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'country', 'city', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('name', 'area', 'country', 'city', 'address', 'email', 'social', 'phone', 'website', 'author')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].queryset = Country.objects.none()

        if 'area' in self.data:
            try:
                area_id = int(self.data.get('area'))
                self.fields['country'].queryset = Country.objects.filter(area_id=area_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['country'].queryset = self.instance.area.country_set.order_by('name')


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('author', 'area', 'country', 'new_ministers', 'dis_course', 'licenced_ministers', 'upgrade_licence', 'preaching_place', 'new_churches', 'water_baptism', 'holy_ghost', 'constituents', 'total_holy_ghost', 'total_baptized')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].queryset = Country.objects.none()

        if 'area' in self.data:
            try:
                area_id = int(self.data.get('area'))
                self.fields['country'].queryset = Country.objects.filter(area_id=area_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['country'].queryset = self.instance.area.country_set.order_by('name')



class DateInput(forms.DateInput):
    input_type = 'date'


class CalendarForm(forms.ModelForm):
    title = forms.CharField()

    class Meta:
            model = Calendar
            fields = ['date_from', 'date_to', 'title', 'link']
            widgets = {
                'date_from' : DateInput(),
                'date_to' : DateInput()
            }
