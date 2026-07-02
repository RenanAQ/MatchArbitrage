import json

with open("w5-combined.json", "r") as f:
    matches = json.load(f)

count = 0
total = 0
skipped = 0
sum_odds = 0  # sum of winning higher odds

for match in matches:
    odds = match.get("odds", {})
    home_odds = odds.get("home")
    away_odds = odds.get("away")

    home_score = match["home_score"]
    away_score = match["away_score"]

    # Skip missing odds
    if home_odds is None or away_odds is None:
        skipped += 1
        continue

    # Skip draws
    if home_score == away_score:
        continue

    total += 1

    winner = "home" if home_score > away_score else "away"

    # Determine higher odds
    if home_odds > away_odds:
        higher_odds_team = "home"
        higher_odds_value = home_odds
    elif away_odds > home_odds:
        higher_odds_team = "away"
        higher_odds_value = away_odds
    else:
        continue  # equal odds

    # If higher odds team won
    if winner == higher_odds_team:
        count += 1
        sum_odds += higher_odds_value

# Results
print(f"Higher-odds team wins: {count} out of {total}")
print(f"Skipped matches: {skipped}")

if count > 0:
    avg_odds = sum_odds / count
    print(f"Average odds (higher-odds winners): {avg_odds:.3f}")
else:
    print("No higher-odds winners found")