import requests
from bs4 import BeautifulSoup
import json  # Import the JSON module

# URL of the React documentation page
url = "https://react.dev/learn"

# Fetch the page content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.text, "lxml")

    # Locate the specific <nav> section with role="navigation"
    target_nav = soup.find("nav", {"role": "navigation"})

    # Initialize the JSON structure
    json_output = []

    if target_nav:
        # Locate the <ul> inside the <nav>
        ul = target_nav.find("ul")

        if ul:
            # Iterate over top-level <li> elements
            for li in ul.find_all("li", recursive=False):
                # Find the main <a> tag directly inside the <li>
                link = li.find("a", recursive=False)

                if link:
                    # Extract title and URL
                    title = link.text.strip() if link.text else "No title"
                    relative_url = link.get("href", "No href")
                    full_url = f"https://react.dev{relative_url}" if relative_url.startswith("/") else relative_url

                    # Prepare the sections list for nested links
                    sections = []

                    # Check for nested <ul> inside the current <li>
                    nested_ul = li.find("ul")
                    if nested_ul:
                        # Iterate over nested <li> elements
                        for nested_li in nested_ul.find_all("li", recursive=False):
                            nested_link = nested_li.find("a", recursive=False)
                            if nested_link:
                                nested_title = nested_link.text.strip() if nested_link.text else "No title"
                                nested_href = nested_link.get("href", "No href")
                                nested_full_url = f"https://react.dev{nested_href}" if nested_href.startswith("/") else nested_href

                                # Add the nested link as a section
                                sections.append({
                                    "title": nested_title,
                                    "url": nested_full_url
                                })

                    # Add the main page entry to the JSON structure
                    json_output.append({
                        "title": title,
                        "url": full_url,
                        "source": "react",
                        "sections": sections
                    })
    else:
        print("Target navigation not found in the page.")
else:
    print(f"Failed to fetch the page. Status Code: {response.status_code}")

# Write the output to a JSON file
with open("docs.json", "w", encoding="utf-8") as json_file:
    json.dump(json_output, json_file, indent=4, ensure_ascii=False)

print("JSON file created: react_docs.json")
