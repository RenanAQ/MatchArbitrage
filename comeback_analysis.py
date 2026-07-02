import json
import os


def is_comeback(match):
    status_str = match.get("status")
    if not status_str:
        return False

    try:
        innings = json.loads(status_str)
    except:
        return False

    home_score = 0
    away_score = 0

    final_home = match.get("hscore")
    final_away = match.get("ascore")

    if final_home == final_away:
        return False

    winner = "home" if final_home > final_away else "away"

    was_behind = False

    for inning in innings:
        home_score += inning.get("home", 0)
        away_score += inning.get("away", 0)

        if winner == "home" and home_score < away_score:
            was_behind = True
        elif winner == "away" and away_score < home_score:
            was_behind = True

    return was_behind


def analyze_week(week):
    file_main = f"w{week}.json"
    file_combined = f"w{week}-combined.json"

    if not os.path.exists(file_main) or not os.path.exists(file_combined):
        print(f"Week {week}: missing file")
        return

    # ✅ Load main file (your structure)
    with open(file_main, "r") as f:
        raw = json.load(f)
        matches = raw.get("data", {}).get("matchList", [])

    # ✅ Load combined file
    with open(file_combined, "r") as f:
        combined = json.load(f)

    # ✅ Build lookup: match_id → odds
    odds_lookup = {m["match_id"]: m for m in combined}

    comeback_count = 0
    total_games = 0
    odds_sum = 0

    for match in matches:
        match_id = match.get("id")

        if match_id not in odds_lookup:
            continue

        odds_entry = odds_lookup[match_id]

        home_score = match.get("hscore")
        away_score = match.get("ascore")

        # Skip bad games
        if home_score is None or away_score is None:
            continue
        if home_score == away_score:
            continue

        odds = odds_entry.get("odds", {})
        home_odds = odds.get("home")
        away_odds = odds.get("away")

        if home_odds is None or away_odds is None:
            continue

        total_games += 1

        # ✅ Check comeback
        if is_comeback(match):
            comeback_count += 1

            # ✅ Add winning team's odds
            if home_score > away_score:
                odds_sum += home_odds
            else:
                odds_sum += away_odds

    avg_odds = odds_sum / comeback_count if comeback_count > 0 else 0

    print(f"Week {week}, {comeback_count}, {avg_odds:.3f}, {total_games}")


# ✅ Run weeks 1 → 13
for week in range(1, 14):
    analyze_week(week)