#!/usr/bin/env bash
# Verify release tag and commit signatures, allowing only explicitly attested
# legacy hashes whose rewrite would destroy merged-PR approval provenance.
set -euo pipefail

MODE="local"
[[ -n "${GITHUB_REPOSITORY:-}" ]] && MODE="github"
if [[ "${1:-}" == "--github" ]]; then MODE="github"; shift; fi

cd "$(dirname "$0")/.."
FROM="${1:-}"
TO="${2:-HEAD}"
if [[ -z "${2:-}" && "${GITHUB_REF_TYPE:-}" == tag ]]; then TO="$GITHUB_REF_NAME"; fi
ATTESTATIONS="data/legacy-commit-attestations.txt"

is_attested() {
  [[ -f "$ATTESTATIONS" ]] && grep -Eq "^${1}[[:space:]]" "$ATTESTATIONS"
}

tag_verified() {
  local type
  type="$(git cat-file -t "$1" 2>/dev/null)"
  if [[ "$MODE" == github && "$type" == commit ]]; then
    [[ "$(gh api "repos/${GITHUB_REPOSITORY}/commits/$(git rev-parse "$1")" \
      --jq '.commit.verification.verified' 2>/dev/null)" == true ]]
  elif [[ "$MODE" == github && "$type" == tag ]]; then
    local tag_sha
    tag_sha="$(git rev-parse "$1^{tag}")"
    [[ "$(gh api "repos/${GITHUB_REPOSITORY}/git/tags/${tag_sha}" \
      --jq '.verification.verified' 2>/dev/null)" == true ]]
  elif [[ "$type" == tag ]]; then
    git verify-tag "$1" >/dev/null 2>&1
  else
    return 1
  fi
}

if [[ -n "$FROM" ]]; then
  RANGE="${FROM}..${TO}"
else
  PREV_TAG="$(git describe --tags --abbrev=0 "${TO}^" 2>/dev/null || true)"
  if [[ -n "$PREV_TAG" ]] && tag_verified "$PREV_TAG"; then
    RANGE="${PREV_TAG}..${TO}"
  else
    RANGE="$TO"
  fi
fi

echo "Signature chain report"
echo " repository: $(git rev-parse --show-toplevel)"
echo " range: ${RANGE}"
echo " mode: ${MODE}"
echo " generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo

TAG_BAD=0
if git show-ref --verify --quiet "refs/tags/${TO}"; then
  if tag_verified "$TO"; then
    if [[ "$(git cat-file -t "$TO")" == tag ]]; then
      echo "tag ${TO}: SIGNED and verified"
    else
      echo "tag ${TO}: lightweight; target commit verified by GitHub"
    fi
  else
    echo "tag ${TO}: NOT VERIFIED"
    TAG_BAD=1
  fi
else
  echo "tag ${TO}: not a tag, nothing to verify"
fi
echo

UNSIGNED=0
TOTAL=0
if [[ "$MODE" == "github" ]]; then
  while read -r sha; do
    [[ -z "$sha" ]] && continue
    TOTAL=$((TOTAL + 1))
    read -r verified reason author <<<"$(gh api "repos/${GITHUB_REPOSITORY}/commits/${sha}" \
      --jq '[.commit.verification.verified, .commit.verification.reason, .commit.author.name] | @tsv' \
      2>/dev/null || echo -e "false\tapi_error\tunknown")"
    if [[ "$verified" == true ]]; then
      printf '  %s  OK       %s\n' "${sha:0:12}" "$author"
    elif is_attested "$sha"; then
      printf '  %s  ATTESTED %s (%s)\n' "${sha:0:12}" "$author" "$reason"
    else
      printf '  %s  UNSIGNED %s (%s)\n' "${sha:0:12}" "$author" "$reason"
      UNSIGNED=$((UNSIGNED + 1))
    fi
  done < <(git rev-list "$RANGE")
else
  while IFS=$'\t' read -r sha flag author subject; do
    [[ -z "$sha" ]] && continue
    TOTAL=$((TOTAL + 1))
    case "$flag" in
      G|U) printf '  %s  OK       %s %s\n' "${sha:0:12}" "$author" "$subject" ;;
      *) if is_attested "$sha"; then
           printf '  %s  ATTESTED %s %s\n' "${sha:0:12}" "$author" "$subject"
         else
           printf '  %s  BAD(%s)   %s %s\n' "${sha:0:12}" "$flag" "$author" "$subject"
           UNSIGNED=$((UNSIGNED + 1))
         fi ;;
    esac
  done < <(git log --format='%H%x09%G?%x09%aN%x09%s' "$RANGE")
fi

echo
echo "${TOTAL} commits checked, ${UNSIGNED} without valid signature or attestation"
if [[ "$TOTAL" -eq 0 ]]; then
  echo "RESULT: FAIL - range ${RANGE} contains no commits"
  exit 1
fi
if [[ "$TAG_BAD" -ne 0 || "$UNSIGNED" -ne 0 ]]; then
  echo "RESULT: FAIL - chain of custody has a hole"
  exit 1
fi
echo "RESULT: PASS"
