"""Production Testing of API"""

import unittest
import time
import requests
from src.proxy import NGINXConfig


URL = "https://dcong.page/covid-data"


class TestEndPointAgeGroup(unittest.TestCase):
    """Testing Age Group End Points"""

    def test_age_group_total(self):
        """/age/total end point"""
        response = requests.get(f"{URL}/age/total")
        self.assertEqual(response.status_code, 200)
        self.assertTrue('AgeGroup_25-29' in response.json())

    def test_age_group(self):
        """/age/25-29 end point"""
        response = requests.get(f"{URL}/age/25-29")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("2022-01-01" in response.json())  # arbitrary. assumes that a datapoint exists for this date.
        self.assertGreater(len(response.json()), 1)



class TestEndPointLocationGroup(unittest.TestCase):
    """Testing Location End Points"""

    def test_location_list(self):
        """Test location/<type> endpoint"""
        response_postcode = requests.get(f"{URL}/location/postcode")
        response_lhd = requests.get(f"{URL}/location/lhd")
        response_lga = requests.get(f"{URL}/location/lga")
        self.assertEqual(response_postcode.status_code, 200)
        self.assertEqual(response_lhd.status_code, 200)
        self.assertEqual(response_lga.status_code, 200)
        self.assertGreater(len(response_postcode.json()), 1)
        self.assertGreater(len(response_lhd.json()), 1)
        self.assertGreater(len(response_lga.json()), 1)

    def test_location_postcode(self):
        """Test location/postcode/<postcode>"""
        response = requests.get(f"{URL}/location/postcode/2000")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 1)
        self.assertTrue("2022-01-01" in response.json())  # arbitrary date

    def test_location_lhd_name(self):
        """Test location/lhd/<name>"""
        response = requests.get(f"{URL}/location/lhd/Western NSW")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 1)
        self.assertTrue("2022-01-01" in response.json())  # arbitrary date

    def test_location_lhd_code(self):
        """Test location/lhd/<code>"""
        response = requests.get(f"{URL}/location/lhd/X850")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 1)
        self.assertTrue("2022-01-01" in response.json())  # arbitrary date

    def test_location_lga_name(self):
        """Test location/lga/<name>"""
        response = requests.get(f"{URL}/location/lga/Ku-ring-gai (A)")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 1)
        self.assertTrue("2022-01-01" in response.json())  # arbitrary date

    def test_location_lga_code(self):
        """Test location/lga/<code>"""
        response = requests.get(f"{URL}/location/lga/14500")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 1)
        self.assertTrue("2022-01-01" in response.json())  # arbitrary date
        time.sleep(5)  # this stops the API crashing from repeating API calls. Arbitary location of the sleep command


class TestEndPointTests(unittest.TestCase):
    """Testing Tests endpoints"""

    def test_tests_list(self):
        """Test tests/<type> endpoint"""
        response_postcode = requests.get(f"{URL}/tests/postcode")
        response_lhd = requests.get(f"{URL}/tests/lhd")
        response_lga = requests.get(f"{URL}/tests/lga")
        self.assertEqual(response_postcode.status_code, 200)
        self.assertEqual(response_lhd.status_code, 200)
        self.assertEqual(response_lga.status_code, 200)
        self.assertGreater(len(response_postcode.json()), 1)
        self.assertGreater(len(response_lhd.json()), 1)
        self.assertGreater(len(response_lga.json()), 1)

    def test_tests_postcode(self):
        """Test tests/postcode/<postcode>"""
        response = requests.get(f"{URL}/tests/postcode/2000")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 1)
        self.assertTrue("2022-01-01" in response.json())  # arbitrary date

    def test_tests_lhd_name(self):
        """Test tests/lhd/<name>"""
        response = requests.get(f"{URL}/tests/lhd/Western NSW")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 1)
        self.assertTrue("2022-01-01" in response.json())  # arbitrary date

    def test_tests_lhd_code(self):
        """Test tests/lhd/<code>"""
        response = requests.get(f"{URL}/tests/lhd/X850")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 1)
        self.assertTrue("2022-01-01" in response.json())  # arbitrary date

    def test_tests_lga_name(self):
        """Test tests/lga/<name>"""
        response = requests.get(f"{URL}/tests/lga/Ku-ring-gai (A)")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 1)
        self.assertTrue("2022-01-01" in response.json())  # arbitrary date

    def test_tests_lga_code(self):
        """Test tests/lga/<code>"""
        response = requests.get(f"{URL}/tests/lga/14500")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 1)
        self.assertTrue("2022-01-01" in response.json())  # arbitrary date
