import os
import requests

def download_url(url, folder, filename):
    if not url:
        return False

    try:
        print(f"Starting download: {filename}")  # Show progress in terminal
        response = requests.get(url, timeout=15)
        if response.ok:
            os.makedirs(folder, exist_ok=True)
            save_path = os.path.join(folder, filename)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {filename}")
            return True
        else:
            print(f"Failed to download (bad response): {filename}")
            return False
    except Exception as e:
        print(f"Download failed: {filename}, Error: {e}")
        return False


def get_url(code, base_url):
    if not code:
        return ""
    return f"{base_url}{code}dd.zip"

