# Duplicates

Duplicate observations can appear when different scanners are used to scan the same code or dependencies. Sometimes one scanner might produce potential duplicates as well, e.g. reporting the same vulnerability for multiple dependencies.

## Find potential duplicates

An asynchronous process to detect potential duplicates is executed when importing scan results. It checks all existing open observations for the same project, the same branch and the same service plus one of two conditions:

* The same title for different components
* Observations with the same source file name and start line number from different scanners

The lists of observations in the user interface show a column if an observation has potential duplicates.

## Mark duplicates

If an observation has potential duplicates, they are shown in a list when showing the observation details. The user can tick one or more of them and mark them as duplicates. This will add an assessment to the observation with the status `DUPLICATE` and a comment.
