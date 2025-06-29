# AutomationBots

A collection of powerful automation tools .

# Installation
```bash
pip install git+https://github.com/weiyang2048/AutomationBots.git
```

# CLI
```bash
automationbots --help
```

## random-folder
```bash
automationbots random-folder # "path" optional
automationbots list-folders # "path" optional
```





## 📦 Modules

### LinkedIn Job Tracker

#### Overview

The `LinkedIn Job Tracker` module automates the process of scraping saved jobs from your LinkedIn account, providing detailed job information, and cross-referencing with your application history.

#### Features

- Automatically scrapes all saved jobs from LinkedIn.
- Provides detailed job information (title, company, location, URLs).
- Cross-references saved jobs with your application history.
- Opens matching jobs in browser tabs for quick review.
- Comprehensive logging system for tracking operations.

#### Usage

**Command Line Interface**

```bash
# List all saved jobs
LinkedInTracker --username your-email@example.com

# Check against applied jobs
LinkedInTracker --username your-email@example.com --action check-applied --applied-jobs-file path/to/job_applications.md
```

**Python API**

```python
from AutomationBots.LinkedInTracker.scraper import (
    open_linkedin,
    get_all_saved_jobs,
    open_applied_jobs
)

# Initialize and login
driver = open_linkedin("your-email@example.com", "your-password")

# Fetch saved jobs
jobs, driver = get_all_saved_jobs(driver)

# Process job data
for job in jobs:
    print(f"{job['title']} at {job['company']} ({job['location']})")
    print(f"URL: {job['jd_url']}")

# Compare with applied jobs
open_applied_jobs(driver, jobs, "job_applications.md")

# Clean up
driver.quit()
```

### ArXivSearcher

#### Overview

The `ArXivSearcher` module is designed to scrape arXiv for research papers based on user input and download the PDFs.

#### Features

- Dynamic folder creation for storing downloaded PDFs.
- Cleans paper titles for use as filenames.
- Provides user feedback through message boxes for various scenarios.

#### Usage

1. Run the script:
   ```bash
   python ArXivSearcher.py
   ```
2. Enter the search query when prompted in the dialog box.
3. The script will download the PDFs of the search results into a folder in your Downloads directory.

## 📝 Logging System

The application uses `loguru` for robust logging with console and file outputs, automatic log rotation, and retention.

## 📜 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

