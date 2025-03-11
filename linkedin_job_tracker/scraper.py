"""
LinkedIn job scraper module.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from collections import defaultdict


def open_linkedin(username, password):
    """
    Log in to LinkedIn with provided credentials.

    Args:
        username (str): LinkedIn username/email
        password (str): LinkedIn password

    Returns:
        webdriver: Selenium webdriver instance with active LinkedIn session
    """
    # Initialize Chrome with webdriver-manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Log in to LinkedIn
    driver.get("https://www.linkedin.com/login")
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")

    username_field.send_keys(username)
    password_field.send_keys(password)

    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(5)  # Wait for login to complete
    return driver


def go_to_saved_jobs(driver):
    """
    Navigate to saved jobs page.

    Args:
        driver (webdriver): Selenium webdriver instance

    Returns:
        webdriver: Updated Selenium webdriver instance
    """
    driver.get("https://www.linkedin.com/my-items/saved-jobs/")
    time.sleep(5)  # Allow the page to load


def get_jobs_current_page(driver):
    """
    Extract job information from the current saved jobs page.

    Args:
        driver (webdriver): Selenium webdriver instance

    Returns:
        tuple: (list of job dictionaries, webdriver instance)
    """
    job_cards = driver.find_elements(By.CLASS_NAME, "mb1")
    jobs = []
    for i, job in enumerate(job_cards):
        lines = job.text.split("\n")
        job_dict = {}
        if len(lines) == 4:
            job_dict["title"] = lines[0]
            job_dict["company"] = lines[2]
            job_dict["location"] = lines[3]
            job_id = (
                job.find_elements(By.TAG_NAME, "a")[0]
                .get_attribute("href")
                .split("?")[0]
                .split("/")[-2]
            )
            jd_url = f"https://www.linkedin.com/jobs/view/{job_id}"
            job_dict["jd_url"] = jd_url
            job_dict["job_id"] = job_id
            jobs.append(job_dict)
    return jobs, driver


def get_all_saved_jobs(driver):
    """
    Extract all saved jobs by paginating through all pages.

    Args:
        driver (webdriver): Selenium webdriver instance

    Returns:
        tuple: (list of all job dictionaries, webdriver instance)
    """
    jobs = []
    start = 0
    next_page = True
    while next_page:
        try:
            # Get to page with pagination
            driver.get(f"https://www.linkedin.com/my-items/saved-jobs/?start={start}")
            time.sleep(5)

            current_jobs, driver = get_jobs_current_page(driver)
            if current_jobs and current_jobs[0] in jobs:
                next_page = False
            else:
                if current_jobs:
                    jobs += current_jobs
                    start += 10
                else:
                    next_page = False
        except Exception as e:
            print(e)
            next_page = False
            print("No more pages")
    return jobs, driver


def open_applied_jobs(driver, jobs, applied_jobs_file):
    """
    Open jobs in new tabs that match already applied jobs.

    Args:
        driver (webdriver): Selenium webdriver instance
        jobs (list): List of job dictionaries
        applied_jobs_file (str): Path to markdown file tracking applied jobs

    Returns:
        None
    """
    with open(applied_jobs_file, "r", encoding="utf-8") as f:
        text = f.read()
    # Convert the lines to markdown
    if "# Additional Companies" in text:
        md_text = text[: text.index("# Additional Companies")]
    else:
        md_text = text

    already_applied = defaultdict(dict)

    for job in jobs:
        job_id = job["job_id"]
        company = job["company"]

        if job_id in md_text:
            already_applied[job_id] = job

        if company in md_text:
            already_applied[job_id] = job

    # Open matches in new tabs
    for item in already_applied:
        if len(already_applied[item].keys()) != 0:
            print(already_applied[item])
            driver.execute_script(
                f"window.open('{already_applied[item]['jd_url']}', '_blank');"
            )
            time.sleep(3)
            saved_buttons = driver.find_elements(By.CLASS_NAME, "jobs-save-button")
            saved_buttons[-1].click()
            time.sleep(1)
