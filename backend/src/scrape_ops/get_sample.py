import json
import random


class GetSample:
    def __init__(
        self,
        sample_save_path=None,
        data_path=None,
        sample_size=100,
        use_existing_sample=False,
        sample_path=None,
    ):
        if use_existing_sample:
            self.sample_path = sample_path
        else:
            self.sample_size = sample_size
            self.data_path = data_path
            self.sample_save_path = sample_save_path

    # Method to load and sample the data
    def take_sample(self):
        with open(self.data_path, "r", encoding="utf-8") as f:
            data = json.load(f)  # Loads entire json file
            sample = random.sample(
                data,
                min(self.sample_size, len(data)),
            )
            return sample

    def save_sample_to_file(self):
        sample = self.take_sample()
        with open(self.sample_output_path, "w", encoding="utf-8") as f:
            json.dump(sample, f, ensure_ascii=False, indent=2)
        print(f"Sample saved to {self.sample_output_path}")

    def get_sample(self):
        with open(self.sample_path, "r", encoding="utf-8") as f:
            sample = json.load(f)
            return sample

    def get_sample_ids(self):
        indexed_sample = {}
        with open(self.sample_path, "r", encoding="utf-8") as f:
            sample = json.load(f)
            for paper in sample:
                indexed_sample[paper.get("id")] = paper
        return indexed_sample
