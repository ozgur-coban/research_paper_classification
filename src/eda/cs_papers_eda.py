import json
import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter, defaultdict
from datetime import datetime


class EDA:
    def __init__(
        self,
        file_path="./data/filtered_cs_papers",
        sample_output_path=None,
        sample_size=100,
        use_already_existing_sample=False,
        sample_path=None,
    ):
        self.file_path = file_path
        self.sample_size = sample_size
        self.use_already_existing_sample = use_already_existing_sample
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
        with open(self.sample_path, "r", encoding="utf-8") as f:
            sample = json.load(f)
            return sample

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
        print(df)
        # Plot histogram of word counts
        plt.figure(figsize=(10, 5))
        sns.histplot(df["Word Count"], bins=30, kde=True)
        plt.xlabel("Word Count per Abstract")
        plt.ylabel("Number of Papers")
        plt.title("Distribution of Abstract Word Counts")
        plt.show()

        return df

    def run_category_distribution(self):
        if self.use_already_existing_sample:
            sample_data = self.get_sample()
        else:
            sample_data = self.load_sample()
        print("Sample Papers:")
        # for paper in sample_data:
        #     print(json.dumps(paper, indent=2))

        category_counts = self.get_category_distribution(sample_data)
        self.plot_category_distribution(category_counts)

    def run_year_distribution(self):
        if self.use_already_existing_sample:
            sample_data = self.get_sample()
        else:
            sample_data = self.load_sample()
        year_counts = self.get_year_published(sample_data)
        self.plot_year_distribution(year_counts)

    def run_test(self):
        if self.use_already_existing_sample:
            sample_data = self.get_sample()
        else:
            sample_data = self.load_sample()
        abstracts = self.get_abstracts(sample_data)
        self.analyze_abstract_lengths(abstracts)
