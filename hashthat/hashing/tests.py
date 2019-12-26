from django.test import TestCase
from django.core.exceptions import ValidationError

from selenium import webdriver

from .utils import get_hash
from .forms import HashForm
from .models import Hash


helloHash = '2CF24DBA5FB0A30E26E83B2AC5B9E29E1B161E5C1FA7425E73043362938B9824'.lower()

# class can be any name
class FunctionalTestCase(TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    # use descriptive names for tests; MUST start with test_
    def test_there_is_homepage(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Enter text here', self.browser.page_source)

    def test_hash_of_hello(self):
        self.browser.get('http://localhost:8000')
        text = self.browser.find_element_by_id('id_text')
        text.send_keys('hello')
        self.browser.find_element_by_name('submit').click()
        self.assertIn(helloHash, self.browser.page_source)

    def test_hash_ajax(self):
        self.browser.get('http://localhost:8000/')
        text = self.browser.find_element_by_id('id_text')
        text.send_keys('hello')
        # self.browser.find_element_by_name('submit').click()
        self.assertIn(helloHash, self.browser.page_source)

    def tearDown(self):
        self.browser.quit()


class UnitTestCase(TestCase):
    def saveHash(self):
        hash = Hash()
        hash.text = 'hello'
        hash.hash = helloHash
        hash.save()
        return hash

    def test_home_homepage_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'hashing/home.html')
    
    def test_hash_form(self):
        form = HashForm(data={'text': 'hello', 'algo': 'sha256'})
        self.assertTrue(form.is_valid())

    def test_hash_func_works(self):
        text_hash = get_hash('sha256', 'hello')
        self.assertEqual(text_hash, helloHash)

    def test_hash_object(self):
        hash = self.saveHash()
        pulled_hash = Hash.objects.get(hash=helloHash)
        self.assertEqual(hash.text, pulled_hash.text)

    def test_viewing_hash(self):
        hash = self.saveHash()
        response = self.client.get(f'/hash/{helloHash}')
        self.assertContains(response, 'hello')

    def test_bad_data(self):
        def bad_hash():
            hash = Hash()
            hash.hash = 'fjsdäpgjdfpgjfaüg9jr90gijfgfijgdfgjfögjfdögjdfoögjdfögjfödgfjsdöogihfögohfdöghdföghdfghfdgsdfgdfl'
            hash.full_clean()
        self.assertRaises(ValidationError, bad_hash) 
