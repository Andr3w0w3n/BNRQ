import os

appdata = os.getenv('APPDATA')
bnrq_path = os.path.join(appdata, 'BNRQ')

print(os.path.exists(os.path.join(bnrq_path, 'settings.json')))