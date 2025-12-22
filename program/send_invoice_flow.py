import datetime
from re import sub
import sys
import platform
from typing import List
from send_invoice_check import SendInvoiceCheck
from send_invoice_send_mail import SendMail
from send_invoice_mail_info import MailInfo
from send_invoice_customer import SendInvoiceCustomer


class SendInvoiceFlow:
    '''
    submission_invoices = 
                ['20251031_T2880_y_.pdf',
                 '20251031_T3350_y_.pdf',
                 '20251031_T3500_y_.pdf',
                 '20251031_T3540_y_.pdf',
                 '20251031_T3830_y_.pdf',
                 '20251031_T3890_y_.pdf',
                 '20251031_T4120_y_.pdf',
                 '2025_T2880_y_ - コピー.pdf']
    
    customer_codeごとのリスト要素数1がほとんど
    attachment_files = 
                ['//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/02請求書/03Pdf/20251031/01未提出/20251031_T3890_y_.pdf']
                ['//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/02請求書/03Pdf/20251031/01未提出/20251031_T3830_y_.pdf']
                ['//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/02請求書/03Pdf/20251031/01未提出/20251031_T3540_y_.pdf']
                ['//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/02請求書/03Pdf/20251031/01未提出/20251031_T3350_y_.pdf']
                ['//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/02請求書/03Pdf/20251031/01未提出/20251031_T4120_y_.pdf']
                ['//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/02請求書/03Pdf/20251031/01未提出/20251031_T2880_y_.pdf', '//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/02請求書/03Pdf/20251031/01未提出/2025_T2880_y_ - コピー.pdf']
                ['//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/02請求書/03Pdf/20251031/01未提出/20251031_T3500_y_.pdf']
    '''

    def __init__(self):
        pass


    def get_isTest(self)-> bool:
        args: List[str] = sys.argv
        if len(args) == 1:
            return False
        if args[1] == "test" or args[1] == "TEST":
            return True


    def create_attachment_files(self, customer_code, sime_day,  
                                      submission_invoices)-> List[str]:
        stt_path: str = \
         fr'//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/02請求書/03Pdf/{sime_day}/01未提出'
        if platform.system() == 'Linux':
            stt_path: str = \
            fr'/mnt/public/営業課ﾌｫﾙﾀﾞ/02請求書/03Pdf/{sime_day}/01未提出'

        attachment_files = []
        for invoice in submission_invoices:
            if customer_code == invoice.split('_')[1]:
                attachment_files.append(f'{stt_path}/{invoice}')


        return attachment_files


    def create_unique_customer_codes(self, submission_invoices)-> List[str]:
        customer_codes:List[str] = []
        try:
            for invoice in submission_invoices:
                customer_codes.append(invoice.split('_')[1])
        except IndexError:
            pass
        # 重複を取る
        unique_customer_codes:List[str] = list(set(customer_codes))

        return unique_customer_codes

    
    def start(self)->None:
        is_test: bool = self.get_isTest()

        sime_day: str = input('締め日を入力してください (例: 20250930) \n : ')
        try:
            date_sime_day:datetime.date = datetime.datetime.strptime(sime_day, '%Y%m%d')
        except ValueError:
            print('年月日が不正です。処理を中止します。')
            sys.exit()

        send_invoice_check:SendInvoiceCheck = SendInvoiceCheck(sime_day)
        submission_invoices: List[str] = send_invoice_check.find_submission_invoices()


        log_path:str = \
                  fr'//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/02請求書/03Pdf/{sime_day}/invoice_log.txt'
        if platform.system() == 'Linux':
            log_path:str = \
                  fr'/mnt/public/営業課ﾌｫﾙﾀﾞ/02請求書/03Pdf/{sime_day}/invoice_log.txt'

        now_date:str = datetime.datetime.now().date().strftime('%Y/%m/%d')
        now_time:str = datetime.datetime.now().time().strftime('%H:%M:%S')
        try:
            with open(log_path, 'a') as f:
                f.write('\n')
                f.write('プログラム実行日 : ' + now_date + '\n')
                f.write('            時刻 : ' + now_time + '\n\n')
                if submission_invoices:
                    print()
                    print(f'提出が必要なinvoiceは以下の{len(submission_invoices)}個です')
                    for submission_invoice in submission_invoices:
                        print(submission_invoice)
                    f.write(f'提出が必要なinvoiceは以下の{len(submission_invoices)}個です\n')
                    for invoice in submission_invoices:
                        f.write(invoice)
                        f.write('\n')
                else:
                    print(f'提出が必要なinvoiceはありません')
                    f.write(f'提出が必要なinvoiceはありません')
                    sys.exit()
        except FileNotFoundError:
            print('締め日のファイルが存在しないため処理を中止します')
            sys.exit()


        mail_info = MailInfo(is_test)
        mail_infos:pd.DataFrame = mail_info.get_mail_infos()
        yaml_data = mail_info.get_yaml_data()

        send_mail:SendMail = SendMail(yaml_data)

        unique_customer_codes: List[str] = self.create_unique_customer_codes(
                                                           submission_invoices)

        # Costomerのインスタンスを生成する
        send_invoice_customers: List[SendInvoiceCustomer] = []
        for customer_code in unique_customer_codes:
            mail_info: pd.DataFrame = \
                    mail_infos.loc[mail_infos['得意先CD'] == customer_code,:]
            attachment_files: List[str] = self.create_attachment_files(
                                          customer_code, 
                                          sime_day, 
                                          submission_invoices)
            send_invoice_customer: SendInvoiceCustomer = \
                    SendInvoiceCustomer(customer_code,
                                        sime_day,
                                        mail_info,
                                        attachment_files,
                                        send_mail)
            send_invoice_customers.append(send_invoice_customer)


        
        success_send_paths = []
        for send_invoice_customer in send_invoice_customers:
            success_send_paths.append(send_invoice_customer.send_invoice())

        print('\n')
        print('送信に成功した請求書pdf')
        cnt: int = 0
        for success_send_path in success_send_paths:
            for line in success_send_path:
                print(line)
                cnt += 1
        print(f'成功: {cnt}個')
        with open(log_path, 'a') as f:
            f.write('\n')
            f.write('>>>>>>送信に成功した請求書pdf<<<<<<\n')
            for success_send_path in success_send_paths:
                for line in success_send_path:
                    f.write(line + '\n')
            f.write(f'成功: {cnt}個\n')
