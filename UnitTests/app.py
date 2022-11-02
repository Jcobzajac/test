import unittest
import requests

#We are going to check behaviour of our components in the code in different cases of requests
#Basically the main purpose is to revision what application will do and
#how the bussiness logic is handled when our applicattion gets wrong input or proper


class TestAPI(unittest.TestCase):
    
    
    def test1(self):
        #1 PROPER FORM
        #Sending the form in form of raw data using post request
        URL_FORM= "http://127.0.0.1:5000/form"
        raw = "name=Tom&surname=Nedved&id=11111111111&first_place=Certified+Kubernetes+Administrator&second_place=Azure+Administrator+Associate&third_place=+Google+Cloud+Associate+Cloud+Engineer&fourth_place=AWS+Certified+Solutions+Architect&comment=++++++++++++"
        rep = requests.post(URL_FORM,data=raw, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertEqual(rep.status_code,200)

        #Our data from form should be displayed in the /declaration/latest page where we have the latest assignment for certification :)
        URL_LATEST = "http://127.0.0.1:5000/declaration/latest"
        rep = requests.get(URL_LATEST)
        html_body = rep.text #Getting structure of html document in order to verify its content
        self.assertIn("1. Certified Kubernetes Administrator", html_body) #1 case
        self.assertIn("2. Azure Administrator Associate", html_body) #2 case
        self.assertIn("3.  Google Cloud Associate Cloud Engineer", html_body) #3 case
        self.assertIn("4. AWS Certified Solutions Architect", html_body) #4 case

    def test2(self):
        #WRONG ID
        #Sending bad id in order to check whether our previous data will be maintained
        URL_FORM = "http://127.0.0.1:5000/form"
        raw = "name=Jennifer&surname=Mosinski&id=1308976530111&first_place=Certified+Kubernetes+Administrator&second_place=Azure+Administrator+Associate&third_place=+Google+Cloud+Associate+Cloud+Engineer&fourth_place=AWS+Certified+Solutions+Architect&comment=++++++++++++1"
        rep = requests.post(URL_FORM,data=raw, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertEqual(rep.status_code,400) #We've sent wrong id, so we should get status code 400 

        #Checking whether our previous state in context of data was maintained
        URL_LATEST  = "http://127.0.0.1:5000/declaration/latest"
        rep = requests.get(URL_LATEST )
        html_body = rep.text #Getting structure of html document in order to verify its content
        self.assertIn("1. Certified Kubernetes Administrator", html_body) #1 case
        self.assertIn("2. Azure Administrator Associate", html_body) #2 case
        self.assertIn("3.  Google Cloud Associate Cloud Engineer", html_body) #3 case
        self.assertIn("4. AWS Certified Solutions Architect", html_body) #4 case

    def test3(self):
        #VALID ID
        #Testing process of redirecting after sending valid id when we want to update our data
        URL_FORM = "http://127.0.0.1:5000/change/update/id"
        raw = "id=11111111111"
        rep = requests.post(URL_FORM,data=raw, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertEqual(rep.status_code,200)
        html_body = rep.text  
        #Checking elements form the html structure, where we should be redirected (labels,comments,content)
        self.assertIn("First Place", html_body) #1 case
        self.assertIn("Second Place", html_body) #2 case
        self.assertIn("<!-- Dropdown options -->", html_body) #3 case
        self.assertIn("label-first_place", html_body) #4 case

    def test4(self):
        #WRONG ID
        #Testing process of redirecting after sending wrong id when we want to update our data
        URL_FORM = "http://127.0.0.1:5000/change/update/id"
        raw = "id=222"
        rep = requests.post(URL_FORM,data=raw, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertEqual(rep.status_code,404)
        html_body = rep.text
        #Checking elements form the html structure, where we should be redirected (labels,comments,content)
        self.assertIn("<h1>This id doesn&#39;t exist</h1>", html_body) #1 case
        self.assertIn("wrapper", html_body) #2 case

    def test5(self):
        #VALID ID
        #Trying delete our existing assignment using valid id
        URL_FORM = "http://127.0.0.1:5000/change/delete/id"
        raw = "id=11111111111"
        rep = requests.post(URL_FORM,data=raw, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertEqual(rep.status_code,200)

    def test6(self):
        #WRONG ID 
        #Trying delete our previous assignment using previous id
        URL_FORM = "http://127.0.0.1:5000/change/delete/id"
        raw = "id=11111111111"
        rep = requests.post(URL_FORM,data=raw, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertEqual(rep.status_code,400)
        html_body = rep.text
        #Checking elements form the html structure, where we should be redirected (labels,comments,content)
        self.assertIn("<h1>This id doesn&#39;t exist</h1>", html_body) #1 case
        self.assertIn("wrapper", html_body) #2 case


if __name__ == "__main__":
    tester = TestAPI()
    tester.test1()
    tester.test2()
    tester.test3()
    tester.test4()
    tester.test5()
    tester.test6()