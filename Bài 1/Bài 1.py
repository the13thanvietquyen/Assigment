from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
import time

# Cấu hình ChromeDriver
service = Service("C:/ChromeDriver/chromedriver.exe")  # Thay đổi đường dẫn
driver = webdriver.Chrome(service=service)

# Danh sách các URL 
STATS_URLS = {
    'standard': "https://fbref.com/en/comps/9/stats/Premier-League-Stats",
    'shooting': "https://fbref.com/en/comps/9/shooting/Premier-League-Stats",
    'passing': "https://fbref.com/en/comps/9/passing/Premier-League-Stats",
    'gca': "https://fbref.com/en/comps/9/gca/Premier-League-Stats",
    'defense': "https://fbref.com/en/comps/9/defense/Premier-League-Stats",
    'possession': "https://fbref.com/en/comps/9/possession/Premier-League-Stats",
    'misc': "https://fbref.com/en/comps/9/misc/Premier-League-Stats",
    'keepers': "https://fbref.com/en/comps/9/keepers/Premier-League-Stats"
}

# Mapping đầy đủ data-stat 
COLUMN_MAP = {
    'player': ('Player', str),
    'nationality': ('Nation', str),
    'position': ('Pos', str),
    'team': ('Team', str),
    'age': ('Age', int),
    
    # Standard Stats
    'minutes': ('Standard_Min', int),
    'goals': ('Standard_Gls', int),
    'assists': ('Standard_Ast', int),
    'cards_yellow': ('Standard_CrdY', int),
    'cards_red': ('Standard_CrdR', int),
    'xg': ('Standard_xG', float),
    'xg_assist': ('Standard_xAG', float),
    'progressive_carries': ('Standard_PrgC', int),
    'progressive_passes': ('Standard_PrgP', int),
    'progressive_passes_received': ('Standard_PrgR', int),
    
    # Per 90 Stats
    'goals_per90': ('Standard_Gls/90', float),
    'assists_per90': ('Standard_Ast/90', float),
    'xg_per90': ('Standard_xG/90', float),
    'xg_assist_per90': ('Standard_xAG/90', float),
    
    # Shooting
    'shots_on_target_percent': ('Shooting_SoT%', float),
    'shots_on_target_per90': ('Shooting_SoT/90', float),
    'goals_per_shot': ('Shooting_G/Sh', float),
    'average_shot_distance': ('Shooting_Dist', float),
    
    # Passing
    'passes_completed': ('Passing_Cmp', int),
    'passes_pct': ('Passing_Total_Cmp%', float),
    'passes_total_distance': ('Passing_TotDist', int),
    'passes_short_pct': ('Passing_Short_Cmp%', float),
    'passes_medium_pct': ('Passing_Medium_Cmp%', float),
    'passes_long_pct': ('Passing_Long_Cmp%', float),
    'assisted_shots': ('Passing_KP', int),
    'passes_into_final_third': ('Passing_1/3', int),
    'passes_into_penalty_area': ('Passing_PPA', int),
    'crosses_into_penalty_area': ('Passing_CrsPA', int),
    
    # Goalkeeping
    'goals_against_per90': ('Goalkeeping_GA90', float),
    'save_percent': ('Goalkeeping_Save%', float),
    'clean_sheets_pct': ('Goalkeeping_CS%', float),
    'penalty_save_percent': ('Goalkeeping_Penalty_Save%', float),
    
    # Defense
    'tackles': ('Defense_Tkl', int),
    'tackles_won': ('Defense_TklW', int),
    'dribblers_tackled': ('Defense_Att', int),
    'challenges_lost': ('Defense_Lost', int),
    'blocks': ('Defense_Blocks', int),
    'blocked_shots': ('Defense_Sh', int),
    'blocked_passes': ('Defense_Pass', int),
    'interceptions': ('Defense_Int', int),
    
    # Possession
    'touches': ('Possession_Touches', int),
    'touches_def_pen_area': ('Possession_Def Pen', int),
    'touches_def_3rd': ('Possession_Def 3rd', int),
    'touches_mid_3rd': ('Possession_Mid 3rd', int),
    'touches_att_3rd': ('Possession_Att 3rd', int),
    'touches_att_pen_area': ('Possession_Att Pen', int),
    'dribble_success_pct': ('Possession_Succ%', float),
    'dribbled_past_pct': ('Possession_Tkld%', float),
    'carries': ('Possession_Carries', int),
    'carry_progressive_distance': ('Possession_PrgDist', int),
    'carries_into_final_third': ('Possession_1/3', int),
    'carries_into_penalty_area': ('Possession_CPA', int),
    'miscontrols': ('Possession_Mis', int),
    'dispossessed': ('Possession_Dis', int),
    'passes_received': ('Possession_Rec', int),
    
    # Misc
    'fouls': ('Misc_Fls', int),
    'fouls_drawn': ('Misc_Fld', int),
    'offsides': ('Misc_Off', int),
    'crosses': ('Misc_Crs', int),
    'ball_recoveries': ('Misc_Recov', int),
    'aerials_won': ('Misc_Won', int),
    'aerials_lost': ('Misc_Lost', int),
    'aerials_won_pct': ('Misc_Won%', float)
}

