from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import os
import time
from PIL import Image

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
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# The directory where the HTML files are stored
html_dir = "html_files"

# The directory where to save the screenshots
screenshot_dir = "screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

html_files = [file for file in os.listdir(html_dir) if file.endswith(".html")]

# Function to print/ update the progress bar
def print_progress_bar(iteration, total, prefix='', suffix='', length=100, fill='█'):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    if iteration == total:
        print()

# Iterate over all HTML files
for i, html_file     in enumerate(html_files):

# Open the HTML file in Chrome
    driver.get(f"file://{os.path.join(os.getcwd(), html_dir, html_file)}")

    
    time.sleep(1)  # Give it a moment to load

    # Take a screenshot and save it
    screenshot_path = os.path.join(screenshot_dir, f"{os.path.splitext(html_file)[0]}.png")
    driver.save_screenshot(screenshot_path)

    # Open the screenshot, rotate it, and save it again
    img = Image.open(screenshot_path)
    img_rotated = img.rotate(90, expand=True)
    img_rotated.save(screenshot_path)

    print_progress_bar(i+1, len(html_files), prefix='Progress:', suffix='Complete', length=50)

driver.quit()
