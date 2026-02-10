from migrate_old_data import load_elo_txt, retry_on_failure, supabase

def normalize_rank_change(val):
    v = (val or "").strip()
    if v in ("↑", "↓", "+"):
        return v
    return None  # 空/未知 -> NULL

def update_player_rank_change(actual_name: str, nick: str, rank_change):
    payload = {"rank_change": rank_change}

    # 优先精确匹配：name + nick_name（如果 nick 存在）
    def _update_precise():
        q = supabase.table("players").update(payload).eq("name", actual_name)
        if nick:
            q = q.eq("nick_name", nick)
        return q.execute()

    res = retry_on_failure(_update_precise)
    if res.data:
        return len(res.data)

    # 兜底：只按 name 匹配（避免部分历史数据 nick_name 不一致导致更新不到）
    def _update_fallback():
        return supabase.table("players").update(payload).eq("name", actual_name).execute()

    res2 = retry_on_failure(_update_fallback)
    return len(res2.data or [])

def main():
    data = load_elo_txt()
    rank_list = data.get("Rank", [])

    updated = 0
    missed = 0
    skipped = 0

    for item in rank_list:
        name = (item.get("姓名") or "").strip()
        nick = (item.get("昵称") or "").strip()

        # 与你现有迁移脚本一致：姓名/昵称都没有就跳过
        if not name and not nick:
            skipped += 1
            continue

        actual_name = name if name else nick
        rank_change = normalize_rank_change(item.get("升降"))

        count = update_player_rank_change(actual_name, nick, rank_change)
        if count > 0:
            updated += count
        else:
            missed += 1
            print(f"⚠️ 未匹配到选手，无法更新 rank_change: name={actual_name!r}, nick={nick!r}")

    print("✅ rank_change 回填完成")
    print(f"   updated_rows={updated}, missed_players={missed}, skipped_items={skipped}")

if __name__ == "__main__":
    main()