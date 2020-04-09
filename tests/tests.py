import os
import requests
import unittest
import psycopg2
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, mapper

DATABASE_URI = 'postgres+psycopg2://cs162_user:cs162_password@localhost:5432/cs162'

class Exps(object):
    pass

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
metadata = MetaData(engine)
expressions = Table('expression', metadata, autoload=True)
mapper(Exps, expressions)

class TestCases(unittest.TestCase):
    
    def setUp(self):
        s = Session()
        
    def tearDown(self):
        s.close()

    def test_correct_expression(self):
        r = requests.post('http://localhost:5000/add', data={'expression': '7+21'})
        self.assertEqual(r.status_code, 200)
        print(r.text)
        self.assertIn('28',r.text)

    def test_expression_db(self):
        r = requests.post('http://localhost:5000/add', data={'expression': '7+21'})
        query = s.query(Exps).all()
        self.assertEqual(len(query),1)

    def test_invalid_expression(self):
        r = requests.post('http://localhost:5000/add', data={'expression': '7+'})
        # Check for internal server error
        self.assertEqual(r.status_code, 500)

        query = s.query(Exps).all()
        self.assertEqual(len(query), 0)


if __name__ == '__main__':
    unittest.main()
