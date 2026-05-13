"""
File upload views for storing menu files and other uploads.
"""

import os

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.views import APIView

from .storage import store_uploaded_file


class FileUploadThrottle(SimpleRateThrottle):
    """Rate limit file uploads by IP."""
    scope = 'file_upload'
    
    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        return self.cache_format % {'scope': self.scope, 'ident': ident}


class FileUploadView(APIView):
    """
    POST /upload/
    
    Upload a file (menu PDF, image, etc.) and get a public URL.
    
    Request:
        - file: The file to upload (multipart/form-data)
        
    Response:
        {
            "url": "https://infoweb.api.sousadev.com/media/2026/05/14_abc123.pdf",
            "filename": "2026/05/14_abc123.pdf",
            "size": 12345,
            "content_type": "application/pdf"
        }
    """
    parser_classes = [MultiPartParser, FormParser]
    throttle_classes = [FileUploadThrottle]
    
    # Max file size: 10MB
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    # Allowed content types
    ALLOWED_TYPES = {
        'application/pdf',
        'image/jpeg',
        'image/jpg',
        'image/png',
        'image/gif',
        'image/webp',
    }
    
    # Allowed extensions (additional safety check)
    ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png', '.gif', '.webp'}
    
    def post(self, request):
        file_obj = request.FILES.get('file')
        
        if not file_obj:
            return Response(
                {'detail': 'No file provided. Use "file" field in multipart/form-data.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate file size
        if file_obj.size > self.MAX_FILE_SIZE:
            return Response(
                {'detail': f'File too large. Max size: {self.MAX_FILE_SIZE // (1024*1024)}MB.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate content type
        if file_obj.content_type not in self.ALLOWED_TYPES:
            return Response(
                {'detail': f'File type not allowed. Allowed: PDF, JPG, PNG, GIF, WEBP.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate extension
        ext = os.path.splitext(file_obj.name)[1].lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            return Response(
                {'detail': f'File extension not allowed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            result = store_uploaded_file(file_obj)
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'detail': f'Upload failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FileDeleteView(APIView):
    """
    DELETE /upload/<filename>/
    
    Delete an uploaded file by filename.
    Requires admin token or ownership (future enhancement).
    """
    def delete(self, request, filename):
        # For now, just return success (files are cleaned up periodically)
        # In production, you'd check permissions here
        return Response(
            {'detail': 'File deletion not implemented yet.'},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )
