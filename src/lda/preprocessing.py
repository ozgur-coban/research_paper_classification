import numpy as np
import pandas as pd
import spacy
import nltk
from nltk.corpus import stopwords
import string
import re
import json
from datetime import datetime


class Preprocessing:
    def __init__(
        self,
        sample,
        vectorizer=None,
        abstract_save_path="./data/normalized_abstracts.json",
        preprocess_abstracts=False,
        normalized_abstract_path=None,
    ):
        self.sample = sample
        # nltk.download("stopwords")
        self.nlp = spacy.load(
            "en_core_web_sm", disable=["ner", "parser"]
        )  # Only keep tokenization
        self.vectorizer = vectorizer
        self.preprocess_abstracts = preprocess_abstracts
        if self.preprocess_abstracts:
            self.abstract_save_path = abstract_save_path
        else:
            self.normalized_abstract_path = normalized_abstract_path
        self.category_list = self.category_list = [
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

    def divide_papers_into_years(self):
        papers_per_year = {}
        for paper in self.sample:
            created_date = paper.get("versions")[0].get("created")
            year = (datetime.strptime(created_date, "%a, %d %b %Y %H:%M:%S %Z")).year
            paper_id = paper.get("id")

            if year not in papers_per_year:
                papers_per_year[year] = []  # Initialize list

            papers_per_year[year].append(paper_id)  # Add ID to the list

        return papers_per_year

    def divide_papers_into_categories(self):
        papers_per_category = {category: [] for category in self.category_list}
        for paper in self.sample:
            paper_id = paper.get("id")
            categories = paper.get(
                "categories", ""
            ).split()  # Split categories (some have multiple)
            for category in categories:
                if category in self.category_list:
                    papers_per_category[category].append(paper_id)
        return papers_per_category

    def divide_papers_by_year_and_category(self):
        papers_per_year = self.divide_papers_into_years()  # Get papers grouped by year
        papers_per_category = (
            self.divide_papers_into_categories()
        )  # Get papers grouped by category

        papers_by_year_category = {}

        for year, paper_ids in papers_per_year.items():
            papers_by_year_category[year] = {
                category: [] for category in self.category_list
            }

            for category in self.category_list:
                # Find papers that belong to both the current year and category
                papers_by_year_category[year][category] = list(
                    set(paper_ids) & set(papers_per_category.get(category, []))
                )

        return papers_by_year_category

    def get_abstract_from_id(self, ids):
        abstracts = []
        for paper in self.sample:
            if paper.get("id") in ids:
                abstract = paper.get("abstract", "")
                abstracts.append(abstract)
        return abstracts

    def normalize_abstracts(self, abstracts):
        """Process abstracts in batches using SpaCy."""
        cleaned_abstracts = []
        batch_size = 100  # Adjust based on your system

        for doc in self.nlp.pipe(abstracts, batch_size=batch_size):
            tokens = [
                token.lemma_.lower()
                for token in doc
                if token.is_alpha and not token.is_stop
            ]
            cleaned_abstracts.append(" ".join(tokens))

        return cleaned_abstracts

    # def get_abstracts_by_year_category(self, papers_by_year_category):
    #     abstracts_by_year_category = {}

    #     for year, categories in papers_by_year_category.items():
    #         abstracts_by_year_category[year] = {}

    #         for category, paper_ids in categories.items():
    #             abstracts_by_year_category[year][category] = self.get_abstract_from_id(
    #                 paper_ids
    #             )
    #     for year, categories in abstracts_by_year_category.items():
    #         for category, abstracts in categories.items():
    #             # Apply normalization to each abstract
    #             normalized_abstracts = [
    #                 self.normalize_abstract(abstract) for abstract in abstracts
    #             ]
    #             abstracts_by_year_category[year][category] = normalized_abstracts

    #     return abstracts_by_year_category

    def get_abstracts_by_year_category(self, papers_by_year_category):
        abstracts_by_year_category = {}

        for year, categories in papers_by_year_category.items():
            abstracts_by_year_category[year] = {}
            for category, paper_ids in categories.items():
                # Get abstracts for the given paper IDs
                abstracts = self.get_abstract_from_id(paper_ids)

                # Normalize abstracts in batches
                normalized_abstracts = self.normalize_abstracts(
                    abstracts
                )  # Use batch processing
                abstracts_by_year_category[year][category] = normalized_abstracts

        return abstracts_by_year_category

    def save_preprocessed_abstracts(self):
        abstracts_by_year_category = self.get_abstracts_by_year_category(
            self.divide_papers_by_year_and_category()
        )
        with open(self.abstract_save_path, "w", encoding="utf-8") as f:
            json.dump(abstracts_by_year_category, f)

    def load_preprocessed_abstracts(self):
        with open(self.normalized_abstract_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_top_tfidf_words(self, abstracts, top_n=500):
        # Filter out empty abstracts
        abstracts = [abstract for abstract in abstracts if abstract.strip()]
        if not abstracts:
            return None

        tfidf_matrix = self.vectorizer.fit_transform(abstracts)
        feature_names = np.array(self.vectorizer.get_feature_names_out())
        avg_tfidf_scores = np.asarray(tfidf_matrix.mean(axis=0)).flatten()

        top_indices = avg_tfidf_scores.argsort()[-top_n:][::-1]
        top_words = feature_names[top_indices]
        top_scores = avg_tfidf_scores[top_indices]

        return pd.DataFrame({"Word": top_words, "TF-IDF Score": top_scores})

    def get_top_tfidf_words_by_category(self):
        category_tfidf_dfs = {}
        normalized_abstracts = self.load_preprocessed_abstracts()
        for year, categories in normalized_abstracts.items():
            category_tfidf_dfs[year] = {}

            for category, abstracts in categories.items():
                # Get the top tfidf words for this category
                tfidf_df = self.get_top_tfidf_words(abstracts)
                if tfidf_df is not None:
                    category_tfidf_dfs[year][category] = tfidf_df

        return category_tfidf_dfs
