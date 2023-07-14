import os
import requests
import re
import sys

# Directory where the TSV files are located
file_path = sys.argv[1] #'/path/to/derai-research-vision/gill/datasets/tsv_file.tsv'
output_img_directory = sys.argv[2] #"/path/to/derai-research-vision/gill/data/ikea_8000_756/training/images"


# Function to extract the line with a "http" link from a file
def extract_link_line(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if 'http' in line:
                line = line.strip().replace('Caption:', '').replace('item_no: ', '')
                return line.strip()


def sanitize_filename(filename):
    """Remove invalid characters from the filename."""
    return re.sub(r'[^\w\-_.]', '', filename)


def save_image(file_path, output_directory):
    """ 
        Function to save the image from the given URL to the output images directory.
        Saving image with their url-stripped filenames to avoid overwriting images with same DAM code.
        inputs:
        file_path: the full path including the tsv file from which the image link will be accessed.
        output_directory: the full path of the directory to save images.
    """
    if os.path.isfile(file_path):
        k=0
        with open(file_path, 'r') as file:
            for line in file:
                link_line = line.strip()
                if link_line:
                    if 'http' in link_line:
                        pattern = r'(https?://\S+)'
                        urls = re.findall(pattern, link_line)[0]
                        try:
                            response = requests.get(urls, stream=True)
                            if response.status_code == 200:
                                file_name = urls.split('/')[-1]  # Extract the file name from theURL
                                file_name = file_name.split('?')[0]  
                                file_name = sanitize_filename(urls)
                                # Create the directory
                                if not os.path.exists(output_directory):
                                    os.makedirs(output_directory)
                                    print("Created dictionary {output_directory}")
                                file_path = os.path.join(output_directory, file_name)
                                # Save images
                                with open(file_path, 'wb') as file:
                                    file.write(response.content)
                                k+=1
                                print(f"{k}th file, saved image: {file_name}")
                            else:
                                print(f"Skipping {urls} due to response.status_code:{response.status_code}.")
                        except requests.exceptions.ConnectionError:
                            print(f"Skipping {urls} due to requests.exceptions.ConnectionError.")
    else:
        print(f"File not found: {file_path}")

save_image(file_path, output_img_directory)
