from rest_framework.test import APIClient, APITestCase
from django.conf import settings

class BeneficiaryAPITest(APITestCase):
    def setUp(self):
        # Optionally, prepare a small CSV file content in memory or adjust settings.CSV_FILE_PATH to point to a test CSV.
        # For simplicity, write a small CSV string to a temp file:
        self.test_csv_path = settings.BASE_DIR / "test_beneficiaries.csv"
        with open(self.test_csv_path, 'w', encoding='utf-8', newline='') as f:
            f.write("Case_Number,HoH_Mobile,Alt_Mobile,first_name_ar,family_name_ar,id_number,Status\n")
            f.write("111,12345,,Ali,Khan,ID111,Active\n")
            f.write("112,67890,55555,Ahmed,Yousef,ID112,Inactive\n")
        settings.CSV_FILE_PATH = str(self.test_csv_path)
        self.client = APIClient()
        self.client.credentials(HTTP_X_API_KEY=settings.API_TOKEN)

    def test_Case_Number_filter(self):
        response = self.client.get('/api/beneficiaries/', {'Case_Number': '111'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['Case_Number'], "111")

    def test_phone_filter(self):
        # Search by phone that is primary
        resp1 = self.client.get('/api/beneficiaries/', {'phone': '67890'})
        self.assertEqual(len(resp1.json()), 1)
        self.assertEqual(resp1.json()[0]['Case_Number'], "112")
        # Search by phone that is alternative
        resp2 = self.client.get('/api/beneficiaries/', {'phone': '55555'})
        self.assertEqual(len(resp2.json()), 1)
        self.assertEqual(resp2.json()[0]['Case_Number'], "112")

    def test_name_filter(self):
        resp = self.client.get('/api/beneficiaries/', {'first_name': 'Ahmed', 'family_name': 'Yousef'})
        self.assertEqual(len(resp.json()), 1)
        self.assertEqual(resp.json()[0]['id_number'], "ID112")

    def test_id_filter_no_result(self):
        resp = self.client.get('/api/beneficiaries/', {'id_number': 'NONEXISTENT'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), [])

    def test_auth_failure(self):
        self.client.credentials()  # remove auth
        resp = self.client.get('/api/beneficiaries/', {'Case_Number': '111'})
        self.assertEqual(resp.status_code, 401)
