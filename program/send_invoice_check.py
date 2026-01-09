import os
import glob
import platform
from typing import List

class SendInvoiceCheck:
    '''
    submission_invoices(提出が必要なinvoiceのリスト)を作るのが目的
    そのために、submitted_invoices(提出済フォルダの中身),
    unsubmitted_invoices(未提出フォルダの中身)を作る
    '''

    def __init__(self, sime_day: str)-> None:
        self.__unsubmitted_folder = \
         fr'//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/02請求書/03Pdf/{sime_day}/01未提出'
        self.__submitted_folder = \
         fr'//192.168.1.247/共有/営業課ﾌｫﾙﾀﾞ/02請求書/03Pdf/{sime_day}/02提出済'
        if platform.system() == 'Linux':
            self.__unsubmitted_folder = \
                fr'/mnt/public/営業課ﾌｫﾙﾀﾞ/02請求書/03Pdf/{sime_day}/01未提出'
            self.__submitted_folder = \
                fr'/mnt/public/営業課ﾌｫﾙﾀﾞ/02請求書/03Pdf/{sime_day}/02提出済' 

        self.__submitted_invoices:List[str] = self.create_submitted_invoices()
        self.__unsubmitted_invoices:List[str] = self.create_unsubmitted_invoices()


    def find_submission_invoices(self)-> List[str]:
        '''
        unsubmitted_invoicesの要素がsubmitted_invoicesの中に存在しなければ、
        _y_があるinvoiceのみ
        submission_invoicesにappendする
        '''
        submission_invoices:List[str] = []

        for invoice in self.__unsubmitted_invoices:
            try:
                y_or_n: str = invoice.split('_')[2] # "y" or "n"
                yuusou: str = invoice.split('_')[3] # "郵送"
                if yuusou == "郵送":
                    continue
                if invoice in self.__submitted_invoices:
                    continue
                if y_or_n == 'y':
                    submission_invoices.append(invoice)
            except IndexError:
                pass
        '''
        '_y_'や'_n_'が無いとIndexErrorが起き、submission_invoicesにappend
        されない
        '''

        return submission_invoices


    def create_submitted_invoices(self)-> List[str]:
        submitted_invoices = []
        # 検索パターンを定義 (指定ディレクトリ内の全ての.pdfファイル)
        search_pattern = os.path.join(self.__submitted_folder, '*.pdf')
        # glob.glob を使ってパターンに一致するファイルパスのリストを取得
        # Windowsのパス区切り文字 \ はPythonで自動的に処理されます
        file_paths = glob.glob(search_pattern)
        # フルパスからファイル名のみを抽出してリストに格納
        submitted_invoices = [os.path.basename(path) for path in file_paths]

        return submitted_invoices


    def create_unsubmitted_invoices(self)-> List[str]:
        unsubmitted_invoices = []
        search_pattern = os.path.join(self.__unsubmitted_folder, '*.pdf')
        file_paths = glob.glob(search_pattern)
        unsubmitted_invoices = [os.path.basename(path) for path in file_paths]

        return unsubmitted_invoices

