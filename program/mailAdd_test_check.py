from re import I
from typing import List
import pandas as pd
from send_invoice_mail_info import MailInfo

class MailAddTestCheck:
    '''
    submission_invoices(提出が必要なinvoiceのリスト)を作るのが目的
    そのために、submitted_invoices(提出済フォルダの中身),
    unsubmitted_invoices(未提出フォルダの中身)を作る
    '''

    def __init__(self, sime_day: str, is_test:bool)-> None:
        self.sime_day = sime_day
        self.is_test = is_test



    def find_submission_invoices(self)-> List[str]:
        '''
        unsubmitted_invoicesの要素がsubmitted_invoicesの中に存在しなければ、
        _y_があるinvoiceのみ
        submission_invoicesにappendする
        '''
        mail_info = MailInfo(self.is_test)
        mail_infos:pd.DataFrame = mail_info.get_mail_infos()

        tokui_cds = list(mail_infos['得意先CD'])
        uniqu_cds = list(set(tokui_cds))

        submission_invoices:List[str] = []
        for cd in uniqu_cds:
            submission_invoices.append(f'{self.sime_day}_{cd}_y_.pdf')
            
        return submission_invoices
