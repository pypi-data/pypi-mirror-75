#require test-repo flake8

Copied from Mercurial core (60ee2593a270)

  $ cd "`dirname "$TESTDIR"`"

run flake8 if it exists; if it doesn't, then just skip

  $ hg files -0 'set:(**.py or grep("^#!.*python")) - removed()' \
  > -X hgext3rd/evolve/thirdparty \
  > 2>/dev/null \
  > | xargs -0 "$PYTHON" -m flake8
