import os
import unittest
import tempfile
from backend.src.app import vital_app


class TestBackendEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = vital_app.test_client()
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        self.temp_file.write(b"column1,column2\nvalue1,value2\n")
        self.temp_file.close()

    def tearDown(self):
        os.unlink(self.temp_file.name)

    # test @vital_app.route('/') route
    def test_home_route(self):

        # Test GET response
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        # print(response.data)

        # Test POST response
        # Open the CSV file to be sent with the request
        with open(self.temp_file.name, 'rb') as csv_file:
            # Create the file payload
            data = {'csv_file': (csv_file, 'test.csv')}  # pass empty CSV

            # Send a POST request to the endpoint
            response = self.app.post('/', data=data, content_type='multipart/form-data')
            # print(response.data)

            # Check if the response status code is 200 (or any other expected status code)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['File Accepted'], True)

    # test @vital_app.route('/process') route
    def test_process_route(self):

        # Test POST response
        # Open the CSV file to be sent with the request
        with open('test_data/Acceleration_with_g_2024-03-02_19-59-46_cat_27.csv', 'rb') as csv_file:
            # Create the file payload
            data = {'csv_file': (csv_file, 'test.csv')}  # pass empty CSV

            # Send a POST request to the endpoint
            response = self.app.post('/process', data=data, content_type='multipart/form-data')

            # Check if the response status code is 200 (or any other expected status code)
            self.assertEqual(response.status_code, 200)
            print(response.data)


if __name__ == '__main__':
    unittest.main()


