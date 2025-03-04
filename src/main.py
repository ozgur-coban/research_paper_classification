from scrape_ops import DataScraper


def main():
    data_scraper = DataScraper(query="cat:cs machine learning")
    data_scraper.fetch_all_results(output_file="../data/arxiv_test.xml")


if __name__ == "__main__":
    main()
