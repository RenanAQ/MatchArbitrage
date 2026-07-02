import json
import os

def analyze_file(filename):
    try:
        with open(filename, "r") as f:
            matches = json.load(f)
    except Exception as e:
        print(f"{filename} -> ERROR: {e}")
        return None

    count = 0
    total_games = 0
    sum_odds = 0

    for match in matches:
        odds = match.get("odds", {})
        home_odds = odds.get("home")
        away_odds = odds.get("away")

        home_score = match.get("home_score")
        away_score = match.get("away_score")

        # Validate data
        if (
            home_odds is None
            or away_odds is None
            or home_score is None
            or away_score is None
        ):
            continue

        # Skip draws
        if home_score == away_score:
            continue

        total_games += 1

        winner = "home" if home_score > away_score else "away"

        # Determine higher odds team
        if home_odds > away_odds:
            higher_team = "home"
            higher_odds_value = home_odds
        elif away_odds > home_odds:
            higher_team = "away"
            higher_odds_value = away_odds
        else:
            continue  # equal odds

        # Check win
        if winner == higher_team:
            count += 1
            sum_odds += higher_odds_value

    avg_odds = (sum_odds / count) if count > 0 else 0

    return count, avg_odds, total_games


# Loop through weeks 1 to 13
for week in range(1, 14):
    # handle both naming styles
    filenames = [
        f"w{week}combined.json",
        f"w{week}-combined.json"
    ]

    file_found = None
    for fname in filenames:
        if os.path.exists(fname):
            file_found = fname
            break

    if not file_found:
        print(f"Week {week}: file not found")
        continue

    result = analyze_file(file_found)

    if result:
        count, avg_odds, total_games = result
        print(f"Week {week}, {count}, {avg_odds:.3f}, {total_games}")