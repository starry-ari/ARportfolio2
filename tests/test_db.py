import unittest
from peewee import *

from app import TimelinePost

MODELS = [TimelinePost]

test_db=SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close() 

    def test_TimelinePost(self):
        dummie_post = TimelinePost.create(name='John Doe', email='jon@example.com', content="Hello World! \n I'm John")
        print(f"Created post with ID:{dummie_post.id}")

        timeline_post = TimelinePost.get_by_id(dummie_post.id)
        print(f"Retrieved post with ID:{timeline_post.id}")

        self.assertEqual(timeline_post.id, dummie_post.id)
        self.assertEqual(timeline_post.name, dummie_post.name)
        self.assertEqual(timeline_post.email, dummie_post.email)
        self.assertEqual(timeline_post.content, dummie_post.content)
        self.assertIsNotNone(timeline_post.created_at)

        print("TEST PASSED: TimelinePost created and retrieved successfully.")


