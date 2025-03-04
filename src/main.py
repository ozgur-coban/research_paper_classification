from scrape_ops import DataScraper


def main():
    data_scraper = DataScraper(query="machine learning")
    # api_response = data_scraper.get_url_response()
    # print(api_response.decode("utf-8"))
    data_scraper.fetch_all_results(output_file="arxiv_papers.xml")


if __name__ == "__main__":
    main()
