# Web Crawler Automation Tools

A collection of powerful automation tools for web scraping and data collection, with a focus on LinkedIn job tracking.

## 🌟 Features

### LinkedIn Job Tracker
- 📋 Automatically scrapes all saved jobs from your LinkedIn account
- 📊 Provides detailed job information (title, company, location, URLs)
- ✅ Cross-references saved jobs with your application history
- 🔗 Opens matching jobs in browser tabs for quick review
- 📝 Comprehensive logging system for tracking operations

## 🚀 Getting Started

### Prerequisites
- Python 3.6 or higher
- Chrome or Firefox web browser
- Internet connection

### Installation

**Option 1: Install from GitHub**
```bash
pip install git+https://github.com/weiyang2048/AutomationBots.git
```

**Option 2: Local Development Setup**
```bash
# Clone the repository
git clone https://github.com/weiyang2048/AutomationBots.git
cd AutomationBots

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## 💻 Usage

### Command Line Interface

```bash
# List all saved jobs
LinkedInTracker --username your-email@example.com

# Check against applied jobs
LinkedInTracker --username your-email@example.com --action check-applied --applied-jobs-file path/to/job_applications.md
```

Note: If credentials are not provided, you'll be prompted to enter them securely.

### Python API

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

## 📝 Logging System

The application uses loguru for robust logging with the following default configuration:

- Console output: INFO level with color formatting
- File output: DEBUG level in `automationbots.log`
- Automatic log rotation at 10MB
- One-week log retention

### Customizing Logs

```python
from loguru import logger
import sys

# Adjust console logging level
logger.remove()
logger.add(sys.stderr, level="DEBUG")

# Disable file logging
logger.configure(handlers=[{"sink": sys.stderr}])
```

## 📄 Job Applications Tracking

Create a markdown file (`job_applications.md`) to track your job applications. The tool will search this file for:
- Job IDs
- Company names
- Application status

## 📦 Dependencies

- Selenium (≥4.0.0)
- webdriver-manager (≥3.8.0)
- loguru (≥0.6.0)
- Chrome/Firefox WebDriver

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.