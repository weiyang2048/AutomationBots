"""
Command-line interface for LinkedIn Job Tracker.
"""

import argparse
import os
import getpass
from linkedin_job_tracker.scraper import (
    open_linkedin,
    go_to_saved_jobs,
    get_all_saved_jobs,
    open_applied_jobs,
)


def main():
    """Entry point for the command-line interface."""
    parser = argparse.ArgumentParser(description="Track and manage LinkedIn saved jobs")
    parser.add_argument(
        "--username",
        default=os.getenv("robinhood_user"),
        help="LinkedIn username/email (will prompt if not provided)",
    )
    parser.add_argument(
        "--password",
        default=os.getenv("robinhood_pass"),
        help="LinkedIn password (will prompt if not provided)",
    )
    parser.add_argument(
        "--applied-jobs-file",
        default="job_applications.md",
        help="Path to the markdown file tracking applied jobs",
    )
    parser.add_argument(
        "--action",
        choices=["list", "check-applied"],
        default="check-applied",
        help="Action to perform: list all saved jobs or check already applied jobs",
    )

    args = parser.parse_args()

    # Prompt for credentials if not provided
    username = args.username or input("LinkedIn username/email: ")
    password = args.password or getpass.getpass("LinkedIn password: ")

    # Check if applied-jobs-file exists
    if args.action == "check-applied" and not os.path.exists(args.applied_jobs_file):
        print(f"Error: Applied jobs file '{args.applied_jobs_file}' not found.")
        return 1

    try:
        # Login to LinkedIn
        driver = open_linkedin(username, password)

        # Get all saved jobs
        jobs, driver = get_all_saved_jobs(driver)

        # Perform requested action
        if args.action == "list":
            print(f"Found {len(jobs)} saved jobs:")
            for job in jobs:
                print(f"{job['title']} at {job['company']} ({job['location']})")
                print(f"URL: {job['jd_url']}")
                print("-" * 80)
        elif args.action == "check-applied":
            print("Checking for already applied jobs...")
            open_applied_jobs(driver, jobs, args.applied_jobs_file)

        # wait for user input to close the browser
        input("Press Enter to close the browser...")
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to close the browser...")
    # finally:
        # if "driver" in locals():
            # driver.quit()


if __name__ == "__main__":
    main()
