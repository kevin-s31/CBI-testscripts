import requests
import json
from pprint import pprint
import os

SNYK_TOKEN = os.getenv('SNYK_TOKEN')

url = "https://api.snyk.io/rest/orgs/d650de94-1285-4861-897f-a79f1435fcf8/projects?version=2023-05-29&limit=100"
headers = {
    'Content-Type': 'Content-Type: application/vnd.api+json',
    'Authorization': 'token ' + SNYK_TOKEN
}

params = {
    # Add any additional parameters here if required
}

list_of_projectIDs = []


def process_data(data):
    for item in data.get('data', []):
        name = item.get('attributes', {}).get('name')
        project_id = item.get('id')
        if name.startswith("kevins311/single_schema_test1:"):
            list_of_projectIDs.append(project_id)
            print({name})
            # print(f"Name: {name}, ID: {project_id}")


response = requests.get(url, headers=headers, params=params)
data = response.json()

# Process the results from the first page
process_data(data)

# Check if the response contains multiple pages
if "pages" in data and "next" in data["pages"]:
    next_url = data["pages"]["next"]

    while next_url:
        response = requests.get(next_url, headers=headers, params=params)
        data = response.json()
        pprint(data)
        # Process the results from the current page
        process_data(data)

        # Check if there is another page available
        if "pages" in data and "next" in data["pages"]:
            next_url = data["pages"]["next"]
        else:
            next_url = None

    # Process the final page of results, if required
    # ...
else:
    print("You're done")

# Print the list of project IDs
#pprint(list_of_projectIDs)
count_of_projectIds = len(list_of_projectIDs)
#print(f"There are {count_of_projectIds} projects under this container repository.")
