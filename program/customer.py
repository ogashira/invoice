class Customer:

    def __init__(self, customer_code, AitNam1, AitNam2, AitNam3,
                 AitPosNo1, AitPosNo2, AitAddr1,
                 AitAddr2, AitAddr3) -> None:
        self.__customer_code:str = customer_code
        self.__customer_nam1:str = AitNam1
        self.__customer_nam2:str = AitNam2
        self.__customer_nam3:str = AitNam3
        self.__customer_pos1:str = AitPosNo1
        self.__customer_pos2:str = AitPosNo2
        self.__customer_addr1:str = AitAddr1
        self.__customer_addr2:str = AitAddr2
        self.__customer_addr3:str = AitAddr3

    def is_customer_matched(self, customer_code) -> bool:
        return self.__customer_code == customer_code

    def filling_page_customer(self, excel, page_count) -> None:
        excel.filling_page_customer(self.__customer_nam1,
                                    self.__customer_nam2,
                                    self.__customer_nam3,
                                    self.__customer_pos1,
                                    self.__customer_pos2,
                                    self.__customer_addr1,
                                    self.__customer_addr2,
                                    self.__customer_addr3,
                                    page_count)
