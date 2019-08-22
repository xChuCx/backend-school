# services/citizens/project/tests/test_citizens.py


import json
import unittest

from project.tests.base import BaseTestCase


class TestCitizensService(BaseTestCase):
    """Tests for the Citizens Service."""

    def test_import(self):
        """1: POST /imports test"""
        with self.client:
            response = self.client.post(
                '/imports',
                data=json.dumps({
                    "citizens": [
                        {
                            "citizen_id": 1,
                            "town": "Москва",
                            "street": "Льва Толстого",
                            "building": "16к7стр5",
                            "apartment": 7,
                            "name": "Иванов Иван Иванович",
                            "birth_date": "26.12.1986",
                            "gender": "male",
                            "relatives": [2]
                        },
                        {
                            "citizen_id": 2,
                            "town": "Москва",
                            "street": "Льва Толстого",
                            "building": "16к7стр5",
                            "apartment": 7,
                            "name": "Иванов Сергей Иванович",
                            "birth_date": "01.04.1997",
                            "gender": "male",
                            "relatives": [1]
                        },
                        {
                            "citizen_id": 3,
                            "town": "Керчь",
                            "street": "Иосифа Бродского",
                            "building": "2",
                            "apartment": 11,
                            "name": "Романова Мария Леонидовна",
                            "birth_date": "23.11.1986",
                            "gender": "female",
                            "relatives": []
                        }
                    ]
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)

    def test_patch(self):
        """2: PATCH test"""
        with self.client:
            response = self.client.post(
                '/imports/1/citizens/3',
                data=json.dumps({
                    "name": "Иванова Мария Леонидовна",
                    "town": "Москва",
                    "street": "Льва Толстого",
                    "building": "16к7стр5",
                    "apartment": 7,
                    "relatives": [1]
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)

    def test_patch_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/imports/0/citizens/3')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)

    def test_patch_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/imports/1/citizens/0')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)

    def test_get_citizens(self):
        """3: GET citizens test"""
        response = self.client.get('/imports/1/citizens')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        # self.assertIn('pong!', data['message'])

    def test_get_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/imports/0/citizens')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)

    def test_birthdays(self):
        """4: birthdays test"""
        response = self.client.get('/imports/1/citizens/birthdays')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        # self.assertIn('pong!', data['message'])

    def test_stat(self):
        """5: stats test"""
        response = self.client.get('/imports/1/towns/stat/percentile/age')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
