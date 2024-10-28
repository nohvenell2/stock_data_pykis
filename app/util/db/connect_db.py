from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv()
DB_ID = os.getenv('DB_ID')
DB_PW = os.getenv('DB_PW')
DB_ADDR = os.getenv('DB_ADDR')
engine = create_engine(f'mysql+pymysql://{DB_ID}:{DB_PW}@{DB_ADDR}')