# command k  command 0 - to close code blocks
# from django send mail method
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
# render call will return html pages for us
# use
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
# could aso say:
# from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
# use to return to the request
# Create your views here.
# Pass in Lead model with our data
from .models import Lead, Agent
from .forms import LeadModelForm, LeadForm, CustomUserCreationForm

# CRUD - Create, Retrieve, Update and Delete + List
# Django generic views are also structured under the CRUD kind of principle:
# list view, detail view, update view, create view, delete view - all use template_name function
# django also provides us with a user creation form wich we can import from the authentication module
# mixins are arguments we add intoo the inheritance of classes - inherit from multiple classes instead of just one

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    # DJANGOS way of using the views template to create a form by using the form_class function to call it
    # making use of our own custom form that uses our model 
    form_class = CustomUserCreationForm
    # just need to specify a specific method for when the form is saved
    def get_success_url(self):
        return reverse("login")

class LandingPageView(generic.TemplateView):
    # function provided by TemplateViews - it takes in your htl page
    template_name = "landing.html"
# have to mka esure the MIxen is first becasue that makes sure it's called first - this makes sure our User can only view the leads if they're logged in 
class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    queryset = Lead.objects.all()
#  the LeadListView class and the default value for our objects is object_views
# but we can change that by using context_object_name and specify our object name:
# now we dont have to chnage the variable in our html template    # 
    context_object_name = "leads"

class LeaDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    queryset = Lead.objects.all()
#  the LeadListView class and the default value for our objects is object_views
# but we can change that by using context_object_name and specify our object name:
# now we dont have to chnage the variable in our html template    # 
    # bsaed pk passe in it will automatically grab that lead
    context_object_name = "lead"

class LeaCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    # DJANGOS way of using the views template to create a form by using the form_class function to call it
    form_class = LeadModelForm
    # just need to specify a specific method for when the form is saved
    def get_success_url(self):
        return reverse("leads:lead-list")
    # use reverse funcion from djago - more correct way - instead of returning a hard coded version like redirect("leads/lead_list.html")
    # send us an email every time we create a new Lead
    # once it submits the form it will go through this form_valid method and then redirect us all leads 
    def form_valid(self, form):
        # TODO send email
        # from_email will be the DEFAULT_FROM_EMAIL in the dejango settings
        # auth_user is the default EMAIL_HOST_USER from the django settings
        # auth_password is the default EMAIL_HOST_PASSWORD from the django settings
# normally if you are using an email provider then you would configure your email host providers details in the settings - get to the settings by insoecting the send_email function and go to djangos doc for them and edit the parts as seen obove commented out 
# But right now we're going to mak euse of django as the source that send the emails
        # will get error at first becasue it says credentials refused - because we havent set up an email provider yet
        # we dont need to be working with a provider - but when your in production you'll want to
        send_mail(
            subject="A lead has been created", 
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeaCreateView, self).form_valid(form)
        
class LeaUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    # DJANGOS way of using the views template to create a form by using the form_class function to call it
    # hat to pass queryset becasue we're updating a specifc lead
    queryset = Lead.objects.all()
    form_class = LeadModelForm
    # just need to specify a specific method for when the form is saved
    def get_success_url(self):
        return reverse("leads:lead-list")
    # use reverse funcion from djago - more correct way - instead of returning a hard coded version like redirect("leads/lead_list.html")

class LeadDeleteView(LoginRequiredMixin, generic.DeleteView):
    # have to provide a template even for delete when youre dealing django template views
    template_name = "leads/lead_delete.html"
    # DJANGOS way of using the views template to create a form by using the form_class function to call it
    # hat to pass queryset becasue we're updating a specifc lead
    queryset = Lead.objects.all()
    # just need to specify a specific method for when the form is saved
    def get_success_url(self):
        return reverse("leads:lead-list")
    # use reverse funcion from djago - more correct way - instead of returning a hard coded version like redirect("leads/lead_list.html")


# CONVERTED all these Functions into classes
# function based views - python functions to handle the view
def landing_page(request):
    return render(request, "landing.html")

