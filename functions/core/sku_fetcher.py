import requests
import json
import logging

class SkuFetcher:
    """Fetches SKU data from Yandex Cloud Billing API"""
    
    API_URL = "https://billing.api.cloud.yandex.net/billing/v1/skus"
    
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}"
        }
    
    def fetch_all_skus(self, output_file="sku.json"):
        """Fetch all SKUs and save to a file"""
        all_skus = []
        next_page_token = None
        
        # First request
        data = self._perform_request()
        all_skus.extend(data.get("skus", []))
        next_page_token = data.get("nextPageToken")
        
        # Loop through pages
        while next_page_token:
            params = {"pageToken": next_page_token}
            data = self._perform_request(params)
            all_skus.extend(data.get("skus", []))
            next_page_token = data.get("nextPageToken")
            logging.info(f"Fetched page with token: {next_page_token}")
        
        # Save the aggregated results to the output file
        with open(output_file, "w") as f:
            json.dump({"skus": all_skus}, f, indent=4)
        
        logging.info(f"All pages have been fetched and saved to {output_file}.")
        return all_skus
    
    def _perform_request(self, params=None):
        """Perform a request to the API and process the response"""
        response = requests.get(self.API_URL, headers=self.headers, params=params)
        if response.status_code != 200:
            logging.error(f"API request failed with status code {response.status_code}")
            response.raise_for_status()
        return response.json()
