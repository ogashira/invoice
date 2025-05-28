import sys
import pandas as pd

from sql_query import SqlRURIDT
from sql_query import SqlRNYUKN
from sql_query import SqlBTSZAN
from sql_query import SqlMTOKUI
from factory import *
from excel import *

class ProgramFlow:

    def __init__(self, sime_day, TAX_RATE):
        self.__df_sime = pd.DataFrame()
        self.__df_sale = pd.DataFrame()
        self.__df_deposit = pd.DataFrame()
        self.__df_customer = pd.DataFrame()

        sql = SqlBTSZAN(sime_day)
        self.__df_sime = sql.fetch_sqldata()
        sql = SqlRURIDT(sime_day)
        self.__df_sale = sql.fetch_sqldata()
        sql = SqlRNYUKN(sime_day)
        self.__df_deposit = sql.fetch_sqldata()
        sql = SqlMTOKUI()
        self.__df_customer = sql.fetch_sqldata()
        self.__TAX_RATE = TAX_RATE


        if not len(self.__df_sime):
            print(f'締め日({sime_day})のデータがありません')
            sys.exit()

        self.__customers = list(self.__df_sime.loc[:, 'TszTokCD'])
        # ['T0020', 'T0060', 'T0100',......] 締め日に該当する全顧客リスト


    def start(self):
        factory = Factory(self.__df_sime, self.__df_sale, 
                                self.__df_deposit, self.__df_customer)
        sales_deposits = factory.create_sales_deposits(self.__customers)

        customers = []
        customers = factory.create_customer(self.__customers)

        invoices = []
        invoices = factory.create_invoice(self.__customers, 
                            sales_deposits, customers, self.__TAX_RATE)
        
        

        for invoice in invoices:
            invoice.filling_page_invoice()



