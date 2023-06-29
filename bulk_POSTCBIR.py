import requests
import json
from pprint import pprint
import os
SNYK_TOKEN = os.getenv('SNYK_TOKEN')
from get_all_projects_REST import list_of_projectIDs

api_url = "https://api.snyk.io/rest/custom_base_images?version=2023-05-29~beta"
headers = {
    'Content-Type': 'application/vnd.api+json',
    'Authorization': 'token ' + SNYK_TOKEN
}

pprint(list_of_projectIDs)

for project_id in list_of_projectIDs:
    payload = {
        "data": {
            "attributes": {
                "include_in_recommendations": True,
                "project_id": project_id,
                #"versioning_schema": {
                    #"is_selected": True,
                    #"type": "single-selection"
                    #"expression": "(?<C0>\\d+)\\.(?<C1>\\d+)\\.(?<C2>\\d+)_(?<C3>\\d+)",
                    #"label": "calendar with flavor schema",
                    #"type": "custom"
                #}
            },
            "type": "custom_base_image"
        }
    }
    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        # Process the response as needed
        print(response.json())
    except requests.exceptions.HTTPError as err:
        error_msg = err.response.json().get('errors', [])
        for error in error_msg:
            if 'A versioning schema already exists' in error.get('detail', '') and 'repository' in error.get('meta', {}):
                repository = error['meta']['repository']
                if repository == f'{project_id.split("/")[0]}/{project_id.split("/")[1]}':
                    # Make subsequent API calls without the versioning_schema field
                    del payload['data']['attributes']['versioning_schema']
                    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
                    # Process the response as needed
                    print(response.json())
            else:
                print(f"Error: {error.get('detail', '')}")
