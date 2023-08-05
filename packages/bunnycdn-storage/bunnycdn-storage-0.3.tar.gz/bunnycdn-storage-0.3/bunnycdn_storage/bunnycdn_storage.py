import requests

class BunnyCDNStorage:
    """docstring for BunnyCDNStorage"""
    def __init__(self, storage_zone, access_token, pullzone_url, storage_zone_region="de", debug=False):
        self._storage_zone = storage_zone
        self._access_token = access_token
        self._storage_zone_region = storage_zone_region
        self._pullzone_url = pullzone_url
        if not pullzone_url.endswith('/'):
            self._pullzone_url += '/'
        self._DEBUG = debug

    def _get_base_url(self):
        """Returns the base URL with the endpoint based on the current storage zone region"""
        if self._DEBUG:
            return 'https://private-anon-09a61cdb75-bunnycdnstorage.apiary-mock.com/{}/'.format(self._storage_zone)

        if self._storage_zone_region == 'de':
            return 'https://storage.bunnycdn.com/{}/'.format(self._storage_zone)
        else:
            return 'https://{}.bunnycdn.com/{}/'.format(self._storage_zone_region, self._storage_zone)

    def _get_pullzone_base_url(self):
        return self._pullzone_url

    def _normalize_path(self, path, is_directory=False):
        """Normalize a path string"""
        if is_directory and not path.endswith('/'):
                path += '/'
        path = path.replace('//', '/')
        path = path.lstrip('/')
        return path

    def _send_http_request(self, path, method, payload=None, data_length=None):
        url = '{}{}'.format(self._get_base_url(), path)
        headers = { 'AccessKey' : self._access_token }
        if method == 'PUT' and payload and data_length: 
            headers.update({
                'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                'Content-Length' : data_length
                })
            r = requests.put(url, headers=headers, data=payload)
        elif method == 'DELETE':
            r = requests.delete(url, headers=headers)
        else:
            r = requests.get(url, headers=headers)

        r.raise_for_status()
        return r.content
        

    def get_storage_objects(self, path):
        """Get the list of storage objects on the given path"""
        path = self._normalize_path(path, is_directory=True)
        return self._send_http_request(path, 'GET')

    def delete_object(self, path):
        """Delete an object at the given path. If the object is a directory, the contents will also be deleted."""
        path = self._normalize_path(path)
        return self._send_http_request(path, 'DELETE')

    def upload_file(self, local_path, path):
        """Upload a local file to the storage"""
        payload = None
        with open(local_path, 'rb') as f:
            payload = f.read()

        path = self._normalize_path(path)
        data_length = str(len(payload))

        return self._send_http_request(path, 'PUT', payload=payload, data_length=data_length)

    def download_file(self, path, local_path):
        """Download the object to a local file"""
        path = self._normalize_path(path)
        content = self._send_http_request(path, 'GET')
        with open(local_path, 'wb') as f:
            f.write(content)

    def object_exists(self, path):
        """Check if object is exists"""
        path = self._normalize_path(path)
        url = '{}{}'.format(self._get_pullzone_base_url(), path)
        r = requests.head(url)
        return r.status_code == 200
