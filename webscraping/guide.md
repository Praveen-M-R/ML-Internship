# SEC RSS Feed Scraper

## Overview
This scraper fetches and parses SEC RSS feeds to extract filing documents such as `8-K`, `10-K`, and `10-Q`. It then downloads and stores these filings for further processing.

## Installation
Ensure you have the necessary dependencies installed:
```sh
pip install requests feedparser beautifulsoup4
```

## Steps to Parse RSS Feed
### 1. Initialize the Scraper Client
The scraper is initialized with environment variables for the driver path and folder path:
```python
scraper = ScraperClient()
```

### 2. Fetch RSS Content
Retrieve the RSS feed from the SEC website:
```python
rss_feed = scraper.fetch_rss_content("https://www.sec.gov/rss" )
```
- The function makes an HTTP request with appropriate headers.
- If the response status is `403`, the SEC might be blocking the request.

### 3. Parse RSS Content
Extract relevant filings from the fetched RSS feed:
```python
document_link = scraper.parse_rss_content(rss_feed, ['8-K', '10-K', '10-Q'])
```
- This function filters filings based on the specified filing types.
- If a matching filing is found, it returns the document link.

### 4. Extract Document Links
Download and save the document from the extracted link:
```python
filings = scraper.extract_doc_link(document_link, "path/to/folder")
```
- If the document is in RSS format, it saves the entry details in an XML file.
- If the document is HTML, it extracts filing links and saves them.

### 5. Download the Filing
Download the filing document using the extracted links:
```python
file_path = scraper.download_file(filings[0], "path/to/folder")
```
- Saves the document locally for further analysis.

### 6. Run the Scraper
Execute the main function to automate the entire process:
```python
scraper.main("https://www.sec.gov/rss", ['8-K', '10-K', '10-Q'])
```