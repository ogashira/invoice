# 請求書自動作成発行システムについて
## システム概要
### 動作環境
- OS  
    - Windows11
    - ~~Linux(WSL2:Ubunts)~~
- インストール先
    - 松戸PC(toyo-pc04)
    - 尾頭PC(toyo-pc12) WSL2(Ubuntu)で開発
### 構築システム
- メインシステム: Python3.10
- Windowsスクリプト(.bat)
### ソースコード
- GitHub Publicリポジトリで公開</br>
[GitHub_ https://github.com/ogashira/invoice](https://github.com/ogashira/invoice)
### 起動方法
Winボタン+R -> i 入力 -> Enter
### 動作
1. programスタートでpythonが締め日を訊いてくる
1. 締め日入力(20250320)してEnter
1. `営業課ﾌｫﾙﾀﾞ/02請求書/Excell/`内に`20250320`フォルダが作られる。
1. そのフォルダの中に3/20締めの顧客の請求書(excelファイル)が作られる。
1. 同時に、`営業課ﾌｫﾙﾀﾞ/02請求書/Pdf/01未提出/内に20250320`フォルダが作られて、3/20締めの顧客の請求書(pdfファイル)が作られる。
1. メール送信で`01未提出/20250320`内の請求書が送信されると、`営業課ﾌｫﾙﾀﾞ/02請求書/Pdf/02提出済/20250320/`内に移動する。
1. 01未提出フォルダ内に残ってしまった請求書はメッセージで作業者に知らせる。</br>
ファイル名は「締め日_顧客コード.xlsx」ファイルツリーは下記のようなイメージ</br>
```
営業課ﾌｫﾙﾀﾞ
    |-02請求書
    |     |─ 01Master
    |     |     |- invoice_format.xlsx   # 請求書のエクセルフォーマット
    |     |     |- invoice.yaml          # 入金区分、メールアドレスなどのyamlファイル
    |     |─ 02Excel
    |     |     |─ 20250320
    |     |     |─ 20250320_T0020.xlsx
    |     |     |─ 20250320_T0060.xlsx
    |     |     |─ 20250320_T0100.xlsx
    |     |─ 03Pdf
    |     |     |─ 01未提出
    |     |     |    |- 20250320
    |     |     |          |─ 20250320_T0020.xlsx
    |     |     |          |─ 20250320_T0060.xlsx
    |     |     |          |─ 20250320_T0100.xlsx
    |     |     |─ 02提出済
    |_    |     |    |- 20250320
```
## クラス図っぽいやつ(日本語概念)
<img src="https://ogaoga.net/markdownApp/images/請求書自動作成発行システムイメージ図.jpg" alt="error" width="800px"></br>
## 仕様説明
- MainクラスはProgramFlowクラスをインスタンス化してstartメソッドを呼び出す。
- ProgramFlowはsql_query.pyにあるSqlBTSZAN(締めデータ),SqlRURIDT(売上データ),SqlRNYUKN(入金データ),SqlMTOKUI(得意先マスタデータ)クラスを使ってsqlデータをeffitAサーバーからfetchする。pandasのDataFrameを利用する。SQLServerに接続する時のID,PassWordは``\\192.168.1.247\共有\技術課ﾌｫﾙﾀﾞ\ﾏｸﾛ\init\sqlForVba.ini``ファイルに書かれている内容を参照する。
- 入手したデータをFactoryクラスに渡す。Factoryクラスでは渡されたDataFrameを使って、Sale, Deposit, SalesDeposits, Customer, Invoiceクラスのインスタンスを生成する。
- 顧客ごとにSaleインスタンスとDepositインスタンスを生成し、それらインスタンスのリストをSalesDepositクラスが保持する。
- SalesDepositクラスの中では、SaleインスタンスリストとDepositインスタンスリストからSales_Depositインスタンスのリストを作る。このリストは売上日または入金日が昇順になるようにソートされる。また、このクラスはSales_depositインスタンスの順番(index)とエクセルの行で構成されたdictionaryを持っている。このdictionaryはyamlファイルを参照して作る。`営業課ﾌｫﾙﾀﾞ/02請求書/01Master/invoice.yaml`
- InvoiceクラスはCustomerクラスのインスタンスとSalesDepositsクラスのインスタンスとExcelクラスのインスタンスを保持している。
- 全てのクラスはsetterやgetterを持っていないので、インスタンス変数の中身は誰も分からない（自分自身しか知らない）
- Invoiceクラスのfilling_page_invoiceメソッドを呼び出すと、InvoiceインスタンスがExcelクラスインスタンスに自分が持っている情報を書き込む。自分の書き込みが終わると、ExcelクラスインスタンスをCustomerインスタンスに渡して、Customerインスタンスが自分がもっている情報をExcelインスタンスに書き込む。同様に、Saleクラス、DepositクラスにExcelインスタンスを渡して、自分自身の情報を書いてもらう。
- 全てのインスタンスがExcelインスタンスに書き終わった時点で、１件のinvoice(請求書)が出来上がるので、「締め日_顧客コード.xlsx」として所定のフォルダに保存する。
- InvoiceクラスのインスタンスはProgramFrowクラスstartメソッドの中でリストとして存在しているので for invoice in invoices: でイテレータとして連続して請求書が作られていく。
- **とりあえず現在はここまで実装しており、請求書が正しく作られるかをテストします。今後、ExcelファイルをPdf化する実装とpdfをメールに添付して送信する実装を行う予定**
