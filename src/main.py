import numpy as np
import pandas as pd
from scrape_ops import DataScraper, JsonExtractor, GetSample
from eda import EDA
from lda import Preprocessing, LDA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer


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
    # eda.plot_tfidf_heatmap()
    # eda.run_test()

    sample_object = GetSample(
        use_existing_sample=True, sample_path="./data/sample_filtered_cs_papers.json"
    )
    sample = sample_object.get_sample()
    eda = EDA(
        use_already_existing_sample=True,
        sample=sample,
        json_save_path="./data/category_distribution.json",
    )
    # eda.save_category_distribution_as_json()
    # eda.save_year_distribution_as_json()
    # eda.save_abstract_length_counts_as_json()
    eda.save_tfidf_distribution_as_json()
    return
    tfidf_vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    # preprocessing_save = Preprocessing(
    #     sample,
    #     preprocess_abstracts=True,
    #     abstract_save_path="./data/normalized_abstracts.json",
    # )
    # preprocessing_save.save_preprocessed_abstracts()

    preprocessing = Preprocessing(
        sample,
        normalized_abstract_path="./data/normalized_abstracts.json",
        vectorizer=tfidf_vectorizer,
    )

    # preprocessing.save_preprocessed_abstracts()
    # papers_by_year_category = preprocessing.divide_papers_by_year_and_category()
    # categories = set()

    # # Iterate through the dictionary to get the categories
    # for year, category_dict in abstracts_by_year_category.items():
    #     for category in category_dict:
    #         categories.add(category)
    # print(categories)
    # abstracts_by_year_category = preprocessing.get_abstracts_by_year_category(
    #     papers_by_year_category
    # )
    category_tfidf_dfs = preprocessing.get_top_tfidf_words_by_category()

    lda = LDA(
        category_tfidf_dfs,
        num_topics=1,
        tfidf_vectorizer=tfidf_vectorizer,
        use_tfidf=True,
        save_lda_results=True,
        save_lda_path="./data/lda_results.json",
    )
    lda.test_tfidf()


if __name__ == "__main__":
    main()
