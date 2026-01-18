



import csv
from bs4 import BeautifulSoup

HTML_PATH = "../data/raw_data/web_data.html"
MARKET_CSV_PATH = "../data/processed_data/market_data.csv"
NEWS_CSV_PATH = "../data/processed_data/news_data.csv"


def read_html_file(filepath: str) -> str:
    print("Reading HTML data")
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def extract_market_data(soup: BeautifulSoup) -> list[dict]:
    print("Filtering market banner fields")
    market_data = []

    market_cards = soup.find_all("div", class_="marketCard")

    for card in market_cards:
        symbol = card.find("span", class_="marketCard-symbol")
        position = card.find("span", class_="marketCard-stockPosition")
        change_pct = card.find("span", class_="marketCard-changePct")

        market_data.append({
            "marketCard_symbol": symbol.get_text(strip=True) if symbol else None,
            "marketCard_stockPosition": position.get_text(strip=True) if position else None,
            "marketCardchangePct": change_pct.get_text(strip=True) if change_pct else None
        })

    print(f"Extracted {len(market_data)} market records")
    return market_data


def extract_latest_news(soup: BeautifulSoup) -> list[dict]:
    print("Filtering latest news fields")
    latest_news = []

    news_items = soup.find_all("li", class_="LatestNews-item")

    for item in news_items:
        timestamp = item.find("time")
        title_tag = item.find("a")

        latest_news.append({
            "LatestNews_timestamp": timestamp.get_text(strip=True) if timestamp else None,
            "title": title_tag.get_text(strip=True) if title_tag else None,
            "link": title_tag["href"] if title_tag and title_tag.has_attr("href") else None
        })

    print(f"Extracted {len(latest_news)} news records")
    return latest_news


def write_csv(filepath: str, data: list[dict]) -> None:
    if not data:
        print(f"No data to write for {filepath}")
        return

    print(f"Storing data into {filepath}...")
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print("CSV created successfully")


def main():
    html = read_html_file(HTML_PATH)
    soup = BeautifulSoup(html, "html.parser")

    market_data = extract_market_data(soup)
    news_data = extract_latest_news(soup)

    write_csv(MARKET_CSV_PATH, market_data)
    write_csv(NEWS_CSV_PATH, news_data)

    print("Data filtering and storage completed.")


if __name__ == "__main__":
    main()

