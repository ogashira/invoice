import openpyxl
import yaml
import platform
import pandas as pd
from typing import List 

class MailInfo(object):
    '''
    顧客のEmailAddressの情報を得る
    send_invoice_main.pyの実行時コマンドライン引数"test"を与えると、
    テスト用のEmailAddressの情報を得る
    '''

    def __init__(self, isTest:bool)-> None:

        start_path: str = ""
        if platform.system() == 'Windows':
            start_path = r'//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/02請求書/01Master/'
        if platform.system() == 'Linux':
            start_path = r'/mnt/public/営業課ﾌｫﾙﾀﾞ/02請求書/01Master/'

        book_name: str = r'email_address.xlsx'
        if isTest:
            book_name = r'test_email_address.xlsx'

        self.__book_path: str = fr'{start_path}{book_name}'

        #ﾒｰﾙ送信先情報のﾃﾞｰﾀを取得

    def get_mail_infos(self)-> pd.DataFrame:
        mail_infos = pd.read_excel(self.__book_path, sheet_name='mail')
        mail_infos = mail_infos.fillna('')

        return mail_infos


    def get_yaml_data(self):
        yaml_path = './'
        if platform.system() == 'Windows':
            yaml_path = r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/coaﾒｰﾙ送信関連/mail_info.yaml'
        if platform.system() == 'Linux':
            yaml_path = r'/mnt/public/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/coaﾒｰﾙ送信関連/mail_info.yaml'
        if platform.system() == 'Darwin':
            yaml_path = r'/Volumes/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/coaﾒｰﾙ送信関連/mail_info.yaml'

        with open(yaml_path, 'r') as file:
            yaml_data = yaml.safe_load(file)

        return yaml_data

