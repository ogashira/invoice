import pandas as pd
import openpyxl
from openpyxl.styles.borders import Border, Side
from openpyxl.styles.fonts import Font
from openpyxl.utils import get_column_letter

class Excel:

    def __init__(self, customer_code, closing_date):
        file_path = (r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/請求書関連/invoice_format.xlsx')
        self.wb = openpyxl.load_workbook(file_path)
        self.ws = self.wb['1']

        self.__customer_code = customer_code
        self.__closing_date = closing_date

    def filling_page_invoice(self, last_balance,
                      deposit, carryover_price, sales_price, tax,
                      billed_price, TAX_RATE):
        self.ws.cell(6, 2).value = self.__customer_code
        self.ws.cell(2, 26).value = (self.__closing_date[:4]  + '年' + 
                                     self.__closing_date[4:6] + '月' + 
                                     self.__closing_date[6:])
        self.ws.cell(22, 1).value = last_balance
        self.ws.cell(22, 7).value = deposit
        self.ws.cell(22, 13 ).value = carryover_price
        self.ws.cell(22, 18 ).value = sales_price
        self.ws.cell(22, 23 ).value = tax
        self.ws.cell(22, 28 ).value = sales_price + tax
        self.ws.cell(22, 35 ).value = billed_price
        self.ws.cell(24, 16 ).value = TAX_RATE + '%'
        self.ws.cell(24, 18 ).value = sales_price
        self.ws.cell(24, 23 ).value = tax

    def filling_page_customer(self, customer_nam1, customer_nam2, 
                              customer_nam3, customer_pos1, customer_pos2,
                              customer_addr1, customer_addr2, customer_addr3):
        self.ws.cell(1,2).value = '〒' + customer_pos1 + '-' + customer_pos2
        self.ws.cell(2,2).value = customer_addr1
        self.ws.cell(3,2).value = customer_addr2
        self.ws.cell(4,2).value = customer_addr3
        self.ws.cell(7,2).value = customer_nam1
        self.ws.cell(8,2).value = customer_nam2
        self.ws.cell(9,2).value = customer_nam3
        if customer_nam2 == ' ' and customer_nam3 == ' ':
            self.ws.cell(7,19).value = '御中'
        if customer_nam2 != ' ' and customer_nam3 == ' ':
            self.ws.cell(8,19).value = '御中'
        if customer_nam3 != ' ':
            self.ws.cell(9,19).value = '御中'
            
            

    def save_file(self):
        self.wb.save(f'{self.__closing_date}_{self.__customer_code}.xlsx')





