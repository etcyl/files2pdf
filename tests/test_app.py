import unittest
from io import BytesIO
import sys
import os

# Ensure the app module is correctly found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  # Import after adjusting the path

class TestFlaskApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the Flask testing client
        cls.client = app.test_client()
        cls.client.testing = True

    def test_merge_multiple_files(self):
        # Simulate file uploads using BytesIO
        data = {
            'files': [
                (BytesIO(b"Sample text content"), "test1.txt"),
                (BytesIO(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x0BIEND\xaeB`\x82"), "test2.png"),  # Minimal PNG header with IEND chunk
            ]
        }

        # Perform the POST request
        response = self.client.post("/", content_type='multipart/form-data', data={
            'files': [
                (BytesIO(b"Sample text content"), "test1.txt"),
                (BytesIO(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x0BIEND\xaeB`\x82"), "test2.png"),
            ]
        })

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/pdf')
        self.assertGreater(len(response.data), 0)  # Check that the PDF data is not empty

if __name__ == '__main__':
    unittest.main()
