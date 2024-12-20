# NeurIPS Datasets and Benchmarks Track Web Scraper and RAG Pipeline

This repository contains a web scraping tool and a Retrieval-Augmented Generation (RAG) process designed to explore and filter datasets from the NeurIPS conference Datasets and Benchmarks Track for the years 2021, 2022, and 2023. The scraping tool gathers metadata and abstracts of relevant papers, and the RAG process enables users to query and analyze the scraped data interactively.

## Features
- **Web Scraper**: Extracts metadata and abstracts from the NeurIPS Datasets and Benchmarks Track.
- **Data Persistence**: Stores the scraped data in serialized `.pkl` files for reuse.
- **RAG Process**: Uses the extracted data to provide answers to user queries, facilitating dataset filtering and exploration.

## Getting Started

### Prerequisites
- Python 3.7 or higher
- Required libraries (install using `requirements.txt`):
  ```bash
  pip install -r requirements.txt
  ```

### Files Overview
- `scraping.py`: Script to scrape metadata and abstracts from NeurIPS conference proceedings.
- `dictionary_papers.pkl`: Serialized file storing metadata of papers.
- `dictionary_abstracts.pkl`: Serialized file storing abstracts of papers.
- `rag.py`: Script to interact with the scraped data using a RAG-based querying process.

## Usage

### Step 1: Scrape NeurIPS Data
Run the `scraping.py` script to generate or update the `.pkl` files containing the metadata and abstracts:
```bash
python scraping.py
```
This will create or update the following files:
- `dictionary_papers.pkl`
- `dictionary_abstracts.pkl`

### Step 2: Query the Data Using RAG
Once the data has been scraped, run the `rag.py` script to start asking questions about the datasets:
```bash
python rag.py
```
This will initialize the RAG pipeline, allowing you to explore the datasets interactively.

## Example Queries
- "What datasets are available for image classification?"
- "List datasets focused on text analysis."
- "Are there benchmarks for reinforcement learning tasks?"

## Contributing
Contributions are welcome! If you find any bugs or have ideas for improvements, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments
- [NeurIPS Conference](https://neurips.cc/) for providing the Datasets and Benchmarks Track.
- The creators of Python and its libraries for enabling efficient data scraping and processing.

