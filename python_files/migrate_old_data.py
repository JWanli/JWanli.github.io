import json
import os
import re
import time
from datetime import date, timedelta
from dotenv import load_dotenv
from supabase import create_client, Client

# === 1. 基础配置 ===
load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("请在 .env 文件中设置 SUPABASE_URL 和 SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 锚点日期：2050年1月1日
ANCHOR_DATE = date(2050, 1, 1)

# 断点续传：从第几个选手开始（0 表示从头开始）
START_FROM_INDEX = 0

def retry_on_failure(func, max_retries=3, delay=2):
    """
    带重试的函数执行器
    """
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"   ⚠️ 请求失败，{delay}秒后重试 ({attempt + 1}/{max_retries}): {str(e)[:50]}")
                time.sleep(delay)
                delay *= 2  # 指数退避
            else:
                raise e

def convert_days_to_date(days_remaining):
    """
    将倒计时天数转换为具体日期
    公式：2050-01-01 - 剩余天数
    """
    try:
        real_date = ANCHOR_DATE - timedelta(days=int(days_remaining))
        return real_date.isoformat()
    except:
        return None

# === 2. 数据读取与清洗 ===

def load_elo_txt(filepath="asset\\elo.txt"):
    """
    读取 elo.txt 文件，去掉 JS 的定义头和注释，解析为 Python 对象
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    json_str = content.strip()
    
    # 1. 去掉 "const eloData =" 头部
    if json_str.startswith("const eloData ="):
        json_str = json_str.replace("const eloData =", "", 1)
    
    # 2. 去掉结尾分号
    if json_str.endswith(";"):
        json_str = json_str[:-1]
    
    # 3. 移除 JavaScript 单行注释 (// ...)
    # 注意：要小心不要误删字符串内的 // (如 URL)
    # 这里用简单方式：删除行首或逗号后的注释行
    lines = json_str.split('\n')
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        # 跳过纯注释行
        if stripped.startswith('//'):
            continue
        # 移除行尾注释 (但要避免字符串内的情况，这里简化处理)
        # 如果行内有 // 且不在引号内，则截断
        # 简单处理：只处理明显的行尾注释
        cleaned_lines.append(line)
    
    json_str = '\n'.join(cleaned_lines)
    
    # 4. 将单引号替换为双引号 (JS 格式 -> JSON 格式)
    # 使用更安全的方式：只替换作为字符串定界符的单引号
    json_str = convert_js_to_json(json_str)
    
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败: {e}")
        # 调试：打印出错位置附近的内容
        error_pos = e.pos if hasattr(e, 'pos') else 0
        print(f"   出错位置附近: ...{json_str[max(0,error_pos-50):error_pos+50]}...")
        exit(1)

def convert_js_to_json(js_str):
    """
    将 JavaScript 对象字面量转换为合法的 JSON
    主要处理：单引号 -> 双引号
    """
    result = []
    in_string = False
    string_char = None
    i = 0
    
    while i < len(js_str):
        char = js_str[i]
        
        if not in_string:
            if char == '"' or char == "'":
                in_string = True
                string_char = char
                # 统一转为双引号
                result.append('"')
            else:
                result.append(char)
        else:
            # 在字符串内
            if char == '\\' and i + 1 < len(js_str):
                # 转义字符，保留
                next_char = js_str[i + 1]
                if next_char == string_char:
                    # \' 或 \" -> 如果是单引号字符串中的 \'，需要转为 \"
                    if string_char == "'":
                        result.append('\\"')
                    else:
                        result.append('\\"')
                    i += 2
                    continue
                else:
                    result.append(char)
            elif char == string_char:
                # 字符串结束
                in_string = False
                string_char = None
                result.append('"')
            elif char == '"' and string_char == "'":
                # 单引号字符串中的双引号需要转义
                result.append('\\"')
            else:
                result.append(char)
        
        i += 1
    
    return ''.join(result)

# === 3. 核心迁移逻辑 ===

# 缓存 team_name -> team_id，减少数据库查询
CACHE_TEAMS = {}

def get_or_create_team_id(team_name):
    team_name = team_name.strip()
    if not team_name or team_name == '-':
        return None
        
    if team_name in CACHE_TEAMS:
        return CACHE_TEAMS[team_name]
    
    def _query():
        return supabase.table('teams').select('id').eq('name', team_name).execute()
    
    res = retry_on_failure(_query)
    if res.data:
        tid = res.data[0]['id']
    else:
        # 新建
        print(f"   ➕ 创建新团体: {team_name}")
        def _insert():
            return supabase.table('teams').insert({"name": team_name}).execute()
        res_ins = retry_on_failure(_insert)
        tid = res_ins.data[0]['id']
    
    CACHE_TEAMS[team_name] = tid
    return tid

def normalize_rank_change(val):
    """
    elo.txt 里的“升降”字段清洗：
    只接受：↑ / ↓ / +
    其他（空、未知）写入 NULL
    """
    v = (val or "").strip()
    if v in ("↑", "↓", "+"):
        return v
    return None

def migrate():
    print("🚀 开始迁移历史数据...")
    
    data = load_elo_txt()
    rank_list = data.get("Rank", [])
    
    print(f"📄 读取到 {len(rank_list)} 位选手数据。")
    
    if START_FROM_INDEX > 0:
        print(f"⏩ 跳过前 {START_FROM_INDEX} 位选手，从第 {START_FROM_INDEX + 1} 位开始")
    
    for idx, item in enumerate(rank_list):
        # 断点续传：跳过已处理的
        if idx < START_FROM_INDEX:
            continue
            
        name = item.get("姓名", "").strip()
        nick = item.get("昵称", "").strip()
        
        # 如果姓名和昵称都为空，跳过
        if not name and not nick: 
            continue
        
        display_name = name if name else nick
        print(f"🔄 [{idx+1}/{len(rank_list)}] 处理选手: {display_name}")
        
        # 添加小延迟，避免请求过快
        time.sleep(0.1)
        
        try:
            # --- A. 准备选手基础信息 ---
            achievements = {
                "champion": [x.strip() for x in item.get("冠军", "").split('\n') if x.strip()],
                "runner_up": [x.strip() for x in item.get("亚军", "").split('\n') if x.strip()],
                "third_place": [x.strip() for x in item.get("季军", "").split('\n') if x.strip()],
                "top4": [x.strip() for x in item.get("四强", "").split('\n') if x.strip()],
                "top6": [x.strip() for x in item.get("六强", "").split('\n') if x.strip()],
                "top8": [x.strip() for x in item.get("八强", "").split('\n') if x.strip()]
            }
            
            grade_str = item.get("挂件", "-1")
            try:
                grade_val = int(grade_str) if grade_str else -1
            except:
                grade_val = -1

            activity_str = item.get("活跃度", "0").replace("%", "") 
            try:
                activity_val = int(activity_str)
            except:
                activity_val = 0 

            # 关键：如果没有姓名，用昵称填充 name 字段
            actual_name = name if name else nick

            # 升降：↑/↓/+ -> 写入 players.rank_change
            rank_change = normalize_rank_change(item.get("升降"))

            player_data = {
                "name": actual_name,
                "nick_name": nick if nick else None,
                "region": item.get("地区") if item.get("地区") else None,
                "current_elo": int(item.get("elo分") or 0),
                "max_elo": int(item.get("Elo峰值") or 0),
                "bio": None, 
                "achievements": achievements,
                "grade": grade_val,
                "activity": activity_val,
                "rank_change": rank_change,
            }
            
            # 写入 Player (先查是否存在，增加联合匹配条件以防同名选手被跳过覆盖)
            def _query_player():
                return supabase.table('players').select('id') \
                    .eq('name', actual_name) \
                    .eq('current_elo', player_data['current_elo']) \
                    .eq('max_elo', player_data['max_elo']) \
                    .eq('activity', player_data['activity']) \
                    .execute()
            
            res_p = retry_on_failure(_query_player)
            
            if res_p.data:
                pid = res_p.data[0]['id']
                def _update_player():
                    return supabase.table('players').update(player_data).eq('id', pid).execute()
                retry_on_failure(_update_player)
            else:
                def _insert_player():
                    return supabase.table('players').insert(player_data).execute()
                res_ins = retry_on_failure(_insert_player)
                pid = res_ins.data[0]['id']
                
            # --- B. 处理团体 (Teams) ---
            team_str = item.get("团体", "")
            if team_str and team_str != '-':
                team_names = re.split(r'[、,;，]', team_str)
                for t_name in team_names:
                    t_name = t_name.strip()
                    if not t_name or t_name == '-':
                        continue
                    tid = get_or_create_team_id(t_name)
                    if tid:
                        try:
                            def _link_team():
                                return supabase.table('player_teams').insert({"player_id": pid, "team_id": tid}).execute()
                            retry_on_failure(_link_team)
                        except:
                            pass
                            
            # --- C. 处理 Elo 历史 ---
            hist_str = item.get("历史数据", "")
            if hist_str:
                hist_items = hist_str.split(';')
                history_rows = []
                
                for h_item in hist_items:
                    if ',' not in h_item: 
                        continue
                    parts = h_item.split(',')
                    if len(parts) != 2:
                        continue
                    days, score = parts
                    
                    match_date = convert_days_to_date(days)
                    if not match_date: 
                        continue
                    
                    history_rows.append({
                        "player_id": pid,
                        "new_elo": int(score),
                        "date": match_date,
                        "source": "import", 
                        "match_id": None
                    })
                
                if history_rows:
                    history_rows.sort(key=lambda x: x['date'])
                    
                    def _insert_history():
                        return supabase.table('elo_history').insert(history_rows).execute()
                    retry_on_failure(_insert_history)
                    
                    last_active_date = history_rows[-1]['date']
                    
                    def _update_last_active():
                        return supabase.table('players').update({"last_active_date": last_active_date}).eq('id', pid).execute()
                    retry_on_failure(_update_last_active)
                    
        except Exception as e:
            print(f"   ❌ 处理失败: {e}")
            print(f"   💡 提示: 修改 START_FROM_INDEX = {idx} 后重新运行可断点续传")
            raise
                
    print("✅ 所有历史数据迁移完成！")

if __name__ == "__main__":
    migrate()