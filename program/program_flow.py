import sys
import pandas as pd

from sql_query import SqlRURIDT
from sql_query import SqlRNYUKN
from sql_query import SqlBTSZAN
from factory import *

class ProgramFlow:

    def __init__(self, sime_day):
        self.__df_sime = pd.DataFrame()
        self.__df_sale = pd.DataFrame()
        self.__df_deposit = pd.DataFrame()

        sql = SqlBTSZAN(sime_day)
        self.__df_sime = sql.fetch_sqldata()
        sql = SqlRURIDT(sime_day)
        self.__df_sale = sql.fetch_sqldata()
        sql = SqlRNYUKN(sime_day)
        self.__df_deposit = sql.fetch_sqldata()

        if not len(self.__df_sime):
            print(f'締め日({sime_day})のデータがありません')
            sys.exit()

        self.__customers = list(self.__df_sime.loc[:, 'TszTokCD'])
        # ['T0020', 'T0060', 'T0100',......]


    def start(self):
        factory = Factory(self.__df_sime, self.__df_sale, self.__df_deposit)
        sales_deposits = factory.create_sales_deposits(self.__customers)

        customers = []
        customers = factory.create_customer(self.__customers)

        invoices = []
        invoices = factory.create_invoice(self.__customers, sales_deposits)

        sales_deposits[1].show_me()