def get_html(url):
    driver.get(url)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table.stats_table')))
    time.sleep(2)
    return driver.page_source

def parse_value(raw_value, dtype):
    try:
        if not raw_value or raw_value.strip() == '':
            return 'N/A'
            
        cleaned_value = raw_value.replace(',', '').replace('%', '').replace('m', '').strip()
        
        # Xử lý giá trị đặc biệt
        if dtype == int:
            return int(float(cleaned_value)) if cleaned_value else 0
        elif dtype == float:
            if '%' in raw_value:
                return round(float(cleaned_value)/100, 3)
            return float(cleaned_value) if cleaned_value else 0.0
        else:
            return raw_value.strip()
    except Exception as e:
        return 'N/A'

# Khởi tạo dictionary lưu dữ liệu
players_data = {}

# Crawl dữ liệu từ tất cả các bảng
for stat_type, url in STATS_URLS.items():
    print(f"Đang crawl: {stat_type}...")
    try:
        html = get_html(url)
        soup = bs(html, 'html.parser')
        table = soup.find('table', id=f'stats_{stat_type}')
        
        if not table:
            continue
            
        for row in table.find('tbody').find_all('tr'):
            # Lấy thông tin cầu thủ
            player_cell = row.find('th', {'data-stat': 'player'}) or row.find('td', {'data-stat': 'player'})
            if not player_cell:
                continue
                
            player_name = player_cell.text.strip()
            if player_name not in players_data:
                players_data[player_name] = {col: 'N/A' for col, _ in COLUMN_MAP.values()}
                players_data[player_name]['Player'] = player_name
                
            # Cập nhật dữ liệu
            for cell in row.find_all(['th', 'td']):
                stat = cell.get('data-stat')
                if stat in COLUMN_MAP:
                    col_name, dtype = COLUMN_MAP[stat]
                    raw_value = cell.text.strip()
                    
                    # Xử lý đặc biệt
                    if stat == 'age' and '-' in raw_value:
                        raw_value = raw_value.split('-')[0]
                    if stat == 'nationality':
                        match = re.search(r'(.+?)\s+\(([A-Z]{3})\)', raw_value)
                        raw_value = f"{match.group(1)} ({match.group(2)})" if match else raw_value
                    
                    # Gán giá trị đã parse
                    parsed_value = parse_value(raw_value, dtype)
                    players_data[player_name][col_name] = parsed_value
    except Exception as e:
        print(f"Lỗi khi crawl {stat_type}: {str(e)}")
        continue

# Lọc và chuẩn bị dữ liệu cuối cùng
filtered_data = []
for player in players_data.values():
    try:
        if player.get('Standard_Min', 0) > 90 or player.get('Standard_Min') == 'N/A':
            # Thay thế None/NaN bằng 'N/A' và đảm bảo thứ tự cột
            ordered_row = [
                player.get(col, 'N/A') if player.get(col) not in [None, ''] else 'N/A'
                for col, _ in COLUMN_MAP.values()
            ]
            filtered_data.append(ordered_row)
    except:
        continue

# Tạo DataFrame
columns = [col for col, _ in COLUMN_MAP.values()]
df = pd.DataFrame(filtered_data, columns=columns)
df.fillna('N/A', inplace=True)

# Xuất CSV
df.to_csv("results.csv", index=False) 
print(f"{len(df)}")
driver.quit()