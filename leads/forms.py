from django import forms
# django provides from for us to make it easier
# passinf our LeadForm to our views file to call in our lead_create function
from django.contrib.auth import get_user_model
from .models import Lead
# going to use djangos model form - allows you to take an existing model adn basicvally convert it into a form
from django.contrib.auth.forms import UserCreationForm, UsernameField

User = get_user_model()

class LeadModelForm(forms.ModelForm):
  class Meta:
    model = Lead
    fields = (
      'first_name',
      'last_name',
      'age',
      'agent',
    )

    

class LeadForm(forms.Form):
  first_name = forms.CharField()
  last_name = forms.CharField()
  age = forms.IntegerField()

# we are specifying our own user model instea dof the default user model provided by UserCreationForm - django
class CustomUserCreationForm(UserCreationForm):
  class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}