from datetime import datetime
from bs4 import BeautifulSoup
import re
from tkinter import simpledialog, messagebox  # pop-up window for user input
import os
import requests


def downloadpath(topic, type):
    """
    Create a folder to store the downloaded files based on the topic and type.

    Parameters:
    topic (str): The topic of the files.
    type (str): The type of files.

    Returns:
    str: The path to the created folder.
    """
    folder_path = os.path.join(os.path.expanduser("~"), "Downloads", f"{type}_{topic}")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    return folder_path


def titlecleaner(title):
    """
    Clean the title by removing line breaks, leading/trailing spaces, and special characters.

    Parameters:
    title (str): The title to be cleaned.

    Returns:
    str: The cleaned title.
    """
    title = title.replace("\n", "").strip()
    return re.sub(r"\W+", " ", title)


def scraper_arxiv():
    """
    Scrape arXiv for papers based on user input and download the PDFs.
    """
    inquiry = simpledialog.askstring(
        title="Arxiv Scrapper", prompt="What do you want to scrape?"
    )

    if inquiry is None:
        messagebox.showinfo("Info", "No input provided. Exiting.")
        return

    time_str = datetime.now().strftime("%Y-%m-%d-%H")
    folder_path = downloadpath(time_str, "arxiv")

    url = f"https://arxiv.org/search/?query={'+'.join(inquiry.split())}&searchtype=all&abstracts=show&order=-announced_date_first&size=25"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to retrieve data: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all("li", class_="arxiv-result")

    if not results:
        messagebox.showinfo("Info", "No results found.")
        return

    for result in results:
        try:
            # Get a valid file name
            title = titlecleaner(result.find("p", class_="title is-5 mathjax").text)
            link = result.find("a", href=lambda href: href and "pdf" in href)["href"]
            filename = os.path.join(folder_path, f"{title}.pdf")
            with open(filename, "wb") as f:
                print(f"Downloading {title} from {link} to {filename}")
                f.write(requests.get(link).content)
        except Exception as e:
            print(f"Failed to download {title}: {e}")


def main():
    scraper_arxiv()


if __name__ == "__main__":
    main()
    input("Press Enter to continue...")
