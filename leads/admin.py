from django.contrib import admin

# Register your models here.
from .models import User, Lead, Agent, UserProfile

# register in the admin:
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Lead)
admin.site.register(Agent)
# wouldnt want users loggin in here becasue it's more of an admin backend
# refersh page and now we have a  whole new section under leads called Users - the name of the app "Leads"

