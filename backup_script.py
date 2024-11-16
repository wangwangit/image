import os
from O365 import Account
import glob

# 获取环境变量中的凭证
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
refresh_token = os.environ['REFRESH_TOKEN']

# 初始化 OneDrive 连接
credentials = (client_id, client_secret)
account = Account(credentials)
account.connection.refresh_token = refresh_token

# 获取 OneDrive 实例
storage = account.storage()
drive = storage.get_default_drive()

# 在 OneDrive 中创建备份文件夹（如果不存在）
backup_folder_name = 'GitHub-Images-Backup'
items = drive.get_items()
backup_folder = None

for item in items:
    if item.name == backup_folder_name:
        backup_folder = item
        break

if not backup_folder:
    backup_folder = drive.create_folder(backup_folder_name)

# 上传所有文件
for file_path in glob.glob('**/*.*', recursive=True):
    if not file_path.startswith('.git') and not file_path.startswith('.github'):
        with open(file_path, 'rb') as file:
            # 保持相同的文件路径结构
            remote_path = os.path.join(backup_folder_name, file_path)
            print(f'Uploading {file_path} to {remote_path}')
            drive.upload_file(file, remote_path)
