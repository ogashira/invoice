import smtplib
from email.message import EmailMessage
import mimetypes
import os # ファイルの存在チェックに使用

# --- 1. 設定情報 ---
SMTP_SERVER = 'smtp.gmail.com' # 例: Gmail
SMTP_PORT = 587
SENDER_EMAIL = 'あなたのメールアドレス'
SENDER_PASSWORD = 'あなたのアプリパスワード'

# 宛先情報
RECEIVER_EMAIL = 'main_recipient@example.com'
# 複数のCCアドレスをリストで指定
CC_EMAILS = [
    'cc_person1@example.com', 
    'cc_person2@example.com',
    'cc_person3@example.com'
]

# 複数の添付ファイルをリストで指定
ATTACHMENT_FILES = [
    'file1.pdf',
    'file2.pdf',
    'report_2025.pdf' # 必要に応じて任意のファイル名に変更
]

# --- 2. メールオブジェクトの作成 ---
msg = EmailMessage()
msg['Subject'] = '【重要】複数CC・複数ファイル添付テスト'
msg['From'] = SENDER_EMAIL
msg['To'] = RECEIVER_EMAIL

# CCをリストからカンマ区切りの文字列に結合して設定
msg['Cc'] = ", ".join(CC_EMAILS)

msg.set_content("""
お疲れ様です。

Pythonスクリプトから送信されたテストメールです。
複数のCCアドレスに送信され、複数のPDFファイルが添付されています。

ご確認よろしくお願いいたします。
""")

# --- 3. 複数のファイルを添付 ---
print("ファイルの添付を開始します...")
missing_files = []

for file_path in ATTACHMENT_FILES:
    if not os.path.exists(file_path):
        missing_files.append(file_path)
        continue

    # ファイルのMIMEタイプを判別
    ctype, encoding = mimetypes.guess_type(file_path)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream' # 不明な場合は汎用的なタイプを使用

    maintype, subtype = ctype.split('/', 1)

    try:
        with open(file_path, 'rb') as fp:
            file_data = fp.read()
        
        # 添付
        msg.add_attachment(file_data,
                           maintype=maintype,
                           subtype=subtype,
                           filename=os.path.basename(file_path)) # ファイル名を設定
        print(f"  - 添付完了: {file_path}")

    except Exception as e:
        print(f"  - エラー: {file_path} の読み込み中にエラーが発生しました: {e}")
        
if missing_files:
    print(f"\n警告: 以下のファイルが見つからなかったため添付されませんでした: {', '.join(missing_files)}")
    # 添付ファイルがない場合は、送信を中止するかどうか検討してください。

# --- 4. SMTPサーバーに接続して送信 ---
print("\nSMTPサーバーに接続し、メールを送信します...")
try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        # TLS/STARTTLSで接続を暗号化
        server.starttls()
        # ログイン
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # 全ての宛先（To, Cc, Bcc）のリストを作成
        all_recipients = [RECEIVER_EMAIL] + CC_EMAILS
        
        # メール送信 (send_messageは内部で正しい宛先リストを処理します)
        server.send_message(msg)
        
    print("\n✅ メールが正常に送信されました。")

except Exception as e:
    print(f"\n❌ メール送信中にエラーが発生しました: {e}")
