# what we use to write tests
# to run tests in terminal: - this will look through all our apps and by defualt go look in the test.py file
# python manage.py test
from django.test import TestCase
from django.shortcuts import reverse
# Create your tests here.
# django will look inside this test.py file and execute all the test we have inside here by default
# tetsing is an entire subject on it's own and you can get really indepth and focused on testing 
# creates test database to execute the tests on - then once it's done with all the tests then it deletes the test database

# inherit from the Testcase
# tetsing our LandingView page to make sure it returns the right template - returns and http 200 statuc code so that it's a successful request
class LandingPageTest(TestCase):
# if you create a method that starts with test_ then it will execute it as a single test - if you had another then djang would execute two test on this landingPageView Testcase
# self keyword gives us a bunch of functionality that we have access to - and we can call different sort of tests
    # easier to keep everything inside one test so we're not running multiple tests

    # want to make a request to our landingpage url '' - and then test the response we get back from the URL
    def test_get(self):
      # TODO some sort of test
      # a way of sending requests - similar to the requests package provide by django that you can import
      # can send differetn HTTP methods - get, post, put etc. as part of the request
      # could hard code it as self.client.get(("/"))
      # but making use of djangos reverse method and the name we gave our landingpage path
      # this will have the html page in the recieved in response - http status code etc.
      response = self.client.get(reverse("landing-page"))
      # print(response.content)
      # if successful we should see 200 
      # print(response.status_code)
      # want to mkae sure it allways is OK
      # takes tw args - response.status_code and the value we want to see from that stasus_code
      # this will compare the response.status_code with 200 - and if it's not = 200 we will get an error syaing this test did not pass
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, "landing.html")
      