#from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

#class NewVistiorTest(LiveServerTestCase):
class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
    
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return 
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        #Sam has heard about a to-do app. They go
        #to check out its homepage
        self.browser.get(self.live_server_url)

        #They notice the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Sam invited to enter to-do item right away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )
        # Sam types "Code python project" into a text box
        inputbox.send_keys('Code python project')
        # When Sam hits enter, then the page update and 
        # returns Sam's typed message as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Code python project')
        
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Code python project', [row.text for row in rows])
       
        # There is another textbox to enter an item, so Sam
        # enters "start web server"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('start web server')
        inputbox.send_keys(Keys.ENTER)
        #The page updates again and shows both items on the list
        self.wait_for_row_in_list_table('1: Code python project')
        self.wait_for_row_in_list_table('2: start web server')
        #Sam sees site has generated unique URL to revisit the saved
        # to-do list

        #Sam visits the unique URL, and the to-do list is saved there

        #Same exits the app

    def test_multiple_users_can_start_lists_at_different_urls(self):
        #Sam starts new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Code python project')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Code python project')

        #sam notices the list has a unique URL
        sam_list_url = self.browser.current_url
        self.assertRegex(sam_list_url, '/lists/.+')

        # now a new user, Alice, comes to site

        #We use new browser session to ensure no info
        # of same's is coming through from cookies, etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Alice visits the homepage. there is not sign
        # of sam's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Code python project', page_text)
        self.assertNotIn('start web server', page_text)

        # Alice starts a new list by entering a new itme. 
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy almond milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy almond milk')

        # Alice gets her own unique URL
        alice_list_url = self.browser.current_url
        self.assertRegex(alice_list_url, '/lists/.+')
        self.assertNotEqual(alice_list_url, sam_list_url)

        #again, no trace of sam's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Code python project', page_text)
        self.assertIn('Buy almond milk', page_text)

    def test_layout_and_styling(self):
        #sam goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        
        # same notices the input box is nicely center
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
                inputbox.location['x'] + inputbox.size['width'] /2,
                512,
                delta=10
            )
        
        #sam starts a new list and sees the input is nicely
        # centered there too
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
                inputbox.location['x'] + inputbox.size['width'] /2,
                512,
                delta=10
        )
        # satisfied, they both go back to sleep
