import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from studybuddy.util import get_user_agents, file_name_from_url


def initialize_driver():
    options = Options()

    # Reduce driver overhead
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Set user agent string
    possible_user_agents = get_user_agents()
    options.add_argument(f"user-agent={random.choice(possible_user_agents)}")

    # Disable automation flags to avoid detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Additional options to mimic a real browser
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")

    # Specify the path to the Chromium binary
    options.binary_location = "/usr/bin/chromium"  # Or replace with the path to chromium binary

    # Specify the path to the ChromeDriver executable
    # If using debian try 'sudo apt install chromium-driver' then it should be:
    chromedriver_path = "/usr/bin/chromedriver"  # Or replace with the path to chromedriver binary

    # Initialize the driver with the specified ChromeDriver path
    driver = webdriver.Chrome(
        service=Service(chromedriver_path),
        options=options
    )

    # Override navigator.webdriver to false, again to help with detection. Here we are using a chromedriver different
    # user agents such as Safari and Firefox with chromedriver. Target Javascript may detect this discrepancy if the
    # following line is not used
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    driver.implicitly_wait(0)

    return driver

class Scraper:
    def __init__(self, selected_language):
        self.selected_language = selected_language
        self.driver = initialize_driver()
        self.wait_timeout = 20 # Max wait time of 20 seconds
        self.wait = WebDriverWait(self.driver, self.wait_timeout)

        self.difficulty_css_selectors = ".text-difficulty-easy, .text-difficulty-medium, .text-difficulty-hard"
        self.language_button_css_selector = "button.px-1\\.5"
        self.language_option_css_selector = "div.border-r.border-solid"
        self.code_line_css_selector = "div.view-lines.monaco-mouse-cursor-text"

    def quit(self):
        self.driver.quit()
        self.driver.session_id = None

    def reinit_driver(self):
        self.driver.quit()
        self.driver = initialize_driver()
        self.wait = WebDriverWait(self.driver, self.wait_timeout)

    def get_selected_language_button(self):
        language_options_lists = self.wait.until(
            ec.presence_of_all_elements_located((By.CSS_SELECTOR, self.language_option_css_selector))
        )
        for language_option_list in language_options_lists:
            current_list_options = language_option_list.find_elements(By.XPATH, "./*")
            for element in current_list_options:
                language_name_element = element.find_element(By.XPATH, "./div")
                if language_name_element.text == self.selected_language:
                    return language_name_element

        return None

    def get_code_lines(self):
        # Wait until new code lines are loaded
        line_elements = self.wait.until(
            ec.visibility_of_all_elements_located((By.CSS_SELECTOR, f"{self.code_line_css_selector} div"))
        )

        code_lines = []
        for line in line_elements:
            line_text = line.text
            code_lines.append(line_text + "\n")
        return code_lines

    def get_url_data(self, url):
        file_name = file_name_from_url(url)
        if not file_name:
            print("Error: Could not parse file name from url.")
            return None

        print("Fetching data for:", file_name)

        self.driver.get(url)

        difficulty = self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR,
                                                                     self.difficulty_css_selectors))).text

        change_language_button = self.wait.until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, self.language_button_css_selector)))
        change_language_button.click()

        # After setting the language the first time, it should remain for each question. The preferred language is
        # stored either in cookies or determined server side. Either way this check is done to prevent any unexpected
        # changes
        if change_language_button.text != self.selected_language:
            selected_language_button = self.get_selected_language_button()
            selected_language_button.click()

        code_lines = self.get_code_lines()

        if not code_lines:
            print(f"Error: No code lines found for selected language: {self.selected_language} for "
                  f"question url: {url}.")
            return None

        return [file_name, difficulty, code_lines]
