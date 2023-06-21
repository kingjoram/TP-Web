from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Profile, Questions, Answers


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


class SignUpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-group mb-3"}), label="login", max_length=50)
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-group mb-3"}), label="Email", max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-group mb-3"}), label='Password',
                               max_length=50)
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-group mb-3"}),
                                      label='Repeat password', max_length=50)

    def clean_password(self):
        data = self.data['password']
        if len(data) < 6:
            raise ValidationError("Password should be more then 5 symbols.")
        return data

    def clean_username(self):
        username_match = User.objects.filter(username=self.cleaned_data["username"])
        if username_match.exists():
            raise ValidationError(f"User with username {self.cleaned_data['username']} already exists")

        data = self.data['username']
        if len(data) < 6:
            raise ValidationError("Username should be more then 5 symbols.")
        return data

    def clean_password_repeat(self):
        passwd_one = self.data['password']
        passwd_two = self.data['password_repeat']
        if passwd_one != passwd_two:
            raise ValidationError("Passwords do not match")


class AskForm(forms.ModelForm):
    tags = forms.CharField()

    class Meta:
        model = Questions
        fields = ['title', 'text', 'tags']

        widgets = {
            'title': forms.TextInput(),
            'text': forms.Textarea(attrs={'placeholder': "Detailed description"}),
            'tags': forms.TextInput(attrs={'placeholder': "Tags"})
        }

        labels = {
            'title': "Question header",
            'text': "Add a description to your question and write it in details.",
            'tags': "Add some tags!",
        }

    def clean_tags(self):
        data = self.data['tags']
        if len(data) > 30:
            raise ValidationError("Tags field length must be less than 30 characters")
        return data

    def clean_title(self):
        data = self.data['title']
        if len(data) > 100:
            raise ValidationError("Title length must be less than 100 characters")
        return data

    def clean_text(self):
        data = self.data['text']
        if len(data) > 5000:
            raise ValidationError("Question body must be less than 5000 characters")
        return data


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answers
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control mb-3', 'placeholder': 'Answer...', 'rows': '3'})
        }
        labels = {
            'text': 'Answer a question!'
        }

    def clean_text(self):
        data = self.data['text']
        if len(data) > 3000:
            raise ValidationError("Answer body must be less than 3000 characters")
        return data
