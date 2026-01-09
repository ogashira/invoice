import math
from re import I
import pandas as pd
from excel import Excel
from customer import Customer
from sales_deposits import SalesDeposits

class Invoice:
    def __init__(self, customer_code, last_balance,
                 deposit, sales_price, tax, billed_price,
                 customers, sales_deposits, excel, TAX_RATE,
                 email_info)->None:

        self.__customer_code:str = customer_code
        self.__last_balance:int = last_balance
        self.__deposit:int = deposit
        self.__carryover_price:int = last_balance - deposit
        self.__sales_price:int = sales_price
        self.__tax:int = tax
        self.__billed_price:int = billed_price
        self.__customer:Customer = customers
        
        # SalesDepositsクラスのインスタンス
        self.__sales_deposits:SalesDeposits = sales_deposits

        # salesとdepositのインスタンスが日付が小さい順に詰まったリストの要素数
        self.__sales_and_deposits_count:int = (
                        self.__sales_deposits.calc_sales_deposits_count())
        self.__invoices_page_count:int = self.calc_invoices_page_count()
        self.__excel:Excel = excel
        self.__TAX_RATE:str = TAX_RATE
        self.__email_info: pd.DataFrame = email_info
        self.__is_post = self.judge_should_post() # 請求書を提出するかどうか？
        self.__is_yuusou = self.judge_is_yuusou() # 郵送かどうか？




    def judge_is_yuusou(self)->bool:
        '''
        郵送かどうか？ 
        '''
        df_tmp = \
        self.__email_info[self.__email_info['得意先CD']==self.__customer_code]
        mail_or_yuusou: str = ''
        if not df_tmp.empty:
            mail_or_yuusou: str = df_tmp['Email'].iloc[0]
        if mail_or_yuusou == '郵送':
            return True

        return False

    def judge_should_post(self)->bool:
        is_exist_free_samples: bool = \
                self.__sales_deposits.is_exist_free_samples()
        is_exist_paid_items: bool = \
                self.__sales_deposits.is_exist_paid_items()
        is_exist_returns: bool = \
                self.__sales_deposits.is_exist_returns()
        is_exist_deposits: bool = False
        if self.__deposit > 0:
            is_exist_deposits = True
                

        # email_address.xlsxに得意先CDがない場合はFalseリターン
        if len(self.__email_info.loc[self.__email_info['得意先CD'] == 
                                                    self.__customer_code,:])==0:
            return False
        
        '''
        2025/12/24現在では、有償品または返品がある場合だけ請求書を送信する
        '''
        if is_exist_paid_items or is_exist_returns:
            return True

        '''
        #TODO後で消す
        print(f'{self.__customer_code}->'  
              f'無償品:{is_exist_free_samples},' 
              f'有償品:{is_exist_paid_items},' 
              f'返品:{is_exist_returns},' 
              f'入金:{is_exist_deposits}') 
        '''

        return False


    def calc_invoices_page_count(self)->int:
        '''
        請求書の枚数（ページ数）を返す
        １ページ目のデータ数は２０行、２ページ以降のデータ数は２７行
        '''
        if self.__sales_and_deposits_count <= 20: 
            return 1
        return math.ceil((self.__sales_and_deposits_count -20) / 27) + 1

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
                                                self.__sales_and_deposits_count
                                                )
        
        self.__excel.arrange_sheets(self.__invoices_page_count)
        self.__excel.save_file(self.__is_post, self.__is_yuusou, 
                               self.__customer_code)
