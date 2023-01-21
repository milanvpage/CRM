from django.db import models
# signals are events that are fired when certain actions take place - django has a lot of built in signal that allwo you to take those signals and do things when they happe 
# listen for the event when user is create and create a USerProfile
# import differnt signals - post_save after the save is commited and pre_save before it's comitted to database
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
# right click and go to definition to read what its about
# You can see in the source code the delfault user it provides


# from django.contrib.auth import get_user_model
# user model provides by django can use in foreign keys - agent can be a user
# User = get_user_model
# Create your models here.
# Like creating Migrations tables in Rails
# CharField is mkaing sure it's a string max length of the string is set to 20
# IntegerField makes sure it's an integer and we set the default value to 0 

# saved migration in sqlite3 database under leads_leads, leads stands fro the app name and lead is the model we created inthis file named lead
# MIGRATE:
# python3 manage.py makemigrations - runs the manage.py file and makes our migrations ( it made out lead migration )
# python3 manage.py migrate - ran the manage.py file to run migrate and migrate our lead model to our database
# just like wehn we run db:migrate (table) in Rails to migrate our postgresSQL database
# only differnece is we're creating it in django with Python

# inherit from AbstractUSer
class User(AbstractUser):
  pass 
# just inheriting and creating our own user
#  this way in the future we can create our own fields if we want to add or take away from the defualt abstarct user default values and validations
# go to setting.py to configre/tell django that we have our own custom user model
# and add to bottom of settings.py -  AUTH_USER_MODEL = 'leads.User'
# delete database like in Rails so we can make a new migration when we add changes

class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  def __str__(self):
      return self.user.username

class Lead(models.Model):

    # SOURCE_CHOICES = (
    #     ('YouTube', 'YouTube'),
    #     ('Google', 'Google'),
    #     ('Newsletter', 'Newsletter'),
    # )
    # name saved in database and the source choices displayed to pick

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    # allows us to create every lead with it's own agent other wise an agent would be able to have only one lead
    agent = models.ForeignKey("Agent", on_delete=models.CASCADE)
    # models.SET_NULL, null=True - set value of the foreign key to be null if we allow null to be true
    # models.set_DEFAULT, default="" set the default value if agent was deleted
    # models.CASCADE - if agent is deleted the lead is deleted too
    # qoutes allow class defined lead above Agent
    # phoned = models.BooleanField(default=False)
    # # did we call them or not/ did we phone them or not? set default value to False
    # source = models.CharField(choices=SOURCE_CHOICES, max_length=100)
    # # source of where the lead came from

    # profile_picture = models.ImageField(blank=True, null=True)
    # # can save without profile picture
    # sepcial_files = models.FileField(blank=True, null=True)
    # # dont need it to uplaod lead becasue we set null=True
    # # like selecting a file from a form - you can selct a file from your computer adn ten you can store that file here in this field - although not uploaded to the databse this would be a reference to that file that gets saved in your project
    def __str__(self):
      return f"{self.first_name} {self.last_name}"
      # to display first and last name in python shell when called
# Link Table to another Table
# Create relationships between tables - like when we Learned Object Oriented Programming with rails


# Using django python manageer to interact with the database
# python Shell - "python in terminal" - python manage.py shell - for our shell of our app
# Lead.objects.all()
# <QuerySet []>
# python manage.py createsuperuser - creates admin user 
# (InteractiveConsole)
# >>> from django.contrib.auth import get_user_model
# >>> User = get_user_model()
# >>> User.objects.all()
# <QuerySet [<User: milan>]>

# from leads.models import Agent
# >>> admin_user = User.objects.get(username="milan")
# >>> admin_user
# <User: milan>

# agent = Agent.objects.create(user=admin_user)
# >>> agent
# <Agent: Agent object (1)>

# Now it outputs:
# from leads.models import Agent
# >>> Agent.objects.all()
# <QuerySet [<Agent: milan@justdjango.com>]>
# >>> 

# >>> from leads.models import Agent
# >>> from leads.models import Lead
# >>> milan_agent = Agent.objects.get(user__email="milan@justdjango.com")
# >>> milan_agent
# <Agent: milan@justdjango.com>
# >>> Lead.objects.create(first_name="Joe", last_name="Soap", age=35, agent=milan_agent)
# <Lead: Lead object (1)>
# __ double underscore helps filter the fields on the user user__
# retireved from database using the user table more of an advanced lookup

# Now it outputs:
# >>> from leads.models import Lead
# >>> Lead.objects.all()
# <QuerySet [<Lead: Joe Soap>]>

# By DEAFULT:
# SUPER USERS and STAFF USERS are able to login into the servers default login portal on http://127.0.0.1:8000/admin/login/?next=/admin/

class Agent(models.Model):
  # Our agent belongs to a a USer/ Organization - 
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  # Allowing multiple Agents to be linked to the same USer - so we pass the foreignkey of the User we are associating with 
  organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
  # works like foriegnkey but makes sure one user can have one agent
  # but most likely should create own User model eventually may need to customize it
  # user is then deleted when agent is deleted
  # foreignkey not smart beasue then it allows us to create many agents for one User
  # allow agent to manage lead - lead belong_to agent
  # first_name = models.CharField(max_length=20)
  # last_name = models.CharField(max_length=20)
  # dont need to pass the first and last name now becasue we have that on the AbstractUser
  

  # Python Shell:
#   agent = Agent.objects.create(user=admin_user)
# >>> agent
# <Agent: Agent object (1)>
  # so email is displayed when agent is called in python shell
  def __str__(self):
    return self.user.email
# Now it outputs:
# from leads.models import Agent
# >>> Agent.objects.all()
# <QuerySet [<Agent: milan@justdjango.com>]>
# >>> 

# called once post_save signal is sent 
# going to creat User profile
# sneder, the model sending, and the insatcne the actual model tha was saved, the created argument that tells us if the model instance was saved, pass in **kwargs key word arguments whihc basically just catches the rest of the arguments if there are any
def post_user_created_signal(sender, instance, created, **kwargs):
  # print(instance, created)
  # create User profile by passing th einstacne as the aprmameters to create one
  if created:
    UserProfile.objects.create(user=instance)
# takes in function you wan tot call and the sender that is sending the event/The model that is sending the event so in this case the model is the User
# omce User model is svaed, Django will sedn out the post_save signal - we are basically listening for that and connecting to that signal and saying once we recieve this event we want this function to handle the event 
post_save.connect(post_user_created_signal, sender=User)