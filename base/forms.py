from django.forms import ModelForm, PasswordInput
from django import forms
from .models import Room, Expense, User


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['name','description']

class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ['amount','description']


class UserForm(ModelForm):
    password = forms.CharField(widget=PasswordInput)
    confirm_password = forms.CharField(widget=PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm Password do not match."
            )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user