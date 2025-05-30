class Deposit:

    def __init__(self, deposit_no, deposit_date, 
                 deposit_kubun, deposit_price):
        self.__deposit_no = deposit_no
        self.__deposit_date = deposit_date
        self.__deposit_kubun = deposit_kubun
        self.__deposit_price = deposit_price

    def show_me(self):
        print(self.__deposit_date, self.__deposit_no)

    def is_date_matched(self, date):
        return date == self.__deposit_date

    def filling_page_sales_deposits(self, excel, row_no, page_count, 
                                    sales_deposits_count):

        excel.filling_page_deposits(row_no, page_count, 
                                    sales_deposits_count,
                                    self.__deposit_no,
                                    self.__deposit_date,
                                    self.__deposit_kubun,
                                    self.__deposit_price)
