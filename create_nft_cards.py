import shutil
import os
import nft_data
import re
from logo_map import logo_map


def generate_html_files(data):
    # Create media directory if not exist
    os.makedirs('media', exist_ok=True)
    os.makedirs('html_files', exist_ok=True)

    # Iterate over the NFT data
    for artist, artist_data in data.items():
        # Check if the artist has collections or directly nft_data
        if 'nft_data' in artist_data:  # The artist has nft_data directly
            generate_html_for_nft_data(artist, '', artist_data)
        else:  # The artist has collections
            for collection, collection_data in artist_data.items():
                generate_html_for_nft_data(artist, collection, collection_data)


def generate_html_for_nft_data(artist, collection, data):
    for nft in data['nft_data']:
        html = master_html

        # Copy media file to media directory and update the path
        old_media_path = os.path.join(data['media_folder'], nft['media'])
        new_media_name = nft['media'].replace('#', '_')  # modify filename here
        new_media_path = os.path.join('media', artist, collection, new_media_name)
        os.makedirs(os.path.dirname(new_media_path), exist_ok=True)
        shutil.copy(old_media_path, new_media_path)
        template_media_path = f"../{new_media_path}"

        # Copy QR code to media directory and update the path
        old_qr_path = os.path.join(data['qr_folder'], nft['qr_code'])
        new_qr_name = f"QR_{nft['qr_code']}"
        new_qr_path = os.path.join('media', artist, collection, new_qr_name)
        os.makedirs(os.path.dirname(new_qr_path), exist_ok=True)
        shutil.copy(old_qr_path, new_qr_path)
        template_qr_path = f"../{new_qr_path}"

        # Replace the placeholders in the template with the actual data
        html = html.replace('ARTWORK_NAME', nft['artwork_name'])
        html = html.replace('ARTIST_NAME', artist)

        # Replace the placeholders in the template with the actual data

        html = html.replace('DESCRIPTION_CONTENT', nft.get('description', ''))


        # If the collection is empty, remove the entire line
        collection = data.get('collection') or nft.get('collection') or collection

        if collection != '':
            html = html.replace('COLLECTION_NAME', collection)
        else:
            # Remove the div starting from its id until its end
            html = re.sub('<div id=\"collection-div\">[\s\S]*?</div>', '', html)

        html = html.replace('QR_CODE_PATH', template_qr_path)

        # Get additional image from logo map
        additional_image_data = logo_map[data['minted_on']]
        additional_image_tag = f'<img src="{additional_image_data["src"]}" style="width:{additional_image_data["width"]};">'
        html = html.replace('LOGO_IMAGE', additional_image_tag)

        # Determine the media type based on the file extension
        media_ext = os.path.splitext(nft['media'])[1]
        media_id = "media-content"
        if media_ext in ['.jpg', '.jpeg', '.png', '.gif', '.JPG', '.JPEG', '.PNG', '.GIF']:
            media_tag = f'<img id="{media_id}" src="{template_media_path}" alt="{nft["artwork_name"]}" style="width:100%; object-fit: contain;" />'
        elif media_ext in ['.mp4', '.webm', '.ogg']:
            media_tag = f'<video id="{media_id}" controls autoplay muted loop style="width:100%; object-fit: contain;"><source src="{template_media_path}" type="video/{media_ext[1:]}">Your browser does not support the video tag.</video>'
        elif media_ext in ['.mp3', '.wav', '.flac']:
            media_tag = f'<audio id="{media_id}" controls style="width:100%;"><source src="{template_media_path}" type="audio/{media_ext[1:]}">Your browser does not support the audio tag.</audio>'
        else:
            media_tag = 'Unknown media type'
        html = html.replace('MEDIA_CONTENT', media_tag)

        # Write the populated HTML to a new file
        base_html_file_name = nft["artwork_name"].replace("#", "_")
        html_file_name = base_html_file_name  # modify filename here
        html_file_path = f'html_files/{html_file_name}.html'


        # Check if the file already exists, and append a number to the filename
        counter = 1
        while os.path.exists(html_file_path):
            html_file_name = f'{base_html_file_name}_{counter}'  # modify filename here
            html_file_path = f'html_files/{html_file_name}.html'
            counter += 1


        with open(f'html_files/{html_file_name}.html', 'w') as file:
            file.write(html)


template_file = 'template.html'
with open(template_file, 'r') as file:
    master_html = file.read()

# Import your custom module where the data structure is stored
data = nft_data.nft_data
generate_html_files(data)
