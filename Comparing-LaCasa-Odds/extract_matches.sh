#!/bin/bash

INPUT_FILE="$1"

if [ -z "$INPUT_FILE" ]; then
    echo "Usage: $0 <json-file>"
    exit 1
fi

echo "country,league,date,time,home,away,halftime_home,halftime_away,end_home,end_away"

jq -r '
.data as $root
|
$root.matchList[]
|
[
    ($root.categoryList[(.category_id|tostring)].name // ""),
    ($root.leagueList[(.league_id|tostring)].name // ""),

    (.md | split(" ")[0]),
    (.md | split(" ")[1] | sub("\\+.*$"; "")),

    .ht,
    .at,

    (
        if .status then
            ((.status | fromjson)[0].home // "")
        else
            ""
        end
    ),

    (
        if .status then
            ((.status | fromjson)[0].away // "")
        else
            ""
        end
    ),

    (.hscore // ""),
    (.ascore // "")
]
| @csv
' "$INPUT_FILE"
