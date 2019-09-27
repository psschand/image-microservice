import unittest
import requests
import uuid

BASE_URL = "http://127.0.0.1:8080"

class TestImageUpload(unittest.TestCase):
    def test_normal_upload(self):
        files = {'image': open('test_image.jpg', 'rb')}
        
        r = requests.request("POST", BASE_URL+'/images', files=files)

        assert(r.status_code == 201)

    def test_bad_image_key(self):
        files = {'bad_image_key': open('test_image.jpg', 'rb')}

        r = requests.request("POST", BASE_URL+'/images', files=files)

        assert(r.status_code == 400)

class TestImageDownload(unittest.TestCase):
    def setUp(self):
        files = {'image': open('test_image.jpg', 'rb')}
        
        r = requests.request("POST", BASE_URL+'/images', files=files)

        self.image_id = r.json()['image_id']

    def test_normal_download(self):
        r = requests.get(BASE_URL+'/images/'+self.image_id)

        assert(r.status_code == 200)

    def test_bad_uuid(self):
        r = requests.get(BASE_URL+'/images/not_a_uuid')

        assert(r.status_code == 400)

    def test_random_uuid(self):
        r = requests.get(BASE_URL+'/images/'+uuid.uuid4().hex)

        assert(r.status_code == 404)

class TestImageConversion(unittest.TestCase):
    def setUp(self):
        files = {'image': open('test_image.jpg', 'rb')}
        
        r = requests.request("POST", BASE_URL+'/images', files=files)

        self.image_id = r.json()['image_id']

    def test_png_conversion(self):
        url = BASE_URL+'/images/'+self.image_id+'.png'

        r = requests.get(url)

        assert(r.status_code == 200)

    def test_gif_conversion(self):
        url = BASE_URL+'/images/'+self.image_id+'.gif'

        r = requests.get(url)

        assert(r.status_code == 200)


if __name__ == '__main__':
    unittest.main()
