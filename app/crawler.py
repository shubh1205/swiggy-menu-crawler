import csv
import logging
import sys

import requests


class Crawler():
    def __init__(self):
        args = sys.argv
        try:
            self.logger = self.get_logger()
            self.logger.info('Crawler Initialized')
            self.restaurant_id = args[1]
            self.base_url = 'https://www.swiggy.com/dapi/menu/pl?page-type=REGULAR_MENU&complete-menu=true&lat=18.55&lng=73.95&restaurantId='
            self.visited_ids = []
        except IndexError as e:
            self.logger.error(str(e))
            raise Exception('Please provide restaurant id as command line argument')
    
    def handle(self):
        try:
            self.logger.info('Script started')
            data = self.fetch_data()
            menu = self.get_menu(data)
            path = self.write_menu(menu)
            return path
        except Exception as e:
            self.logger.error(e)
            raise e
        finally:
            self.logger.info('Script ended')
    
    def get_logger(self):
        formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler = logging.FileHandler('logs/crawler.log', mode='a')
        handler.setFormatter(formatter)
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        return logger

    def fetch_data(self):
        self.logger.info('Fetching API data')
        url = self.base_url + self.restaurant_id
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
        response = requests.get(url, verify=False, headers=headers)
        if response.status_code != 200:
            raise Exception(f'Unable to fetch data {response.status_code}')
        
        response = response.json()
        return response['data'].get('cards', [])
    
    def get_menu(self, data):
        self.logger.info('Getting menu from API data')
        menu = []
        for section in data:
            if section.get('groupedCard'):
                menu.extend(
                    self.get_items(section.get('groupedCard', {}).get('cardGroupMap', {}))
                )
        return menu
    
    def get_items(self, card_group):
        items = []
        for cards in card_group.values():
            cards = cards['cards']
            for card in cards:
                card = card.get('card', {}).get('card', {})
                if card.get('@type', '') == 'type.googleapis.com/swiggy.presentation.food.v2.ItemCategory':
                    for item in card.get('itemCards', []):
                        if item.get('card', {}).get('@type', '') == 'type.googleapis.com/swiggy.presentation.food.v2.Dish':
                            item_info = item.get('card', {}).get('info', {})
                            if item_info.get('id') not in self.visited_ids:
                                items.append({
                                    'id': item_info.get('id'),
                                    'category': item_info.get('category'),
                                    'name': item_info.get('name'),
                                    'imageId': item_info.get('imageId'),
                                    'isVeg': item_info.get('isVeg', 0),
                                    'price': item_info.get('price')/100,
                                    'finalPrice': item_info.get('finalPrice'),
                                    'inStock': item_info.get('inStock', 0),
                                    'rating': item_info.get('ratings', {}).get('aggregatedRating', {}).get('rating'),
                                    'ratingCount': item_info.get('ratings', {}).get('aggregatedRating', {}).get('ratingCountV2'),
                                    'description': item_info.get('description')
                                })
                                self.visited_ids.append(item_info.get('id'))
        return items

    def write_menu(self, menu):
        self.logger.info('Writing TSV file')
        if len(menu):
            with open(f'csv_data_store/{self.restaurant_id}_flatten_menu.tsv', 'w') as file:
                writer = csv.DictWriter(file, delimiter='\t', fieldnames=menu[0].keys())
                writer.writeheader()
                writer.writerows(menu)
        return f'csv_data_store/{self.restaurant_id}_flatten_menu.tsv'

if __name__ == '__main__':
    try:
        crawler = Crawler()
        path = crawler.handle()
        print(f'Data exported successfully at path: {path}')
    except Exception as e:
        print(f'ERROR: {e}')
