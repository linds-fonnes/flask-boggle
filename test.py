from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True

    def test_homepage(self):
        with self.client:
            res = self.client.get("/")
            self.assertEqual(res.status_code, 200)
            self.assertIn("board", session)
            
    def test_not_on_board(self):
        self.client.get("/")
        res = self.client.get("/check-word?word=buttercup")
        self.assertEqual(res.json['result'], 'not-on-board')
    
    def test_not_word(self):
        self.client.get("/")
        res = self.client.get("/check-word?word=usagitsukino")
        self.assertEqual(res.json["result"], "not-word")
    
    def test_valid_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess["board"] = [["D","O","G","G","G"],
                                ["D","O","G","G","G"],
                                ["D","O","G","G","G"],
                                ["D","O","G","G","G"],
                                ["D","O","G","G","G"]]
        res = self.client.get("/check-word?word=dog")
        self.assertEqual(res.json["result"],"ok")