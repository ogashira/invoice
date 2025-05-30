import pandas as pd

from deposit import Deposit
from sale import Sale
from sales_deposits import SalesDeposits
from customer import Customer
from invoice import Invoice
from excel import Excel


class Factory:

    def __init__(self, df_sime, df_sale, df_deposit, df_customer):
        self.__df_sime = df_sime
        self.__df_sale = df_sale
        self.__df_deposit = df_deposit
        self.__df_customer = df_customer

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
            df_of_customer_customer = (
                            self.__df_customer[self.__df_customer['TokSeikyuCD'] 
                            == customer_code])
            if df_of_customer_customer is not None:
                for i in range(len(df_of_customer_customer)):
                    name1 = df_of_customer_customer.iloc[i,:]['AitNam1']
                    name2 = df_of_customer_customer.iloc[i,:]['AitNam2']
                    name3 = df_of_customer_customer.iloc[i,:]['AitNam3']
                    pos_no1 = df_of_customer_customer.iloc[i,:]['AitPosNo1']
                    pos_no2 = df_of_customer_customer.iloc[i,:]['AitPosNo2']
                    addr1 = df_of_customer_customer.iloc[i,:]['AitAddr1']
                    addr2 = df_of_customer_customer.iloc[i,:]['AitAddr2']
                    addr3 = df_of_customer_customer.iloc[i,:]['AitAddr3']

                    customer = Customer(customer_code, name1, name2, name3,
                                     pos_no1, pos_no2, addr1, addr2, addr3)
                    customers.append(customer)
                    
        return customers


        
            
    def create_invoice(self, list_customers, sales_deposits, customers,
                                                              TAX_RATE ):

        invoices = []
        for customer_code in list_customers:
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
                    ins_customer = None
                    for customer in customers:
                        if customer.is_customer_matched(customer_code):
                            ins_customer = customer

                    ins_sales_deposits = None
                    for one_of_sales_deposits in sales_deposits:
                        if (one_of_sales_deposits.
                                      is_customer_matched(customer_code)):
                            ins_sales_deposits = one_of_sales_deposits

                    excel = Excel(customer_code, closing_date)

                    invoice = Invoice(customer_code, 
                                      last_balance, deposit, sales_price,
                                      tax, billed_price, ins_customer, 
                                      ins_sales_deposits, excel, TAX_RATE)
                    invoices.append(invoice)                    
        return invoices
                    
                    




