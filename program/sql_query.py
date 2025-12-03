import warnings
import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
from sql_server import SqlServer


class SqlBTSZAN:

    def __init__(self, SIME_DAY)->None:
        self.SIME_DAY = SIME_DAY
      
    def fetch_sqldata(self)->pd.DataFrame:
        warnings.filterwarnings("ignore", category=UserWarning)
        sql_server:SqlServer = SqlServer()
        cnxn = sql_server.get_cnxn()

        sql_query:str = ("SELECT TszTokCD, TszSimeDay, TszSeiZanZ, TszUriKinT," 
                         " TszZeiKinT, TszNyuKinT,"
                         " TszSeiZanK, TszUriKin1, TszNyuKin1, TszNyuKin7"
                         " FROM dbo.BTSZAN"
                         " WHERE TszSimeDay =" + self.SIME_DAY + 
                         " AND (TszTokCD < 'T6000'"
                         " OR TszTokCD > 'W')"
                         " ORDER BY TszTokCD"
                        )
        sime_data:pd.DataFrame = pd.read_sql(sql_query, cnxn)

        return sime_data


class SqlRURIDT:

    def __init__(self, bill_day)->None:
        self.bill_day = bill_day
      
    def fetch_sqldata(self)->pd.DataFrame:
        warnings.filterwarnings("ignore", category=UserWarning)
        sql_server:SqlServer = SqlServer()
        cnxn = sql_server.get_cnxn()

        sql_query:str = ("SELECT RURIDT.RurUNo, RURIDT.RurTokCD,"
                        " RURIDT.RurSeiCD, RURIDT.RurHinCD, RURIDT.RurUriDay,"
                        " RURIDT.RurToriKBN, RURIDT.RurHinNam, RURIDT.RurUriTniCD,"
                        " RURIDT.RurKoSu, RURIDT.RurUriTnk, RURIDT.RurUriKin,"
                        " RURIDT.RurzeiTni, RURIDT.RurZeiKin, RURIDT.RurSeiYMDY,"
                        " RURIDT.RurSeiUpFlg, RURIDT.RurCMNo"
                        " From dbo.RURIDT"
                        " WHERE RurSeiYMDY =" + self.bill_day +
                        " AND (RURIDT.RurToriKBN = 1 OR RURIDT.RurToriKBN = 2"
                        " OR RURIDT.RurToriKBN = 3)"
                        " ORDER BY RURIDT.RurSeiCD, RURIDT.RurUriDay, RURIDT.RurUNo"
                       )
        sales_data:pd.DataFrame = pd.read_sql(sql_query, cnxn)

        return sales_data


class SqlRNYUKN:
    '''
    入金のデータは締め日１ヵ月前～締め日までの範囲を取得する
    '''

    def __init__(self, SIME_DAY)->None:
        self.SIME_DAY = SIME_DAY


    def fetch_sqldata(self)->pd.DataFrame:

        def is_end_of_month(date_to_check: datetime.datetime) -> bool:
            """
            指定された日付がその月の最終日であるかを判定する。
            """
            # 1. まず、次の月の1日を取得します。
            #    現在の月に1ヶ月を足し、日の部分を1日に設定します。
            first_day_of_next_month = (date_to_check +
                                 relativedelta(months=1)).replace(day=1)

            # 2. 次の月の1日から1日引くと、現在の月の最終日になります。
            last_day_of_current_month = (first_day_of_next_month - 
                                                     datetime.timedelta(days=1))

            # 3. 元の日付の日と計算した最終日の日が一致するかを比較し す。
            return date_to_check.day == last_day_of_current_month.day

            
        def calc_stt_day(sime_day: str)-> str:
            '''
            sime_dayが月末なら当月の1日を、それ以外は1月前の翌日を返す
            '''
            date_sime_day = datetime.datetime.strptime(sime_day, '%Y%m%d')
            # １月前の翌日
            date_stt_day = (date_sime_day - relativedelta(months=1) + 
                                                      relativedelta(days=1))
            # 月末だったら当月の１日
            if is_end_of_month(date_sime_day):
                date_stt_day = date_sime_day.replace(day=1)
            
            stt_day: str = date_stt_day.strftime('%Y%m%d')

            return stt_day


        warnings.filterwarnings("ignore", category=UserWarning)
        stt_day:str = calc_stt_day(self.SIME_DAY)

        sql_server:SqlServer = SqlServer()
        cnxn = sql_server.get_cnxn()

        print(stt_day, "~", self.SIME_DAY)

        sql_query:str = ("SELECT RnyNNo, RnyNGNo, RnySeiCD, RnyToriKBN,"
                        " RnyNyuDay, RnyNyuKin, RnyTegataDay, RnyTegataNo,"
                        " RnySeiUpFlg"
                        " From dbo.RNYUKN"
                        " WHERE RnyNyuDay >=" + stt_day + 
                        " AND RnyNyuDay <=" + self.SIME_DAY +
                        " ORDER BY RnySeiCD, RnyNyuDay"
                        )
        deposit_data:pd.DataFrame = pd.read_sql(sql_query, cnxn)

        return deposit_data


class SqlMTOKUI:

      
    def fetch_sqldata(self)->pd.DataFrame:
        warnings.filterwarnings("ignore", category=UserWarning)
        sql_server:SqlServer = SqlServer()
        cnxn = sql_server.get_cnxn()

        sql_query:str = ("SELECT MTOKUI.TokTokCD, MTOKUI.TokNonyuCD,"
                        " MTOKUI.TokSeikyuCD,"
                        " MAITEM.AitNam1, MAITEM.AitNam2, MAITEM.AitNam3,"
                        " MAITEM.AitPosNo1, MAITEM.AitPosNo2,"
                        " MAITEM.AitAddr1, MAITEM.AitAddr2, MAITEM.AitAddr3"
                        " From dbo.MTOKUI"
                        " JOIN dbo.MAITEM"
                        " ON MTOKUI.TokTokCD = MAITEM.AitCD1"
                        " AND MTOKUI.TokNonyuCD = MAITEM.AitCD2"
                        " WHERE MTOKUI.TokNonyuCD = ' '"
                        " AND MTOKUI.TokTokCD = MTOKUI.TokSeikyuCD"
                        " ORDER BY MTOKUI.TokTokCD"
                        )
        tokui_data:pd.DataFrame = pd.read_sql(sql_query, cnxn)

        return tokui_data
