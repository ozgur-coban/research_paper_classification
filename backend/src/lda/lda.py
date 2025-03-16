import json
import numpy as np
from sklearn.decomposition import LatentDirichletAllocation


class LDA:
    def __init__(
        self,
        tfidf_dfs,
        num_topics,
        tfidf_vectorizer,
        count_dict=None,
        count_vectorizer=None,
        use_tfidf=True,
        save_lda_results=False,
        save_lda_path=None,
    ):
        self.num_topics = num_topics
        if use_tfidf:
            self.tfidf_dfs = tfidf_dfs
            self.vectorizer = tfidf_vectorizer

        else:
            self.count_dict = count_dict
            self.vectorizer = count_vectorizer
        self.lda = LatentDirichletAllocation(n_components=num_topics)
        self.lda_results = {}
        if save_lda_results:
            self.save_lda_path = save_lda_path

    def apply_lda_using_tfidf(self):
        for year, categories in self.tfidf_dfs.items():
            self.lda_results[year] = {}
            for category, df in categories.items():
                # Create a list of words from the dataframe
                words = df["Word"].values
                tfidf_matrix = self.vectorizer.transform([" ".join(words)])
                self.lda.fit(tfidf_matrix)
                self.lda_results[year][category] = self.lda.components_

    def apply_lda_using_countvectorizer(self):
        """Applies LDA using CountVectorizer on raw abstracts."""
        for year, categories in self.count_dict.items():
            self.lda_results[year] = {}

            for category, abstracts in categories.items():
                if not abstracts:
                    continue  # Skip empty categories

                # Convert abstracts into a document-term matrix
                dt_matrix = self.vectorizer.fit_transform(abstracts)

                # Apply LDA
                self.lda.fit(dt_matrix)

                # Store topic-word distributions
                self.lda_results[year][category] = self.lda.components_

    def display_topics(self, num_top_words=10):
        """Displays the top words for each topic."""
        feature_names = (
            self.vectorizer.get_feature_names_out()
        )  # Get words from vectorizer

        topics_result = {}

        for year, categories in self.lda_results.items():
            year_result = {}
            for category, topics in categories.items():
                category_result = []
                for topic_idx, topic in enumerate(topics):
                    top_words = [
                        feature_names[i]
                        for i in topic.argsort()[: -num_top_words - 1 : -1]
                    ]
                    category_result.append(
                        {"topic_idx": topic_idx, "top_words": top_words}
                    )
                year_result[category] = category_result
            topics_result[year] = year_result

        return topics_result

    def convert_numpy(self, obj):
        """Recursively convert NumPy arrays to lists for JSON serialization."""
        if isinstance(obj, np.ndarray):
            return obj.tolist()  # Convert NumPy arrays to lists
        elif isinstance(obj, dict):
            return {
                key: self.convert_numpy(value) for key, value in obj.items()
            }  # Recursively process dictionaries
        elif isinstance(obj, list):
            return [
                self.convert_numpy(item) for item in obj
            ]  # Recursively process lists
        else:
            return obj  # Keep other types unchanged

    def save_lda_results(self, topics_json):
        with open(self.save_lda_path, "w") as f:
            json.dump(topics_json, f)

    def run_tfidf(self):
        self.apply_lda_using_tfidf()
        topics_json = self.display_topics()
        if self.save_lda_path:
            self.save_lda_results(topics_json)
