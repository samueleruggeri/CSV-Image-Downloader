import pandas as pd
import requests
import os
from urllib.parse import urlparse
from pathlib import Path
import socket

requests.packages.urllib3.util.connection.HAS_IPV6 = False
old_getaddrinfo = socket.getaddrinfo

def new_getaddrinfo(*args, **kwargs):
    responses = old_getaddrinfo(*args, **kwargs)
    return [response for response in responses if response[0] == socket.AF_INET]

socket.getaddrinfo = new_getaddrinfo

def download_images_from_csv(csv_file, output_folder):
    """
    Download images from URLs contained in a CSV file and save them to a specified folder.
    Forces the use of IPv4 for connections.
    
    Args:
        csv_file (str): Path to the CSV file
        output_folder (str): Destination folder for the images
    """
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    try:
        df = pd.read_csv(csv_file)
        
        image_columns = [col for col in df.columns if any(df[col].astype(str).str.contains('http.*\.png', case=False, na=False))]
        
        if not image_columns:
            print("No image link columns found in CSV!")
            return
            
        image_column = image_columns[0]
        print(f"I use the column: {image_column}")
        
        total_images = df[image_column].count()
        print(f"Found {total_images} images to download")
        
        session = requests.Session()
        session.timeout = 30
        
        for index, row in df.iterrows():
            image_url = row[image_column]
            if pd.isna(image_url): 
                continue
                
            try:

                filename = os.path.basename(urlparse(image_url).path)
                output_path = os.path.join(output_folder, filename)
                
                if not os.path.exists(output_path):

                    response = session.get(image_url, stream=True)
                    response.raise_for_status() 
                    
                    with open(output_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                            
                    print(f"[{index+1}/{total_images}] Downloaded: {filename}")
                else:
                    print(f"[{index+1}/{total_images}] Already existing: {filename}")
                
            except requests.exceptions.RequestException as e:
                print(f"Network error while downloading {image_url}: {str(e)}")
            except Exception as e:
                print(f"Generic error while downloading {image_url}: {str(e)}")
                
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")

if __name__ == "__main__":
    csv_file = "file.csv" # The file is in the same folder
    output_folder = "Output"  # Images will be saved here
    
    print("Forced IPv4 download start...")
    download_images_from_csv(csv_file, output_folder)