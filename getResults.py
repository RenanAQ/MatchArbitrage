import json


def merge_match_data(matches_file, odds_file, output_file):
    # Load match information (w1.json)
    with open(matches_file, "r", encoding="utf-8") as f:
        matches_data = json.load(f)

    # Load odds information (w1-odds.json)
    with open(odds_file, "r", encoding="utf-8") as f:
        odds_data = json.load(f)

    # Extract the match lists and odds map
    match_list = matches_data.get("data", {}).get("matchList", [])
    odds_map = odds_data.get("data", {}).get("matches", {})

    combined_results = []

    for match in match_list:
        match_id = str(match.get("id"))

        # Initialize the details from w1.json, pulling 'md' for the date
        match_entry = {
            "match_id": match.get("id"),
            "match_date": match.get(
                "md"
            ),  # Extracts the timestamp string (e.g. "2026-03-26 00:05:00+00")
            "home_team": match.get("ht"),
            "away_team": match.get("at"),
            "home_score": match.get("hscore"),
            "away_score": match.get("ascore"),
            "odds": {"home": None, "away": None},
        }

        # If a corresponding entry exists in the odds file, merge market 200 (Moneyline)
        if match_id in odds_map:
            moneyline_market = odds_map[match_id].get("200", {})
            market_odds = moneyline_market.get("odds", {})

            # Extract home ('1') and away ('2') outcome odds values
            home_odds = market_odds.get("1", {}).get("value")
            away_odds = market_odds.get("2", {}).get("value")

            match_entry["odds"]["home"] = (
                float(home_odds) if home_odds else None
            )
            match_entry["odds"]["away"] = (
                float(away_odds) if away_odds else None
            )

        combined_results.append(match_entry)

    # Export structured data into the destination file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(combined_results, f, indent=4, ensure_ascii=False)

    print(
        f"Successfully processed {len(combined_results)} matches. Saved to {output_file}"
    )


if __name__ == "__main__":
    merge_match_data(
        matches_file="w1.json",
        odds_file="w1-odds.json",
        output_file="combined_matches_odds.json",
    )