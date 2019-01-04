import requests
import json
from bs4 import BeautifulSoup


class Scrape:

    def __init__(self, USERNAME):
        REQ = requests.Session()

        print('Getting User ID..')
        USERID = self.GET_USERID(USERNAME, REQ)
        if USERID == False:
            print('User ID not found, try again..')
            return

        print('Getting Product list..')
        PRODUCTS = self.GET_PRODUCTS(USERID, REQ)
        if PRODUCTS == False:
            print('Product list not found, try again..')
            return

        #
        # for product in PRODUCTS:
        #     print('Product name: {}'.format(product['name']))
        # ----------------------------------------------------------
        # Now you can get any products data from the seller profile and only use the USERNAME
        # Just write a code like above then you either save it on .csv or json format
        #

        print('Saving hTML page..')
        self.SAVE_PAGE(USERNAME, REQ)

        print('Complete...')

    def SAVE_PAGE(self, USERNAME, REQ):
        URL = "https://shopee.co.id/{}".format(USERNAME)

        RESPONSE = REQ.get(URL)
        SOUP = BeautifulSoup(RESPONSE.content, 'html.parser')

        # Save HTML content to file
        FILE_NAME = 'Shopee_{}.html'.format(USERNAME)

        with open(FILE_NAME, 'w') as file:
            return file.write(SOUP.prettify())

    def GET_USERID(self, USERNAME, REQ):
        HEADERS = {
            "accept-encoding": "gzip, deflate, br",
            "content-type": "application/json",
            "if-none-match": "55b03-1ae7d4aa7c47753a96c0ade3a9ea8b35",
            "origin": "https://shopee.co.id",
            "referer": "https://shopee.co.id/asusofficialshop",
            "x-api-source": "pc",
            "x-csrftoken": "8XtQ7bHlv09rlx5U4NPN6rmavFn7MvTO",
            "x-requested-with": "XMLHttpRequest",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "cookie": 'SPC_IA=-1; SPC_EC=-; SPC_F=QpolQhTSikpnxRXO6T4RjIW8ZGHNBmBn; REC_T_ID=ac80cdde-0e7d-11e9-a8c2-3c15fb3af585; SPC_T_ID="e4t1VmH0VKB0NajA1BrHaDQlFRwWjTZT7o83rrHW+p16sTf1NJK7ksWWDicCTPq8CVO/S8sxnw25gNR0DLQz3cv7U3EQle9Z9ereUnPityQ="; SPC_SI=k2en4gw50emawx5fjaawd3fnb5o5gu0w; SPC_U=-; SPC_T_IV="in3vKQSBLhXzeTaGwMInvg=="; _gcl_au=1.1.557205539.1546426854; csrftoken=8XtQ7bHlv09rlx5U4NPN6rmavFn7MvTO; welcomePkgShown=true; bannerShown=true; _ga=GA1.3.472488305.1546426857; _gid=GA1.3.1348013297.1546426857; _fbp=fb.2.1546436170115.11466858'
        }

        URL = "https://shopee.co.id/api/v1/shop_ids_by_username/"
        DATA = {
            "usernames": [USERNAME]
        }
        GET_DATA = REQ.post(URL, headers=HEADERS, json=DATA)
        RESULT = GET_DATA.json()
        USERID = RESULT[0][USERNAME]

        return USERID

    def GET_PRODUCTS(self, USERID, REQ):
        HEADERS = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }

        URL = 'https://shopee.co.id/api/v2/search_items/?match_id={}&order=desc&page_type=shop'.format(
            USERID
        )

        GET_DATA = REQ.get(URL, headers=HEADERS)
        RESULT = GET_DATA.json()

        # Save JSON content to file
        FILE_NAME = 'Shopee_{}.json'.format(USERID)
        with open(FILE_NAME, 'w') as file:
            json.dump(RESULT, file)

        return RESULT['items']


URL = input('Paste the username here: ')
Scrape(URL)
