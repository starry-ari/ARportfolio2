# tests/test_app.py

import unittest
import os
from app import create_app

os.environ['TESTING'] = 'true'

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        # Optional: check React root div or JS reference instead
        assert "<div id=" in html or "React" in html


    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json_data = response.get_json()
        assert "timeline_posts" in json_data
        assert isinstance(json_data["timeline_posts"], list)

    def test_malformed_timeline_post(self):
        # Missing name
        response = self.client.post(
            "/api/timeline_post",
            data={
                "email": "john@example.com",
                "content": "Hello world, I'm John!"
            },
            content_type='application/x-www-form-urlencoded'
        )
        assert response.status_code == 400 or response.status_code == 500

        # Empty content
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "content": ""
            },
            content_type='application/x-www-form-urlencoded'
        )
        assert response.status_code == 400 or response.status_code == 500

        # Invalid email
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "not-an-email",
                "content": "Hello world"
            },
            content_type='application/x-www-form-urlencoded'
        )
        assert response.status_code == 400 or response.status_code == 500

    def test_create_and_fetch_timeline_post(self):
        post_data = {
            "name": "Alice",
            "email": "alice@example.com",
            "content": "Hello from Alice!"
        }
        post_response = self.client.post(
            "/api/timeline_post",
            data=post_data,
            content_type='application/x-www-form-urlencoded'
        )
        assert post_response.status_code == 200
        post_json = post_response.get_json()
        assert post_json["name"] == "Alice"
        assert post_json["email"] == "alice@example.com"
        assert post_json["content"] == "Hello from Alice!"

        get_response = self.client.get("/api/timeline_post")
        assert get_response.status_code == 200
        get_json = get_response.get_json()
        assert any(p["content"] == "Hello from Alice!" for p in get_json["timeline_posts"])
