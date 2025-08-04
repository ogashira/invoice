class Sale:
    
    def __init__(self, sale_no, sale_date, hinban, hinmei,
                 sale_qty, tani, unit_price, sale_price, tekiyo)->None:
        self.__sale_no:str = sale_no
        self.__sale_date:str = sale_date
        self.__sale_hinban:str = hinban
        self.__sale_hinmei:str = hinmei
        self.__sale_qty:int = sale_qty
        self.__sale_tani:str = tani
        self.__sale_unit_price:int = unit_price
        self.__sale_price:int = sale_price
        self.__tekiyo:str = tekiyo

    def filling_page_sales_deposits(self, excel, row_no, count_page_sum_row,
                                            sales_deposits_count, page_count)->None:
        excel.filling_page_sales(row_no, count_page_sum_row, 
                                 sales_deposits_count,
                                 self.__sale_no,
                                 self.__sale_date,
                                 self.__sale_hinban,
                                 self.__sale_hinmei,
                                 self.__sale_qty,
                                 self.__sale_tani,
                                 self.__sale_unit_price,
                                 self.__sale_price,
                                 self.__tekiyo,
                                 page_count)


    def is_date_matched(self, date)->bool:
        return date == self.__sale_date
