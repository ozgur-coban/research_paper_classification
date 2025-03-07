from scrape_ops import DataScraper, JsonExtractor, GetSample
from eda import EDA
from lda import Preprocessing


def main():
    # eda = EDA(
    #     file_path="./data/filtered_cs_papers.json",
    #     sample_output_path="./data/sample_filtered_cs_papers.json",
    #     sample_size=9000,
    #     use_already_existing_sample=True,
    #     sample_path="./data/sample_filtered_cs_papers.json",
    # )
    # eda.save_sample_to_file()
    # eda.run_category_distribution()
    # eda.run_year_distribution()
    # yearly_tfidf_dfs = eda.get_top_tfidf_words_per_year()
    # eda.plot_tfidf_heatmap(yearly_tfidf_dfs)
    # eda.run_test()

    sample_object = GetSample(
        use_existing_sample=True, sample_path="./data/sample_filtered_cs_papers.json"
    )
    sample = sample_object.get_sample()
    preprocessing = Preprocessing(sample)
    preprocessing.test_sample()


if __name__ == "__main__":
    main()
