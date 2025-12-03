import datetime
from dateutil.relativedelta import relativedelta

def is_end_of_month(date_to_check: datetime.datetime) -> bool:
    """
    指定された日付がその月の最終日であるかを判定します。
    """
    # 1. まず、次の月の1日を取得します。
    #    現在の月に1ヶ月を足し、日の部分を1日に設定します。
    first_day_of_next_month = (date_to_check +
relativedelta(months=1)).replace(day=1)

    # 2. 次の月の1日から1日引くと、現在の月の最終日になります。
    last_day_of_current_month = first_day_of_next_month - datetime.timedelta(days=1)

    # 3. 元の日付の日と計算した最終日の日が一致するかを比較し す。
    return date_to_check == last_day_of_current_month

    
def calc_stt_day(sime_day: str)-> str:
    date_sime_day = datetime.datetime.strptime(sime_day, '%Y%m%d')
    if is_end_of_month(date_sime_day):
        date_stt_day = date_sime_day.replace(day=1)
    else:
        date_stt_day = date_sime_day - relativedelta(months=1) + relativedelta(days=1)
    
    stt_day: str = date_stt_day.strftime('%Y%m%d')

    return stt_day




sime_day = '20241130'
print(calc_stt_day(sime_day))
