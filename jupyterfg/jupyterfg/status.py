import requests


def submit_status(status, url):
    if url is not None:
        print(f"Submitting the following status to {url}")
        print(f"{status}")
        requests.put(url, params=status)
