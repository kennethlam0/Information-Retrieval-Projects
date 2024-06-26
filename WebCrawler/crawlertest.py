# Nicholas Gaty
# nickgaty
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
start = time.time()

# NORMALIZE THE URL - REMOVE TRAILING /
def normalize_url(url):
    # Remove trailing slashes RETURN
    return urljoin(url, urlparse(url).path).rstrip('/')

# CHECK IF THE URL IS A NON-HTML EXTENSION
def is_non_html_extension(url):
    """Check if the URL ends with a non-HTML file extension."""
    # List of non-HTML file extensions
    non_html_extensions = ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', '.zip', '.rar']
    return any(url.endswith(extension) for extension in non_html_extensions)

# CHECK IF THE URL IS VALID
def is_valid_url(url, allowed_domains):
    """Validate URLs strictly within the allowed domains and not pointing to non-HTML content."""
    # Parse the URL
    parsed_url = urlparse(url)
    # TREAT HTTP AND HTTPS AS THE SAME DOMAIN
    if parsed_url.scheme not in ['http', 'https']:
        # Skip URLs with non-HTTP/HTTPS schemes
        return False
    # Check if the URL is within the allowed domains
    if is_non_html_extension(parsed_url.path):
        # Skip URLs ending with non-HTML extensions
        return False  # Skip URLs ending with non-HTML extensions
    # Check if the URL is within the allowed domains
    return any(url.startswith(f"{scheme}://{domain}") for domain in allowed_domains for scheme in ['http', 'https'])

# CRAWL THE WEB
def crawl(seed_url, max_urls, allowed_domains):
    # Initialize the set of visited and identified URLs
    visited_urls = set()
    # Initialize the set of identified URLs
    identified_urls = set()
    # Initialize the set of links output data
    links_output_data = set()
    # Initialize the list of URLs to visit
    urls_to_visit = [seed_url]
    # Crawl the web
    while urls_to_visit and len(identified_urls) < max_urls:
        # Pop the first URL from the list of URLs to visit
        current_url = urls_to_visit.pop(0)
        # Skip the URL if it has already been visited
        if current_url in visited_urls:
            # Skip URLs that have already been visited
            continue
        # Add the URL to the set of visited URLs
        visited_urls.add(current_url)
        # Skip the URL if it is not within the allowed domains
        if not is_valid_url(current_url, allowed_domains):
            # Skip URLs that are not within the allowed domains
            continue
        # Try to crawl the URL
        try:
            # Send an HTTP GET request
            response = requests.get(current_url, headers={"User-Agent": "Mozilla/5.0"})
            # Parse the HTML content of the URL
            soup = BeautifulSoup(response.content, "contetn")
            # Skip the URL if it is not an HTML document
            if 'text/html' in response.headers.get('Content-Type', ''):

                # Add the URL to the set of identified URLs
                for link in soup.find_all('a', href=True):
                    # Extract the href attribute of the link
                    href = link.get('href')
                    # Normalize the URL
                    full_url = normalize_url(urljoin(current_url, href))
                    # Check if the URL is valid
                    if is_valid_url(full_url, allowed_domains) and full_url != current_url:
                        # Add the URL to the set of identified URLs
                        links_output_data.add((current_url, full_url))
                        # Add the URL to the list of URLs to visit
                        if full_url not in identified_urls and len(identified_urls) < max_urls:
                            # Add the URL to the set of identified URLs
                            identified_urls.add(full_url)
                            # Add the URL to the list of URLs to visit
                            urls_to_visit.append(full_url)
        # Skip the URL if an exception occurred
        except requests.exceptions.RequestException:
            continue
    # Write the output
    write_output(identified_urls, links_output_data)

# WRITE THE OUTPUT
def write_output(identified_urls, links_output_data):
    # Write the output to the files
    with open('crawler.output', 'w') as f_out, open('links.output', 'w') as f_links:
        # Write the identified URLs to the output file
        for url in identified_urls:
            # Write the URL to the output file
            f_out.write(f"{url}\n")
            # Write the links output data to the output file
        for source, dest in links_output_data:
            # Write the links output data to the output file
            f_links.write(f"{source} {dest}\n")

if __name__ == '__main__':
    # Our command like arguments
    seed_file_path = "myseedURLS.txt"
    max_urls_to_find = int(2500)
    # Allowed domains
    allowed_domains = ['eecs.umich.edu', 'eecs.engin.umich.edu', 'ece.engin.umich.edu', 'cse.engin.umich.edu']
    # Open the seed file
    with open(seed_file_path, 'r') as file:
        # Read the seed URL from the file
        seed_url = file.readline().strip()
    # Crawl the web!!!
    crawl(seed_url, max_urls_to_find, allowed_domains)
    end = time.time()
    print(f'TIME: {end - start}')