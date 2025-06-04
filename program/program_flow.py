import sys
from numpy import empty
import pandas as pd

from sql_query import SqlRURIDT
from sql_query import SqlRNYUKN
from sql_query import SqlBTSZAN
from sql_query import SqlMTOKUI
from factory import Factory

class ProgramFlow:

    def __init__(self, SIME_DAY, TAX_RATE)->None:
        self.__df_sime:pd.DataFrame = pd.DataFrame()
        self.__df_sale:pd.DataFrame = pd.DataFrame()
        self.__df_deposit:pd.DataFrame = pd.DataFrame()
        self.__df_customer:pd.DataFrame = pd.DataFrame()

        sql_zan:SqlBTSZAN = SqlBTSZAN(SIME_DAY)
        self.__df_sime:pd.DataFrame = sql_zan.fetch_sqldata()
        sql_uri:SqlRURIDT = SqlRURIDT(SIME_DAY)
        self.__df_sale:pd.DataFrame = sql_uri.fetch_sqldata()
        sql_iri:SqlRNYUKN = SqlRNYUKN(SIME_DAY)
        self.__df_deposit:pd.DataFrame = sql_iri.fetch_sqldata()
        sql_tokui:SqlMTOKUI = SqlMTOKUI()
        self.__df_customer:pd.DataFrame = sql_tokui.fetch_sqldata()
        self.__TAX_RATE = TAX_RATE


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
        sales_deposits = factory.create_sales_deposits(self.__customers)
        # SalesDepositsの配列

        customers:list = []
        customers = factory.create_customer(self.__customers)

        invoices:list = []
        invoices = factory.create_invoice(self.__customers, 
                            sales_deposits, customers, self.__TAX_RATE)
        

        for invoice in invoices:
            invoice.filling_page_invoice()

        print('請求書をExcelファイルで作成しました')



