class Deposit:

    def __init__(self, deposit_no:str, deposit_date:str,
                 deposit_kubun:str, deposit_price:int,
                 nyukin_kubun_from_yaml:dict) -> None:
        # nyukin_kubun_from_yamlはyamlから入手したdictionary
        self.__deposit_no:str = deposit_no
        self.__deposit_date:str = deposit_date
        self.__deposit_kubun:str = nyukin_kubun_from_yaml[deposit_kubun][:3]
        self.__deposit_price:int = deposit_price


    def is_date_matched(self, date) -> bool:
        return date == self.__deposit_date

    def filling_page_sales_deposits(self, excel, row_no, count_page_sum_row, 
                                    sales_deposits_count, page_count)->None:

        excel.filling_page_deposits(row_no, page_count, 
                                    sales_deposits_count,
                                    self.__deposit_no,
                                    self.__deposit_date,
                                    self.__deposit_kubun,
                                    self.__deposit_price)
