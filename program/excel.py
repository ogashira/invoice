import pandas as pd
import openpyxl
import platform
from openpyxl.styles.borders import Border, Side
from openpyxl.styles.fonts import Font
from openpyxl.utils import get_column_letter


class Excel:

    def __init__(self, customer_code, closing_date):
        pf = platform.system()
        if pf == 'Windows':
            path = r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/請求書関連/invoice_format.xlsx'
        else:
            path = r'/mnt/public/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/請求書関連/invoice_format.xlsx'

        file_path = (path)
        self.wb = openpyxl.load_workbook(file_path)
        self.ws = self.wb['1']

        self.__customer_code = customer_code
        self.__closing_date = closing_date

    def filling_page_invoice(self, last_balance, deposit, carryover_price, 
                             sales_price, tax, billed_price, TAX_RATE, 
                            ):
        '''
        1ページにしか記載されない情報
        '''
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
                              customer_addr1, customer_addr2, customer_addr3,
                              page_count):
        '''
        1ページの行数は70行、フォーマットは10ページ分ある
        '''
        self.ws.delete_rows(page_count * 70 + 1, 700)

        for i in range(page_count):
            self.ws.cell(i*70+6, 2).value = self.__customer_code
            self.ws.cell(i*70+2, 26).value = (self.__closing_date[:4]  + '年' + 
                                         self.__closing_date[4:6] + '月' + 
                                         self.__closing_date[6:])
            self.ws.cell(i*70+1,2).value = ('〒' + customer_pos1 + '-' + 
                                                                 customer_pos2)
            self.ws.cell(i*70+2,2).value = customer_addr1
            self.ws.cell(i*70+3,2).value = customer_addr2
            self.ws.cell(i*70+4,2).value = customer_addr3
            self.ws.cell(i*70+7,2).value = customer_nam1
            self.ws.cell(i*70+8,2).value = customer_nam2
            self.ws.cell(i*70+9,2).value = customer_nam3
            if customer_nam2 == ' ' and customer_nam3 == ' ':
                self.ws.cell(i*70+7,19).value = '御中'
            if customer_nam2 != ' ' and customer_nam3 == ' ':
                self.ws.cell(i*70+8,19).value = '御中'
            if customer_nam3 != ' ':
                self.ws.cell(i*70+9,19).value = '御中'

    def filling_page_sales(self,row_no, page_count, 
                           sales_deposits_count,
                           sale_no,
                           sale_date,
                           sale_hinban,
                           sale_hinmei,
                           sale_qty,
                           sale_tani,
                           sale_unit_price,
                           sale_price,
                           tekiyo):

        koumoku = '売上'
        if sale_hinban == '999999':
            koumoku = '値引'
        self.ws.cell(row_no, 1).value = sale_date[4:6] + '/' + sale_date[6:]
        self.ws.cell(row_no + 1, 1).value = koumoku 
        self.ws.cell(row_no, 3).value = sale_no
        self.ws.cell(row_no, 7).value = sale_hinban
        self.ws.cell(row_no + 1, 7).value = sale_hinmei
        self.ws.cell(row_no, 20).value = sale_qty
        self.ws.cell(row_no, 24).value = sale_tani
        self.ws.cell(row_no, 26).value = sale_unit_price
        self.ws.cell(row_no, 30).value = sale_price
        self.ws.cell(row_no, 34).value = tekiyo


    def filling_page_deposits(self,row_no, page_count, 
                              sales_deposits_count,
                              deposit_no,
                              deposit_date,
                              deposit_kubun,
                              deposit_price):
        self.ws.cell(row_no, 1).value = deposit_date[4:6] + '/' + deposit_date[6:]
        self.ws.cell(row_no+1, 1).value = deposit_kubun
        self.ws.cell(row_no, 3).value = deposit_no
        self.ws.cell(row_no, 7).value = '＜ 御 入 金 ＞'
        self.ws.cell(row_no, 30).value = deposit_price



    def save_file(self):
        self.wb.save(f'{self.__closing_date}_{self.__customer_code}.xlsx')





