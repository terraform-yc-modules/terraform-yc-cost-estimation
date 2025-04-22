import argparse
import logging
from core.sku_fetcher import SkuFetcher
from util.logging import configure_logging

def main():
    parser = argparse.ArgumentParser(description="Yandex Cloud IAM token")
    parser.add_argument("token", help="IAM token")
    parser.add_argument("--output", default="sku.json", help="Output file path")
    args = parser.parse_args()

    # Initialize logging
    configure_logging(logging.INFO)
    
    # Create fetcher and fetch SKUs
    fetcher = SkuFetcher(args.token)
    fetcher.fetch_all_skus(args.output)

if __name__ == "__main__":
    main()
