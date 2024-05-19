import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time

class TestUIResetPassword(unittest.TestCase):

    def setUp(self):
        # Setup Chrome WebDriver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)  # Implicit wait for 10 seconds
        self.base_url = "http://localhost:80"  

    def tearDown(self):
        self.driver.quit()  # Close the browser after each test

    def test_valid_reset_request(self):
        driver = self.driver
        driver.get(f"{self.base_url}/forgot_password")

        # Find the email input field and submit a valid email
        email_input = driver.find_element(By.NAME, "email")
        email_input.send_keys("testresearcher@zewailcity.edu.eg")
        email_input.send_keys(Keys.RETURN)
        time.sleep(2)


        # Check that we are redirected to the reset password page
        self.assertIn("Reset Password", driver.title)
        legend = driver.find_element(By.TAG_NAME, "legend")
        self.assertIn("Reset Password", legend.text)

    def test_invalid_reset_request(self):
        driver = self.driver
        driver.get(f"{self.base_url}/forgot_password")

       
        email_input = driver.find_element(By.NAME, "email")
        email_input.send_keys("invaliduser@zewailcity.edu.eg")
        email_input.send_keys(Keys.RETURN)
        time.sleep(2)

        self.assertIn("Sign In / Sign Up", driver.title)

    def test_researcher_signup(self):
        driver = self.driver
        driver.get(f"{self.base_url}/researcher_signup")

        # Fill out the form fields
        driver.find_element(By.NAME, "fname").send_keys("John")
        driver.find_element(By.NAME, "lname").send_keys("Doe")
        driver.find_element(By.NAME, "username").send_keys("johndoe1")
        driver.find_element(By.NAME, "email").send_keys("johndoe1@zewail.edu.eg")
        driver.find_element(By.NAME, "password").send_keys("SuperSecretPassword123")
        driver.find_element(By.NAME, "confirm_password").send_keys("SuperSecretPassword123")
        driver.find_element(By.NAME, "field_of_study").send_keys("Computer Science")
        driver.find_element(By.NAME, "linkedin_account").send_keys("https://linkedin.com/in/johndoe")
        driver.find_element(By.NAME, "google_scholar_account").send_keys("https://scholar.google.com/citations?user=johndoe")

        # Submit the form
        driver.find_element(By.NAME, "submit").click()
        time.sleep(2)

        
        # Verify redirection to the home page
        self.assertIn("Sign In / Sign Up", driver.title)
        self.assertIn("<title>Sign In / Sign Up</title>", driver.page_source)

    
if __name__ == "__main__":
    unittest.main()