# in order to use this function we need to add it to our URLs - urls.py file
def lead_list(request):
    # return HttpResponse("Hello World")
    # return render(request, "leads/home_page.html")
    # add context in that 3rd parameter
    # pass in keys and values of information we want to pass in
    # context = {
    #     "name": "Joe",
    #     "age": 35
    # }
    # like grabbing data from our javascript classes we mad in Flatiron project
    leads = Lead.objects.all()
    context = {
        "leads": leads
    }
    return render(request, "leads/lead_list.html", context)

# pk stand fro primrary key
# important we call it pk becasue the url is also using pk to define the route
def lead_detail(request, pk):   
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(request, "leads/lead_detail.html", context)

def lead_create(request):
    # print(request.POST)
    # this prints in terminal
    # <QueryDict: {'csrfmiddlewaretoken': ['vjJVcyjbZxsbbCV2L5e6r9Pm27q1QMm085MxiRjDHkgv4hY8LZJLkdAdxPcWoLNJ'], 'first_name': ['Milan'], 'first_last': ['h'], 'age': ['3']}>
    
    # if request method is not post we're going to originally set the form as so:
    # to be this empty instantiated form 
    form = LeadModelForm()
    
    # if it is a POST request: 
    if request.method == "POST":
        print('Recieving POST request')
        form = LeadModelForm(request.POST)
        # django can check if the form is valid and print the cleaned data from that form 
        # django model forms let us automatically save the data to the database as a new model
        if form.is_valid():
            form.save()
            print("This lead has been created")
            return redirect("/leads")
    context = {
        "form": form
    }
    return render(request, "leads/lead_create.html", context)

def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    # pass in instacne=lead to specify that we want to save/update an existing lead and not create a new one - so we ave to pass it in to specify
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        "form": form,
        "lead": lead
    }
    return render(request, "leads/lead_update.html", context)

def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    # delete() comes from django models and just allows you to easily delte the model like that
    lead.delete()
    return redirect("/leads")

# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm()
#     # if it is a POST request: 
#     if request.method == "POST":
#         print('Recieving POST request')
#         form = LeadForm(request.POST)
#         # django can check if the form is valid and print the cleaned data from that form 
#         if form.is_valid():
#             print("Form is vaild")
#             print(form.cleaned_data)
#             # now can create new lead with cleaned_data
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             # grabs the first row in the agent table
#             agent = Agent.objects.first()
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age
#             # update database by calling .save() on the model 
#             lead.save()
#             print("This lead has been created")
#             return redirect("/leads")
#     context = {
#         "form": form,
#         "lead": lead
#     }
#     return render(request, "leads/lead_update.html", context)



# def lead_create(request):
#     # print(request.POST)
#     # this prints in terminal
#     # <QueryDict: {'csrfmiddlewaretoken': ['vjJVcyjbZxsbbCV2L5e6r9Pm27q1QMm085MxiRjDHkgv4hY8LZJLkdAdxPcWoLNJ'], 'first_name': ['Milan'], 'first_last': ['h'], 'age': ['3']}>
    
#     # if request method is not post we're going to originally set the form as so:
#     # to be this empty instantiated form 
    # form = LeadModelForm()

    # # if it is a POST request: 
    # if request.method == "POST":
    #     print('Recieving POST request')
    #     form = LeadModelForm(request.POST)
    #     # django can check if the form is valid and print the cleaned data from that form 
    #     if form.is_valid():
    #         print("Form is vaild")
    #         print(form.cleaned_data)
    #         # now can create new lead with cleaned_data
    #         first_name = form.cleaned_data['first_name']
    #         last_name = form.cleaned_data['last_name']
    #         age = form.cleaned_data['age']
    #         # grabs the first row in the agent table
    #         agent = Agent.objects.first()
    #         Lead.objects.create(
    #             first_name=first_name,
    #             last_name=last_name,
    #             age=age,
    #             agent=agent
    #         )
    #         print("This lead has been created")
    #         return redirect("/leads")
    # context = {
    #     "form": form
    # }
    # return render(request, "leads/lead_create.html", context)
