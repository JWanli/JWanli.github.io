from supabase import create_client, Client

# 1. 配置 (务必使用 service_role key)
SUPABASE_URL = "https://hvsmloywzdlvegjfvyss.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh2c21sb3l3emRsdmVnamZ2eXNzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Nzk0Mjg1NywiZXhwIjoyMDgzNTE4ODU3fQ.pPVNQGhC7A2mP2pSNwBkSxUn8FJtn6UOVwEW45YQsn4" 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

DEFAULT_ELO = 450 # 如果选手没有历史记录了，恢复成的默认分

def rollback_tournament(tournament_id):
    print(f"🔄 正在准备回滚赛事 ID: {tournament_id} ...")

    # 1. 先找出这场比赛包含哪些对局 (match_ids)
    res_matches = supabase.table('matches').select('id, winner_id, loser_id').eq('tournament_id', tournament_id).execute()
    matches = res_matches.data
    
    if not matches:
        print("❌ 未找到该赛事，或该赛事下没有对局。")
        return

    match_ids = [m['id'] for m in matches]
    # 收集所有受影响的选手 ID (去重)
    affected_player_ids = set()
    for m in matches:
        affected_player_ids.add(m['winner_id'])
        affected_player_ids.add(m['loser_id'])
    
    print(f"📄 找到 {len(match_ids)} 场对局，涉及 {len(affected_player_ids)} 名选手。")

    # 2. 删除这些对局产生的 Elo 历史记录
    # 注意：这里我们过滤 match_id 在我们列表里的记录
    print("🗑️ 正在删除 Elo 历史记录...")
    supabase.table('elo_history').delete().in_('match_id', match_ids).execute()

    # 3. 将对局标记为“未计算”，以便修正后重算
    print("Tb 正在重置对局状态为 '未计算'...")
    supabase.table('matches').update({'is_calculated': False}).in_('id', match_ids).execute()

    # 4. 关键步骤：修复选手的 current_elo
    print("Hb 正在恢复选手当前积分...")
    
    for pid in affected_player_ids:
        # 查询该选手 剩余的、最新的 一条历史记录
        # order('id', desc=True) 意味着找 ID 最大的，也就是最近发生的
        res_history = supabase.table('elo_history')\
            .select('new_elo')\
            .eq('player_id', pid)\
            .order('id', desc=True)\
            .limit(1)\
            .execute()
        
        if res_history.data:
            # 如果还有历史记录（比如前 4 年的），就恢复成最近那次的分
            restore_score = res_history.data[0]['new_elo']
            print(f"  - 选手 {pid}: 恢复至 {restore_score}")
        else:
            # 如果没有历史记录了（说明这场比赛是他第一次打），恢复成初始分
            restore_score = DEFAULT_ELO
            print(f"  - 选手 {pid}: 恢复至初始分 {restore_score}")
        
        # 更新选手表
        supabase.table('players').update({'current_elo': restore_score}).eq('id', pid).execute()

    print(f"✅ 赛事 {tournament_id} 回滚完成！")
    print("现在你可以去修改 matches 表里的参数，然后重新运行 calc 脚本了。")

if __name__ == "__main__":
    t_id = input("请输入要撤销的赛事 ID (tournament_id): ")
    confirm = input(f"⚠️ 确定要撤销赛事 {t_id} 的所有计算结果吗？这会将选手分数恢复到赛前状态。(y/n): ")
    if confirm.lower() == 'y':
        rollback_tournament(int(t_id))