import platform
import pandas as pd
import yaml
import sys
from typing import List, Dict

from deposit import Deposit
from sale import Sale
from sales_deposits import SalesDeposits
from customer import Customer
from invoice import Invoice
from excel import Excel


class Factory:
    """
    インスタンスを生成する
    Attributes:
        __df_sime (pd.DataFrame) : 締め日のデータフレーム
        __df_sale (pd.DataFrame) : 売上のデータフレーム
        __df_deposit (pd.DataFrame) : 入金のデータフレーム
        __df_customer (pd.DataFrame) : 得意先マスタのデータフレーム
    """

    def __init__(self, df_sime: pd.DataFrame, df_sale: pd.DataFrame, 
                 df_deposit: pd.DataFrame, df_customer: pd.DataFrame)->None:
        self.__df_sime = df_sime
        self.__df_sale = df_sale
        self.__df_deposit = df_deposit
        self.__df_customer = df_customer

        path:str = r'//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/02請求書/01Master/invoice.yaml'
        if platform.system() == 'Linux':
            path = r'/mnt/public/営業課ﾌｫﾙﾀﾞ/02請求書/01Master/invoice.yaml'
        with open(path, 'r', encoding='utf-8') as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)
        self.__instance_index_row = yaml_data['instanceIndex_saleExcelRow']

        email_path: str = \
        r'//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/02請求書/01Master/email_address.xlsx'
        if platform.system() == 'Linux':
            email_path = \
            r'/mnt/public/営業課ﾌｫﾙﾀﾞ/02請求書/01Master/email_address.xlsx'

        args: List[str] = sys.argv
        if len(args) > 1 and (args[1] == "test" or args[1] == "TEST"):
            email_path: str = \
            r'//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/02請求書/01Master/test_email_address.xlsx'
            if platform.system() == 'Linux':
                email_path = \
                r'/mnt/public/営業課ﾌｫﾙﾀﾞ/02請求書/01Master/test_email_address.xlsx'

        self.__email_info:pd.DataFrame = pd.read_excel(email_path, sheet_name='mail')
        

    def create_sales_deposits(self, customers:list, 
                              tani_code: Dict, nyuukin_kubun: Dict)-> list:
        '''
        SalesDepositsクラスのインスタンスを作る
        SaleクラスのインスタンスとDepositクラスのインスタンスを
        作って、SalesDepositsクラスに渡す。同時に売上日、入金日の集合
        も作って、SalesDepositsクラスに渡す

        Args:
            customers (list) : 顧客コードのリスト
        Returns:
            sales_deposits(list) : SalesDepositクラスのインスタンスのリスト
        '''
        sales_deposits:list = []
        for customer_code in customers:  # customer_code => 'TokSeikyuCD'
            df_of_customer_sale = (
                            self.__df_sale[self.__df_sale['RurSeiCD'] 
                            == customer_code])
            df_of_customer_deposit = (
                         self.__df_deposit[self.__df_deposit['RnySeiCD'] 
                         == customer_code])
            sales:object = []
            deposits:object = []
            sales_deposits_date_set = set()
            if df_of_customer_sale is not None:
                for i in range(len(df_of_customer_sale)): # Seriesにしてから取り出す
                    sale_no:str    = df_of_customer_sale.iloc[i,:]['RurUNo']
                    sale_date:str  = df_of_customer_sale.iloc[i,:]['RurUriDay']
                    hinban:str     = df_of_customer_sale.iloc[i,:]['RurHinCD']
                    hinmei:str     = df_of_customer_sale.iloc[i,:]['RurHinNam']
                    sale_qty:int   = df_of_customer_sale.iloc[i,:]['RurKoSu']
                    tani:str       = df_of_customer_sale.iloc[i,:]['RurUriTniCD']
                    unit_price:int = df_of_customer_sale.iloc[i,:]['RurUriTnk']
                    sale_price:int = df_of_customer_sale.iloc[i,:]['RurUriKin']
                    tekiyo:str     = df_of_customer_sale.iloc[i,:]['RurCMNo']
                    toriKbn:str    = df_of_customer_sale.iloc[i,:]['RurToriKBN']
                    if tani != ' ':
                        tani = tani_code[tani]

                    sale:Sale = Sale(sale_no, sale_date, hinban, hinmei,
                                     sale_qty, tani, 
                                     unit_price, sale_price,
                                     tekiyo, toriKbn)
                    sales.append(sale)
                    sales_deposits_date_set.add(sale_date)

            if df_of_customer_deposit is not None:
                for i in range(len(df_of_customer_deposit)):
                    deposit_no:str    = (df_of_customer_deposit.iloc[i,:]
                                                             ['RnyNNo'])
                    deposit_date:str  = (df_of_customer_deposit.iloc[i,:]
                                                          ['RnyNyuDay'])
                    deposit_kubun:str = (df_of_customer_deposit.iloc[i,:]
                                                         ['RnyToriKBN'])
                    deposit_price:int = (df_of_customer_deposit.iloc[i,:]
                                                          ['RnyNyuKin'])
                    deposit:Deposit = Deposit(deposit_no, deposit_date, 
                            deposit_kubun, deposit_price, nyuukin_kubun)
                    deposits.append(deposit)
                    sales_deposits_date_set.add(deposit_date)

            sales_deposits_instance:SalesDeposits = SalesDeposits(sales, deposits, 
                                 sales_deposits_date_set, customer_code, 
                                                    self.__instance_index_row)
            sales_deposits.append(sales_deposits_instance)

        return sales_deposits
        

    def create_customer(self, customers_list)->list:

        customers:object = []
        for customer_code in customers_list:
            df_of_customer_customer = (
                            self.__df_customer[self.__df_customer['TokSeikyuCD'] 
                            == customer_code])
            if df_of_customer_customer is not None:
                for i in range(len(df_of_customer_customer)):
                    name1:str = df_of_customer_customer.iloc[i,:]['AitNam1']
                    name2:str = df_of_customer_customer.iloc[i,:]['AitNam2']
                    name3:str = df_of_customer_customer.iloc[i,:]['AitNam3']
                    pos_no1:str = df_of_customer_customer.iloc[i,:]['AitPosNo1']
                    pos_no2:str = df_of_customer_customer.iloc[i,:]['AitPosNo2']
                    addr1:str = df_of_customer_customer.iloc[i,:]['AitAddr1']
                    addr2:str = df_of_customer_customer.iloc[i,:]['AitAddr2']
                    addr3:str = df_of_customer_customer.iloc[i,:]['AitAddr3']

                    customer:Customer = Customer(customer_code, name1, name2, name3,
                                     pos_no1, pos_no2, addr1, addr2, addr3)
                    customers.append(customer)
                    
        return customers


        
            
    def create_invoice(self, list_customers, sales_deposits, customers,
                                                             TAX_RATE)-> list:
        closing_date: str = self.__df_sime.loc[0,  'TszSimeDay']

        invoices:object = []
        for customer_code in list_customers:
            df_of_customer_sime = (
                    self.__df_sime[self.__df_sime['TszTokCD']
                                                       == customer_code])
            if df_of_customer_sime is not None:
                

                for i in range(len(df_of_customer_sime)):
                    last_balance:int = (df_of_customer_sime.iloc[i,:]
                                                            ['TszSeiZanZ'])
                    deposit:int = df_of_customer_sime.iloc[i,:]['TszNyuKinT']
                    sales_price:int = (df_of_customer_sime.iloc[i,:]
                                                            ['TszUriKinT'])
                    tax:int = df_of_customer_sime.iloc[i,:]['TszZeiKinT']
                    billed_price:int = (df_of_customer_sime.iloc[i,:]
                                                            ['TszSeiZanK'])
                    ins_customer:object = None
                    for customer in customers:
                        if customer.is_customer_matched(customer_code):
                            ins_customer:object = customer

                    ins_sales_deposits:object = None
                    for one_of_sales_deposits in sales_deposits:
                        if (one_of_sales_deposits.
                                      is_customer_matched(customer_code)):
                            ins_sales_deposits:object = one_of_sales_deposits

                    excel:Excel = Excel(closing_date)

                    invoice:Invoice = Invoice(customer_code, 
                                      last_balance, deposit, sales_price,
                                      tax, billed_price, ins_customer, 
                                      ins_sales_deposits, excel, TAX_RATE,
                                      self.__email_info)
                    invoices.append(invoice)                    
        return invoices
                    
                    



