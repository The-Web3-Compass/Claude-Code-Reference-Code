set -euo pipefail

MARKER='<!-- claude-code-review -->'

if [ -z "${PR_NUMBER:-}" ]; then
  echo "PR_NUMBER env var is required" >&2
  exit 1
fi

if [ -z "${REVIEW_JSON_PATH:-}" ]; then
  echo "REVIEW_JSON_PATH env var is required" >&2
  exit 1
fi

SUMMARY=$(jq -r '.summary' "$REVIEW_JSON_PATH")

BODY_PREFIX="$MARKER

**Claude Code Review**

$SUMMARY"

EXISTING_IDS=$(gh pr view "$PR_NUMBER" --json comments \
  --jq ".comments[] | select(.body | contains(\"$MARKER\")) | .id")

if [ -n "$EXISTING_IDS" ]; then
  echo "$EXISTING_IDS" | while read -r cid; do
    gh api -X DELETE "repos/${GITHUB_REPOSITORY}/issues/comments/${cid}" >/dev/null
  done
fi

gh pr comment "$PR_NUMBER" --body "$BODY_PREFIX"

jq -c '.findings[]' "$REVIEW_JSON_PATH" | while read -r finding; do
  FILE=$(echo "$finding" | jq -r '.file')
  SEVERITY=$(echo "$finding" | jq -r '.severity')
  CATEGORY=$(echo "$finding" | jq -r '.category')
  DESCRIPTION=$(echo "$finding" | jq -r '.description')
  SUGGESTION=$(echo "$finding" | jq -r '.suggestion')
  LINE=$(echo "$finding" | jq -r '.line // "N/A"')

  gh pr comment "$PR_NUMBER" --body "**[$SEVERITY] $CATEGORY**, \`$FILE\` (line $LINE)

$DESCRIPTION

**Suggested fix:** $SUGGESTION"
done
