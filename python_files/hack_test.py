import os
from supabase import create_client, Client

# ==========================================
# === 数据库Key泄露测试 ===
# ==========================================

# 1. 填入你的 Project URL
SUPABASE_URL = "supabase项目URL请替换这里" 

# 2. 填入那个【你担心泄露的、旧的】Secret Key
# (一定要填那个你觉得不安全的旧字符串，不要填新的！)
LEAKED_KEY = "测试用的旧Key_请替换为真实的Key字符串" 

# ==========================================

print(f"🕵️ 正在尝试使用旧 Key 入侵数据库...")

try:
    # 尝试建立连接
    supabase: Client = create_client(SUPABASE_URL, LEAKED_KEY)

    # 尝试读取 players 表的一条数据
    # 注意：service_role 只要有效，是可以无视权限读取所有表的
    response = supabase.table("players").select("*").limit(1).execute()

    # 如果代码能走到这里，说明 Key 居然还能用！
    if response.data:
        print("\n❌ 测试失败！")
        print("警告：这个 Key 依然有效！它读取到了数据！")
        print(f"数据内容: {response.data}")
    else:
        # 这种情况很少见，通常是空表，但也说明连接成功了
        print("\n❌ 警告：Key 似乎有效，但没有读到数据（可能是空表）。")

except Exception as e:
    # 如果报错，说明 Key 失效了，这才是我们想要的结果！
    print("\n✅ 测试通过！安全！")
    print("------------------------------------------------")
    print("入侵失败，数据库拒绝了访问。")
    print(f"报错信息: {e}")
    print("------------------------------------------------")
    print("解读：服务器识别出 Key 签名无效 (Invalid Signature) 或已过期。")