import pandas as pd
from ..db.connect_db import engine
import os

curr_dir = os.path.dirname(os.path.abspath(__file__))
file_name = 'us_stock_index_history.csv'
file_path = [curr_dir,'datafiles',file_name]
file_path = os.path.join(*file_path)
data = pd.read_csv(file_path)
print(data)