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
                        " RURIDT.RurSeiUpFlg, RJYUCD.RjcCMNo"
                        " From dbo.RURIDT"
                        " LEFT JOIN dbo.RJYUCD"
                        " ON RURIDT.RurJCNo = RJYUCD.RjcJCNo"
                        " AND RURIDT.RurJGNo = RJYUCD.RjcJGNo"
                        " WHERE RurSeiYMDY =" + self.bill_day +
                        " AND (RURIDT.RurToriKBN = 1 OR RURIDT.RurToriKBN = 3)"
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
        warnings.filterwarnings("ignore", category=UserWarning)
        date_SIME_DAY:datetime.date = datetime.datetime.strptime(self.SIME_DAY, '%Y%m%d')
        date_stt_day:datetime.date = (date_SIME_DAY - relativedelta(months=1) 
                                      + relativedelta(days=1))
        stt_day:str = date_stt_day.strftime('%Y%m%d')

        sql_server:SqlServer = SqlServer()
        cnxn = sql_server.get_cnxn()

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
