import unittest
import requests

#We will try send not suitable data to our application and checkout the results of these actions


class TestAPI(unittest.TestCase):
    
    
    def test1(self):
        #1 Lack of the name
        #Sending the form in form of raw data using post request
        URL_FORM= "http://127.0.0.1:5000/form"
        raw = "name=&surname=Dangod&id=12345678900&first_place=Certified+Kubernetes+Administrator&second_place=Azure+Administrator+Associate&third_place=+Google+Cloud+Associate+Cloud+Engineer&fourth_place=AWS+Certified+Solutions+Architect&comment=++++++++++++"
        rep = requests.post(URL_FORM,data=raw, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertEqual(rep.status_code,400)

    def test2(self):
        #2 Lack of the surname
        #Sending the form in form of raw data using post request
        URL_FORM= "http://127.0.0.1:5000/form"
        raw = "name=Marek&surname=&id=12345678900&first_place=Certified+Kubernetes+Administrator&second_place=Azure+Administrator+Associate&third_place=+Google+Cloud+Associate+Cloud+Engineer&fourth_place=AWS+Certified+Solutions+Architect&comment=++++++++++++"
        rep = requests.post(URL_FORM,data=raw, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertEqual(rep.status_code,400)

    def test3(self):
        #3 Lack of the id
        #Sending the form in form of raw data using post request
        URL_FORM= "http://127.0.0.1:5000/form"
        raw = "name=Marek&surname=Dangod=&id=&first_place=Certified+Kubernetes+Administrator&second_place=Azure+Administrator+Associate&third_place=+Google+Cloud+Associate+Cloud+Engineer&fourth_place=AWS+Certified+Solutions+Architect&comment=++++++++++++"
        rep = requests.post(URL_FORM,data=raw, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        html_body = rep.text #Getting structure of html document in order to verify its content
        self.assertIn("wrapper", html_body) #1 case
        self.assertIn("Wrong id. The lenght of id is 11 characters", html_body) #2 case

    def test4(self):
        #4 Too short name
        #Sending the form in form of raw data using post request
        URL_FORM= "http://127.0.0.1:5000/form"
        raw = "name=Ma&surname=Dangod=&id=12345678900&first_place=Certified+Kubernetes+Administrator&second_place=Azure+Administrator+Associate&third_place=+Google+Cloud+Associate+Cloud+Engineer&fourth_place=AWS+Certified+Solutions+Architect&comment=++++++++++++"
        rep = requests.post(URL_FORM,data=raw, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        html_body = rep.text #Getting structure of html document in order to verify its content
        self.assertIn("wrapper", html_body) #1 case
        self.assertIn("Too short name or surname. Minimum length is 3 characters", html_body) #2 case

    def test5(self):
        #5 Too short surname
        #Sending the form in form of raw data using post request
        URL_FORM= "http://127.0.0.1:5000/form"
        raw = "name=Marek&surname=D=&id=12345678900&first_place=Certified+Kubernetes+Administrator&second_place=Azure+Administrator+Associate&third_place=+Google+Cloud+Associate+Cloud+Engineer&fourth_place=AWS+Certified+Solutions+Architect&comment=++++++++++++"
        rep = requests.post(URL_FORM,data=raw, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertEqual(rep.status_code,400)

    def test6(self):
        #5 Too short id
        #Sending the form in form of raw data using post request
        URL_FORM= "http://127.0.0.1:5000/form"
        raw = "name=Marek&surname=Dangod=&id=123&first_place=Certified+Kubernetes+Administrator&second_place=Azure+Administrator+Associate&third_place=+Google+Cloud+Associate+Cloud+Engineer&fourth_place=AWS+Certified+Solutions+Architect&comment=++++++++++++"
        rep = requests.post(URL_FORM,data=raw, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertEqual(rep.status_code,400)

    def test7(self):
        #5 Too long id
        #Sending the form in form of raw data using post request
        URL_FORM= "http://127.0.0.1:5000/form"
        raw = "name=Marek&surname=Dangod=&id=123123123123123123&first_place=Certified+Kubernetes+Administrator&second_place=Azure+Administrator+Associate&third_place=+Google+Cloud+Associate+Cloud+Engineer&fourth_place=AWS+Certified+Solutions+Architect&comment=++++++++++++"
        rep = requests.post(URL_FORM,data=raw, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertEqual(rep.status_code,400)

if __name__ == "__main__":
    tester = TestAPI()
    tester.test1()
    tester.test2()
    tester.test3()
    tester.test4()
    tester.test5()
    tester.test6()