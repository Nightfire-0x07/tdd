from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVistiorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        #Sam has heard about a to-do app. They go
        #to check out its homepage
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1. Code python project' for row in rows),
            "New to-do item did not appear in table"
        )
        # There is another textbox to enter an item, so Sam
        # enters "start web server"
        self.fail('Finish the test')
        #The page updates again and shows both items on the list

        #Sam sees site has generated unique URL to revisit the saved
        # to-do list

        #Sam visits the unique URL, and the to-do list is saved there

        #Same exits the app

if __name__ == '__main__':
    unittest.main(warnings='ignore')
