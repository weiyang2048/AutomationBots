from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="linkedin_job_tracker",
    version="0.1.0",
    author="Wei Yang",
    author_email="weiyang2048@gmail.com",
    description="A tool to track and manage saved LinkedIn jobs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/web_crawler",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "selenium>=4.0.0",
        "webdriver-manager>=3.8.0",
        "loguru>=0.6.0",
    ],
    entry_points={
        "console_scripts": [
            "linkedin-job-tracker=linkedin_job_tracker.cli:main",
        ],
    },
) 