from selenium import webdriver
import unittest, time, os
from selenium.webdriver.common.by import By
basedir = os.path.abspath(os.path.dirname(__file__))
print("mqy", basedir)

class TestUser(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path=os.path.join(basedir,'geckodriver'))
        
    def test_register(self):
        self.driver.get("http://localhost:3000/register")
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.ID, 'firstName').send_keys("testfirst")
        self.driver.find_element(By.ID, 'lastName').send_keys("testlast")
        self.driver.find_element(By.ID, "email").send_keys("test@gmail.com")
        self.driver.find_element(By.ID, "password").send_keys("testpassword!")
        self.driver.find_element(By.ID, "submit").click()
        self.driver.implicitly_wait(5)
        self.driver.get('http://localhost:3000/login')
        self.driver.implicitly_wait(5)
        email = self.driver.find_element(By.ID, 'email')
        email.send_keys('test@gmail.com')
        password = self.driver.find_element(By.ID, 'password')
        password.send_keys('testpassword!')
        submit = self.driver.find_element(By.ID, 'submit')
        submit.click()
        self.driver.implicitly_wait(5)
        time.sleep(5)
        self.assertIn('dashboard', self.driver.current_url)
        time.sleep(5)

    def tearDown(self):
        self.driver.close()

if __name__=='__main__':
  unittest.main(verbosity=2)