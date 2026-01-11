import os
import random
from datetime import datetime, timedelta

from dotenv import load_dotenv # 需要 pip install python-dotenv
from supabase import create_client, Client

# === 配置 ===
load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
if url is None or key is None:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY; set them in your environment or .env file.")
supabase: Client = create_client(url, key)

# === 模拟素材 ===
TOURNAMENTS = [
    {"name": "2025春节演武大会", "date": "2025-02-15"},
    {"name": "2025夏季排位赛", "date": "2025-06-20"},
    {"name": "2025中原武术节", "date": "2025-09-10"},
]

PLAYERS = [
    "杨过", "小龙女", "郭靖", "黄蓉", "金轮法王", 
    "老顽童", "黄药师", "欧阳锋", "洪七公", "一灯大师",
    "独孤求败", "风清扬", "令狐冲", "东方不败", "任我行"
]

RULES = [
    {"type": "round", "params": {"C": 7, "G": 7}},  # 7回合制
    {"type": "round", "params": {"C": 5, "G": 5}},  # 5回合制
    {"type": "cap", "params": {"Q": 11}},           # 11分
]

def generate_mock_data(count=50):
    print(f"🎲 正在生成 {count} 场模拟对局...")
    
    mock_rows = []
    
    for _ in range(count):
        # 1. 随机选一场比赛
        tournament = random.choice(TOURNAMENTS)
        
        # 2. 随机选两个不同的人
        p_a = random.choice(PLAYERS)
        p_b = random.choice(PLAYERS)
        while p_a == p_b:
            p_b = random.choice(PLAYERS)
            
        # 3. 随机比分 (模拟一些悬殊和势均力敌)
        score_a = random.randint(0, 10)
        score_b = random.randint(0, 10)
        
        # 4. 随机赛制
        rule = random.choice(RULES)
        
        row = {
            "tournament_name": tournament["name"],
            "date": tournament["date"],
            "player_a_name": p_a,
            "player_b_name": p_b,
            "score_a": score_a,
            "score_b": score_b,
            "rule_type": rule["type"],
            "rule_params": rule["params"]
        }
        mock_rows.append(row)
        
    # 5. 批量写入 raw_matches
    # 注意：如果数据量太大，Supabase 建议分批插入，这里50条一次性没问题
    res = supabase.table('raw_matches').insert(mock_rows).execute()
    print(f"✅ 成功插入 {len(res.data)} 条原始数据到 raw_matches 表！")
    print("现在你的数据库里已经有素材了，可以去跑计算脚本了。")

if __name__ == "__main__":
    generate_mock_data(50)