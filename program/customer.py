class Customer:

    def __init__(self, customer_code, AitNam1, AitNam2, AitNam3,
                 AitPosNo1, AitPosNo2, AitAddr1,
                 AitAddr2, AitAddr3):
        self.__customer_code = customer_code
        self.__customer_nam1 = AitNam1
        self.__customer_nam2 = AitNam2
        self.__customer_nam3 = AitNam3
        self.__customer_pos1 = AitPosNo1
        self.__customer_pos2 = AitPosNo2
        self.__customer_addr1 = AitAddr1
        self.__customer_addr2 = AitAddr2
        self.__customer_addr3 = AitAddr3

    def is_customer_matched(self, customer_code):
        return self.__customer_code == customer_code

    def filling_page_customer(self, excel, page_count):
        excel.filling_page_customer(self.__customer_nam1,
                                    self.__customer_nam2,
                                    self.__customer_nam3,
                                    self.__customer_pos1,
                                    self.__customer_pos2,
                                    self.__customer_addr1,
                                    self.__customer_addr2,
                                    self.__customer_addr3,
                                    page_count)
        

    def show_me(self):
        print(self.__customer_code)
        print(self.__customer_nam1)
