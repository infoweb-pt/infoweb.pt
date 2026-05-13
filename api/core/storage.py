"""
Simple file storage for uploaded menu files.
Stores files in MEDIA_ROOT and serves them via MEDIA_URL.
"""

import hashlib
import os
import uuid
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class MenuFileStorage(FileSystemStorage):
    """Custom storage that organizes files by date and generates unique filenames."""
    
    def __init__(self):
        super().__init__(
            location=settings.MEDIA_ROOT,
            base_url=settings.MEDIA_URL,
        )
    
    def get_available_name(self, name, max_length=None):
        """Generate a unique filename with UUID."""
        ext = Path(name).suffix.lower()
        # Only allow safe extensions
        allowed_exts = {'.pdf', '.jpg', '.jpeg', '.png', '.gif', '.webp'}
        if ext not in allowed_exts:
            ext = '.bin'
        
        # Generate unique filename
        unique_id = uuid.uuid4().hex[:12]
        timestamp = datetime.now().strftime('%Y%m%d')
        new_name = f"{timestamp}_{unique_id}{ext}"
        
        # Organize by month
        month_dir = datetime.now().strftime('%Y/%m')
        return os.path.join(month_dir, new_name)
    
    def generate_url(self, name):
        """Generate the full public URL for a file."""
        return f"{settings.MEDIA_URL}{name}"


def store_uploaded_file(uploaded_file):
    """
    Store an uploaded file and return its public URL.
    
    Args:
        uploaded_file: Django UploadedFile object
        
    Returns:
        dict with 'url', 'filename', 'size', 'content_type'
    """
    storage = MenuFileStorage()
    filename = storage.save(uploaded_file.name, uploaded_file)
    
    return {
        'url': storage.generate_url(filename),
        'filename': filename,
        'size': uploaded_file.size,
        'content_type': uploaded_file.content_type,
    }
