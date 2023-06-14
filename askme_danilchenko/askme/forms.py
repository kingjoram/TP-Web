from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)


class SettingsForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = {'username', 'last_name', 'first_name', 'avatar'}

    def save(self, commit=True):
        user = super().save(commit)

        profile = user.profile
        if profile.avatar and self.cleaned_data['avatar']:
            profile.avatar = self.cleaned_data['avatar']
            profile.save()

        return user