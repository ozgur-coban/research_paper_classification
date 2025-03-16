import json
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from config import CATEGORY_LIST


class EDA:
    def __init__(
        self,
        file_path=None,
        sample_output_path=None,
        sample_size=100,
        use_already_existing_sample=False,
        sample_path=None,
        sample=None,
        json_save_path=None,
    ):
        self.file_path = file_path
        self.sample_size = sample_size
        self.use_already_existing_sample = use_already_existing_sample
        self.json_save_path = json_save_path
        self.category_list = [
            "cs.AI",
            "cs.AR",
            "cs.CC",
            "cs.CE",
            "cs.CG",
            "cs.CL",
            "cs.CR",
            "cs.CV",
            "cs.CY",
            "cs.DB",
            "cs.DC",
            "cs.DL",
            "cs.DM",
            "cs.DS",
            "cs.ET",
            "cs.FL",
            "cs.GL",
            "cs.GR",
            "cs.GT",
            "cs.HC",
            "cs.IR",
            "cs.IT",
            "cs.LG",
            "cs.LO",
            "cs.MA",
            "cs.MM",
            "cs.MS",
            "cs.NA",
            "cs.NE",
            "cs.NI",
            "cs.OH",
            "cs.OS",
            "cs.PF",
            "cs.PL",
            "cs.RO",
            "cs.SC",
            "cs.SD",
            "cs.SE",
            "cs.SI",
            "cs.SY",
            "econ.EM",
            "econ.GN",
            "econ.TH",
            "eess.AS",
            "eess.IV",
            "eess.SP",
            "eess.SY",
            "math.AC",
            "math.AG",
            "math.AP",
            "math.AT",
            "math.CA",
            "math.CO",
            "math.CT",
            "math.CV",
            "math.DG",
            "math.DS",
            "math.FA",
            "math.GM",
            "math.GN",
            "math.GR",
            "math.GT",
            "math.HO",
            "math.IT",
            "math.KT",
            "math.LO",
            "math.MG",
            "math.MP",
            "math.NA",
            "math.NT",
            "math.OA",
            "math.OC",
            "math.PR",
            "math.QA",
            "math.RA",
            "math.RT",
            "math.SG",
            "math.SP",
            "math.ST",
            "astro-ph.CO",
            "astro-ph.EP",
            "astro-ph.GA",
            "astro-ph.HE",
            "astro-ph.IM",
            "astro-ph.SR",
            "cond-mat.dis",
            "cond-mat.mes",
            "cond-mat.mtrl",
            "cond-mat.other",
            "cond-mat.quant",
            "cond-mat.soft",
            "cond-mat.stat",
            "cond-mat.str",
            "cond-mat.supr",
            "nlin.AO",
            "nlin.CD",
            "nlin.CG",
            "nlin.PS",
            "nlin.SI",
            "physics.acc",
            "physics.ao",
            "physics.app",
            "physics.atm",
            "physics.atom",
            "physics.bio",
            "physics.chem",
            "physics.class",
            "physics.comp",
            "physics.data",
            "physics.ed",
            "physics.flu",
            "physics.gen",
            "physics.geo",
            "physics.hist",
            "physics.ins",
            "physics.med",
            "physics.optics",
            "physics.plasm",
            "physics.pop",
            "physics.soc",
            "physics.space",
            "q-bio.BM",
            "q-bio.CB",
            "q-bio.GN",
            "q-bio.MN",
            "q-bio.NC",
            "q-bio.OT",
            "q-bio.PE",
            "q-bio.QM",
            "q-bio.SC",
            "q-bio.TO",
            "q-fin.CP",
            "q-fin.EC",
            "q-fin.GN",
            "q-fin.MF",
            "q-fin.PM",
            "q-fin.PR",
            "q-fin.RM",
            "q-fin.ST",
            "q-fin.TR",
            "stat.AP",
            "stat.CO",
            "stat.ME",
            "stat.ML",
            "stat.OT",
            "stat.TH",
        ]
        if use_already_existing_sample:
            self.sample_path = sample_path
            self.sample = sample
        else:
            self.sample_output_path = sample_output_path

    # Method to load and sample the data
    def load_sample(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)  # Loads entire json file
            sample = random.sample(
                data,
                min(self.sample_size, len(data)),
            )
            return sample

    def save_sample_to_file(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            sample = random.sample(
                data, min(self.sample_size, len(data))
            )  # Take random sample
        with open(self.sample_output_path, "w", encoding="utf-8") as f:
            json.dump(sample, f, ensure_ascii=False, indent=2)
        print(f"Sample saved to {self.sample_output_path}")

    def get_sample(self):
        if self.sample_path:
            with open(self.sample_path, "r", encoding="utf-8") as f:
                sample = json.load(f)
                return sample
        else:
            return self.sample

    def get_sample_ids(self):
        indexed_sample = {}

        sample = self.sample
        for paper in sample:
            indexed_sample[paper.get("id")] = paper
        return indexed_sample

    def save_json_to_file(self, json_data):
        data = json.loads(json_data)
        with open(self.json_save_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Sample saved to {self.json_save_path}")

    # Extract CS subcategories from the sampled data
    def get_category_distribution(self, sample):
        category_counts = {
            category: 0 for category in self.category_list
        }  # Initialize category counts

        for paper in sample:
            categories = paper.get(
                "categories", ""
            ).split()  # Split categories (some have multiple)
            for category in categories:
                if (
                    category in self.category_list
                ):  # Check if category is in predefined list
                    category_counts[category] += 1

        return category_counts

    def get_category_distribution_as_json(self, category_counts, top_n=30):
        # Sort the category counts and get the top N
        most_common = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[
            :top_n
        ]

        # Extract labels and values
        labels, values = zip(*most_common)

        # Prepare data as a dictionary
        data = {"CS Subcategories": list(labels), "Number of Papers": list(values)}

        # Convert to JSON format
        return json.dumps(data)

    # Plot the top CS subcategories
    def plot_category_distribution(self, category_counts, top_n=30):
        most_common = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[
            :top_n
        ]

        labels, values = zip(*most_common)

        df = pd.DataFrame({"CS Subcategory": labels, "Number of Papers": values})

        plt.figure(figsize=(12, 6))
        sns.barplot(
            x="CS Subcategory", y="Number of Papers", data=df, palette="Blues_d"
        )
        plt.xticks(rotation=45, ha="right")
        plt.xlabel("CS Subcategories")
        plt.ylabel("Number of Papers")
        plt.title(f"Top {top_n} CS Subcategories in ArXiv Dataset")
        plt.show()

    def get_year_published(self, sample):
        year_counts = {}
        for paper in sample:
            created_date = paper.get("versions")[0].get("created")
            year = (datetime.strptime(created_date, "%a, %d %b %Y %H:%M:%S %Z")).year
            year_counts[year] = year_counts.get(year, 0) + 1
        return year_counts

    def get_year_published_as_json(self, year_counts):
        data = {
            "Years": list(year_counts.keys()),
            "Year Counts": list(year_counts.values()),
        }
        return json.dumps(data)

    def plot_year_distribution(self, year_counts):
        df = pd.DataFrame(
            list(year_counts.items()), columns=["Year", "Number of Articles"]
        )
        plt.figure(figsize=(12, 6))
        sns.barplot(x="Year", y="Number of Articles", data=df)

        plt.xlabel("Publication Year")
        plt.ylabel("Number of Articles")
        plt.title("Histogram of Articles Published by Year")
        plt.xticks(rotation=45)
        plt.show()

    def get_abstracts(self, sample):
        paper_abstracts = {}
        for paper in sample:
            id = paper.get("id")
            abstract = paper.get("abstract")
            paper_abstracts[id] = abstract
        return paper_abstracts

    def analyze_abstract_lengths(self, abstracts):
        lengths = [
            len(abstract.split()) for abstract in abstracts.values()
        ]  # Word count
        char_lengths = [
            len(abstract) for abstract in abstracts.values()
        ]  # Character count

        df = pd.DataFrame({"Word Count": lengths, "Character Count": char_lengths})

        print(df.describe())  # Summary statistics
        # Plot histogram of word counts
        plt.figure(figsize=(10, 5))
        sns.histplot(df["Word Count"], bins=30, kde=True)
        plt.xlabel("Word Count per Abstract")
        plt.ylabel("Number of Papers")
        plt.title("Distribution of Abstract Word Counts")
        plt.show()

        return df

    def get_abstract_lengths_as_json(self, abstracts):
        lengths = [len(abstract.split()) for abstract in abstracts.values()]
        data = {"Word Counts": lengths}
        return json.dumps(data)

    def generate_word_cloud(self, abstracts):
        # Join all abstracts into one large string
        all_abstracts = " ".join(abstracts.values())

        # Generate a word cloud
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
            all_abstracts
        )

        # Display the word cloud
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()

    def get_top_tfidf_words_as_df(self, abstracts, top_n=10):
        vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
        tfidf_matrix = vectorizer.fit_transform(abstracts)
        feature_names = np.array(vectorizer.get_feature_names_out())
        avg_tfidf_scores = np.asarray(tfidf_matrix.mean(axis=0)).flatten()

        top_indices = avg_tfidf_scores.argsort()[-top_n:][::-1]
        top_words = feature_names[top_indices]
        top_scores = avg_tfidf_scores[top_indices]

        return pd.DataFrame({"Word": top_words, "TF-IDF Score": top_scores})

    def get_top_tfidf_words(self, abstracts, top_n=10):
        vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
        tfidf_matrix = vectorizer.fit_transform(abstracts)
        feature_names = np.array(vectorizer.get_feature_names_out())
        avg_tfidf_scores = np.asarray(tfidf_matrix.mean(axis=0)).flatten()

        top_indices = avg_tfidf_scores.argsort()[-top_n:][::-1]
        top_words = feature_names[top_indices]
        top_scores = avg_tfidf_scores[top_indices]

        return {"Word": top_words, "TF-IDF Score": top_scores}

    def divide_papers_into_years(self, sample):
        papers_per_years = {}
        for paper in sample:
            created_date = paper.get("versions")[0].get("created")
            year = (datetime.strptime(created_date, "%a, %d %b %Y %H:%M:%S %Z")).year
            paper_id = paper.get("id")

            if year not in papers_per_years:
                papers_per_years[year] = []  # Initialize list

            papers_per_years[year].append(paper_id)  # Add ID to the list

        return papers_per_years

    def get_abstract_from_id(self, sample, ids):
        abstracts = []
        # print(sample.keys())
        for id in ids:
            abstract = sample.get(id).get("abstract")
            abstracts.append(abstract)
        return abstracts

    def get_top_tfidf_words_per_year(self):
        papers_per_years = self.divide_papers_into_years(sample=self.sample)
        yearly_abstracts = {}
        for year in papers_per_years.keys():
            paper_ids = papers_per_years[year]
            yearly_abstracts[year] = self.get_abstract_from_id(
                sample=self.get_sample_ids(), ids=paper_ids
            )
        yearly_tfidf_dfs = {}
        for year, abstracts in yearly_abstracts.items():
            df = self.get_top_tfidf_words_as_df(abstracts=abstracts, top_n=10)
            yearly_tfidf_dfs[year] = df
        return yearly_tfidf_dfs

    # def get_top_tfidf_words_per_year_as_json(self):
    #     papers_per_years = self.divide_papers_into_years(sample=self.sample)
    #     yearly_abstracts = {}
    #     for year in papers_per_years.keys():
    #         paper_ids = papers_per_years[year]
    #         yearly_abstracts[year] = self.get_abstract_from_id(
    #             sample=self.get_sample_ids(), ids=paper_ids
    #         )
    #     yearly_tfidfs = {}
    #     for year, abstracts in yearly_abstracts.items():
    #         df = self.get_top_tfidf_words_as_df(abstracts=abstracts, top_n=10)

    #         yearly_tfidfs[year] = df.to_dict(orient="records")
    #     data = yearly_tfidfs
    #     return json.dumps(data, indent=2)
    def get_top_tfidf_words_per_year_as_json(self):
        papers_per_years = self.divide_papers_into_years(sample=self.sample)

        # Create lists for Plotly heatmap
        years_list = []
        words_list = []
        scores_list = []

        for year in papers_per_years.keys():
            paper_ids = papers_per_years[year]
            abstracts = self.get_abstract_from_id(
                sample=self.get_sample_ids(), ids=paper_ids
            )

            # Get TF-IDF DataFrame
            df = self.get_top_tfidf_words_as_df(abstracts=abstracts, top_n=20)

            # Append to lists
            years_list.extend([year] * len(df))  # Repeat 'year' for each word
            words_list.extend(df["Word"].tolist())  # Extract words
            scores_list.extend(df["TF-IDF Score"].tolist())  # Extract scores

        # Create JSON structure
        heatmap_data = {
            "Years": years_list,
            "Words": words_list,
            "TF-IDF Scores": scores_list,
        }

        return json.dumps(heatmap_data, indent=2)

    def run_category_distribution(self):
        if self.use_already_existing_sample:
            sample_data = self.get_sample()
        else:
            sample_data = self.load_sample()
        category_counts = self.get_category_distribution(sample_data)
        self.plot_category_distribution(category_counts)

    def save_category_distribution_as_json(self):
        if self.use_already_existing_sample:
            sample_data = self.get_sample()
        else:
            sample_data = self.load_sample()
        category_counts = self.get_category_distribution(sample_data)
        self.json_save_path = "./data/category_distribution.json"
        self.save_json_to_file(
            json_data=self.get_category_distribution_as_json(
                category_counts=category_counts
            )
        )

    def run_year_distribution(self):
        if self.use_already_existing_sample:
            sample_data = self.get_sample()
        else:
            sample_data = self.load_sample()
        year_counts = self.get_year_published(sample_data)
        self.plot_year_distribution(year_counts)

    def save_year_distribution_as_json(self):
        year_counts = self.get_year_published(self.sample)
        self.json_save_path = "./data/year_distribution.json"
        self.save_json_to_file(self.get_year_published_as_json(year_counts=year_counts))

    def save_abstract_length_counts_as_json(self):
        abstracts = self.get_abstracts(self.sample)

        self.json_save_path = "./data/abstract_length_distribution.json"
        self.save_json_to_file(
            json_data=self.get_abstract_lengths_as_json(abstracts=abstracts)
        )

    def plot_tfidf_heatmap(self, top_n=10):
        """
        Creates a heatmap showing the evolution of top TF-IDF words over time.

        Parameters:
        yearly_tfidf_dfs: dict -> {year: dataframe_of_tfidf_words}
        top_n: int -> Number of top words to consider

        """
        yearly_tfidf_dfs = self.get_top_tfidf_words_as_df()
        # Collect all unique top words across years
        all_words = set()
        for df in yearly_tfidf_dfs.values():
            all_words.update(df["Word"].head(top_n))

        # Create a DataFrame for heatmap
        heatmap_data = pd.DataFrame(index=sorted(all_words))

        for year, df in yearly_tfidf_dfs.items():
            word_scores = df.set_index("Word")["TF-IDF Score"]
            heatmap_data[year] = word_scores

        # Fill missing values with 0 (some words might not appear in every year)
        heatmap_data = heatmap_data.fillna(0)

        # Plot heatmap
        plt.figure(figsize=(12, 6))
        sns.heatmap(heatmap_data, cmap="Blues", annot=False, linewidths=0.5)
        plt.xlabel("Year")
        plt.ylabel("Top Words")
        plt.title("TF-IDF Score Evolution of Keywords Over Time")
        plt.show()

    def save_tfidf_distribution_as_json(self):
        yearly_tfidfs = self.get_top_tfidf_words_per_year_as_json()
        self.json_save_path = "./data/tfidf_distribution.json"
        self.save_json_to_file(json_data=yearly_tfidfs)

    def run_test(self):
        if self.use_already_existing_sample:
            sample_data = self.get_sample()
        else:
            sample_data = self.load_sample()
        # abstracts = self.get_abstracts(sample_data)
        # self.analyze_abstract_lengths(abstracts)
        # self.generate_word_cloud(abstracts)
        # print(self.get_top_tfidf_words_as_df(abstracts))
        print(sample_data)
