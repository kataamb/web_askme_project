from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import CharField

from django.contrib.auth.hashers import check_password

from app.models import *


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        super().clean()

        user = Profile.objects.get_by_username( self.cleaned_data['username'] )

        if not user:
            raise ValidationError("No such user")


        # check password in log in
        password = self.cleaned_data['password']
        if not check_password(password, user.user.password):
            raise ValidationError("Incorrect password")




class RegisterForm(forms.ModelForm):
    login = CharField()
    password = forms.CharField(widget=forms.PasswordInput) # to change widget
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    avatar = forms.ImageField(allow_empty_file=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password' ]

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data['password'])
        user.save()

        profile = Profile(avatar=self.cleaned_data['avatar'],
                          login=self.cleaned_data['login'],
                          user=user)
        profile.save()

        return [user, profile]


    def clean(self):
        super().clean()

        pswd = self.cleaned_data['password']
        check_pswd = self.cleaned_data['confirm_password']

        if pswd != check_pswd:
            raise ValidationError("Passwords do not match")


class EditForm(forms.Form):
    username = CharField()
    login = CharField()
    email = CharField()
    first_name = CharField()
    avatar = forms.ImageField(allow_empty_file=True)


    def __init__(self, profile, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile = profile
        print(profile)

    def save(self, commit=True):
        print(self.cleaned_data)
        self.profile.user.username = self.cleaned_data['username']
        self.profile.user.email = self.cleaned_data['email']
        self.profile.user.first_name = self.cleaned_data['first_name']

        self.profile.user.save()
        print(self.profile.user.username, self.profile.user.first_name)


        self.profile.avatar, self.profile.login = self.cleaned_data['avatar'], self.cleaned_data['login']
        self.profile.save()

        return self.profile



    def clean(self):
        super().clean()






class QuestionForm(forms.ModelForm):
    text_body = forms.CharField(widget=forms.TextInput, max_length=255)  # to change widget
    tags = forms.CharField(max_length=255)
    class Meta:
        model = Question
        fields = ['title', 'text_body']

    def __init__(self, profile, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile = profile


    def clean(self):

        super().clean()

        tags_list = self.cleaned_data["tags"]
        tags_list = [i.strip() for i in tags_list.split(",")]

        if len(tags_list) > 3:
            raise ValidationError("Too many tags!")

        tag_objs = Tag.objects

        lst = []

        for tag in tags_list:
            tg = tag_objs.get_tag_by_name(tag)
            if not tg:
                #raise ValidationError(f"Tag {tag} doesn't exsist!")
                # if no tag, create  and add to db
                new_tag = Tag(name=tag)
                new_tag.save()
                # get from db
                tg = tag_objs.get_tag_by_name(tag)
            lst.append(tg[0])

        self.cleaned_data["tags"] = lst

        print(lst)


    def save(self, commit=True):
        question = super().save(commit=False)
        #question = Question(title = self.)

        question.user = self.profile
        question.likes_count = 0

        question.save()

        tags = self.cleaned_data["tags"]
        question.tags.add(*tags)

        return question





class AnswerForm(forms.ModelForm):
    text_body = forms.CharField(widget=forms.TextInput, max_length=255)  # to change widget
    class Meta:
        model = Answer
        fields = ['text_body']

    def __init__(self, profile, question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile = profile
        self.question = question


    def clean(self):
        super().clean()


    def save(self, commit=True):
        answer = super().save(commit=False)

        answer.user = self.profile
        answer.question = self.question
        answer.likes_count = 0

        answer.save()

        return answer
