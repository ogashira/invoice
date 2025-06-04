import pandas as pd
from sql_query import *
from program_flow import *

def main()->None:

    SIME_DAY = input('締め日を入力してください (例: 20250930) \n : ')
    TAX_RATE = '10'

    try:
        date_SIME_DAY:datetime.date = datetime.datetime.strptime(SIME_DAY, '%Y%m%d')
    except ValueError:
        print('年月日が不正です。処理を中止します。')
        sys.exit()


    program_flow:object = ProgramFlow(SIME_DAY, TAX_RATE)
    program_flow.start()




if __name__ == '__main__':
    main()
