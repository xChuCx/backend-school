# services/citizens/project/tests/test_citizens.py


import json
import unittest

from project.tests.base import BaseTestCase


class TestCitizensService(BaseTestCase):
    """Tests for the Citizens Service."""

    def test_00_import(self):
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
                content_type='application/json')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['data']['import_id'])

    def test_01_import_invalid(self):
        """Ensure error is thrown if request  invalid"""
        with self.client:
            response = self.client.post(
                '/imports',
                data=json.dumps({}),
                content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_02_import_invalid_int(self):
        """Ensure error is thrown if invalid types"""
        with self.client:
            response = self.client.post(
                '/imports',
                data=json.dumps({
                    "citizens": [{
                        "citizen_id": "1",
                        "town": "Москва",
                        "street": "Льва Толстого",
                        "building": "16к7стр5",
                        "apartment": 7,
                        "name": "Иванов Иван Иванович",
                        "birth_date": "26.12.1986",
                        "gender": "male",
                        "relatives": [2]
                    }]
                }),
                content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_03_import_invalid_str(self):
        """Ensure error is thrown if invalid types"""
        with self.client:
            response = self.client.post(
                '/imports',
                data=json.dumps({
                    "citizens": [{
                        "citizen_id": 1,
                        "town": "Москва",
                        "street": "Льва Толстого",
                        "building": 16,
                        "apartment": 7,
                        "name": "Иванов Иван Иванович",
                        "birth_date": "26.12.1986",
                        "gender": "male",
                        "relatives": [2]
                    }]
                }),
                content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_04_import_invalid_date(self):
        """Ensure error is thrown if invalid types"""
        with self.client:
            response = self.client.post(
                '/imports',
                data=json.dumps({
                    "citizens": [{
                        "citizen_id": 1,
                        "town": "Москва",
                        "street": "Льва Толстого",
                        "building": "16к7стр5",
                        "apartment": 7,
                        "name": "Иванов Иван Иванович",
                        "birth_date": "32.12.1986",
                        "gender": "male",
                        "relatives": [2]
                    }]
                }),
                content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_05_import_invalid_tupl(self):
        """Ensure error is thrown if invalid types"""
        with self.client:
            response = self.client.post(
                '/imports',
                data=json.dumps({
                    "citizens": [{
                        "citizen_id": 1,
                        "town": "Москва",
                        "street": "Льва Толстого",
                        "building": "16к7стр5",
                        "apartment": 7,
                        "name": "Иванов Иван Иванович",
                        "birth_date": "26.12.1986",
                        "gender": "male",
                        "relatives": 2
                    }]
                }),
                content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_06_patch(self):
        """2: PATCH test"""
        with self.client:
            response = self.client.patch(
                '/imports/1/citizens/2',
                data=json.dumps({
                    "town": "Киев",
                    "street": "Льва Толстого",
                    "building": "16к7",
                    "apartment": 6,
                    "name": "Олегов Олег Олегович",
                    "birth_date": "09.09.1996",
                    "gender": "male",
                    "relatives": [3]
                }),
                content_type='application/json'
            )

            resp = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(resp['data']['citizen_id'], 2)
            self.assertEqual(resp['data']['town'], "Киев")
            self.assertEqual(resp['data']['street'], "Льва Толстого")
            self.assertEqual(resp['data']['building'], "16к7")
            self.assertEqual(resp['data']['apartment'], 6)
            self.assertEqual(resp['data']['name'], "Олегов Олег Олегович")
            self.assertEqual(resp['data']['birth_date'], "09.09.1996")
            self.assertEqual(resp['data']['gender'], "male")
            self.assertEqual(resp['data']['relatives'], [3])

    def test_07_patch_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.patch(
                '/imports/1/citizens/99999',
                data=json.dumps({"town": "Киев"}),
                content_type='application/json',
            )
            self.assertEqual(response.status_code, 400)

    def test_08_patch_incorrect_import(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.patch(
                '/imports/0/citizens/2',
                data=json.dumps({"town": "Киев"}),
                content_type='application/json',
            )
            self.assertEqual(response.status_code, 400)

    def test_09_patch_incorrect_int(self):
        """Ensure error is thrown if invalid types"""
        with self.client:
            response = self.client.patch(
                '/imports/1/citizens/2',
                data=json.dumps({"apartment": "6"}),
                content_type='application/json',
            )
            self.assertEqual(response.status_code, 400)

    def test_10_patch_incorrect_date(self):
        """Ensure error is thrown if invalid types"""
        with self.client:
            response = self.client.patch(
                '/imports/1/citizens/2',
                data=json.dumps({"birth_date": "33.12.1986"}),
                content_type='application/json',
            )
            self.assertEqual(response.status_code, 400)

    def test_11_patch_unknown(self):
        """Ensure error is thrown if unknown field"""
        with self.client:
            response = self.client.patch(
                '/imports/1/citizens/2',
                data=json.dumps({"citizen_id": 5}),
                content_type='application/json',
            )
            self.assertEqual(response.status_code, 400)

    def test_12_get_citizens(self):
        """3: GET citizens test"""
        response = self.client.get('/imports/1/citizens')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['data'])

    def test_13_get_incorrect(self):
        """Ensure error is thrown if the id does not exist."""
        response = self.client.get('/imports/0/citizens')
        self.assertEqual(response.status_code, 400)

    def test_14_birthdays(self):
        """4: birthdays test"""
        response = self.client.get('/imports/1/citizens/birthdays')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['data'])

    def test_15_birthdays_invalid(self):
        """Ensure error is thrown if the id does not exist."""
        response = self.client.get('/imports/0/citizens/birthdays')
        self.assertEqual(response.status_code, 400)

    def test_16_stat(self):
        """5: stats test"""
        response = self.client.get('/imports/1/towns/stat/percentile/age')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['data'])

    def test_17_stat_invalid(self):
        """Ensure error is thrown if the id does not exist."""
        response = self.client.get('/imports/0/towns/stat/percentile/age')
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
