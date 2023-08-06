===============================================
Testing evolution of obsolete working directory
===============================================

Pulling changes from other repos can make your working directory parent (wdir)
obsolete, most probably because now it has a new successor. But there are
other cases as well where it might be pruned with no successors or split
in multiple changesets etc.

This test file deals with all the possible cases for the evolution from an
obsolete working directory parent.

.. Case A: obsolete wdp with single successor
..     Resolution : simply update to the successor
..
.. Case B: obsolete wdp with no successor (simply pruned)
..     Resolution : update to a not-dead ancestor
..
.. Case C: obsolete wdp with multiple successor (divergence rewriting)
..     Resolution : #TODO: not handled yet
..
.. Case D: obsolete wdp with multiple successor (split rewriting)
..     Resolution : #TODO: not handled yet

A. Obsolete wdp with single successor
-------------------------------------

Setup
  $ . $TESTDIR/testlib/common.sh
  $ cat >> $HGRCPATH <<EOF
  > [extensions]
  > evolve=
  > rebase=
  > [alias]
  > glog = log --graph --template "{rev}:{node|short} ({phase}): {desc|firstline} {if(troubles, '[{troubles}]')}\n"
  > EOF

  $ hg init repo
  $ cd repo
  $ mkcommit c_A
  $ mkcommit c_B
  $ hg amend -m "u_B"
  $ hg up -r 'desc(c_B)' --hidden
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset 707ee88b2870
  (hidden revision '707ee88b2870' was rewritten as: 9bf151312dec)
  working directory parent is obsolete! (707ee88b2870)
  (use 'hg evolve' to update to its successor: 9bf151312dec)

  $ hg evolve
  update:[2] u_B
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  working directory is now at 9bf151312dec
  $ hg glog
  @  2:9bf151312dec (draft): u_B
  |
  o  0:9f0188af4c58 (draft): c_A
  

B. Obsolete wdp with no successor
---------------------------------

  $ hg prune .
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  working directory is now at 9f0188af4c58
  1 changesets pruned
  $ hg up -r 'desc(c_B)' --hidden
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset 707ee88b2870
  (hidden revision '707ee88b2870' is pruned)
  working directory parent is obsolete! (707ee88b2870)
  (use 'hg evolve' to update to its parent successor)

  $ hg evolve
  update:[0] c_A
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  working directory is now at 9f0188af4c58
  $ hg glog
  @  0:9f0188af4c58 (draft): c_A
  

C. Obsolete wdp with multiple successor (divergence rewriting)
---------------------------------------------------------------

  $ hg metaedit -r 'desc(u_B)' -d '0 1' --hidden
  $ hg metaedit -r 'desc(c_B)' -d '0 1' --hidden
  2 new content-divergent changesets
  $ hg up -r 'min(desc(c_B))' --hidden
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset 707ee88b2870
  (hidden revision '707ee88b2870' has diverged)
  working directory parent is obsolete! (707ee88b2870)
  (707ee88b2870 has diverged, use 'hg evolve --list --content-divergent' to resolve the issue)

  $ hg evolve
  parent is obsolete with multiple successors:
  [3] u_B
  [4] c_B
  [2]

  $ hg glog
  *  4:39e54eb7aa3c (draft): c_B [content-divergent]
  |
  | *  3:90624b574289 (draft): u_B [content-divergent]
  |/
  | @  1:707ee88b2870 (draft): c_B
  |/
  o  0:9f0188af4c58 (draft): c_A
  

D. Obsolete wdp with multiple successor (split rewriting)
----------------------------------------------------------

#TODO: yet to write tests for this case
