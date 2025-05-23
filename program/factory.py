import pandas as pd

from deposit import Deposit
from sale import Sale
from sales_deposits import SalesDeposits
from customer import Customer
from invoice import Invoice


class Factory:

    def __init__(self, df_sime, df_sale, df_deposit):
        self.__df_sime = df_sime
        self.__df_sale = df_sale
        self.__df_deposit = df_deposit

    def create_sales_deposits(self, customers):
        '''
        SalesDepositsクラスのインスタンスを作る
        SaleクラスのインスタンスとDepositクラスのインスタンスを
        作って、SalesDepositsクラスに渡す。同時に売上日、入金日の集合
        も作って、SalesDepositsクラスに渡す
        '''
        sales_deposits = []
        for customer_code in customers:  # customer_code => 'TokSeikyuCD'
            df_of_customer_sale = (
                            self.__df_sale[self.__df_sale['RurSeiCD'] 
                            == customer_code])
            df_of_customer_deposit = (
                         self.__df_deposit[self.__df_deposit['RnySeiCD'] 
                         == customer_code])
            sales = []
            deposits = []
            sales_deposits_date_set = set()
            if df_of_customer_sale is not None:
                for i in range(len(df_of_customer_sale)): # Seriesにしてから取り出す
                    sale_no      = df_of_customer_sale.iloc[i,:]['RurUNo']
                    sale_date  = df_of_customer_sale.iloc[i,:]['RurUriDay']
                    hinban      = df_of_customer_sale.iloc[i,:]['RurHinCD']
                    hinmei      = df_of_customer_sale.iloc[i,:]['RurHinNam']
                    sale_qty   = df_of_customer_sale.iloc[i,:]['RurKoSu']
                    tani        = df_of_customer_sale.iloc[i,:]['RurUriTniCD']
                    unit_price  = df_of_customer_sale.iloc[i,:]['RurUriTnk']
                    sale_price = df_of_customer_sale.iloc[i,:]['RurUriKin']
                    tekiyo      = df_of_customer_sale.iloc[i,:]['RjcCMNo']
                    sale = Sale(sale_no, sale_date, hinban, hinmei,
                                      sale_qty, tani, unit_price, sale_price,
                                      tekiyo)
                    sales.append(sale)
                    sales_deposits_date_set.add(sale_date)

            if df_of_customer_deposit is not None:
                for i in range(len(df_of_customer_deposit)):
                    deposit_no    = (df_of_customer_deposit.iloc[i,:]
                                                             ['RnyNNo'])
                    deposit_date  = (df_of_customer_deposit.iloc[i,:]
                                                          ['RnyNyuDay'])
                    deposit_kubun = (df_of_customer_deposit.iloc[i,:]
                                                         ['RnyToriKBN'])
                    deposit_price = (df_of_customer_deposit.iloc[i,:]
                                                          ['RnyNyuKin'])
                    deposit = Deposit(deposit_no, deposit_date, 
                                           deposit_kubun, deposit_price)
                    deposits.append(deposit)
                    sales_deposits_date_set.add(deposit_date)

            sales_deposits_instance = SalesDeposits(sales, deposits, 
                                 sales_deposits_date_set, customer_code)
            sales_deposits.append(sales_deposits_instance)

        return sales_deposits
        

    def create_customer(self, customers_list):

        customers = []
        for customer_code in customers_list:
            df_of_customer_sale = (
                            self.__df_sale[self.__df_sale['RurSeiCD'] 
                            == customer_code])
            if df_of_customer_sale is not None:
                for i in range(len(df_of_customer_sale)):
                    name1 = df_of_customer_sale.iloc[i,:]['RurTokNam1']
                    name2 = df_of_customer_sale.iloc[i,:]['RurTokNam2']
                    name3 = df_of_customer_sale.iloc[i,:]['RurTokNam3']
                    pos_no1 = df_of_customer_sale.iloc[i,:]['RurTokPosNo1']
                    pos_no2 = df_of_customer_sale.iloc[i,:]['RurTokPosNo2']
                    addr1 = df_of_customer_sale.iloc[i,:]['RurTokAddr1']
                    addr2 = df_of_customer_sale.iloc[i,:]['RurTokAddr2']
                    addr3 = df_of_customer_sale.iloc[i,:]['RurTokAddr3']

                    customer = Customer(customer_code, name1, name2, name3,
                                     pos_no1, pos_no2, addr1, addr2, addr3)
                    customers.append(customer)
                    
        return customers


        
            
    def create_invoice(self, customers, sales_deposits ):
        for customer_code in customers:
            df_of_customer_sime = (
                    self.__df_sime[self.__df_sime['TszTokCD'] 
                                                       == customer_code])
            if df_of_customer_sime is not None:
                for i in range(len(df_of_customer_sime)):
                    closing_date = (df_of_customer_sime.iloc[i,:]
                                                            ['TszSimeDay']) 
                    last_balance = (df_of_customer_sime.iloc[i,:]
                                                            ['TszSeiZanZ'])
                    deposit = df_of_customer_sime.iloc[i,:]['TszNyuKinT']
                    sales_price = (df_of_customer_sime.iloc[i,:]
                                                            ['TszUriKinT'])
                    tax = df_of_customer_sime.iloc[i,:]['TszZeiKinT']
                    billed_price = (df_of_customer_sime.iloc[i,:]
                                                            ['TszSeiZanK'])


