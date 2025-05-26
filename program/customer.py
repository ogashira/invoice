class Customer:

    def __init__(self, customer_code, AitNam1, AitNam2, AitNam3,
                 AitPosNo1, AitPosNo2, AitAddr1,
                 AitAddr2, AitAddr3):
        self.__customer_code = customer_code
        self.__customer_nam1 = AitNam1

    def is_customer_matched(self, customer_code):
        return self.__customer_code == customer_code

    def filling_page_customer(self, excel):
        excel.filling_page_customer(self.__customer_nam1)
        

    def show_me(self):
        print(self.__customer_code)
        print(self.__customer_nam1)
