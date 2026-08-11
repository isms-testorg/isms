#!/usr/bin/env bash
# Verify the signature chain over a range of commits.
#
# This is the "chain of truth" evidence: every change to the management system
# was made through a signed commit by an identified person, and the release tag
# itself is signed.
#
# Two modes, because they answer the question in different places:
#
#   local  (default)  git verify-commit against the keys in your keyring.
#                     Works offline, needs the signers' public keys.
#   github (--github, automatic in Actions)
#                     GitHub's own verification.verified flag. This is what CI
#                     must use: a runner has no signer public keys, so local
#                     verification would report "no public key" for every
#                     commit and prove nothing.
#
# Usage: tools/verify_chain.sh [--github] [<from-ref>] [<to-ref>]
# Default range: previous tag (or root commit) to HEAD.

set -euo pipefail

MODE="local"
if [[ -n "${GITHUB_REPOSITORY:-}" ]]; then MODE="github"; fi
if [[ "${1:-}" == "--github" ]]; then MODE="github"; shift; fi

cd "$(dirname "$0")/.."

FROM="${1:-}"
TO="${2:-HEAD}"

if [[ -n "$FROM" ]]; then
  RANGE="${FROM}..${TO}"
else
  # No explicit start: walk back to the previous tag. If there is none, walk
  # the whole history as a single ref rather than a range. Falling back to the
  # root commit would produce `root..HEAD`, which silently excludes the root
  # itself and, in a one-commit repository, checks nothing at all while
  # reporting success.
  PREV_TAG="$(git describe --tags --abbrev=0 "${TO}^" 2>/dev/null || true)"
  if [[ -n "$PREV_TAG" ]]; then
    RANGE="${PREV_TAG}..${TO}"
  else
    RANGE="$TO"
  fi
fi
echo "Signature chain report"
echo "  repository: $(git rev-parse --show-toplevel)"
echo "  range:      ${RANGE}"
echo "  mode:       ${MODE}"
echo "  generated:  $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo

# --- the tag itself -----------------------------------------------------
if git rev-parse "$TO" >/dev/null 2>&1 && git cat-file -t "$TO" 2>/dev/null | grep -q tag; then
  if git verify-tag "$TO" >/dev/null 2>&1; then
    echo "tag ${TO}: SIGNED and verified"
  else
    echo "tag ${TO}: NOT VERIFIED"
    TAG_BAD=1
  fi
else
  echo "tag ${TO}: not an annotated tag, nothing to verify"
fi
echo

# --- the commits --------------------------------------------------------
UNSIGNED=0
TOTAL=0

if [[ "$MODE" == "github" ]]; then
  while read -r sha; do
    [[ -z "$sha" ]] && continue
    TOTAL=$((TOTAL + 1))
    read -r verified reason author <<<"$(gh api "repos/${GITHUB_REPOSITORY}/commits/${sha}" \
      --jq '[.commit.verification.verified, .commit.verification.reason, .commit.author.name] | @tsv' \
      2>/dev/null || echo -e "false\tapi_error\tunknown")"
    if [[ "$verified" == "true" ]]; then
      printf '  %s  OK        %s\n' "${sha:0:12}" "$author"
    else
      printf '  %s  UNSIGNED  %s (%s)\n' "${sha:0:12}" "$author" "$reason"
      UNSIGNED=$((UNSIGNED + 1))
    fi
  done < <(git rev-list "$RANGE")
else
  while IFS=$'\t' read -r sha flag author subject; do
    [[ -z "$sha" ]] && continue
    TOTAL=$((TOTAL + 1))
    # %G? : G good, U good but untrusted key, X expired, Y expired key,
    #       R revoked key, E cannot check, N no signature.
    case "$flag" in
      G|U) printf '  %s  OK        %s  %s\n' "${sha:0:12}" "$author" "$subject" ;;
      *)   printf '  %s  %-8s  %s  %s\n' "${sha:0:12}" "BAD($flag)" "$author" "$subject"
           UNSIGNED=$((UNSIGNED + 1)) ;;
    esac
  done < <(git log --format='%H%x09%G?%x09%aN%x09%s' "$RANGE")
fi

echo
echo "${TOTAL} commits checked, ${UNSIGNED} without a valid signature"

# Verifying nothing is not the same as verifying successfully.
if [[ "$TOTAL" -eq 0 ]]; then
  echo "RESULT: FAIL - the range ${RANGE} contains no commits, nothing was verified"
  exit 1
fi

if [[ "${TAG_BAD:-0}" -ne 0 || "$UNSIGNED" -ne 0 ]]; then
  echo "RESULT: FAIL - the chain of custody has a hole"
  exit 1
fi
echo "RESULT: PASS"
