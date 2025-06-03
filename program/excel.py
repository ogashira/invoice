import openpyxl
import platform
from openpyxl.styles.borders import Border, Side
from openpyxl.styles.fonts import Font
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet


class Excel:

    def __init__(self, customer_code, closing_date)->None:
        pf:str = platform.system()
        if pf == 'Windows':
            path = r'//192.168.1.247/共有/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/請求書関連/invoice_format.xlsx'
        else:
            path = r'/mnt/public/技術課ﾌｫﾙﾀﾞ/200. effit_data/ﾏｽﾀ/請求書関連/invoice_format.xlsx'

        file_path = (path)
        self.wb:openpyxl.Workbook = openpyxl.load_workbook(filename=file_path,
                                                                 data_only=True)
        self.ws:Worksheet = self.wb['1']

        self.__customer_code:str= customer_code
        self.__closing_date:str = closing_date

    def filling_page_invoice(self, last_balance, deposit, carryover_price, 
                             sales_price, tax, billed_price, TAX_RATE, 
                            )->None:
        '''
        1ページにしか記載されない情報
        '''
        self.ws.cell(row=22, column=1).value = last_balance
        self.ws.cell(row=22, column=7).value = deposit
        self.ws.cell(row=22, column=13).value = carryover_price
        self.ws.cell(row=22, column=18 ).value = sales_price
        self.ws.cell(row=22, column=23 ).value = tax
        self.ws.cell(row=22, column=28 ).value = sales_price + tax
        self.ws.cell(row=22, column=35 ).value = billed_price
        self.ws.cell(row=24, column=16 ).value = TAX_RATE + '%'
        self.ws.cell(row=24, column=18 ).value = sales_price
        self.ws.cell(row=24, column=23 ).value = tax


    def filling_page_customer(self, customer_nam1, customer_nam2, 
                              customer_nam3, customer_pos1, customer_pos2,
                              customer_addr1, customer_addr2, customer_addr3,
                              page_count)->None:
        '''
        1ページの行数は70行、フォーマットは10ページ分ある
        '''
        self.ws.delete_rows(page_count * 70 + 1, 700)

        for i in range(page_count):
            self.ws.cell(row=i*70+1, column=40).value = page_count
            self.ws.cell(row=i*70+6, column=2).value = self.__customer_code #type:ignore
            self.ws.cell(row=i*70+2, column=26).value = (self.__closing_date[:4]  + '年' + #type:ignore
                                         self.__closing_date[4:6] + '月' + 
                                         self.__closing_date[6:])
            self.ws.cell(row=i*70+1,column=2).value = ('〒' + customer_pos1 + '-' + 
                                                                 customer_pos2)
            self.ws.cell(row=i*70+2,column=2).value = customer_addr1
            self.ws.cell(row=i*70+3,column=2).value = customer_addr2
            self.ws.cell(row=i*70+4,column=2).value = customer_addr3
            self.ws.cell(row=i*70+7,column=2).value = customer_nam1
            self.ws.cell(row=i*70+8,column=2).value = customer_nam2 #type:ignore
            self.ws.cell(row=i*70+9,column=2).value = customer_nam3 #type:ignore
            if customer_nam2 == ' ' and customer_nam3 == ' ':
                self.ws.cell(row=i*70+7,column=19).value = '御中' #type:ignore
            if customer_nam2 != ' ' and customer_nam3 == ' ':
                self.ws.cell(row=i*70+8,column=19).value = '御中' #type:ignore
            if customer_nam3 != ' ':
                self.ws.cell(row=i*70+9,column=19).value = '御中' #type:ignore

    def filling_page_sales(self,row_no, count_page_sum_row, 
                           sales_deposits_count,
                           sale_no,
                           sale_date,
                           sale_hinban,
                           sale_hinmei,
                           sale_qty,
                           sale_tani,
                           sale_unit_price,
                           sale_price,
                           tekiyo,
                           page_count)->None:

        last_page_sum_row = 0
        if page_count == 1:
            last_page_sum_row = 69
        last_page_sum_row = 139 + (page_count -2) * 70


        koumoku = '売上'
        if sale_hinban == '999999':
            koumoku = '値引'
        self.ws.cell(row=row_no, column=1).value = (sale_date[4:6] + '/' + 
                                                              sale_date[6:])
        self.ws.cell(row=row_no + 1, column=1).value = koumoku #type:ignore
        self.ws.cell(row=row_no, column=3).value = sale_no
        self.ws.cell(row=row_no, column=7).value = sale_hinban#type:ignore
        self.ws.cell(row=row_no + 1, column=7).value = sale_hinmei
        self.ws.cell(row=row_no, column=20).value = sale_qty
        self.ws.cell(row=row_no, column=24).value = sale_tani
        self.ws.cell(row=row_no, column=26).value = sale_unit_price
        self.ws.cell(row=row_no, column=30).value = sale_price
        self.ws.cell(row=row_no, column=34).value = tekiyo
        self.ws.cell(row=count_page_sum_row, column=26).value = ( #type:ignore
                    self.ws.cell(row=count_page_sum_row, column=26).value + 1)
        self.ws.cell(row=count_page_sum_row, column=29).value = (
            self.ws.cell(row=count_page_sum_row, column=29).value + sale_price)
        self.ws.cell(row=last_page_sum_row, column=26).value = (#type:ignore
                      self.ws.cell(row=last_page_sum_row, column=26).value + 1)
        self.ws.cell(row=last_page_sum_row+1, column=26).value = (#type:ignore
                    self.ws.cell(row=last_page_sum_row+1, column=26).value + 1)
        self.ws.cell(row=last_page_sum_row, column=29).value = (
             self.ws.cell(row=last_page_sum_row, column=29).value + sale_price)
        self.ws.cell(row=last_page_sum_row+1, column=29).value = (
           self.ws.cell(row=last_page_sum_row+1, column=29).value + sale_price)



    def filling_page_deposits(self,row_no, page_count, 
                              sales_deposits_count,
                              deposit_no,
                              deposit_date,
                              deposit_kubun,
                              deposit_price)->None:
        self.ws.cell(row=row_no, column=1).value = (deposit_date[4:6] + '/' + 
                                                             deposit_date[6:])
        self.ws.cell(row=row_no+1, column=1).value = deposit_kubun
        self.ws.cell(row=row_no, column=3).value = deposit_no
        self.ws.cell(row=row_no, column=7).value = '＜ 御 入 金 ＞' #type:ignore
        self.ws.cell(row=row_no, column=30).value = deposit_price

    def arrange_sheets(self, page_count)->None:
        for i in range(68, (page_count-1) * 70 + 69, 70):
            self.ws.cell(row=i, column=26).value = \
                            str(self.ws.cell(row=i, column=26).value) + '件' #type:ignore
            self.ws.cell(row=i + 1, column=26).value = \
                          str(self.ws.cell(row=i+1, column=26).value) + '件'#type:ignore
            self.ws.cell(row=i + 2, column=26).value = \
                          str(self.ws.cell(row=i+2, column=26).value) + '件'#type:ignore

        for i in range((page_count-1) * 70, 68, -70):
            self.ws.cell(row=i, column=21).value = None
            self.ws.cell(row=i, column=26).value = None
            self.ws.cell(row=i, column=29).value = None
            self.ws.cell(row=i-1, column=21).value = None
            self.ws.cell(row=i-1, column=26).value = None
            self.ws.cell(row=i-1, column=29).value = None

            sheet_range:object = self.ws.iter_rows(min_row=i-1, max_row=i, 
                                                           min_col=1, max_col=40)

            border_no:Border = Border(top=None, bottom=None, left=None, right=None)
            for row in sheet_range:
                for cell in row:
                    cell.border = border_no
            
        # print設定
        max_row:int = page_count * 70
        print_area:str = 'A1:AN' + str(max_row)
        self.ws.print_area = print_area 


    def save_file(self)->None:
        self.wb.save(filename= f'{self.__closing_date}_{self.__customer_code}.xlsx')





