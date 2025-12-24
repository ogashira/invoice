class SalesDeposits:

    def __init__(self, sales, deposits, sales_deposits_date_set, 
                                    customer_code, instance_index_row)->None:
        self.__customer_code:str = customer_code
        self.__sales:list = sales
        self.__instance_index_row:dict = instance_index_row
        self.__deposits:list = deposits
        # 売上日と入金日の集合をリストにして並び替える
        self.__sales_deposits_date_list:list = sorted(
                                             list(sales_deposits_date_set))

        self.__sales_and_deposits:list = []
        # 売上日、入金日が小さい順にsalesとdepositのインスタンスを詰める
        # 売上日と入金日が重なった時は入金日を先にする。

        self.__create_sales_and_deposits() 


    def is_exist_free_samples(self)->bool:
        '''
        Invoiceクラスから呼ばれる
        無償サンプルがあるのかを判定
        明細数が0より大きくて、
        単価が0のものが1つ以上あるか。
        '''
        if len(self.__sales) == 0:
            return False

        pattern: bool = False
        for sale in self.__sales:
            if sale.get_sale_unit_price() > 0:
                pattern = True
                break
        
        return pattern


    def is_exist_paid_items(self)->bool:
        '''
        有償サンプルまたは有償の製品が存在するか？
        明細数が0より大きくて、
        数量が1以上で単価が0より大きいものが1つ以上ある
        '''
        if len(self.__sales) == 0:
            return False

        pattern: bool = False
        for sale in self.__sales:
            if sale.get_sale_qty() > 0 and sale.get_sale_unit_price() > 0:
                pattern = True
                break
            
        return pattern


    def is_exist_returns(self)-> bool:
        '''
        明細に返品が存在するか？
        明細数が0より大きくて、
        数量が0より小さいものが1つ以上あるか。
        '''
        if len(self.__sales) == 0:
            return False

        pattern: bool = False
        for sale in self.__sales:
            if sale.get_sale_qty() < 0:
                pattern = True
                break
        
        return pattern



    def __create_sales_and_deposits(self)->None:
        for date in self.__sales_deposits_date_list:
            for deposit in self.__deposits:  # 入金日を優先
                if deposit.is_date_matched(date):
                    self.__sales_and_deposits.append(deposit)
            for sale in self.__sales:
                if sale.is_date_matched(date):
                    self.__sales_and_deposits.append(sale)


    def is_customer_matched(self, customer_code)->bool:
        return self.__customer_code == customer_code


    def calc_sales_deposits_count(self)->int:
        return len(self.__sales_and_deposits)


    def filling_page_sales_deposits(self, excel, page_count, 
                                    sales_deposits_count)->None:

        '''
        self.__instance_index_row = {0:28, 20:84, 47:154, 74:224, 101:294, 128:364, 
                                           155:434, 182:504, 209:574, 236:644}
        ２ページ目以降のインスタンス個数とエクセルの行数との関係
        インスタンス20個目を処理したら行数を84にする
        '''

        instances_count:int = 0
        row_no:int = 0 #エクセルの行
        count_page_sum_row:int = 0
        first_row_no:int = 0
        while True:
            if instances_count >= len(self.__sales_and_deposits):
                break
            
            instance = self.__sales_and_deposits[instances_count] #インスタンス
            if instances_count in self.__instance_index_row:
                row_no = self.__instance_index_row[instances_count]
                first_row_no = self.__instance_index_row[instances_count]
                
            if instances_count < 20:
                count_page_sum_row = first_row_no + 20 * 2  # 1ページ目の件数の入力行
            else:
                count_page_sum_row = first_row_no + 27 * 2



            instance.filling_page_sales_deposits(
                                   excel, row_no, count_page_sum_row,
                                   sales_deposits_count, page_count)
            row_no += 2
            instances_count += 1
