from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import os
import time
from PIL import Image


def screenshot_html_files(skip_existing, jpeg_quality=95):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set the browser window size
    height = 1920
    width = 1080
    chrome_options.add_argument(f"--window-size={width}x{height}")

    # Set up the webdriver
    webdriver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(
        service=webdriver_service, options=chrome_options)

    # The directory where the HTML files are stored
    html_dir = "html_files"

    # The directory where to save the screenshots
    screenshot_dir = "screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)

    # Get all HTML files recursively, and their relative paths
    html_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(
        html_dir) for f in filenames if f.endswith(".html")]

    # Function to print/ update the progress bar
    def print_progress_bar(iteration, total, prefix='', suffix='', length=100, fill='█'):
        percent = 100 * (iteration / float(total))
        filled_length = int(length * (percent / 100))
        bar = fill * filled_length + '-' * (length - filled_length)
        percent_string = percent = ("{0:.1f}").format(percent)
        print(f'\r{prefix} |{bar}| {percent_string}% {suffix}', end='\r')
        if iteration == total:
            print()

    # Iterate over all HTML files
    for i, relative_html_path in enumerate(html_files):

        # Remove the 'html_files/' prefix from the relative path
        relative_screenshot_path = relative_html_path[len(html_dir) + 1:]

        # Construct the path where the screenshot will be saved
        base_screenshot_path = os.path.splitext(
            relative_screenshot_path)[0] + ".png"
        screenshot_path = os.path.join(screenshot_dir, base_screenshot_path)

        # Make sure the directory exists
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        
        # Check if screenshot exists and skip if necessary
        if skip_existing and os.path.exists(screenshot_path):
            continue

        # Open the HTML file in Chrome
        driver.get(f"file://{os.path.join(os.getcwd(), relative_html_path)}")

        time.sleep(1)  # Give it a moment to load

        # Take a screenshot and save it
        driver.save_screenshot(screenshot_path)

        # Open the screenshot, rotate it, and save it again
        img = Image.open(screenshot_path)
        img_rotated = img.rotate(90, expand=True)
        # # Convert RGBA to RGB
        # if img_rotated.mode == 'RGBA':
        #     img_rotated = img_rotated.convert("RGB")
        img_rotated.save(screenshot_path, "png")

        print_progress_bar(i+1, len(html_files),
                           prefix='Progress:', suffix='Complete', length=50)

    driver.quit()


screenshot_html_files(skip_existing=True)
