from scrape_ops import DataScraper, JsonExtractor
from eda import EDA


def main():
    # data_scraper = DataScraper(query="cat:cs machine learning")
    # data_scraper.fetch_all_results(output_file="../data/arxiv_test.xml")

    # json_extractor = JsonExtractor(
    #     input_file="./data/arxiv-metadata-oai-snapshot.json",
    #     output_file="./data/filtered_cs_papers.json",
    # )
    # json_extractor.filter_json_by_category(category_prefix="cs.")
    eda = EDA(
        file_path="./data/filtered_cs_papers.json",
        sample_output_path="./data/sample_filtered_cs_papers.json",
        sample_size=9000,
        use_already_existing_sample=True,
        sample_path="./data/sample_filtered_cs_papers.json",
    )
    # eda.save_sample_to_file()
    # eda.run_category_distribution()
    # eda.run_year_distribution()
    eda.run_test()


if __name__ == "__main__":
    main()
