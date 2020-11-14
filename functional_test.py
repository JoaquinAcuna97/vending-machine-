from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def tearDown(self):
        self.driver.quit()

    def test_can_start_a_vending_machine_and_add_coin(self):
        # Joaquin has heard about a cool new online vending machine app. he goes
        # to check out its homepage
        self.driver.get('http://127.0.0.1:8000/')
        assert 'Vending Machine' in self.driver.title,\
            "Browser title was " + self.driver.title


if __name__ == '__main__':
    unittest.main(warnings='ignore')