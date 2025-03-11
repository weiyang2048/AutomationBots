# LinkedIn Job Tracker

A Python package for tracking and managing saved LinkedIn jobs. This tool helps you keep track of your saved jobs on LinkedIn, and can check for jobs that you've already applied to.

## Features

- Scrape all saved jobs from your LinkedIn account
- List job details including title, company, location, and URL
- Check saved jobs against a list of jobs you've already applied to
- Open matching jobs in new browser tabs for review
- Comprehensive logging with loguru

## Installation

### From GitHub

```bash
pip install git+https://github.com/your-username/web_crawler.git
```

### Local Development Installation

Clone the repository:

```bash
git clone https://github.com/your-username/web_crawler.git
cd web_crawler
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install in development mode:

```bash
pip install -e .
```

## Usage

### Command Line Interface

After installation, you can use the command line interface:

```bash
# List all saved jobs
linkedin-job-tracker --username your-email@example.com

# Check saved jobs against already applied jobs
linkedin-job-tracker --username your-email@example.com --action check-applied --applied-jobs-file path/to/job_applications.md
```

If you don't provide username/password, the tool will prompt you for them.

### Python API

You can also use the package in your Python code:

```python
from linkedin_job_tracker.scraper import (
    open_linkedin,
    get_all_saved_jobs,
    open_applied_jobs
)

# Log in to LinkedIn
driver = open_linkedin("your-email@example.com", "your-password")

# Get all saved jobs
jobs, driver = get_all_saved_jobs(driver)

# Print job details
for job in jobs:
    print(f"{job['title']} at {job['company']} ({job['location']})")
    print(f"URL: {job['jd_url']}")

# Check against applied jobs
open_applied_jobs(driver, jobs, "job_applications.md")

# Don't forget to close the browser
driver.quit()
```

## Logging

The package uses loguru for logging. By default, logs are:
- Displayed in the console with INFO level and colorized formatting
- Saved to a file named `linkedin_job_tracker.log` with DEBUG level
- File logs are automatically rotated when they reach 10 MB
- Old logs are retained for 1 week

You can customize the logging configuration by accessing the logger:

```python
from loguru import logger

# Change the console log level
logger.remove()  # Remove existing handlers
logger.add(sys.stderr, level="DEBUG")  # Add with new level

# Disable file logging
logger.configure(handlers=[{"sink": sys.stderr}])
```

## Applied Jobs Format

The `job_applications.md` file should be a markdown file tracking your job applications. The tool searches this file for job IDs and company names to identify matches.

## Requirements

- Python 3.6+
- Selenium 4.0.0+
- webdriver-manager 3.8.0+
- loguru 0.6.0+
- Chrome/Firefox web browser and corresponding webdriver

## License

MIT