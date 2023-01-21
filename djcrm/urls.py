"""djcrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# import django settings module
from django.conf import settings
# is a function that takes in two things - we can then addiiotnal path to our urls here
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from leads.views import landing_page, LandingPageView, SignupView

urlpatterns = [
    # list of paths - manages paths in our web app - tells django which view to handle that path
    path('admin/', admin.site.urls),
    # thia allows our landing page class to be used as a biew - by using as_view
    path('', LandingPageView.as_view(), name='landing-page'),
    # path('', landing_page, name='landing-page'),
    # point to our new urls.py file inside our leads app to handle requests that go to a specific path
    path('leads/', include('leads.urls', namespace="leads") ),
    # document_root if the folder of our static  files that we want to have access in this path, the STATIC_URL path
    # instead of always adding the staic path in here - we can check to see if our project is in debug mode
    # static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')

]
# if settings DEBUG is true then we'll add an extra URL pattern here
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# Can view the contents of the files - in production mode tho we would not want to do this