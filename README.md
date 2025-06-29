# AutomationBots

A comprehensive collection of automation tools designed to streamline various tasks including job tracking, research paper discovery, and file management.

## Table of Contents

- [AutomationBots](#automationbots)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Command Line Interface](#command-line-interface)
  - [Modules](#modules)
    - [LinkedIn Job Tracker](#linkedin-job-tracker)
      - [Overview](#overview)
      - [Features](#features)
      - [Usage](#usage)
    - [ArXiv Searcher](#arxiv-searcher)
      - [Overview](#overview-1)
      - [Features](#features-1)
      - [Usage](#usage-1)
    - [Random Folder Opener](#random-folder-opener)
      - [Overview](#overview-2)
      - [Usage](#usage-2)
  - [Logging System](#logging-system)
  - [License](#license)
  - [Contributing](#contributing)

## Installation

Install the package directly from GitHub:

```bash
pip install git+https://github.com/weiyang2048/AutomationBots.git
```

## Command Line Interface

Access the main CLI interface:

```bash
automationbots --help
```

## Modules

### LinkedIn Job Tracker

#### Overview

The LinkedIn Job Tracker module automates the process of scraping saved jobs from your LinkedIn account, providing detailed job information, and cross-referencing with your application history.

#### Features

- Automated scraping of all saved jobs from LinkedIn
- Detailed job information extraction (title, company, location, URLs)
- Cross-referencing saved jobs with application history
- Browser tab automation for quick job review
- Comprehensive logging system for operation tracking

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

### ArXiv Searcher

#### Overview

The ArXiv Searcher module is designed to scrape arXiv for research papers based on user input and download the PDFs automatically.

#### Features

- Dynamic folder creation for organized PDF storage
- Automatic paper title cleaning for filename compatibility
- User-friendly dialog-based interface
- Batch PDF downloading capabilities

#### Usage

1. Run the script:
   ```bash
   python ArXivSearcher.py
   ```
2. Enter the search query when prompted in the dialog box
3. The script will download the PDFs of the search results into a folder in your Downloads directory

### Random Folder Opener

#### Overview

A utility module for managing and opening random folders from a specified directory.

#### Usage

```bash
# Open a random folder from current directory
automationbots random-folder

# Open a random folder from specified path
automationbots random-folder "path"

# List all folders in current directory
automationbots list-folders

# List all folders in specified path
automationbots list-folders "path"
```

## Logging System

The application uses `loguru` for robust logging with the following features:

- Console and file outputs
- Automatic log rotation
- Configurable retention policies
- Structured logging for better debugging

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

