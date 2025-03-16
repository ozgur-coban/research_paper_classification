import xml.etree.ElementTree as ET
import urllib.request as libreq
import urllib.parse
import time


class DataScraper:
    def __init__(
        self,
        query,
        start_date="202412010000",
        end_date="202412310000",
        max_results=1000,
    ):
        self.base_url = "http://export.arxiv.org/api/query?"
        self.query = query
        self.start_date = start_date
        self.end_date = end_date
        self.max_results = max_results

    def fetch_batch(self, start_index):
        """Fetch a batch of results starting from a specific index."""
        search_query = urllib.parse.quote(
            f"{self.query} AND submittedDate:[{self.start_date} TO {self.end_date}]"
        )
        print("search_query", search_query)
        request_url = f"{self.base_url}search_query={search_query}&start={start_index}&max_results={self.max_results}&sortBy=submittedDate&sortOrder=descending"

        req = libreq.Request(request_url, headers={"User-Agent": "Mozilla/5.0"})
        with libreq.urlopen(req) as url:
            r = url.read()
        return r

    def fetch_all_results(self, output_file="../../data/arxiv_test.xml"):
        """Fetch all results by paginating and saving to a file."""
        start_index = 0
        batch_number = 1

        with open(output_file, "wb") as file:
            while True:
                print(f"Fetching batch {batch_number} (starting at {start_index})...")
                response = self.fetch_batch(start_index)

                # Parse XML and check if <entry> exists
                root = ET.fromstring(response)
                entries = root.findall("{http://www.w3.org/2005/Atom}entry")

                if not entries:
                    print("No more articles found. Stopping.")
                    break  # Stop if no <entry> elements exist

                file.write(response)  # Append batch to file
                start_index += self.max_results
                batch_number += 1

                time.sleep(2)  # Be polite, avoid overloading the API

        print(f"Results saved to {output_file}")
