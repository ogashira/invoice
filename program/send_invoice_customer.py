from typing import List, Dict
import pandas as pd

from send_invoice_send_mail import SendMail


class SendInvoiceCustomer:

    def __init__(self, customer_code: str, 
                 sime_day: str,
                 mail_info: pd.DataFrame, 
                 attachment_files: List[str],
                 send_mail: SendMail)-> None:

        self.__mail_to_customer_info: Dict = {}
        self.__mail_to_customer_info['customer_code'] = customer_code
        self.__mail_to_customer_info['year'] = sime_day[:4]
        self.__mail_to_customer_info['month'] = sime_day[4:6]
        self.__mail_to_customer_info['office_name'] = \
                                                mail_info.loc[:,'会社'].iloc[0]
        self.__mail_to_customer_info['busyo_name'] = \
                                                mail_info.loc[:,'部署'].iloc[0]
        self.__mail_to_customer_info['tantou_name'] = \
                                              mail_info.loc[:,'担当者'].iloc[0]
        self.__mail_to_customer_info['title'] = \
                                              mail_info.loc[:,'件名'].iloc[0]
        # メルアドまたは、"郵送"を取得することになる
        self.__mail_to_customer_info['to_main'] = \
               mail_info.loc[mail_info['main or cc'] == 'main','Email'].iloc[0]
        self.__mail_to_customer_info['to_ccs'] = \
                   list(mail_info.loc[mail_info['main or cc'] == 'cc','Email'])

        self.__attachment_files: List[str] = attachment_files
        self.send_mail: SendMail = send_mail


    def send_invoice(self)-> List[str]: 
        success_send_paths = \
                self.send_mail.send_mail(self.__mail_to_customer_info, 
                                                      self.__attachment_files)
        return success_send_paths


    def show_customer_code(self)-> str:
        '''
        これは使っていない
        '''
        return self.__mail_to_customer_info['customer_code']
