class Invoice:
    def __init__(self, customer_code, closing_date, last_balance,
                 deposit, sales_price, tax, billed_price,
                 customers, sales_deposits):

        self.__customer_code = customer_code
        self.__closing_date = closing_date
        self.__last_balance = last_balance
        self.__deposit = deposit
        self.__carryover_price = last_balance - deposit
        self.__sales_price = sales_price
        self.__tax = tax
        self.__billed_price = billed_price
        self.__customers = customers
        self.__sales_deposit_lists = sales_deposits
