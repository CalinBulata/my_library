from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import chromedriver_autoinstaller

from selenium.webdriver.common.by import By

from django.urls import reverse

from loans.models import Book

import time

class SeleniumTestCase(StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()

        driver_path = chromedriver_autoinstaller.install()

        self.options = ChromeOptions()
        self.options.add_argument("--headless=new")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")

        self.service = ChromeService(driver_path)

        self.browser = webdriver.Chrome(service=self.service, options=self.options)
        self.root_url = self.live_server_url

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

    def test_welcome(self):
        self.browser.get(self.live_server_url + '/welcome/')
        self.assertRegex(self.browser.page_source, "[w,W]elcome\\s+to\\s+[m,M]y\\s+[l,L]ibrary")
        self.assertRegex(self.browser.page_source, f'href=\"[{self.live_server_url}/]books/\"')

    def test_create_book_form_loads(self):
        create_book_url = self.live_server_url + reverse('create_book')
        self.browser.get(create_book_url)

        authors_field = self.browser.find_element(By.NAME, 'authors')
        title_field = self.browser.find_element(By.NAME, 'title')
        publication_date = self.browser.find_element(By.NAME, 'publication_date')
        isbn = self.browser.find_element(By.NAME, 'isbn')

        submit_button = self.browser.find_element(By.XPATH, '//input[@type="submit"]')

        self.assertIsNotNone(authors_field)
        self.assertIsNotNone(title_field)
        self.assertIsNotNone(publication_date)
        self.assertIsNotNone(isbn)
        self.assertIsNotNone(submit_button)

        self.assertEqual(submit_button.get_attribute('value'), 'Create')

    def test_create_book(self):
        before_count = Book.objects.count()

        create_book_url = self.root_url + reverse('create_book')
        self.browser.get(self.live_server_url + '/create_book/')
        self.assertEqual(self.browser.current_url, create_book_url)

        self.browser.find_element(By.NAME, 'authors').send_keys("Doe, J.")
        self.browser.find_element(By.NAME, 'title').send_keys("The title of a book")
        self.browser.find_element(By.NAME, 'publication_date').send_keys("01/04/2024")
        isbn_field = self.browser.find_element(By.NAME, 'isbn')
        isbn_field.send_keys("000")

        submit_button_invalid = self.browser.find_element(By.XPATH, '//input[@type="submit"]')
        self.browser.execute_script("arguments[0].click();", submit_button_invalid)

        self.assertEqual(self.browser.current_url, create_book_url)

        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count)

        isbn_field_after = self.browser.find_element(By.NAME, 'isbn')
        self.assertIn("is-invalid", isbn_field_after.get_attribute("class"))

        isbn_field_after.clear()
        isbn_field_after.send_keys("1234567890123")

        submit_button_valid = self.browser.find_element(By.XPATH, '//input[@type="submit"]')
        self.browser.execute_script("arguments[0].click();", submit_button_valid)

        books_list_url = self.root_url + reverse('list_books')
        self.assertEqual(self.browser.current_url, books_list_url)

        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count + 1)