import os
import shutil
import smtplib

from typing import List, Dict
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders



class SendMail(object):

    def __init__(self, yaml_data)-> None:

        self.__yaml_data = yaml_data


    def send_mail(self, info: Dict, 
                  attachment_files: List[str])-> List[str]:

        year: str = info['year']
        month: str = info['month']

        def move_successSendCsvFiles(csvPath, dst_folder):
            dst_path = os.path.join(dst_folder, os.path.basename(csvPath))
            shutil.move(csvPath, dst_path)


        success_send_mail: List[str] = []
        customer_code: str = info['customer_code']
        office_name: str = info['office_name'] 
        busyo_name: str = info['busyo_name']
        tantou_name: str = info['tantou_name']
        mailAddress: str = info['to_main']
        # ccのリストの最後にmatsudoアドレスを追加する
        ccs: List[str] = info['to_ccs']
        ccs.append('h_matsudo@toyo-jupiter.co.jp')

        charset = 'utf-8'

        #smtp_host = 'smtp.toyo-jupiter.co.jp'
        smtp_host = self.__yaml_data['eigyou']['smtp_host']
        smtp_port= self.__yaml_data['eigyou']['smtp_port']
        username = self.__yaml_data['eigyou']['username']
        password = self.__yaml_data['eigyou']['password']
        from_address = self.__yaml_data['eigyou']['from_address']
        to_address = mailAddress
        

        body = MIMEText(
                f'{office_name} \n'
                f'{busyo_name} \n'
                f'{tantou_name} \n'
                '\n\n' 
                'いつも大変お世話になっております \n'
                f'{year}年{month}月の請求書を送付いたします。\n\n'
                'よろしくお願い申し上げます。\n\n\n'
                '東洋工業塗料株式会社 \n'
                '松戸\n\n'
                 , 'plain', charset)


        msg = MIMEMultipart()

        msg['Subject'] = Header('請求書', charset)
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Cc'] = ', '.join(ccs)
        msg.attach(body)


        missing_files = []
        for file_path in attachment_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
                continue
            
            attach = MIMEBase('application', 'pdf')
            try:
                with open(file_path, 'br') as f:
                    attach.set_payload(f.read())
            except Exception:
                print('添付失敗')

            encoders.encode_base64(attach)
            attach.add_header("Content-Disposition", "attachement", 
                                  filename = os.path.basename(file_path))
            msg.attach(attach)

           #/192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/02請求書/03Pdf/20251031/02提出済
            dst_folder: str = '/'.join(file_path.split('/')[:-2]) + '/02提出済'
            try:
                smtp = smtplib.SMTP(smtp_host, smtp_port)
                smtp.login(username, password)
                smtp.send_message(msg)
                success_send_mail.append(os.path.basename(file_path))
                #success_send_mail.append(destination)
                smtp.quit
                move_successSendCsvFiles(file_path,  dst_folder)
            except Exception:
                print('mail送信失敗')



        return success_send_mail

