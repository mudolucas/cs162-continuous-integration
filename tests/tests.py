import os
import requests
import unittest
import psycopg2
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, mapper

DATABASE_URI = 'postgres+psycopg2://cs162_user:cs162_password@localhost:5432/cs162'

class Exps(object):
    pass

class TestCases(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData(self.engine)
        self.expressions = Table('expression', self.metadata, autoload=True)
        self.mapper(Exps, self.expressions)
        self.s = self.Session()

    def tearDown(self):
        self.connection.close()

    def test_correct_expression(self):
        r = requests.post('http://localhost:5000/add', data={'expression': '7+21'})
        self.assertEqual(r.status_code, 200)
        print(r.text)
        self.assertIn('28',r.text)

    def test_expression_db(self):
        r = requests.post('http://localhost:5000/add', data={'expression': '7+21'})
        query = self.s.query(Exps).all()
        self.assertEqual(len(query),1)

    def test_invalid_expression(self):
        r = requests.post('http://localhost:5000/add', data={'expression': '7+'})
        # Check for internal server error
        self.assertEqual(r.status_code, 500)

        query = self.s.query(Exps).all()
        self.assertEqual(len(query), 0)


if __name__ == '__main__':
    unittest.main()
