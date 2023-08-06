#!/usr/bin/env bash
set -euo pipefail

unset GREP_OPTIONS

# This script finds compatibility-related comments with a node hash specified
# in all files in a given directory (. by default) and looks up the hash in a
# repo (~/hg by default) to determine if each of the comments is correct and,
# if not, it suggests the correct release. This can prevent accidentally
# removing a piece of code that was misattributed to a different (earlier)
# release of core hg.

# Usage: $0 WDIR HGREPO where WDIR is usually evolve/hgext3rd/ and HGREPO is
# the place with core Mercurial repo (not just checkout). Said repo has to be
# sufficiently up-to-date, otherwise this script may not work correctly.

workdir=${1:-'.'}
hgdir=${2:-~/hg}
grep -Ern 'hg <= [0-9.]+ \([0-9a-f+]+\)' "$workdir" | while read -r line; do
    bashre='hg <= ([0-9.]+) \(([0-9a-f+]+)\)'
    if [[ $line =~ $bashre ]]; then
        expected=${BASH_REMATCH[1]}
        revset=${BASH_REMATCH[2]}
        tagrevset="max(tag('re:^[0-9]\\.[0-9]$') - ($revset)::)"
        lastrel=$(HGPLAIN=1 hg --cwd "$hgdir" log -r "$tagrevset" -T '{tags}')
        if [[ "$lastrel" != "$expected" ]]; then
            echo "$line"
            echo "actual last major release without $revset is $lastrel"
            echo
        fi
    fi
done
