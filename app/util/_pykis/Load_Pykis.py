from dotenv import load_dotenv
import os
from pykis import PyKis
load_dotenv()
SITE_ID=os.getenv('SITE_ID')
ACC_NO_REAL=os.getenv('ACC_NO_REAL')
APP_KEY_REAL=os.getenv('APP_KEY_REAL')
APP_SEC_REAL=os.getenv('APP_SEC_REAL')
#ACC_NO_TEMP=os.getenv('ACC_NO_TEMP')
#APP_KEY_TEMP=os.getenv('APP_KEY_TEMP')
#APP_SEC_TEMP=os.getenv('APP_SEC_TEMP')
KIS = PyKis(
    id=SITE_ID,
    account=ACC_NO_REAL,
    appkey=APP_KEY_REAL,
    secretkey=APP_SEC_REAL,
    keep_token=True
)