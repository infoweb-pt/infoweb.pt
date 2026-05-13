"""Tests for file upload endpoint."""

import io

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class FileUploadTests(APITestCase):
    def test_upload_pdf(self):
        """Test uploading a PDF file."""
        file_content = b'%PDF-1.4 test pdf content'
        file = io.BytesIO(file_content)
        file.name = 'menu.pdf'
        file.content_type = 'application/pdf'
        
        response = self.client.post(
            '/upload/',
            {'file': file},
            format='multipart'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('url', response.data)
        self.assertIn('filename', response.data)
        self.assertIn('size', response.data)
        self.assertEqual(response.data['size'], len(file_content))
        self.assertEqual(response.data['content_type'], 'application/pdf')
    
    def test_upload_jpg(self):
        """Test uploading a JPG image."""
        file_content = b'\xff\xd8\xff\xe0\x00\x10JFIF'  # JPG magic bytes
        file = io.BytesIO(file_content)
        file.name = 'menu.jpg'
        file.content_type = 'image/jpeg'
        
        response = self.client.post(
            '/upload/',
            {'file': file},
            format='multipart'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('url', response.data)
    
    def test_upload_no_file(self):
        """Test uploading without a file."""
        response = self.client.post('/upload/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_upload_invalid_type(self):
        """Test uploading an invalid file type."""
        file = io.BytesIO(b'not an image')
        file.name = 'malicious.exe'
        file.content_type = 'application/x-msdownload'
        
        response = self.client.post(
            '/upload/',
            {'file': file},
            format='multipart'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_upload_too_large(self):
        """Test uploading a file that's too large."""
        file = io.BytesIO(b'x' * (11 * 1024 * 1024))  # 11MB
        file.name = 'huge.pdf'
        file.content_type = 'application/pdf'
        
        response = self.client.post(
            '/upload/',
            {'file': file},
            format='multipart'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
