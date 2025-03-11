"""
LinkedIn job scraper module.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from collections import defaultdict
import random
from loguru import logger


def open_linkedin(username, password):
    """
    Log in to LinkedIn with provided credentials.

    Args:
        username (str): LinkedIn username/email
        password (str): LinkedIn password

    Returns:
        webdriver: Selenium webdriver instance with active LinkedIn session
    """
    logger.info("Initializing Chrome driver")
    # Initialize Chrome with webdriver-manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Log in to LinkedIn
    logger.info("Navigating to LinkedIn login page")
    driver.get("https://www.linkedin.com/login")
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")

    username_field.send_keys(username)
    password_field.send_keys(password)

    logger.info("Submitting login credentials")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(20)  # Wait for login to complete
    logger.info("Login completed")
    return driver


def go_to_saved_jobs(driver):
    """
    Navigate to saved jobs page.

    Args:
        driver (webdriver): Selenium webdriver instance

    Returns:
        webdriver: Updated Selenium webdriver instance
    """
    logger.info("Navigating to saved jobs page")
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
    logger.debug("Finding job cards on current page")
    job_cards = driver.find_elements(By.CLASS_NAME, "mb1")
    logger.info(f"Found {len(job_cards)} job cards on page")

    jobs = []
    for i, job in enumerate(job_cards):
        lines = job.text.split("\n")
        job_dict = {}
        # remove ', Verified'
        lines = [line for line in lines if ", Verified" not in line]

        if len(lines) >= 3:
            job_dict["title"] = lines[0]
            job_dict["company"] = lines[1]
            job_dict["location"] = lines[2]
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
            logger.debug(f"Parsed job: {job_dict['title']} at {job_dict['company']}")

    return jobs, driver


def get_all_saved_jobs(driver):
    """
    Extract all saved jobs by paginating through all pages.

    Args:
        driver (webdriver): Selenium webdriver instance

    Returns:
        tuple: (list of all job dictionaries, webdriver instance)
    """
    logger.info("Starting to fetch all saved jobs")
    jobs = []
    start = 0
    next_page = True
    while next_page:
        try:
            # Get to page with pagination
            logger.debug(f"Navigating to saved jobs page starting at index {start}")
            driver.get(f"https://www.linkedin.com/my-items/saved-jobs/?cardType=SAVED&start={start}")
            time.sleep(10)

            current_jobs, driver = get_jobs_current_page(driver)
            if current_jobs and current_jobs[0] in jobs:
                logger.info("Duplicate job found, reached end of pagination")
                next_page = False
            else:
                if current_jobs:
                    jobs += current_jobs
                    start += 10
                    logger.info(
                        f"Found {len(current_jobs)} jobs, total now: {len(jobs)}"
                    )
                else:
                    logger.info(
                        "No jobs found on current page, reached end of pagination"
                    )
                    next_page = False
        except Exception as e:
            logger.error(f"Error fetching jobs: {e}")
            next_page = False
            logger.info("No more pages")

    logger.success(f"Finished fetching all saved jobs, found {len(jobs)} total")
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
    logger.info(f"Checking saved jobs against applied jobs file: {applied_jobs_file}")

    with open(applied_jobs_file, "r", encoding="utf-8") as f:
        text = f.read()
    # Convert the lines to markdown
    if "# Additional Companies" in text:
        md_text = text[: text.index("# Additional Companies")]
    else:
        md_text = text

    already_applied = defaultdict(dict)

    logger.debug("Searching for matches between saved jobs and applied jobs")
    for job in jobs:
        job_id = job["job_id"]
        company = job["company"]

        if " INTERN" in job["title"].upper():
            already_applied[job_id] = job
            logger.debug(f"Match found by job ID: {job['title']} at {job['company']}")
            continue

        if job_id in md_text:
            already_applied[job_id] = job
            logger.debug(f"Match found by job ID: {job['title']} at {job['company']}")
            continue

        if company.upper() in md_text.upper():
            already_applied[job_id] = job
            logger.debug(
                f"Match found by company name: {job['title']} at {job['company']}"
            )
            continue

    logger.info(f"Found {len(already_applied)} matches with already applied jobs")

    # Open matches in new tabs
    for item in already_applied:
        if len(already_applied[item].keys()) != 0:
            job_info = already_applied[item]
            logger.info(
                f"Opening already applied job: {job_info['title']} at {job_info['company']}"
            )

            # Remove the job if it is already in jobs list
            if job_info in jobs:
                logger.debug(f"Removing job from active list: {job_info['title']}")
                jobs.remove(job_info)

            driver.execute_script(f"window.open('{job_info['jd_url']}', '_blank');")
            time.sleep(5)

            logger.debug("Switching to new tab")
            driver.switch_to.window(driver.window_handles[-1])

            try:
                saved_buttons = driver.find_elements(By.CLASS_NAME, "jobs-save-button")
                if saved_buttons:
                    logger.debug("Clicking unsave button")
                    saved_buttons[-1].click()
                    time.sleep(1)
            except Exception as e:
                logger.error(f"Error unsaving job: {e}")

    # random display 10 jobs
    logger.info("Randomly selecting 10 jobs to display")
    random.shuffle(jobs)
    for job in jobs[:10]:
        logger.log(
            "DATA", f"Random job: {job['title']} at {job['company']} ({job['jd_url']})"
        )
