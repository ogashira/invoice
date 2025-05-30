class Sale:
    
    def __init__(self, sale_no, sale_date, hinban, hinmei,
                 sale_qty, tani, unit_price, sale_price, tekiyo):
        self.__sale_no = sale_no
        self.__sale_date = sale_date
        self.__sale_hinban = hinban
        self.__sale_hinmei = hinmei
        self.__sale_qty = sale_qty
        self.__sale_tani = tani
        self.__sale_unit_price = unit_price
        self.__sale_price = sale_price
        self.__tekiyo = tekiyo

    def show_me(self):
        print(self.__sale_date, self.__sale_no)

    def is_date_matched(self, date):
        return date == self.__sale_date
