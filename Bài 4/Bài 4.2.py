import pandas as pd
from pathlib import Path

def safe_read_csv(file_path, default_data=None):

    try:
        if not Path(file_path).exists():
            raise FileNotFoundError(f"{file_path}")
            
        data = pd.read_csv(file_path)
        
        if data.empty:
            return default_data if default_data is not None else pd.DataFrame()
            
        return data
        
    except Exception as e:
        print(f"{str(e)}")
        return default_data if default_data is not None else pd.DataFrame()

# Sử dụng
data = safe_read_csv(
    'results4.csv',  
    default_data=pd.DataFrame({'player': ['Demo'], 'goals': [0]})
)

print(data)