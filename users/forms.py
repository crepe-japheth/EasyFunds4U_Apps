# users/forms.py
from django import forms
from .models import User

class AdminUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Type Password'}), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Re-Type Password'}), label="Confirm Password")

    class Meta:
        model = User
        fields = ["username", "email", "role", "branch"]


        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Type Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Type Email Address'}),
            'role': forms.Select(attrs={'class': 'form-control', 'placeholder':'Select Role'}),
            'branch': forms.Select(attrs={'class': 'form-control', 'placeholder':'Select Branch'}),
        }    
        labels = {
            'username': 'Username', 
            'email': 'Email Address',
            'role': 'User Role',
            'branch': 'Branch',
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
