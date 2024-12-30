import requests
from bs4 import BeautifulSoup
import pickle

# List of URLs to scrape
urls = [
    "https://papers.nips.cc/paper/2022",
    "https://papers.nips.cc/paper/2023"
]

extra_url = "https://datasets-benchmarks-proceedings.neurips.cc/paper/2021"

# Function to scrape papers of interest
def scrape_datasets_and_benchmarks_papers(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all list items with the class 'datasets_and_benchmarks'
        papers = soup.find_all('li', class_='datasets_and_benchmarks')
        # Extract paper titles and links
        paper_list = []
        for paper in papers:
            title = paper.text.strip()
            link = paper.a['href'] if paper.a else None
            paper_list.append((title, link))
        return paper_list
    else:
        print(f"Failed to fetch {url} (status code: {response.status_code})")
        return []


def scrape_round_papers(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all list items with the class 'round1' or 'round2'
        papers = soup.find_all('li', class_=['round1', 'round2'])
        # Extract paper titles and links
        paper_list = []
        for paper in papers:
            # Extract the actual title from the visible text of the <a> tag
            title = paper.a.text.strip() if paper.a else paper.text.strip()
            print("title", title)  # Debugging line to check the extracted title
            link = paper.a['href'] if paper.a else None
            paper_list.append((title, link))
        return paper_list
    else:
        print(f"Failed to fetch {url} (status code: {response.status_code})")
        return []

# Main script
all_papers = []
# Scrape the main URLs
for url in urls:
    papers = scrape_datasets_and_benchmarks_papers(url)
    all_papers.extend(papers)

print("all_papers", all_papers)

# Scrape the extra URL for round1 and round2 papers
round_papers = scrape_round_papers(extra_url)
all_papers.extend(round_papers)


print("round_papers", round_papers)

# Display the results
print("Datasets and Benchmarks Papers:")
counter = 1
dictionary_papers = {}	
dictionary_papers_pdf = {}	
for title, link in all_papers:
    print("\nPaper", counter)
    print(f"- {title}")
    counter += 1
    if link:
        # full_link = f"https://datasets-benchmarks-proceedings.neurips.cc{link}" if 'datasets-benchmarks-proceedings' in extra_url else f"https://papers.nips.cc{link}"
        if "Abstract-Datasets_and_Benchmarks" in link:
            full_link = f"https://papers.nips.cc{link}"
        if "Abstract-round" in link:
            full_link = f"https://datasets-benchmarks-proceedings.neurips.cc{link}" 
        dictionary_papers[title] = full_link
        if '-Abstract-' in link:
            new_link = link.replace('-Abstract-', '-Paper-').replace("html", "pdf").replace("hash", "file")
            pdf_link = f"https://datasets-benchmarks-proceedings.neurips.cc{new_link}" if 'datasets-benchmarks-proceedings' in full_link else f"https://papers.nips.cc{new_link}"
            dictionary_papers_pdf[title] = pdf_link
            print(f"Link: {pdf_link}")

# Save dictionary_papers as pkl
with open('dictionary_papers.pkl', 'wb') as f:
    pickle.dump(dictionary_papers, f)
print("dictionary_papers_pdf")
dictionary_papers_pdf

# Function to extract the abstract from a paper link
def extract_abstract(link):
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Locate the 'h4' tag with text "Abstract"
        abstract_header = soup.find('h4', string="Abstract")
        if abstract_header:
            # Find the next sibling 'p' tag containing the abstract
            abstract_paragraph = abstract_header.find_next('p')
            if abstract_paragraph:
                return abstract_paragraph.text.strip()
        return "Abstract not found."
    else:
        return f"Failed to fetch content from {link} (status code: {response.status_code})"

# Create a new dictionary with titles and abstracts
counter = 1
dictionary_abstracts = {}
for title, link in dictionary_papers.items():
    print(f"\nPaper {counter}")
    print(f"Extracting abstract for '{title}'...")
    print(f"Link: {link}")
    abstract = extract_abstract(link)
    dictionary_abstracts[title] = abstract
    print(f"Abstract: {abstract}\n")
    counter += 1

# save dictionary_abstracts as pkl
with open('dictionary_abstracts.pkl', 'wb') as f:
    pickle.dump(dictionary_abstracts, f)

# Print the result
for title, abstract in dictionary_abstracts.items():
    print(f"{title}:\n{abstract}\n")

