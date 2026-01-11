"""
Replay-all ETL to recompute Elo from raw matches
and sync derived tables into Supabase.
"""

from __future__ import annotations

import json
import os
from typing import Any, Mapping, TypeAlias, cast

from dotenv import load_dotenv
from supabase import Client, create_client

# === 配置 ===
load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
if url is None or key is None:
    raise RuntimeError(
        "Missing SUPABASE_URL or SUPABASE_KEY; "
        "set them in your environment "
        "or .env file."
    )
supabase: Client = create_client(url, key)

# 内存缓存，减少数据库查询
CACHE_PLAYERS: dict[str, int] = {}  # name -> id
CACHE_TOURNAMENTS: dict[str, int] = {}  # name -> id

JSON: TypeAlias = (
    None
    | bool
    | int
    | float
    | str
    | list["JSON"]
    | dict[str, "JSON"]
)


def _as_dict(value: Any) -> dict[str, Any]:
    """Narrow an unknown value to a dict or raise a clear error."""
    if isinstance(value, dict):
        return cast(dict[str, Any], value)
    raise TypeError(f"Expected dict, got: {type(value)!r}")


def _as_json_dict(value: Any) -> dict[str, JSON]:
    """Narrow an unknown value to a JSON dict or raise a clear error."""
    if value is None:
        return {}
    if isinstance(value, dict):
        return cast(dict[str, JSON], value)
    raise TypeError(f"Expected dict, got: {type(value)!r}")


def _as_list(value: Any) -> list[dict[str, Any]]:
    """Narrow an unknown value to a list[dict] (best-effort) or raise."""
    if value is None:
        return []
    if not isinstance(value, list):
        raise TypeError(f"Expected list, got: {type(value)!r}")
    out: list[dict[str, Any]] = []
    for item in value:
        if isinstance(item, dict):
            out.append(cast(dict[str, Any], item))
    return out


