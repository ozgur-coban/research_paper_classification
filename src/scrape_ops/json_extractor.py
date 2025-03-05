import json


class JsonExtractor:
    def __init__(self, input_file, output_file="filtered_cs_papers.json"):
        self.input_file = input_file
        self.output_file = output_file

    def filter_json_by_category(self, category_prefix="cs-"):
        with (
            open(self.input_file, "r", encoding="utf-8") as infile,
            open(self.output_file, "w", encoding="utf-8") as outfile,
        ):
            outfile.write("[\n")  # Start JSON array
            first_entry = True

            for line in infile:
                try:
                    paper = json.loads(line)  # Read line as JSON object
                    if "categories" in paper and any(
                        cat.startswith(category_prefix)
                        for cat in paper["categories"].split()
                    ):
                        if not first_entry:
                            outfile.write(",\n")  # Separate JSON objects with a comma
                        json.dump(paper, outfile, ensure_ascii=False, indent=2)
                        first_entry = False
                except json.JSONDecodeError:
                    continue  # Skip invalid JSON lines

            outfile.write("\n]")  # End JSON array

        print(f"Filtered CS papers saved to {self.output_file}")
