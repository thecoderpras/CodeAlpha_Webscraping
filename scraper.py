import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "http://quotes.toscrape.com/"

def scrape_quotes():
    page_url = BASE_URL
    all_data = []

    while page_url:
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, "html.parser")

        quotes = soup.find_all("div", class_="quote")

        for quote in quotes:
            text = quote.find("span", class_="text").text
            author = quote.find("small", class_="author").text
            all_data.append([text, author])

        next_button = soup.find("li", class_="next")
        if next_button:
            next_page = next_button.find("a")["href"]
            page_url = BASE_URL + next_page
        else:
            page_url = None

    return all_data


def save_to_csv(data):
    with open("quotes_dataset.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Quote", "Author"])
        writer.writerows(data)


if __name__ == "__main__":
    data = scrape_quotes()
    save_to_csv(data)
    print("Scraping completed. Dataset saved as quotes_dataset.csv")