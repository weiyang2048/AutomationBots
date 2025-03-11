#!/usr/bin/env python3
"""
Example script demonstrating how to use the LinkedIn Job Tracker package.
"""
import os
import argparse
from linkedin_job_tracker.scraper import (
    open_linkedin,
    get_all_saved_jobs,
    open_applied_jobs
)


def main():
    """Main function to demonstrate package usage."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Example script for LinkedIn Job Tracker"
    )
    parser.add_argument("--username", required=True, help="LinkedIn username/email")
    parser.add_argument("--password", required=True, help="LinkedIn password")
    parser.add_argument(
        "--output-file",
        default="saved_jobs.csv",
        help="Output CSV file to save job listings"
    )
    parser.add_argument(
        "--applied-jobs-file",
        default="job_applications.md",
        help="Path to markdown file with already applied jobs"
    )
    
    args = parser.parse_args()
    
    try:
        # Login to LinkedIn
        print("Logging in to LinkedIn...")
        driver = open_linkedin(args.username, args.password)
        
        # Get all saved jobs
        print("Retrieving saved jobs...")
        jobs, driver = get_all_saved_jobs(driver)
        
        # Export jobs to CSV
        print(f"Exporting {len(jobs)} jobs to {args.output_file}...")
        export_to_csv(jobs, args.output_file)
        
        # If applied jobs file exists, check for applied jobs
        if os.path.exists(args.applied_jobs_file):
            print("Checking for already applied jobs...")
            open_applied_jobs(driver, jobs, args.applied_jobs_file)
        else:
            print(f"Applied jobs file {args.applied_jobs_file} not found. Skipping check.")
        
        print("Done!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()


def export_to_csv(jobs, output_file):
    """Export job listings to a CSV file."""
    import csv
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['title', 'company', 'location', 'jd_url', 'job_id']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for job in jobs:
            writer.writerow({k: job.get(k, '') for k in fieldnames})


if __name__ == "__main__":
    main() 