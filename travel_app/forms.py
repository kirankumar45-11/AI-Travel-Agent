from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Trip

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'profile_pic', 'bio']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
        }

INDIAN_STATES = [
    ('Andhra Pradesh', 'Andhra Pradesh'), ('Arunachal Pradesh', 'Arunachal Pradesh'), ('Assam', 'Assam'),
    ('Bihar', 'Bihar'), ('Chhattisgarh', 'Chhattisgarh'), ('Goa', 'Goa'), ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'), ('Himachal Pradesh', 'Himachal Pradesh'), ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'), ('Kerala', 'Kerala'), ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'), ('Manipur', 'Manipur'), ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'), ('Nagaland', 'Nagaland'), ('Odisha', 'Odisha'), ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'), ('Sikkim', 'Sikkim'), ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'), ('Tripura', 'Tripura'), ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'), ('West Bengal', 'West Bengal'),
    ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'), ('Chandigarh', 'Chandigarh'),
    ('Dadra and Nagar Haveli and Daman and Diu', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('Delhi', 'Delhi'), ('Jammu and Kashmir', 'Jammu and Kashmir'), ('Ladakh', 'Ladakh'),
    ('Lakshadweep', 'Lakshadweep'), ('Puducherry', 'Puducherry')
]

class TripPlannerForm(forms.Form):
    starting_point = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Starting from...',
        'list': 'states-list'
    }))
    destination = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Where to?',
        'list': 'states-list'
    }))
    budget = forms.DecimalField(max_digits=12, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total budget'}))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    travel_type = forms.ChoiceField(choices=Trip.TRAVEL_TYPES, widget=forms.Select(attrs={'class': 'form-control'}))
    trip_scope = forms.ChoiceField(
        choices=[('Inside India', 'Inside India'), ('Outside India', 'Outside India')],
        widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'predictCost()'})
    )

class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXXX XXXX XXXX XXXX'}))
    expiry_date = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'}))
    cvv = forms.CharField(max_length=3, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'CVV'}))
    card_holder = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}))
