from sale import Sale
from deposit import Deposit


class SalesDeposits:

    def __init__(self, sales, deposits, sales_deposits_date_set, customer_code):
        self.__customer_code = customer_code
        self.__sales = sales
        self.__deposits = deposits
        # 売上日と入金日の集合をリストにして並び替える
        self.__sales_deposits_date_list = sorted(list(sales_deposits_date_set))

        self.__sales_deposits = []
        # 売上日、入金日が小さい順にsalesとdepositのインスタンスを詰める
        # 売上日と入金日が重なった時は入金日を先にする。

        self.__create_sales_deposits() 


    def __create_sales_deposits(self):
        for date in self.__sales_deposits_date_list:
            for deposit in self.__deposits:  # 入金日を優先
                if deposit.is_date_matched(date):
                    self.__sales_deposits.append(deposit)
            for sale in self.__sales:
                if sale.is_date_matched(date):
                    self.__sales_deposits.append(sale)


    def is_customer_matched(self, customer_code):
        return self.__customer_code == customer_code


    def show_me(self):
        for instance in self.__sales_deposits:
            instance.show_me()
