import pandas as pd

# Đọc dữ liệu từ file CSV
df = pd.read_csv('results.csv')

# Điền giá trị mặc định cho các cột quan trọng (0 cho số, 'N/A' cho chuỗi)
df.fillna({
    # Các cột số - điền 0
    'Standard_Gls': 0,
    'Standard_Ast': 0,
    'Standard_xG': 0,
    'Standard_xAG': 0,
    'Passing_Cmp': 0,
    'Defense_Tkl': 0,
    'Possession_Touches': 0,
    'Standard_Min': 0,
    'Standard_MP': 0,
    'Standard_Starts': 0,
    'Standard_90s': 0,
    
    # Các cột tỷ lệ/chuỗi - điền 'N/A'
    'Shooting_SoT%': 'N/A',
    'Shooting_SoT': 'N/A',
    'Passing_Att': 'N/A',
    'Passing_Cmp%': 'N/A',
    'Defense_Int': 'N/A',
    'Defense_Blocks': 'N/A',
    'Possession_Prog': 'N/A',
    'Playing_Time_90s': 'N/A'
}, inplace=True)

# Đối với tất cả các cột còn lại chưa được xử lý, điền 'N/A'
for column in df.columns:
    if df[column].isna().any():  
        if column not in ['Standard_Gls', 'Standard_Ast', 'Standard_xG', 'Standard_xAG', 
                         'Passing_Cmp', 'Defense_Tkl', 'Possession_Touches',
                         'Standard_Min', 'Standard_MP', 'Standard_Starts', 'Standard_90s']:
            df[column].fillna('N/A', inplace=True)

# Hàm ước tính giá trị chuyển nhượng 
def estimate_transfer_value(row):
    base_value = 0
    
    # Giá trị cơ bản theo vị trí 
    if 'FW' in row['Pos']:
        base_value = 15
    elif 'MF' in row['Pos']:
        base_value = 10
    elif 'DF' in row['Pos']:
        base_value = 8
    elif 'GK' in row['Pos']:
        base_value = 5
    else:
        base_value = 5  
    
    
    age_factor = max(0.5, 1.5 - (row['Age'] - 20) * 0.03)  
    
    
    performance_factor = 1 + (
        row['Standard_Gls'] * 0.2 +
        row['Standard_Ast'] * 0.15 +
        row['Standard_xG'] * 0.1 +
        row['Standard_xAG'] * 0.1
    ) / 10
    
    # Điều chỉnh theo thời gian thi đấuu
    minutes_factor = min(1, row['Standard_Min'] / 2000)  
    
    # Giá trị ước tính
    transfer_value = base_value * age_factor * performance_factor * minutes_factor
    
    # Làm tròn và giới hạn giá trị tối thiểu 
    transfer_value = max(0.5, round(transfer_value, 1))
    
    return transfer_value

# Thêm cột Transfer_Value 
df['Transfer_Value'] = df.apply(estimate_transfer_value, axis=1)

# Định dạng giá trị chuyển nhượng 
df['Transfer_Value_Str'] = df['Transfer_Value'].apply(lambda x: f"€{x}M")


print(df[['Player', 'Team', 'Pos', 'Age', 'Standard_Gls', 'Standard_Ast', 'Transfer_Value']] 
      .sort_values('Transfer_Value', ascending=False)
      .head(20))

# Lưu file 
df.to_csv('results4.csv', index=False)