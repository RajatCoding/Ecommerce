from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from .models import Customer


User = get_user_model()

class RegisterForm(forms.ModelForm):
    """
    The default 

    """

    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm): 
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'is_active',]

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label=("Password"),
        
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
        help_text=None,
        required=True
        )
    password2 = forms.CharField(
        label=("Confirm Password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
        help_text=None
        )
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "mobile_no","state","city","address","zipcode" ]
        labels = {"email": "Email"}
        widgets = {
        'first_name': forms.TextInput(attrs = {'class':'form-control','placeholder':'Enter First Name'}),

        'last_name': forms.TextInput(attrs = {'class':'form-control','placeholder':'Enter Last Name'}),

        'mobile_no': forms.TextInput(attrs = {'class':'form-control','placeholder':'Mobile Number'}),

        'email': forms.EmailInput(attrs = {'class':'form-control','placeholder':'Enter your email','required':'true'}),

        'address': forms.Textarea(attrs = {'class':'form-control','placeholder':'Enter your address','rows':4}),

        'address': forms.Textarea(attrs = {'class':'form-control','placeholder':'Enter your address','rows':4}),

        'zipcode': forms.TextInput(attrs = {'class':'form-control'}),

        'city': forms.TextInput(attrs = {'class':'form-control'}),

        'state': forms.Select(attrs = {'class':'form-control'}),

        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "mobile_no","address","zipcode", "state","city"]
        labels = {"email": "Email"}
        widgets = {
        'first_name': forms.TextInput(attrs = {'class':'form-control','placeholder':'Enter First Name'}),

        'last_name': forms.TextInput(attrs = {'class':'form-control','placeholder':'Enter Last Name'}),

        'mobile_no': forms.TextInput(attrs = {'class':'form-control','placeholder':'Mobile Number'}),

        'email': forms.EmailInput(attrs = {'class':'form-control','placeholder':'Enter your email','required':'true'}),

        'address': forms.Textarea(attrs = {'class':'form-control','placeholder':'Enter your address','rows':4}),

        'zipcode': forms.TextInput(attrs = {'class':'form-control'}),

        'city': forms.TextInput(attrs = {'class':'form-control'}),

        'state': forms.Select(attrs = {'class':'form-control'}),

        }

class VerifyOtpForm(forms.Form):
     Otp = forms.CharField(
        label=("OTP"),
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'OTP'}),
        help_text=None
        )
    
class LoginForm(AuthenticationForm):
 username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class':'form-control'}))
 password = forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'form-control'}))

class PwdChange(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus':True,  'class':'form-control'}))

    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())

    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}))
        


class AddOtherAddressForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "mobile_no", "state", "city", "locality", "zipcode"]
        
        widgets = {
        'name': forms.TextInput(attrs = {'class':'form-control','placeholder':'Enter First Name'}),

       
        'mobile_no': forms.TextInput(attrs = {'class':'form-control','placeholder':'Mobile Number'}),

       

        'locality': forms.Textarea(attrs = {'class':'form-control','placeholder':'Enter your address','rows':4}),

        'zipcode': forms.TextInput(attrs = {'class':'form-control'}),

        'city': forms.TextInput(attrs = {'class':'form-control'}),

        'state': forms.Select(attrs = {'class':'form-control'}),

        }

class AddressUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "mobile_no", "state", "city", "locality", "zipcode"]
        
        widgets = {
        'name': forms.TextInput(attrs = {'class':'form-control','placeholder':'Enter First Name'}),

       
        'mobile_no': forms.TextInput(attrs = {'class':'form-control','placeholder':'Mobile Number'}),

       

        'locality': forms.Textarea(attrs = {'class':'form-control','placeholder':'Enter your address','rows':4}),

        'zipcode': forms.TextInput(attrs = {'class':'form-control'}),

        'city': forms.TextInput(attrs = {'class':'form-control'}),

        'state': forms.Select(attrs = {'class':'form-control'}),

        }