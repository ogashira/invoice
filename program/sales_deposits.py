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

    def calc_sales_deposits_count(self):
        return len(self.__sales_deposits)

    def filling_page_sales_deposits(self, excel, page_count, 
                                    sales_deposits_count):
        dic_row = {20:84, 47:154, 74:224, 101:294, 128:364, 
                   155:434, 182:504, 209:574, 236:644}
        '''
        ２ページ目以降のインスタンス個数とエクセルの行数との関係
        19(インスタンス20個目を処理したら行数を84にする)
        '''
        instances_count = 0
        row_no = 28 #エクセルの行
        while True:
            if instances_count >= len(self.__sales_deposits):
                break
            
            instance = self.__sales_deposits[instances_count] #インスタンス
            if instances_count < 20:
                instance.filling_page_sales_deposits(
                                       excel, row_no, page_count,
                                       sales_deposits_count)
                row_no += 2
                instances_count += 1
                continue

            if instances_count in dic_row:
                row_no = dic_row[instances_count]
            instance.filling_page_sales_deposits(
                                       excel, row_no, page_count,
                                       sales_deposits_count)
            row_no += 2
            instances_count += 1

    def show_me(self):
        for instance in self.__sales_deposits:
            instance.show_me()

