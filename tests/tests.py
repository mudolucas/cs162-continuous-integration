import os
import requests
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, mapper
import psycopg2

DB_URI = 'postgresql://cs162_user:cs162_password@127.0.0.1/cs162?port=5432'
engine = create_engine(DB_URI)

class TestCases(unittest.TestCase):
    
    def setUp(self):
        with engine.connect() as connection:
            connection.execute("DELETE FROM Expression")
    
    def tearDown(self):
        with engine.connect() as connection:
            connection.execute("DELETE FROM Expression")

    def test_correct_expression(self):
        r = requests.post('http://127.0.0.1:5000/add', data={'expression': '7+22'})
        self.assertEqual(r.status_code, 200)
        self.assertIn('29',r.text)

    def test_expression_db(self):
        r = requests.post('http://127.0.0.1:5000/add', data={'expression': '10+30'})
        with engine.connect() as connection:
            query = connection.execute("SELECT COUNT('*') FROM Expression WHERE text='10+30'")
            rows = query.fetchall()
            self.assertEqual(len(rows),1)

    def test_invalid_expression(self):
        r = requests.post('http://127.0.0.1:5000/add', data={'expression': '20+'})
        # Check for internal server error
        self.assertEqual(r.status_code, 500)
        with engine.connect() as connection:
            query = connection.execute("SELECT COUNT('*') FROM Expression")
            rows = query.fetchall()
            print(rows)
            self.assertEqual(len(rows),0)

if __name__ == '__main__':
    unittest.main()
