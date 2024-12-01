from django import forms

class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(max_length=15, label="Номер телефона", widget=forms.TextInput(attrs={'placeholder': 'Введите номер'}))

class VerificationCodeForm(forms.Form):
    code = forms.CharField(max_length=4, label="Код подтверждения", widget=forms.TextInput(attrs={'placeholder': 'Введите код'}))
