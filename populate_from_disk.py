import shutil
import os

def generate_html_files(data):
    # Create media directory if not exist
    os.makedirs('media', exist_ok=True)
    os.makedirs('html_files', exist_ok=True)

    # Iterate over the NFT data
    for artist, artist_data in data.items():
        for nft in artist_data['nft_data']:
            html = master_html

            # Copy media file to media directory and update the path
            old_media_path = os.path.join(artist_data['media_folder'], nft['media'])
            new_media_path = os.path.join('media', artist, nft['media'])
            os.makedirs(os.path.dirname(new_media_path), exist_ok=True)
            shutil.copy(old_media_path, new_media_path)
            template_media_path = f"../{new_media_path}"

            # Copy QR code to media directory and update the path
            old_qr_path = os.path.join(artist_data['qr_folder'], nft['qr_code'])
            new_qr_path = os.path.join('media', artist, nft['qr_code'])
            os.makedirs(os.path.dirname(new_qr_path), exist_ok=True)
            shutil.copy(old_qr_path, new_qr_path)
            template_qr_path = f"../{new_qr_path}"

            # Replace the placeholders in the template with the actual data
            html = html.replace('ARTWORK_NAME', nft['artwork_name'])
            html = html.replace('ARTIST_NAME', artist)
            html = html.replace('COLLECTION_NAME', nft['collection'])
            html = html.replace('EDITION_NUMBER', nft['edition'])
            html = html.replace('DESCRIPTION_CONTENT', nft['description'])

            html = html.replace('QR_CODE_PATH', template_qr_path)

            # Determine the media type based on the file extension
            media_ext = os.path.splitext(nft['media'])[1]
            media_path = new_media_path

            if media_ext in ['.jpg', '.jpeg', '.png', '.gif']:
                media_tag = f'<img src="{template_media_path}" alt="{nft["artwork_name"]}" style="width:100%; height:100%; object-fit: contain;" />'
            elif media_ext in ['.mp4', '.webm', '.ogg']:
                media_tag = f'<video controls autoplay loop style="width:100%; height:100%; object-fit: contain;"><source src="{template_media_path}" type="video/{media_ext[1:]}">Your browser does not support the video tag.</video>'
            elif media_ext in ['.mp3', '.wav', '.flac']:
                media_tag = f'<audio controls style="width:100%;"><source src="{template_media_path}" type="audio/{media_ext[1:]}">Your browser does not support the audio tag.</audio>'
            else:
                media_tag = 'Unknown media type'
            html = html.replace('MEDIA_CONTENT', media_tag)
            # Write the populated HTML to a new file
            with open(f'html_files/{nft["artwork_name"]}.html', 'w') as file:
                file.write(html)


template_file = 'template.html'
with open(template_file, 'r') as file:
    master_html = file.read()

# Import your custom module where the data structure is stored
import nft_data
data = nft_data.nft_data
generate_html_files(data)
