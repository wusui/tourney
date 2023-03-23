# Single Elimination tournament picking standings generator

### General Description

This repository contains python scripts that enables one to produce a table of what future outcomes
are needed in order to determine probable winners in a pick 'em style pool of competing entries.
Okay -- enough of this pretense of being general.  The purpose of this code is to track possible
future outcomes in NCAA championship basketball championship tournaments.

### Confession

I have been running this pool for several years and though that I had everything fully automated
in 2022.  The 2022 code broke as far as I can tell due to format changes on the ESPN pages that I
was scraping.  I ended up recreating the wheel and realized that what I needed is a boring general
purpose tournament result tracker which received input from local files.

So this repository consists of scripts that do the computations needed and formatting of the results
into an html table.  The code should work at any point in the tournament although it has been tailored
to work best when the Sweet Sixteen is reached.  This is the sweet spot where the problem is too
big to do by hand but not too big that an inordinate amount of CPU time is spent.  It is also useful
to run this at the Elite 8 point.  Anything less than that can be computed by hand, and anything
over that takes too long to run.

### Scripts

* get_reality.py -- Do computations needed
* format.py -- Produce the html table
* read_after_js.py -- Helpful scraping tool to get the raw text of a webpage after javascript runs

### Data required

From the user's standpoint, this is the most import part of this document because it describes what is
needed in order to use this program.  Three files are important for this:

reality.txt: An or-bar separated list of winning team numbers.  Reading left to right, each round follows
the previous round

team_info.txt: One entry per line text file consist of team information.  Entries are colon separated text
consisting of the team number, abbreviation, and name.

picks.json: Dict indexed by entrant. Contents of each entry is a list of team numbers in the same order as the teams listed in reality.txt

