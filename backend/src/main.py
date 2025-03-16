from scrape_ops import GetSample
from eda import EDA
from lda import Preprocessing, LDA
from sklearn.feature_extraction.text import TfidfVectorizer


def main():
    # Step 1: Get Sample Data
    sample_object = GetSample(
        use_existing_sample=True, sample_path="./data/sample_filtered_cs_papers.json"
    )
    sample = sample_object.get_sample()

    # Step 2: Perform Exploratory Data Analysis (EDA)
    eda = EDA(
        use_already_existing_sample=True,
        sample=sample,
        json_save_path="./data/category_distribution.json",
    )
    # Uncomment the following lines as needed to save EDA results
    # eda.save_category_distribution_as_json()
    # eda.save_year_distribution_as_json()
    # eda.save_abstract_length_counts_as_json()
    # eda.save_tfidf_distribution_as_json()

    # Step 3: Preprocess Data (e.g., normalize abstracts)
    tfidf_vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    preprocessing = Preprocessing(
        sample,
        normalized_abstract_path="./data/normalized_abstracts.json",
        vectorizer=tfidf_vectorizer,
    )
    # Uncomment the following line to preprocess and save abstracts
    # preprocessing.save_preprocessed_abstracts()

    # Step 4: Get Top TF-IDF Words by Category
    category_tfidf_dfs = preprocessing.get_top_tfidf_words_by_category()

    # Step 5: Apply Latent Dirichlet Allocation (LDA)
    lda = LDA(
        category_tfidf_dfs,
        num_topics=1,
        tfidf_vectorizer=tfidf_vectorizer,
        use_tfidf=True,
        save_lda_results=True,
        save_lda_path="./data/lda_results.json",
    )
    lda.run_tfidf()  # You might call this method to check your LDA results


if __name__ == "__main__":
    main()
