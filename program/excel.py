import pandas as pd
import openpyxl
from openpyxl.styles.borders import Border, Side
from openpyxl.styles.fonts import Font
from openpyxl.utils import get_column_letter

class Excel:

    def __init__(self, customer_code):
        file_path = (r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/請求書関連/invoice_format.xlsx')
        self.wb = openpyxl.load_workbook(file_path)
        self.ws = self.wb['1']

        self.__customer_code = customer_code

    def filling_page_invoice(self, closing_date, last_balance,
                      deposit, carryover_price, sales_price, tax,
                      billed_price):
        self.ws.cell(4, 2).value = self.__customer_code
        self.ws.cell(2, 27).value = closing_date
        self.ws.cell(22, 1).value = last_balance
        self.ws.cell(22, 7).value = deposit
        self.ws.cell(22, 13 ).value = carryover_price
        self.ws.cell(22, 18 ).value = sales_price
        self.ws.cell(22, 28 ).value = tax
        self.ws.cell(22, 35 ).value = billed_price

    def filling_page_customer(self, customer_nam1):
        self.ws.cell(5,2).value = customer_nam1

    def save_file(self):
        self.wb.save(f'20250320_{self.__customer_code}.xlsx')





