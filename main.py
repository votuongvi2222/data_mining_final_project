import requests
from utils.crawler.crawler import Crawler
# import urllib
# import httplib2
from utils.crawler.data import text_formater, writer, reader
from utils.brand.category.category import Category
import csv
import re
import json
import pandas as pd
import os

HEADERS = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}
# HEADERS = {
#     "accept": "*/*",
#     "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-origin",
#     "x-api-source": "pc",
#     "x-requested-with": "XMLHttpRequest",
#     "x-shopee-language": "vi",
#     "cookie": "votuongvi"
# }
        
WEB_URL = 'https://shopee.vn/'
MALL_ALL_BRANDS_URL = 'https://shopee.vn/mall/brands/'
MALL_BRAND_URL = 'https://shopee.vn{}'
GET_SHOP_CATEGORIES = 'https://shopee.vn/api/v2/shop/get_categories?limit={}&offset={}&shopid={}'
GET_SHOP_DETAIL = 'https://shopee.vn/api/v4/shop/get_shop_detail?username={}'
GET_SHOP_PRODUCTS = 'https://shopee.vn/api/v4/search/search_items?by=pop&limit={}&match_id={}&newest={}&order=sales&page_type=shop&scenario=PAGE_OTHERS&version=2'
GET_PRODUCT_DETAIL_V2 = 'https://shopee.vn/api/v2/item/get?itemid={}&shopid={}'
GET_PRODUCT_DETAIL_V4 = 'https://shopee.vn/api/v4/item/get?itemid={}&shopid={}'
GET_PRODUCT_RATINGS = 'https://shopee.vn/api/v2/item/get_ratings?filter=0&flag=1&itemid={}&limit={}&offset={}&shopid={}&type=0'

def getText(curElement):

    elementText = curElement.text

    if not elementText:
        elementText = curElement.get_attribute("innerText")

    if not elementText:
        elementText = curElement.get_attribute("textContent")
    return elementText

def get_all_product_categories(): 
    categories = []
    crawler = Crawler()
    mall_brands_page = crawler.get_raw_content(MALL_ALL_BRANDS_URL)
    if mall_brands_page:
        for category in crawler.get_tags_by_css_selector(None, 'li.official-shop-brand-list__category-item'):
            # print('Category: ',category)
            category_link = crawler.get_tags_by_css_selector(category, 'a.official-shop-brand-list__category-link')[0].get_attribute('href')
            category_name = getText(crawler.get_tags_by_css_selector(category, 'div.official-shop-brand-list__category-name')[0])
            _category = Category(
                title=category_name,
                link=category_link
            )
            categories.append(_category)
            # writer.to_txt('category_links.txt', str(text_formater.format_text(category_link)) + '\n', mode='a+')
    return categories

def get_brands(category, limit=10):
    crawler = Crawler()
    brands = []
    count = 0
    category_page = crawler.get_raw_content(category.link)
    if category_page:
        for brand in crawler.get_tags_by_css_selector(None, 'div.full-brand-list-item')[::5]:
            if count >= limit:
                break
            link = crawler.get_tags_by_css_selector(brand, 'a.full-brand-list-item__brand-cover-image')[0].get_attribute('href')
            print('======\n',link, link.split('/'))
           
            if len(link.split('/')) > 4:
                continue
            count = count + 1

            name = getText(crawler.get_tags_by_css_selector(brand, 'div.full-brand-list-item__brand-name')[0])
            username = link.split('/')[-1]
            category_name = category.title
            response_brand = requests.get(GET_SHOP_DETAIL.format(username), headers=HEADERS)
            if response_brand.status_code != 200:
                break
            data = json.loads(response_brand.text)['data']
            try:
                response_categories = requests.get(GET_SHOP_CATEGORIES.format(100, 0, data["shopid"]), headers=HEADERS)
                
                categories = json.loads(response_categories.text)['data']['items']
            except:
                categories = []

            _brand = {
                'username': username,
                'name': name,
                'link': link,
                'category': category_name,
                'country': data['country'],
                'shop_location': data['shop_location'],
                'user_id': data['userid'],
                'shop_id': data['shopid'],
                'cancellation_rate': data['cancellation_rate'],
                'response_rate': data['response_rate'],
                'rating_normal': data['rating_normal'],
                'rating_bad': data['rating_bad'],
                'rating_good': data['rating_good'],
                'total_avg_star': data['account']['total_avg_star'],
                'follower_count': data['follower_count'],
                'following_count': data['account']['following_count'],
                'item_count': data['item_count'],
                'product_categories': categories
            }
            brands.append(_brand)
            # writer.to_txt('category_links.txt', str(text_formater.format_text(category_link)) + '\n', mode='a+')
    return brands

def save_brands_to_csv(brands):
     
    with open('./out/ShopeeMall.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                'index',
                'name',
                'link',
                'category',
                'country',
                'shop_location',
                'user_id',
                'shop_id',
                'cancellation_rate',
                'response_rate',
                'rating_normal',
                'rating_bad',
                'rating_good',
                'total_avg_star',
                'follower_count',
                'following_count',
                'item_count'
            ]
        )
        index = 0
        for brand in brands:
            print(brand['name'])
            writer.writerow(
                [
                    index,
                    brand['name'],
                    brand['link'],
                    brand['category'],
                    brand['country'],
                    brand['shop_location'],
                    brand['user_id'],
                    brand['shop_id'],
                    brand['cancellation_rate'],
                    brand['response_rate'],
                    brand['rating_normal'],
                    brand['rating_bad'],
                    brand['rating_good'],
                    brand['total_avg_star'],
                    brand['follower_count'],
                    brand['following_count'],
                    brand['item_count']
                ]
            )
            index = index + 1
        
