"""
New Undo Script for ETL Architecture.
Instead of rolling back derived tables, we simply remove the bad data
from the SOURCE (raw_matches) and let the ETL script handle the rest.
"""

import os
from dotenv import load_dotenv
from supabase import Client, create_client

# === 配置 ===
load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
if url is None or key is None:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY")
supabase: Client = create_client(url, key)

def delete_tournament_from_raw(tournament_name: str) -> None:
    print(f"🗑️ 正在从原始数据 (raw_matches) 中删除赛事: {tournament_name} ...")
    
    # 1. 查询并确认
    # 注意：raw_matches 存的是 tournament_name 文本，不是 ID
    res = (
        supabase.table("raw_matches")
        .select("*")
        .eq("tournament_name", tournament_name)
        .execute()
    )
    rows = res.data
    
    if not rows:
        print(f"❌ 未在 raw_matches 中找到名称为 '{tournament_name}' 的记录。")
        return

    print(f"⚠️ 找到了 {len(rows)} 条原始对局记录。")
    print("示例数据:", rows[0])
    
    confirm = input("确定要永久删除这些原始数据吗？删除后请重新运行 ETL 脚本。(y/n): ")
    if confirm.lower() != 'y':
        print("已取消。")
        return

    # 2. 执行删除
    (
        supabase.table("raw_matches")
        .delete()
        .eq("tournament_name", tournament_name)
        .execute()
    )
    
    print(f"✅ 已删除赛事 '{tournament_name}' 的原始记录。")
    print("👉 下一步：请运行 'python 2_run_etl.py' 来刷新排行榜。")

if __name__ == "__main__":
    t_name = input("请输入要撤销的赛事名称 (raw_matches 中的 tournament_name): ")
    delete_tournament_from_raw(t_name)