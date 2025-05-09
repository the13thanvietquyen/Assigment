import pandas as pd

# Đọc dữ liệu từ file CSV
df = pd.read_csv('results2.csv')

# Danh sách các chỉ số để đánh giá
chi_so_quan_trong = [
    'Median of Standard_Gls', 'Mean of Standard_Gls',  
    'Median of Standard_Ast', 'Mean of Standard_Ast', 
    'Median of Standard_xG', 'Mean of Standard_xG',    
    'Median of Standard_xAG', 'Mean of Standard_xAG',  
    'Median of Passing_Cmp', 'Mean of Passing_Cmp',    
    'Median of Possession_Touches', 'Mean of Possession_Touches',  
    'Median of Defense_Int', 'Mean of Defense_Int',    
    'Median of Goalkeeping_Save%', 'Mean of Goalkeeping_Save%'     
]

# Tìm đội dẫn đầu cho từng chỉ số
doi_dan_dau = {}
for chi_so in chi_so_quan_trong:
    doi_tot_nhat = df.loc[df[chi_so].idxmax(), 'Team']
    doi_dan_dau[chi_so] = doi_tot_nhat

# Đếm số lần mỗi đội dẫn đầu
diem_so_doi = {}
for doi in doi_dan_dau.values():
    if doi in diem_so_doi:
        diem_so_doi[doi] += 1
    else:
        diem_so_doi[doi] = 1

# Sắp xếp các đội theo điểm số
doi_xep_hang = sorted(diem_so_doi.items(), key=lambda x: x[1], reverse=True)

# Hiển thị kết quả

for chi_so, doi in doi_dan_dau.items():
    print(f"{chi_so}: {doi}")


for doi, diem in doi_xep_hang:
    print(f"{doi}: {diem}")

# Xác định đội có thành tích tốt nhất
doi_tot_nhat = doi_xep_hang[0][0]
print(f"\nĐội có thành tích tốt nhất: {doi_tot_nhat}")