import unittest
from unittest.mock import patch
from flask import Flask
from blueprints.pictures import pictures_bp

class TestPicturesBlueprint(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(pictures_bp)
        self.client = self.app.test_client()

    @patch('manager.pictures_manager.fetch_user_pictures')
    def test_get_pictures_success(self, mock_fetch_user_pictures):
        mock_fetch_user_pictures.return_value = {"success": True, "message": "Fetched pictures.", "data": []}
        response = self.client.get('/pictures/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Fetched pictures.", response.get_json().get("message"))

    @patch('manager.pictures_manager.upload_picture')
    def test_upload_picture_success(self, mock_upload_picture):
        mock_upload_picture.return_value = {"success": True, "message": "Picture uploaded successfully."}
        response = self.client.post('/pictures/upload', json={"user_id": 1, "image_id": "image123", "is_profile": True})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Picture uploaded successfully.", response.get_json().get("message"))

    @patch('manager.pictures_manager.remove_picture')
    def test_delete_picture_success(self, mock_remove_picture):
        mock_remove_picture.return_value = {"success": True, "message": "Picture removed successfully."}
        response = self.client.delete('/pictures/1/123')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Picture removed successfully.", response.get_json().get("message"))

    @patch('manager.pictures_manager.change_profile_picture')
    def test_set_profile_picture_success(self, mock_change_profile_picture):
        mock_change_profile_picture.return_value = {"success": True, "message": "Profile picture updated successfully."}
        response = self.client.put('/pictures/set-profile', json={"user_id": 1, "picture_id": 123})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Profile picture updated successfully.", response.get_json().get("message"))

if __name__ == '__main__':
    unittest.main()





