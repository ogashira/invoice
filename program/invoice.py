import math
from re import I
from excel import Excel
from customer import Customer
from sales_deposits import SalesDeposits

class Invoice:
    def __init__(self, customer_code, last_balance,
                 deposit, sales_price, tax, billed_price,
                 customers, sales_deposits, excel, TAX_RATE)->None:

        self.__customer_code:str = customer_code
        self.__last_balance:int = last_balance
        self.__deposit:int = deposit
        self.__carryover_price:int = last_balance - deposit
        self.__sales_price:int = sales_price
        self.__tax:int = tax
        self.__billed_price:int = billed_price
        self.__customer:Customer = customers
        self.__sales_deposits:SalesDeposits = sales_deposits

        self.__sales_deposits_count:int = (
                        self.__sales_deposits.calc_sales_deposits_count())
        self.__invoices_page_count:int = self.calc_invoices_page_count()
        self.__excel:Excel = excel
        self.__TAX_RATE:str = TAX_RATE


    def calc_invoices_page_count(self)->int:
        '''
        請求書の枚数（ページ数）を返す
        １ページ目のデータ数は２０行、２ページ以降のデータ数は２７行
        '''
        if self.__sales_deposits_count <= 20: 
            return 1
        return math.ceil((self.__sales_deposits_count -20) / 27) + 1

    def filling_page_invoice(self)->None:
        self.__excel.filling_page_invoice(
                self.__last_balance, self.__deposit, self.__carryover_price,
                self.__sales_price, self.__tax, self.__billed_price,
                self.__TAX_RATE)

        self.__customer.filling_page_customer(self.__excel,
                                              self.__invoices_page_count)

        self.__sales_deposits.filling_page_sales_deposits(
                                                self.__excel,
                                                self.__invoices_page_count, 
                                                self.__sales_deposits_count
                                                )
        
        self.__excel.arrange_sheets(self.__invoices_page_count)
        self.__excel.save_file()
