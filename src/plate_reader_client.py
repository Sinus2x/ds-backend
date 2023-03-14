import requests
import json
from typing import List


class PlateReaderClient:
    def __init__(self, host: str):
        self.host = host

    def _process_response(self, res):
        if not res.ok:
            return f'Error {res.status_code}: {res.text}'
        return res.json()

    def read_plate_number(self, im):
        res = requests.post(
            f'{self.host}/readPlateNumber',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=im
        )
        return self._process_response(res)

    def read_number_by_id(self, id: str):
        res = requests.get(
            f'{self.host}/readNumberByID',
            json={
                'id': id
            }
        )
        return self._process_response(res)

    def read_numbers_by_id(self, ids: List[str]):
        res = requests.get(
            f'{self.host}/readNumbersByID',
            data={
                'ids': ids
            }
        )
        return self._process_response(res)

    def greeting(self, user: str):
        res = requests.post(
            f'{self.host}/readPlateNumber',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            json={
                'user': user,
            },
        )
        return self._process_response(res)


if __name__ == '__main__':
    client = PlateReaderClient(host='http://127.0.0.1:8080')
    with open('./images/9965.jpg', 'rb') as im:
        res = client.read_plate_number(im)
        print(res)
        res = client.read_number_by_id('10022')
        print(res)
        res = client.read_numbers_by_id(['10022', '9965'])
        print(res)