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



class MailAddTestSendMail(object):

    def __init__(self, yaml_data)-> None:

        self.__yaml_data = yaml_data


    def send_mail(self, info: Dict, 
                  submission_invoices: List[str])-> List[str]:

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
        title: str = info['title']
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

        title = f'【重要】請求書電子化に伴うメールアドレス確認のお願い（東洋工業塗料株式会社)'
        

        body = MIMEText(
                f'{office_name} \n'
                f'{busyo_name} \n'
                f'{tantou_name} \n'
                '\n\n' 
                
                'いつも大変お世話になっております。 東洋工業塗料 松戸でございます。\n'
                '平素は格別のご高配を賜り、厚く御礼申し上げます。\n'
                'さて、ご案内申し上げました通り、2026年2月発送分より、請求書の送付方法を従来の郵送から\n'
                '電子メール（PDF形式）へ変更させていただくこととなりました。\n'
                'つきましては、送付先の誤りを防ぐため、事前にメールアドレスの疎通確認を行っております。\n'
                'お忙しいところ恐縮ですが、本メールを受信されましたら、本メールへそのまま「受信確認済み」\n'
                'とご返信をいただけますでしょうか。\n'
                'また、CCでお送りしたご担当者様にも本メールが届いているかのご確認も頂けたら幸いです\n'
                'ご不明な点がございましたら、お気軽にお問い合わせください。 \n'
                '今後とも変わらぬお引き立てを賜りますよう、お願い申し上げます。\n\n'
                '東洋工業塗料株式会社 \n'
                '松戸\n\n'
                 , 'plain', charset)


        msg = MIMEMultipart()

        msg['Subject'] = Header(title, charset)
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Cc'] = ', '.join(ccs)
        msg.attach(body)


        missing_files = []
        tmp: List[str] = []
        try:
            smtp = smtplib.SMTP(smtp_host, smtp_port)
            smtp.login(username, password)
            smtp.send_message(msg)
            smtp.quit
            # 上のfor文で呼ばれた順番にtmpに詰まっている
            success_send_mail.append(customer_code)
        except Exception as e:
            print('mail送信失敗')
            print(e)



        return success_send_mail