def _require_first_row(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Return the first row or raise if the response is empty."""
    if rows:
        return rows[0]
    raise RuntimeError("Supabase response contained no rows.")


# === 1. 工具函数：ID 智能解析 ===


def get_or_create_tournament_id(
    name: str,
    date_str: str,
) -> int:
    """Get a tournament id by name, creating the row if it doesn't exist."""
    if name in CACHE_TOURNAMENTS:
        return CACHE_TOURNAMENTS[name]

    query = (
        supabase.table("tournaments")
        .select("id")
        .eq("name", name)
    )
    res = query.execute()
    rows = _as_list(res.data)

    if rows:
        row = _require_first_row(rows)
        t_id = int(row["id"])
    else:
        print(f"🏆 注册新赛事: {name}")
        new_row: dict[str, JSON] = {
            "name": name,
            "date": date_str,
        }
        ins = (
            supabase.table("tournaments")
            .insert(new_row)
            .execute()
        )
        ins_rows = _as_list(ins.data)
        ins_row = _require_first_row(ins_rows)
        t_id = int(ins_row["id"])

    CACHE_TOURNAMENTS[name] = t_id
    return t_id


def get_or_create_player_id(name: str) -> int:
    """
    核心逻辑：
    先查 Mapping 表 -> 没找到则创建 Player + Mapping
    """
    if name in CACHE_PLAYERS:
        return CACHE_PLAYERS[name]

    query = (
        supabase.table("player_mappings")
        .select("target_player_id")
        .eq("alias_name", name)
    )
    res = query.execute()
    rows = _as_list(res.data)

    if rows:
        row = _require_first_row(rows)
        p_id = int(row["target_player_id"])
        CACHE_PLAYERS[name] = p_id
        return p_id

    print(f"👤 发现新选手: {name}，正在注册...")

    player_row: dict[str, JSON] = {
        "name": name,
        "current_elo": 450,
    }
    res_p = (
        supabase.table("players")
        .insert(player_row)
        .execute()
    )
    p_rows = _as_list(res_p.data)
    p_row = _require_first_row(p_rows)
    new_p_id = int(p_row["id"])

    mapping_row: dict[str, JSON] = {
        "alias_name": name,
        "target_player_id": new_p_id,
    }
    supabase.table("player_mappings").insert(
        mapping_row
    ).execute()

    CACHE_PLAYERS[name] = new_p_id
    return new_p_id


# === 2. 核心公式 (大枪 Elo) ===


def calculate_expectancy(
    r_a: float,
    r_b: float,
) -> float:
    """Classic Elo expectancy (probability A wins)."""
    return 1.0 / (1.0 + 10.0 ** ((r_b - r_a) / 400.0))


def calculate_s_factor(
    score_a: float,
    score_b: float,
    rule_type: str,
    rule_params: Mapping[str, Any],
) -> float:
    """Compute the S factor for custom rules ('round' or 'cap')."""
    params = dict(rule_params)

    s_val = 0.5

    if rule_type == "round":
        c_val = int(params.get("C", 7))
        g_val = int(params.get("G", 7))

        total = score_a + score_b
        if total > 0:
            term1 = (
                (score_a / total)
                * (g_val / c_val)
            )
        else:
            term1 = 0.0

        if c_val > 0:
            term2 = (c_val - g_val) / (c_val * 2)
        else:
            term2 = 0.0

        s_val = term1 + term2

    if rule_type == "cap":
        q_val = int(params.get("Q", 11))
        s_val = (score_a + q_val - score_b) / (2 * q_val)

    return float(s_val)


def get_k_factor(
    rule_type: str,
    rule_params: Mapping[str, Any],
) -> int:
    """Return K based on rule settings (single-return for lint)."""
    params = dict(rule_params)

    k_val = 32

    if rule_type == "round":
        c_val = int(params.get("C", 7))
        k_map = {
            1: 8,
            3: 16,
            5: 24,
        }
        if c_val in k_map:
            k_val = k_map[c_val]
        elif c_val >= 7:
            k_val = 32
        else:
            k_val = 32

    elif rule_type == "cap":
        k_val = 20

    return int(k_val)


# === 3. 主流程 ===


def _reset_derived_tables() -> None:
    print("🧹 清空历史数据...")
    (
        supabase.table("elo_history")
        .delete()
        .neq("id", 0)
        .execute()
    )
    (
        supabase.table("matches")
        .delete()
        .neq("id", 0)
        .execute()
    )
    (
        supabase.table("players")
        .update(
            {
                "current_elo": 450,
            }
        )
        .neq("id", 0)
        .execute()
    )


def _load_raw_matches() -> list[dict[str, Any]]:
    print("📖 读取 raw_matches...")
    res = (
        supabase.table("raw_matches")
        .select("*")
        .order("date", desc=False)
        .execute()
    )
    return _as_list(res.data)


def _get_player_current_elo(player_id: int) -> int:
    res = (
        supabase.table("players")
        .select("current_elo")
        .eq("id", player_id)
        .single()
        .execute()
    )
    row = _as_dict(res.data)
    return int(row.get("current_elo", 450) or 450)


def _set_player_elo(player_id: int, new_elo: int) -> None:
    (
        supabase.table("players")
        .update(
            {
                "current_elo": new_elo,
            }
        )
        .eq("id", player_id)
        .execute()
    )


def _normalize_rule_params(value: Any) -> dict[str, JSON]:
    normalized = json.loads(
        json.dumps(value or {})
    )
    return _as_json_dict(normalized)


def _process_raw_match(raw: dict[str, Any]) -> None:
    tournament_name = str(raw.get("tournament_name", ""))
    date_str = str(raw.get("date", ""))

    player_a_name = str(raw.get("player_a_name", ""))
    player_b_name = str(raw.get("player_b_name", ""))

    score_a = int(raw.get("score_a", 0) or 0)
    score_b = int(raw.get("score_b", 0) or 0)

    rule_type = str(raw.get("rule_type", ""))
    rule_params = _normalize_rule_params(
        raw.get("rule_params")
    )

    t_id = get_or_create_tournament_id(
        tournament_name,
        date_str,
    )
    p_a_id = get_or_create_player_id(player_a_name)
    p_b_id = get_or_create_player_id(player_b_name)

    p_a_curr = _get_player_current_elo(p_a_id)
    p_b_curr = _get_player_current_elo(p_b_id)

    s_a = calculate_s_factor(
        score_a,
        score_b,
        rule_type,
        rule_params,
    )
    e_a = calculate_expectancy(
        float(p_a_curr),
        float(p_b_curr),
    )
    k_val = get_k_factor(
        rule_type,
        rule_params,
    )

    change_a = int(round(k_val * (s_a - e_a)))
    change_b = -change_a

    new_a = int(p_a_curr) + int(change_a)
    new_b = int(p_b_curr) + int(change_b)

    a_is_winner = score_a >= score_b
    winner_id = p_a_id if a_is_winner else p_b_id
    loser_id = p_b_id if a_is_winner else p_a_id

    score_winner = max(score_a, score_b)
    score_loser = min(score_a, score_b)

    match_data: dict[str, JSON] = {
        "tournament_id": t_id,
        "winner_id": winner_id,
        "loser_id": loser_id,
        "score_winner": score_winner,
        "score_loser": score_loser,
        "rule_type": rule_type,
        "rule_params": rule_params,
        "is_calculated": True,
    }
    m_res = (
        supabase.table("matches")
        .insert(match_data)
        .execute()
    )
    m_rows = _as_list(m_res.data)
    m_row = _require_first_row(m_rows)
    m_id = int(m_row["id"])

    hist_a: dict[str, JSON] = {
        "player_id": p_a_id,
        "match_id": m_id,
        "old_elo": p_a_curr,
        "new_elo": new_a,
        "change_val": change_a,
        "date": date_str,
    }
    hist_b: dict[str, JSON] = {
        "player_id": p_b_id,
        "match_id": m_id,
        "old_elo": p_b_curr,
        "new_elo": new_b,
        "change_val": change_b,
        "date": date_str,
    }
    supabase.table("elo_history").insert(
        [
            hist_a,
            hist_b,
        ]
    ).execute()

    _set_player_elo(p_a_id, new_a)
    _set_player_elo(p_b_id, new_b)

    msg = (
        f" ✅ {player_a_name}"
        f"({new_a})"
        f" vs {player_b_name}"
        f"({new_b})"
        f" | 变动: {change_a}"
    )
    print(msg)


def run_etl() -> None:
    """Replay-all ETL: truncates derived tables, then recomputes Elo."""
    print("🚀 开始全量重算 (Replay All Mode)...")

    _reset_derived_tables()

    raw_matches = _load_raw_matches()
    print(f"📊 待处理对局: {len(raw_matches)} 场")

    for raw in raw_matches:
        _process_raw_match(raw)

    print("🎉 全量计算完成！所有数据已同步。")


if __name__ == "__main__":
    run_etl()