class ScraperClient:
    def __init__(self):
        self.driver_path = os.environ.get("DRIVER_PATH", "driver")
        self.folder_path = os.environ.get("FOLDER_PATH")

    def _generate_slug(self, length=8):
        """Generate a random slug."""
        return str(uuid.uuid4()).replace("-", "")[:length]

    def fetch_rss_content(self, url):
        """Fetch SEC RSS feed and return the parsed entries."""
        headers = {
            "User-Agent": "MyApp/1.0 (praveen@example.com)",
            "Accept-Encoding": "gzip, deflate",
            "Host": "www.sec.gov",
            "Accept": "application/xml, text/xml",
            "Connection": "keep-alive",
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 403:
                logging.error(
                    "SEC is blocking your request. Try a different IP or User-Agent."
                )
                return None
            return feedparser.parse(response.text)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching SEC RSS feed: {e}")
            return None

    def parse_rss_content(self, feed_data, filing_types):
        """Scrape RSS feed for specific filing types based on the 'filing_types' parameter."""
        if not feed_data or not feed_data.entries:
            logging.warning("No entries found in the RSS feed.")
            return None

        logging.info(f"Scraping {filing_types} filings...")

        for entry in feed_data.entries:
            title = entry.title
            filing_type_in_title = title.split(" - ")[0].strip()

            if (
                filing_type_in_title in {"8-K", "10-K", "10-Q"}
                and filing_type_in_title in filing_types
            ):
                logging.info(f"Found Filing: {title}")
                doc_link = entry.link
                logging.info(f"Document Link: {doc_link}")
                return doc_link

        logging.warning("No matching filings found.")
        return None

    def extract_doc_link(self, file_link, folder_path):
        """Download and save the document from the provided link."""
        headers = {
            "User-Agent": "MyApp/1.0 (praveen@example.com)",
            "Accept-Encoding": "gzip, deflate",
            "Host": "www.sec.gov",
            "Accept": "application/xml, text/xml",
            "Connection": "keep-alive",
        }

        try:
            # Send the request to the URL
            response = requests.get(file_link, headers=headers)
            if response.status_code != 200:
                logging.error("RSS File not found.")
                return None

            # Check if the content is an RSS feed (XML)
            if "application/xml" in response.headers.get(
                "Content-Type", ""
            ) or "text/xml" in response.headers.get("Content-Type", ""):
                feed = feedparser.parse(response.text)

                if not feed.entries:
                    logging.warning("No entries found in the feed.")
                    return None

                latest_entry = feed.entries[0]
                file_name = f"{self._generate_slug(5)}_{latest_entry.title.replace(' ', '_')}.xml"
                file_path = os.path.join(folder_path, file_name)

                with open(file_path, "w") as f:
                    f.write(f"Title: {latest_entry.title}\n")
                    f.write(f"Link: {latest_entry.link}\n")
                    f.write(f"Published: {latest_entry.published}\n")
                    f.write(f"Summary: {latest_entry.summary}\n")

                logging.info(f"Feed entry saved successfully: {file_path}")
                return file_path
            else:
                # If the content is HTML, parse it to find the relevant links
                soup = BeautifulSoup(response.text, "html.parser")
                filings = []

                rows = soup.find_all("tr")
                for row in rows:
                    if "10-K" in row.text or "10-Q" in row.text or "8-K" in row.text:
                        link_tag = row.find("a")
                        if link_tag:
                            filing_link = "https://www.sec.gov" + link_tag.get("href")
                            filings.append(
                                filing_link.replace("ix?", "ixviewer/ix.html?")
                            )

                if filings:
                    file_name = f"{self._generate_slug(5)}_filings.html"
                    file_path = os.path.join(folder_path, file_name)

                    with open(file_path, "w") as f:
                        for link in filings:
                            f.write(f"{link}\n")

                    logging.info(f"Filings saved successfully: {file_path}")
                    return filings
                else:
                    logging.warning("No filings found in the HTML page.")
                    return None
        except Exception as e:
            logging.error(f"Error downloading file: {e}")
            raise e

    def download_file(self, url, folder_path):
        headers = {
            "User-Agent": "MyApp/1.0 (praveen@example.com)",
            "Accept-Encoding": "gzip, deflate",
            "Host": "www.sec.gov",
            "Accept": "application/xml, text/xml",
            "Connection": "keep-alive",
        }

        logging.info(f"Fetching: {url}")

        # Extract actual document URL if it's an inline viewer link
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        if "doc" in query_params:
            url = f"https://www.sec.gov{query_params['doc'][0]}"  # Append domain if needed

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            file_name = os.path.basename(urlparse(url).path) + "l"

            with open(os.path.join(folder_path, file_name), "wb") as file:
                file.write(response.content)

            print(f"File saved as {file_name}")
            return os.path.join(folder_path, file_name)
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
            return ""

    def main(self, url, filing_types):
        """Main method to execute the scraping process."""
        try:
            rss_feed = self.fetch_rss_content(url)
            if not rss_feed:
                logging.error("Failed to fetch RSS feed.")
                return

            document_link = self.parse_rss_content(rss_feed, filing_types)
            if not document_link:
                logging.error("No document link found.")
                return

            logging.info(f"Document Link:  {json.dumps(document_link)}")
            filings = self.extract_doc_link(document_link, self.folder_path)
            if filings:
                logging.info(f"Document downloaded successfully: {filings[0]}")
            else:
                logging.error("Failed to download document.")
            file_path = self.download_file(filings[0], self.folder_path)
            return file_path
        except Exception as err:
            logging.error(f"Error occurred during scraping: {err}")
