# Install packages
# !pip install requests

import requests

def download_large_file(url, destination):
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        print("File downloaded successfully!")
    except requests.exceptions.RequestException as e:
        print("Error downloading the file:", e)

# Example usage
url = 'https://objectstore.e2enetworks.net/ai4b-public-nlu-nlg/v1-indiccorp/bn.txt'
save_path = '/temp/bn.txt'
download_large_file(url, save_path)
