import shutil
import nft_data
import os

# def load_nft_data(base_dir='artists'):
#     nft_data = []

#     # Iterate over all artist directories
#     for artist_dir in glob.glob(os.path.join(base_dir, '*')):
#         artist = os.path.basename(artist_dir)

#         # Iterate over all NFT directories for this artist
#         for nft_dir in glob.glob(os.path.join(artist_dir, '*')):
#             nft = os.path.basename(nft_dir)
#             media_file = None
#             qr_code = None
#             description = None

#             # Iterate over all files in this NFT directory
#             for nft_file in glob.glob(os.path.join(nft_dir, '*')):
#                 _, ext = os.path.splitext(nft_file)
#                 basename = os.path.basename(nft_file)

#                 # Classify the files based on their file type
#                 if ext.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webm', '.ogg', '.mp3', '.wav', '.flac']:
#                     media_file = basename
#                 elif 'qr' in basename.lower() and ext.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
#                     qr_code = basename
#                 elif ext.lower() == '.txt':
#                     with open(nft_file, 'r') as file:
#                         description = file.read()

#             # Add this NFT to the data
#             nft_data.append({
#                 'filename': nft,
#                 'media': media_file,
#                 'artist': artist,
#                 'collection': 'Collection Name',  # Update this if you have a way to determine the collection
#                 'edition': '1/1',  # Update this if you have a way to determine the edition
#                 'description': description,
#                 'qr_code': qr_code,
#             })

#     return nft_data


def generate_html_files(nft_data):
    # Create media directory if not exist
    os.makedirs('media', exist_ok=True)
    os.makedirs('html_files', exist_ok=True)

    # Iterate over the NFT data
    for nft in nft_data:
        html = master_html

        # Copy media file to media directory and update the path
        old_media_path = os.path.join(nft['nft_folder'], nft['media'])
        new_media_path = os.path.join('media', nft['media'])
        shutil.copy(old_media_path, new_media_path)
        template_media_path = f"../{new_media_path}"

        # Copy QR code to media directory and update the path
        old_qr_path = os.path.join(nft['qr_folder'], nft['qr_code'])
        new_qr_path = os.path.join('media', nft['qr_code'])
        shutil.copy(old_qr_path, new_qr_path)
        template_qr_path = f"../{new_qr_path}"

        # Replace the placeholders in the template with the actual data
        html = html.replace('ARTWORK_NAME', nft['artwotk_name'])
        html = html.replace('ARTIST_NAME', nft['artist'])
        html = html.replace('COLLECTION_NAME', nft['collection'])
        html = html.replace('EDITION_NUMBER', nft['edition'])
        html = html.replace('DESCRIPTION_CONTENT', nft['description'])

        html = html.replace(
            'QR_CODE_PATH', template_qr_path)

        # Determine the media type based on the file extension
        media_ext = os.path.splitext(nft['media'])[1]
        media_path = new_media_path

        if media_ext in ['.jpg', '.jpeg', '.png', '.gif']:
            media_tag = f'<img src="{template_media_path}" alt="{nft["artwotk_name"]}" style="width:100%; height:100%; object-fit: contain;" />'
        elif media_ext in ['.mp4', '.webm', '.ogg']:
            media_tag = f'<video controls autoplay loop style="width:100%; height:100%; object-fit: contain;"><source src="{template_media_path}" type="video/{media_ext[1:]}">Your browser does not support the video tag.</video>'
        elif media_ext in ['.mp3', '.wav', '.flac']:
            media_tag = f'<audio controls style="width:100%;"><source src="{template_media_path}" type="audio/{media_ext[1:]}">Your browser does not support the audio tag.</audio>'
        else:
            media_tag = 'Unknown media type'
        html = html.replace('MEDIA_CONTENT', media_tag)
        # Write the populated HTML to a new file
        with open(f'html_files/{nft["artwotk_name"]}.html', 'w') as file:
            file.write(html)


template_file = 'template.html'
with open(template_file, 'r') as file:
    master_html = file.read()

nft_data = nft_data.nft_data
generate_html_files(nft_data)
