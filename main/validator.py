import os
import magic
from django.core.exceptions import ValidationError

def validate_is_torrent(file):
    valid_mime_types = ['application/x-bittorrent']
    file_mime_type = magic.from_buffer(file.read(1024), mime=True)
    
    if file_mime_type not in valid_mime_types:
        raise ValidationError('Unsupported file type.')
    valid_file_extensions = ['.torrent']
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        print('nice2')
        raise ValidationError('Unacceptable file extension.')