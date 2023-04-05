import sys
import traceback

import requests


class Crawler():
    def __init__(self):
        args = sys.argv
        try:
            self.restaurant_id = args[1]
            self.base_url = 'https://www.swiggy.com/dapi/menu/pl?page-type=REGULAR_MENU&complete-menu=true&lat=18.56&lng=73.95&restaurantId='
        except IndexError:
            raise Exception('Please provide restaurant id as command line argument')
    
    def handle(self):
        data = self.fetch_data()
        menu = self.get_menu(data)
        self.write_menu(menu)

    def fetch_data(self):
        url = self.base_url + self.restaurant_id
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f'Unable to fetch data {response.status_code}')
        
        response = response.json()
        return response['data'].get('cards', [])
    
    def get_menu(self, data):
        pass

    def write_menu(self, menu):
        pass

if __name__ == '__main__':
    try:
        crawler = Crawler()
        crawler.handle()
    except Exception as e:
        print(f'ERROR: {e}')