from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.utils.html import strip_tags
from .models import Post


User = get_user_model()

class User_Login_Form(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username*'}), 
        label='')
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password*'}), 
        label='')

    def clean(self, *args, **kwargs):

        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:

            user = authenticate(username=username, password=password)
            
            if not user:
                raise forms.ValidationError("This user does not exist...")

            if not user.check_password(password):
                raise forms.ValidationError("Incorect Password")

            if not user.check_password(password):
                raise forms.ValidationError("This user is no longer active")

            return super(User_Login_Form, self).clean(*args, **kwargs)




class Post_Form(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ["message"]
        widgets = {
            'message': forms.TextInput(
                attrs={'id': 'user_message', 'required': True, 'placeholder': 'Say something...', "autocomplete": "off"}
            ),
        }

    def clean(self, *args, **kwargs):
        cleaned_data = super(Post_Form, self).clean()
        message = strip_tags(self.cleaned_data.get("message"))

        print message
        return message