def get_products_per_brand(limit=100, shop_ids=[], offset=0):
    for shop_id in shop_ids:
        products = []

        print(limit, shop_id, offset, GET_SHOP_PRODUCTS.format(limit, shop_id, offset))
        crawler = Crawler()
        shop_page = crawler.get_raw_content(GET_SHOP_PRODUCTS.format(limit, shop_id, offset))
        if shop_page:
            shop_products = getText(crawler.get_tags_by_css_selector(None, 'pre')[0])

            items = json.loads(shop_products)['items']
            # print(items[0])
            # break
            for item_basic in items:
                item=item_basic['item_basic']
                product = {
                    'item_id': item["itemid"],
                    'shop_id': item["shopid"],
                    'name': item["name"],
                    'sold': item["sold"],
                    'historical_sold': item["historical_sold"],
                    'liked_count': item["liked_count"],
                    'cmt_count': item["cmt_count"],
                    'price': item["price"],
                    'price_min': item["price_min"],
                    'price_max': item["price_max"],
                    'rating_star': item["item_rating"]["rating_star"],
                    'start1': item["item_rating"]["rating_count"][1],
                    'start2': item["item_rating"]["rating_count"][2],
                    'start3': item["item_rating"]["rating_count"][3],
                    'start4': item["item_rating"]["rating_count"][4],
                    'start5': item["item_rating"]["rating_count"][5],
                    'rcount_with_context': item["item_rating"]["rcount_with_context"],
                    'rcount_with_image': item["item_rating"]["rcount_with_image"]
                }
                products.append(product)
        save_products_to_csv('./out/products/Products-{}.csv'.format(shop_id), products)

def save_products_to_csv(fn, products):
    with open(fn, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                'index',
                'item_id',
                'shop_id',
                'name',
                'sold',
                'historical_sold',
                'liked_count',
                'cmt_count',
                'price',
                'price_min',
                'price_max',
                'rating_star',
                'start1',
                'start2',
                'start3',
                'start4',
                'start5',
                'rcount_with_context',
                'rcount_with_image'
            ]
        )
        index = 0
        for product in products:
            writer.writerow(
                [
                    index,
                    product['item_id'],
                    product['shop_id'],
                    product['name'],
                    product['sold'],
                    product['historical_sold'],
                    product['liked_count'],
                    product['cmt_count'],
                    product['price'],
                    product['price_min'],
                    product['price_max'],
                    product['rating_star'],
                    product['start1'],
                    product['start2'],
                    product['start3'],
                    product['start4'],
                    product['start5'],
                    product['rcount_with_context'],
                    product['rcount_with_image']

                ]
            )
            index = index + 1
        
def get_comments_per_brand(shop_ids=[]):
    for shop_id in shop_ids:
        df_shop = pd.read_csv('./out/products/Products-{}.csv'.format(shop_id))
        comments = []   
        crawler = Crawler()

        for i in df_shop.index:
            try:
                item_id = df_shop['item_id'][i]
                total = df_shop['cmt_count'][i]
                count = 0

                while count <= total and count <= 200:

                    print(GET_PRODUCT_RATINGS.format(item_id, 30, count, shop_id))

                    product_page = crawler.get_raw_content(GET_PRODUCT_RATINGS.format(item_id, 30, count, shop_id))
                    count = count + 30
                    if product_page:
                        product_comments = getText(crawler.get_tags_by_css_selector(None, 'pre')[0])

                        ratings = json.loads(product_comments)['data']['ratings']

                        for rating in ratings:
                            comment = {
                                'order_id': rating["orderid"],
                                'item_id': rating["itemid"],
                                'cmt_id': rating["cmtid"],
                                'user_id': rating["userid"],
                                'comment': rating["comment"],
                                'rating_star': rating["rating_star"],
                                'author_username': rating["author_username"],
                                'anonymous': rating["anonymous"]
                            }
                            comments.append(comment)
                # print(comments)
            except:
                continue
        save_comments_to_csv('./out/comments/Comments-{}.csv'.format(shop_id), comments)
   
def save_comments_to_csv(fn, comments):
    with open(fn, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                'index',
                'order_id',
                'item_id',
                'cmt_id',
                'user_id',
                'comment',
                'rating_star',
                'author_username',
                'anonymous'
            ]
        )
        index = 0
        for comment in comments:
            writer.writerow(
                [
                    index,
                    comment['order_id'],
                    comment['item_id'],
                    comment['cmt_id'],
                    comment['user_id'],
                    comment['comment'],
                    comment['rating_star'],
                    comment['author_username'],
                    comment['anonymous']
                ]
            )
            index = index + 1

           
if __name__ == '__main__':
    # categories = get_all_product_categories()
    # all_brands = []

    # for category in categories:
    #     brands = get_brands(category, limit=5)

    #     all_brands = all_brands + brands

    # save_brands_to_csv(all_brands)

    df = pd.read_csv('./out/ShopeeMall.csv')
    # get_products_per_brand(100, df.shop_id[108:], 0)
    # print(df.shop_id[:106])
    crawled_shop_ids = []
    for shop_id in df.shop_id:
        fn = './out/products/Products-{}.csv'.format(shop_id)
        file_exists = os.path.isfile(fn)
        if(file_exists):
            crawled_shop_ids.append(shop_id)
    
    # print(crawled_shop_ids[39:])
    get_comments_per_brand(crawled_shop_ids[39:])




