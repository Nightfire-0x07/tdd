from selenium import webdriver
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
        self.fail('Finish the Test!')
        # Sam invited to enter to-do item right away

        # Sam types "Code python project" into a text box

        # When Sam hits enter, then the page update and 
        # returns Sam's typed message as an item in a to-do list

        # There is another textbox to enter an item, so Sam
        # enters "start web server"

        #The page updates again and shows both items on the list

        #Sam sees site has generated unique URL to revisit the saved
        # to-do list

        #Sam visits the unique URL, and the to-do list is saved there

        #Same exits the app

if __name__ == '__main__':
    unittest.main(warnings='ignore')
