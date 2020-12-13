from django import forms
from .models import EmployeeInfo, ContactUs

class EmployeeForm(forms.ModelForm):
    id=forms.RegexField(regex=r'^[0-9]',
                        max_length=20,
                        label="ID",
                        required=True,
                        error_messages={"invalid":("Should be Integer Value")},
                        widget=forms.TextInput(attrs={'id':"eid"}),
                        )

    name=forms.RegexField(regex=r'^[a-zA-Z\s]+$',
                          max_length=30,
                          label="Name",
                          required=True,
                          error_messages={"invalid":("This value may contain only letters")},
                          widget=forms.TextInput(attrs={'id':"ename"}),
                          )

    class Meta:
        model=EmployeeInfo
        fields=['id','name']

class ContactUsForm(forms.ModelForm):
    class Meta:
        model=ContactUs
        fields="__all__"
