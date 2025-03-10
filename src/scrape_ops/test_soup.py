import requests
import re
from bs4 import BeautifulSoup


url = "https://arxiv.org/category_taxonomy"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find all categories
categories = [category.get_text() for category in soup.find_all("h4")]

print(categories)
# Use regex to find categories that match the xx.xx pattern
category_codes = [
    re.match(r"([a-zA-Z\-]+\.[A-Za-z]+)", category).group(1)
    for category in categories
    if re.match(r"([a-zA-Z\-]+\.[A-Za-z]+)", category)
]

category_names = [
    re.match(r"([a-zA-Z\-]+\.[A-Za-z]+)\s?\(([^)]+)\)", category).group(1)
    + " ("
    + re.match(r"([a-zA-Z\-]+\.[A-Za-z]+)\s?\(([^)]+)\)", category).group(2)
    + ")"
    for category in categories
    if re.match(r"([a-zA-Z\-]+\.[A-Za-z]+)\s?\(([^)]+)\)", category)
]

print(category_names)
