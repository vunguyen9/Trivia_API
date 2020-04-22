import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'Who is the richest person in the world ?',
            'answer' : 'Jeff Bezos',
            'category': '5',
            'difficulty': 2
        }

        self.new_question_2 = {
            'question': '',
            'answer' : 'Jeff Bezos',
            'category': '5',
            'difficulty': 2
        }


        

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_sent_requesting_beyong_valid_page(self):
        res = self.client().get('/questions?page=999', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_question_search_with_results(self):
        res = self.client().post('/search', json=({'searchTerm': 'Tom'}))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 1)

    def test_get_question_search_without_results(self):
        res = self.client().post('/search', json=({'searchTerm': 'absads'}))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertFalse(data['total_questions'])
        self.assertEqual(len(data['questions']), 0)

    def test_get_questions_by_category_id_with_results(self):
        res = self.client().get('categories/1/questions', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 3)

    def test_get_questions_by_category_id_without_results(self):
        res = self.client().get('categories/0/questions', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(data['total_questions'])
        self.assertEqual(len(data['questions']), 0)

    def test_get_quizzes_with_results(self):
        res = self.client().post('/quizzes', json={'previous_questions': [20,21], 'quiz_category': {'id': 1, 'type': 'Science'}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['question'].get('answer'), 'Blood')

    def test_get_quizzes_without_results(self):
        res = self.client().post('/quizzes', json={'previous_questions': None, 'quiz_category': None})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_questions'])

    def test_400_if_question_creation_not_allowed(self):
        res = self.client().post('/questions', json=self.new_question_2)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_delete_question(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 5)
        self.assertTrue(data['total_questions'])

    def test_delete_question_with_invaid_id(self):
        res = self.client().delete('/questions/999')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()