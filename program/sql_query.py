import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
from sql_server import SqlServer


class SqlBTSZAN(object):

    def __init__(self, sime_day):
        self.sime_day = sime_day
      
    def fetch_sqldata(self):
        sql_server = SqlServer()
        cnxn = sql_server.get_cnxn()

        sql_query = ("SELECT TszTokCD, TszSimeDay, TszSeiZanZ, TszUriKinT, TszZeiKinT,"
                    " TszNyuKinT,"
                    " TszSeiZanK, TszUriKin1, TszNyuKin1, TszNyuKin7 "
                    " FROM dbo.BTSZAN"
                    " WHERE TszSimeDay =" + self.sime_day +
                    " ORDER BY TszTokCD"
                    )
        sime_data = pd.read_sql(sql_query, cnxn)

        return sime_data


class SqlRURIDT(object):

    def __init__(self, bill_day):
        self.bill_day = bill_day
      
    def fetch_sqldata(self):
        sql_server = SqlServer()
        cnxn = sql_server.get_cnxn()

        sql_query = ("SELECT RURIDT.RurUNo, RURIDT.RurTokCD,"
                    " RURIDT.RurSeiCD, RURIDT.RurHinCD, RURIDT.RurUriDay,"
                    " RURIDT.RurToriKBN, RURIDT.RurHinNam, RURIDT.RurUriTniCD,"
                    " RURIDT.RurKoSu, RURIDT.RurUriTnk, RURIDT.RurUriKin,"
                    " RURIDT.RurzeiTni, RURIDT.RurZeiKin, RURIDT.RurSeiYMDY,"
                    " RURIDT.RurSeiUpFlg, RURIHD.RurTokNam1, RURIHD.RurTokNam2,"
                    " RURIHD.RurTokNam3, RURIHD.RurTokPosNo1,"
                    " RURIHD.RurTokPosNo2, RURIHD.RurTokAddr1,"
                    " RURIHD.RurTokAddr2, RURIHD.RurTokAddr3, RJYUCD.RjcCMNo"
                    " From dbo.RURIDT"
                    " LEFT JOIN dbo.RURIHD"
                    " ON RURIDT.RurUNo = RURIHD.RurUNo"
                    " LEFT JOIN dbo.RJYUCD"
                    " ON RURIDT.RurJCNo = RJYUCD.RjcJCNo"
                    " AND RURIDT.RurJGNo = RJYUCD.RjcJGNo"
                    " WHERE RurSeiYMDY =" + self.bill_day +
                    " AND (RURIDT.RurToriKBN = 1 OR RURIDT.RurToriKBN = 3)"
                    " ORDER BY RURIDT.RurSeiCD, RURIDT.RurUriDay, RURIDT.RurUNo"
                    )
        sales_data = pd.read_sql(sql_query, cnxn)

        return sales_data


class SqlRNYUKN(object):
    '''
    入金のデータは締め日１ヵ月前～締め日までの範囲を取得する
    '''

    def __init__(self, sime_day):
        self.sime_day = sime_day

    def fetch_sqldata(self):
        date_sime_day = datetime.datetime.strptime(self.sime_day, '%Y%m%d')
        date_stt_day = (date_sime_day - relativedelta(months=1) 
                                      + relativedelta(days=1))
        stt_day = date_stt_day.strftime('%Y%m%d')

        sql_server = SqlServer()
        cnxn = sql_server.get_cnxn()

        sql_query = ("SELECT RnyNNo, RnyNGNo, RnySeiCD, RnyToriKBN,"
                    " RnyNyuDay, RnyNyuKin, RnyTegataDay, RnyTegataNo,"
                    " RnySeiUpFlg"
                    " From dbo.RNYUKN"
                    " WHERE RnyNyuDay >=" + stt_day + 
                    " AND RnyNyuDay <=" + self.sime_day +
                    " ORDER BY RnySeiCD, RnyNyuDay"
                    )
        deposit_data = pd.read_sql(sql_query, cnxn)

        return deposit_data
