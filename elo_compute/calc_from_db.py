from supabase import create_client, Client
import json

# 1. 配置 (填你的 URL 和 Key)
import os
from dotenv import load_dotenv # 需要 pip install python-dotenv

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
if url is None or key is None:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY; set them in your environment or .env file.")
supabase: Client = create_client(url, key)

# 2. 核心公式 (和大枪规则一致)
def calculate_expectancy(R_A, R_B):
    return 1 / (1 + 10 ** ((R_B - R_A) / 400))

def calculate_score_factor(match_row, score_own, score_opp):
    """根据数据库里的 rule_params 计算 S 值"""
    params = match_row['rule_params'] # 读取我们刚补全的 JSON
    rule = match_row['rule_type']
    
    P_A = score_own
    P_B = score_opp
    
    if rule == 'round':
        C = params.get('C', 7) # 默认7回合
        G = params.get('G', 7)
        # 防止除以0
        term1 = (P_A / (P_A + P_B)) * (G / C) if (P_A + P_B) > 0 else 0
        term2 = (C - G) / (C * 2) if C > 0 else 0
        return term1 + term2
        
    elif rule == 'cap':
        Q = params.get('Q', 20)
        return (P_A + Q - P_B) / (2 * Q)
        
    return 0.5 # 默认

def get_k_factor(match_row):
    """根据规则计算 K"""
    params = match_row['rule_params']
    rule = match_row['rule_type']
    
    # 简单示例逻辑，你可以根据你的详细文档完善
    if rule == 'round':
        C = params.get('C', 7)
        if C >= 4: return 32
    return 32

# 3. 主流程：只读取 is_calculated = FALSE 的比赛
def process_new_matches():
    # 获取所有未计算的比赛，按 ID 排序确保时间顺序
    response = supabase.table('matches')\
        .select("*")\
        .eq('is_calculated', False)\
        .order('id')\
        .execute()
    
    matches = response.data
    if not matches:
        print("没有新比赛需要计算。")
        return

    print(f"发现 {len(matches)} 场新比赛，开始计算...")

    # 获取所有选手的最新分数缓存
    all_players = supabase.table('players').select("*").execute().data
    player_map = {p['id']: p for p in all_players}

    for m in matches:
        w_id = m['winner_id']
        l_id = m['loser_id']
        
        winner = player_map.get(w_id)
        loser = player_map.get(l_id)
        
        if not winner or not loser:
            print(f"错误：找不到选手 ID {w_id} 或 {l_id}")
            continue
            
        # --- 开始计算 ---
        R_w_old = winner['current_elo']
        R_l_old = loser['current_elo']
        
        # 计算 winner 的 S 值
        S_w = calculate_score_factor(m, m['score_winner'], m['score_loser'])
        E_w = calculate_expectancy(R_w_old, R_l_old)
        
        K = get_k_factor(m)
        
        change_w = round(K * (S_w - E_w))
        change_l = -change_w # 零和游戏
        
        R_w_new = R_w_old + change_w
        R_l_new = R_l_old + change_l
        
        # --- 更新数据库 ---
        
        # 1. 写入历史记录 (elo_history)
        history_data = [
            {"player_id": w_id, "match_id": m['id'], "old_elo": R_w_old, "new_elo": R_w_new, "change_val": change_w, "date": "2025-01-09"}, # 日期最好也是数据库里读取
            {"player_id": l_id, "match_id": m['id'], "old_elo": R_l_old, "new_elo": R_l_new, "change_val": change_l, "date": "2025-01-09"}
        ]
        supabase.table('elo_history').insert(history_data).execute()
        
        # 2. 更新选手当前分 (players)
        supabase.table('players').update({'current_elo': R_w_new}).eq('id', w_id).execute()
        supabase.table('players').update({'current_elo': R_l_new}).eq('id', l_id).execute()
        
        # 3. 标记这场比赛已计算 (matches) !!! 重要
        supabase.table('matches').update({'is_calculated': True}).eq('id', m['id']).execute()
        
        # 更新本地缓存，以便下一场比赛利用最新分
        winner['current_elo'] = R_w_new
        loser['current_elo'] = R_l_new
        
        print(f"比赛 {m['id']} 处理完毕：胜者变动 {change_w}, 败者变动 {change_l}")

if __name__ == "__main__":
    process_new_matches()