import sys
import pandas as pd
from typing import Dict

from sql_query import ISelectData, SqlRURIDT
from sql_query import SqlRNYUKN
from sql_query import SqlBTSZAN
from sql_query import SqlMTOKUI
from sql_query import SqlMTANIM
from sql_query import SqlMTORIK
from factory import Factory

class ProgramFlow:

    def __init__(self, SIME_DAY:str, TAX_RATE:str)->None:

        self.__df_sime:pd.DataFrame = pd.DataFrame()
        self.__df_sale:pd.DataFrame = pd.DataFrame()
        self.__df_deposit:pd.DataFrame = pd.DataFrame()
        self.__df_customer:pd.DataFrame = pd.DataFrame()

        sql_zan:ISelectData = SqlBTSZAN(SIME_DAY)
        self.__df_sime:pd.DataFrame = sql_zan.fetch_sqldata()
        sql_uri:ISelectData = SqlRURIDT(SIME_DAY)
        self.__df_sale:pd.DataFrame = sql_uri.fetch_sqldata()
        sql_iri:ISelectData = SqlRNYUKN(SIME_DAY)
        self.__df_deposit:pd.DataFrame = sql_iri.fetch_sqldata()
        sql_tokui:ISelectData = SqlMTOKUI()
        self.__df_customer:pd.DataFrame = sql_tokui.fetch_sqldata()
        self.__TAX_RATE = TAX_RATE
        sql_tani:ISelectData = SqlMTANIM()
        df_tani:pd.DataFrame = sql_tani.fetch_sqldata()
        # dfを辞書に変換
        self.tani_code:Dict = dict(zip(df_tani['TniTniCD'],
                                                df_tani['TniTniNam']))

        sql_mtorik:ISelectData = SqlMTORIK()
        df_nyuukin_kubun:pd.DataFrame = sql_mtorik.fetch_sqldata()
        # dfを辞書に変換
        self.nyuukin_kubun:Dict = dict(zip(df_nyuukin_kubun['TrkTrkKBN'],
                                             df_nyuukin_kubun['TrkNam']))


        if not len(self.__df_sime):
            print(f'締め日({SIME_DAY})のデータがありません')
            sys.exit()

        self.__customers:list = list(self.__df_sime.loc[:, 'TszTokCD'])
        # ['T0020', 'T0060', 'T0100',......] 締め日に該当する全顧客リスト


    def start(self)->None:

        print('請求書を作成しています。しばらくお待ちください....')
        factory:Factory = Factory(self.__df_sime, self.__df_sale, 
                                self.__df_deposit, self.__df_customer)

        sales_deposits:list = []
        sales_deposits = \
        factory.create_sales_deposits(self.__customers, 
                                      self.tani_code, self.nyuukin_kubun)
        # SalesDepositsの配列

        customers:list = []
        customers = factory.create_customer(self.__customers)

        invoices:list = []
        invoices = factory.create_invoice(self.__customers, 
                            sales_deposits, customers, self.__TAX_RATE)
        
        #請求書をexcelファイルで作成する
        cnt:int = 0
        for invoice in invoices:
            invoice.filling_page_invoice()
            cnt += 1
            print(f'{cnt}/{len(invoices)}個の請求書を作成しました。')

        print('請求書全てをExcelとPdfで作成しました')

        # 請求書をpdfに変換する



