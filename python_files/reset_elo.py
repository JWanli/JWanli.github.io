from supabase import create_client, Client

import os
import sys
import datetime
import getpass

from dotenv import load_dotenv # 需要 pip install python-dotenv

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
if url is None or key is None:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY; set them in your environment or .env file.")
supabase: Client = create_client(url, key)


def require_confirmation_or_exit() -> None:
    """
    安全锁：
    1) 必须输入当天口令（例如：RESET 2026-01-09）
    2) 如果设置了环境变量 RESET_ELO_PASSPHRASE，则还必须再输入该密码（隐藏输入）
    """
    today = datetime.date.today().isoformat()
    phrase = f"RESET {today}"

    print("⚠️ 你正在执行高危操作：将清空 Elo 历史并重置所有选手分数/比赛计算状态。")
    user = input(f"为继续，请准确输入：{phrase}\n> ").strip()
    if user != phrase:
        print("❌ 口令不匹配，已取消。")
        sys.exit(1)

    expected_pw = os.getenv("RESET_ELO_PASSPHRASE")
    if expected_pw is not None:
        pw = getpass.getpass("再输入 RESET_ELO_PASSPHRASE（不会回显）> ")
        if pw != expected_pw:
            print("❌ 密码不正确，已取消。")
            sys.exit(1)


def reset_all():
    print("⚠️ 正在重置所有数据...")

    # 1. 清空历史记录表 (elo_history)
    supabase.table("elo_history").delete().neq("id", 0).execute()

    # 2. 将所有选手的 current_elo 重置为初始分 (比如 450)
    supabase.table("players").update({"current_elo": 450}).neq("id", 0).execute()

    # 3. 将所有比赛标记为“未计算” (is_calculated = False)
    supabase.table("matches").update({"is_calculated": False}).neq("id", 0).execute()

    print("✅ 重置完成！数据库已回到初始状态。")
    print("现在你可以重新运行计算脚本，修正数据了。")


if __name__ == "__main__":
    require_confirmation_or_exit()
    reset_all()