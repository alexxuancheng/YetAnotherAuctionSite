from django import forms
from django.contrib.auth import get_user_model
from .models import Account
User = get_user_model()
  
class RegisterForm(forms.ModelForm):
    LauguageChoices=(
        ('en', 'English'),
        ('zh-hans', 'Chinese'),
        ('fi','Finnish')
    )
     
    language    = forms.ChoiceField(choices=LauguageChoices)
    password1   = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2   = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError("Cannot use this email. It's already registered")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        
        if commit:
            user.save()
        return user

class EmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError("Cannot use this email. It's already registered")
        return email

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(EmailForm, self).save(commit=False)

        if commit:
            user.save()
            # user.profile.send_activation_email()
        # create a new user hash for activating email.
        return user

class PasswordForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
    # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(PasswordForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        #user.password = "asdfasd"
        # user.is_active = False

        if commit:
            user.save()
            # user.profile.send_activation_email()
        # create a new user hash for activating email.
        return user
    