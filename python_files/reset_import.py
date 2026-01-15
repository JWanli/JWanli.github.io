import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def reset_database():
    print("🧹 正在清空数据库，准备重新导入...")

    # 1. 清空 Elo 历史 (CASCADE 会自动处理关联，但显式删除更保险)
    print("   - 清空 elo_history...")
    supabase.table('elo_history').delete().neq('id', 0).execute()

    # 2. 清空 比赛结果 (matches) - 如果你有的话
    print("   - 清空 matches...")
    supabase.table('matches').delete().neq('id', 0).execute()

    # 3. 清空 选手-团体关联
    print("   - 清空 player_teams...")
    supabase.table('player_teams').delete().neq('id', 0).execute()

    # 4. 清空 团体
    print("   - 清空 teams...")
    supabase.table('teams').delete().neq('id', 0).execute()

    # 5. 清空 映射表
    print("   - 清空 player_mappings...")
    supabase.table('player_mappings').delete().neq('id', 0).execute()
    
    # 6. 清空 选手 (最后删，因为被别人引用)
    print("   - 清空 players...")
    supabase.table('players').delete().neq('id', 0).execute()

    print("✅ 数据库已清空！现在可以运行 migrate_old_data.py 了。")

if __name__ == "__main__":
    confirm = input("⚠️ 确定要清空所有选手和历史数据吗？(y/n): ")
    if confirm.lower() == 'y':
        reset_database()