
# CHANGELOG

## Version 2.0.0 (2020-06-22)
### New features

- distance: add a function to convert distance of alignments to confidence
- blocking: add a new parameter 'repeatable' to MinHashingBlocking

### Bug fixes

- manifest: use `exclude` to exclude files (prune is for directories)
- aligner: pipeline aligner returns the pair distance too


## Version 1.0.0 (2020-04-20)
### Continuous integration

- flake8: run flake8 on the tests as well


## Version 0.9.6 (2020-05-07)
### Bug fixes

- manifest: add a missing repository
- pin check-manifest version waiting for upstream bug fix (https://github.com/mgedmin/check-manifest/issues/115)
- tests: allow the test of XHTML validation to fail

### Continuous integration

- black: add a black check
- manifest: add a check-manifest ci test

### Various changes

- Make the code black :)


## Version 0.9.5 (2019-12-03)
### Various changes

- pkg: version 0.9.5
- pkg: ignore "examples" module
- Update debian packaging with support for Python3
- Add check-manifest
- Re-add python2 support for a last python2 compatible release
- tox: use "py3" instead of "py37"
- CI: Add a gitlab-ci.yml to run unittests and flake8
- tox: Upgrade testing version from py3.6 to py3.7
- tox: Drop python27 tests
- distances: Use array in favour of deprecated matrix
- flake8: Fix E303 too many blank lines
- flake8: Fix W605, invalid escape sequence
- tests, dataio: Add a missing prefix in a sparql query
- tests, minhashing: Properly fix the random seed from minhashing tests
- tests, distance: Use AlmostEqual to compare floating numbers
- dataio, rqlquery: Fix url quoting and encoding issues (2to3)
- dataio: dtd_validation with external DTD requires a network connection
- data: Make sure the french_lemmas file is closed
- setup: Remove the databnf entry point
- 2to3, kmeans: Use the integer division to compute the number of clusters


## Version 0.9.4 (2019-09-06)
### Various changes

- pkg: Prepare 0.9.4
- sparql: Enable user to set a custom useragent


## Version 0.9.3 (2019-06-07)
### Various changes

- pkg: Prepare 0.9.3
- distance: Set the jaccard distance of empty sets to 1.
- normalize: Use a generator to filter instead of a list


## Version 0.9.2 (2019-05-09)
### Various changes

- pkg: prepare 9.0.2
- aligner: Use the processings' weight to compute the distance matrix


## Version 0.9.1 (2018-09-03)
### Various changes

- 0.9.1
- fix py3 incompatibilities found by running tox -e py36
- add tox configuration
- flake8
- py3: use six for xrange / basestrign compat
- autopep8
- py3: user iter to iterate on dict values
- py3: use itervalues from six
- py3: use xrange from six
- py3: use six.string_types instead of basestring
- 0.9.0: 
- py3: use six.iteritems instead of dict.iteritems
- py3: add deps on six
- py3: use text_type from six instead of unicode
- py3: no print, no old exception, no cPickle
- pkg: standard python package - continue
- python-modernize -w
- pkg: standard python package
- setup: python3: use items() instead of iteritems()
- add replacement char for \u2019
- aligner: one more safety belt to avoid crash on empty sets
- aligner: safety belt to avoid crash on empty sets


## Version 0.8.0 (2016-07-08)
### Various changes

- prepare 0.8.0
- make Minlsh.predict() accept a minclustersize parameter


## Version centos/0.7.2-2 (2016-01-29)
### Various changes

- pkg: do not include all files in spec
- pkg: Fix copyright in __pkginfo__.py
- pkg: Remove redundant lxml entry in __pkginfo__ depends


## Version 0.7.2 (2015-07-20)
### Various changes

- pkg: 0.7.2
- debian: use dh_python2
- add dependency to lxml (closes #287976)
- pkg: update setup.py script to make it pip installable


## Version nazca-centos-version-0.7.1-1 (2014-11-25)
### Various changes

- prepare 0.7.1
- distances: TemporalProcessing should only be available if dateutil is installed (closes #279606)
- debian: recommend python-dateutil (closes #279605)
- dataio: provide compatibility with CW 3.19 (closes #279602)
- fix NameError (s/query/rql) in dataio.rqlquery (closes #279601)
- tests: skip SPARQL tests when python-sparqlwrapper is not installed (closes #279604)
- debian: recommend python-sparqlwrapper (closes #279603)


## Version nazca-centos-version-0.7.0-1 (2014-11-23)
### Various changes

- support sklearn 0.10->0.14 versions for minhashing
- tests: skip TokenizerTest and FilterTests when NLTK is not installed
- tests: update tests against dbpedia to make them pass (hopefully more permanently)
- preparing 0.7.0
- tests: skip prettyprint tests when NLTK is not available
- debian: Rename binary package as python-nazca
- pkg: Add missing dependencies on scipy and scikit-learn in __pkginfo__ and debian/control
- utils: Use sentences delimiter from NLTK
- utils: Extract words splitting regular expression for easier overridding


## Version nazca-centos-version-0.6.1-1 (2014-07-15)
### Various changes

- preparing 0.6.1
- notebooks: Fix a syntax error
- distances: Correctly check if index is not None rather than if index, as one can used the first column (index=0) for processing, closes #257026
- notebooks: Add affiliation
- notebooks: Update notebooks


## Version nazca-centos-version-0.6.0-1 (2014-06-30)
### Various changes

- preparing 0.6.0
- distance: Now, it is possible to pass tuple to the distance processing to create a subrecord
- test: Add test for GeographicalProcessing
- notebooks: Adding notebooks
- distances: Raise an error on bad units for Geographical distance
- doc: add a logo for the project
- aligner: Keep the distance matrix by default, closes #252735
- distances: Add an ExactMatchProcessing, closes #252734
- blocking: Add compatibility for older version of sklearn, closes #252733
- Provides Processings for all the distances, closes #248557
- distance: Add safety belt on geographical distance units, closes #248555
- api: Make autocast API constistant, closes #248554


## Version nazca-centos-version-0.5.1-1 (2014-04-24)
### Various changes

- preparing 0.5.1
- sparql: handle empty result of _sparqlexecute (closes #235720)
- normalize: Correctly check for 0 or None in normalization indexes, closes #241166


## Version nazca-debian-version-0.5.0-2 (2014-04-09)
### Various changes

- debian: fix package description in control file


## Version nazca-centos-version-0.5.0-1 (2014-04-08)
### Various changes

- dataio: Add a variable to avoid autocast in parsefile
- preparing 0.5.0
- distances: add a `SoundexProcessing`, related to #234919
- display ExceptionErrors in sparklquery
- distances: Add difflib match distance, closes #234655


## Version nazca-version-0.4.3 (2014-03-25)
### Various changes

- preparing 0.4.3
- manifest: Add missing data/*.txt


## Version nazca-centos-version-0.4.2-2 (2014-03-21)
### Various changes

- fix .spec


## Version nazca-version-0.4.2 (2014-03-21)
### Various changes

- preparing 0.4.2
- test: Handle both unittest2 and unittest in Python > 2.6
- fix setup.py


## Version nazca-centos-version-0.4.1 (2014-03-10)
### Various changes

- add spec file for rpm


## Version nazca-version-0.4.1 (2014-03-10)
### Various changes

- preparing 0.4.1
- minhashing: Correctly build k grams in minhashing, closes #221665


## Version nazca-version-0.4.0 (2014-01-08)
### Various changes

- preparing 0.4.0
- data: Avoid .py files for data
- ner: Disambiguation word should be case-insensitive, closes #200147
- ner: Fix sparql results for types filtering after modifying in dataio
- dataio: Create an helper that execute a sparql query and return a clean json dict, see #198745
- doc: Merge docs and update doc, related to #187461
- data: Move french lemmas in data module, related to #187461
- rename: Rename modules with shorter names, related to #187461
- named entities: Split core into preprocessors and filters modules, related to #187461
- named entities: Move tokenizer to utils and create a sources module for named entities, related to #187461
- dataio: Merge dataio and tests, related to #187461
- ner: Cleanup Nerdy, related to #187461
- Rename ner in named_entities, related to #187461
- utils: Create an utils folder, related to #187461
- ner: Remove unused files and move tests, related to #187461
- old api: Remove deprecated old API, closes #197016
- normalize: Remove deprecated "ignorennonascii" in unormalize, closes #187456
- nazca: Create a record linkage directory, related to #187461
- test: Fix typo in test
- nerdy: Move nerdy into ner directory.
- fix tags for centos/ debian, version 0.1.0


## Version python-nerdy-centos-version-0.1.0-1 (2013-07-01)
### Various changes

- packaging: add spec file for centos
- pkg: add debian folder
- pkg: add setup.py and __pkginfo__.py (prepare 0.1.0)
- Add a class attribute to HTML pprint_entity
- Allow kwargs to be passed to pretty printers pprint_entity and pprint_text
- Add a XHTML valid pretty printer
- filters: Add a based-rules replacement filter
- core: Correctly build the session execute call
- core: Fix issue in sliding window for the Nerdy Process.
- core: Fix Types filter.
- core: Add a NerDisambiguation process
- doc: Add doc and examples
- test: Add tests
- core: Add core NER functions and logic
- dataio: Add utils for data io and requests
- tokenizer: Add a RichString tokenizer
- stopwords: Add stopwords file
- Initial commit


## Version nazca-version-0.3.0 (2013-10-08)
### Various changes

- preparing 0.3.0
- doc: Update doc
- distances: Extract cdist in a function, see #183470
- aligner: Now, returned pairs also have the distance between the two elements, see #183463
- old api: Update old api and corresponding tests, see #183461
- aligner: Simplify for now the aligners pipeline, see #183468
- logger: Add a logger, see #183459
- aligner: Add an option to normalize distance matrix, see #183457
- dataio: Make autocaste optional for sparql io, see #183448
- blocking: Add a merge blocking, see #182023.
- blocking: Protect key blocking against none values, see #183446
- data: Add reference data, see #183444
- aligner: Add aligners pipeline, see #182035
- aligner: Update verbose infos, see #183439
- minhashing: Protect minhashing against shape < 1, see #182033
- blocking: Add pipeline blocking, see #182032
- aligner: Add tools to align from files, see #182030
- blocking: Now blocking techniques return indice or id or both, see #183415
- blocking: Add a NGram blocking technique, for blocking on the N first letters of a key, see #182023
- refactor: Refactor normalize module and objectify it, see #182001


## Version nazca-version-0.2.3 (2013-04-25)
### Various changes

- Preparing 0.2.3
- matrix: "temporal()" may not be defined, depending one dateutil


## Version nazca-debian-version-0.2.2 (2013-04-24)
### Various changes

- preparing 0.2.2
- distances: Conditionate the temporal functions by the correct import of dateutil, closes #134762
- preparing 0.2.1
- align: Correctly check the best value, closes #134571
- setup: include every python module under the nazca package (closes #134570)


## Version nazca-version-0.2.0 (2013-04-04)
### Various changes

- preparing 0.2.0
- doc: Use sphinx roles and update the sample code (closes #119623)
- Aligner: `normalize_set` handles tuples. (closes #117136)
- doc: Little explanation on alignall_iterative() (closes #116943)
- aligner: Speed up the alignset reduction (closes #116942)
- aligner: Enable the user to customize the equality_threshold (closes #116940)
- aligner: Enable the user to reuse the cache returned by alignall_iterative() (closes #116938)
- aligner: Add the alignall_iterative() function (closes #116932)
- dataio: Implements split_file() (closes #116931)
- doc: Typo + a litte text about the online demo. (closes #116939)
- aligner: Enables the user to give formatting options (closes #116930)
- aligner: Deal with possible singleton value for KDTree
- normalize: Dont simplify item if they aren't basestrings


## Version nazca-version-0.1.0 (2012-12-18)
### Various changes

- Remove unused files
- setup: Add setup and __pkginfo__
- debian: Change package name
- debian: Fix changelog bis
- debian: Fix changelog


## Version python-nazca-0.1.0 (2012-11-29)
### Various changes

- aligner: the neighbouring function in ``alignall`` is optional.
- dataio: Add a ``rqlquery()`` function
- dataio: ``parsefile()`` handles string or stream as ``filename``
- dataio: Avoid many imports of the same module (SPARQLWrapper and JSON)
- dataio: Don't assume by default the input of ``autocasted`` is a string.
- test: Try to protect some tests from a deprecated version of scikit learn
- test: Remove unused pytestconf.py
- Rename package into Nazca and change imports
- doc: Enhancements in the doc
- test: Add the french lemmas file for tests
- minhashing: Remove depracated __main__
- aligner: Correct the bug raised in 4d53757fbadf
- demo: Use the new formating parsefile options
- dataio: Add a formating option
- distance: Don't read letters uselessly to compute the soundexcode
- normalize: Make the loadlemmas() function more readable
- Remove useless imports
- Remove useless variables
- align: Assert all inputs of all items have the same length.
- matrix: Add comment on normalization
- distance: Move out the custom parser info.
- doc: Some other corrections
- doc: Some corrections
- doc: First version
- demo: Rename imports
- aligner: Normalize the sets before calling the findneigbours() function
- demo: Add some prints to show the alignment progress
- demo: Add some prints to show the alignment progress
- demo: Use a global function to compute paths
- normalize: In simplify() replace punctuation by a space
- Add some XXX on Adrien's comments
- minhashing: Add a verbose mode
- aligner: Remove a useless import
- Remove a useless file
- Respect (or try to respect) pep8
- minhashing: consume less memory
- test: Remove a useless line
- minhashing: Compute the union step by step
- minhashing: Buckets are row-dependant
- dataio: Add a forgotten encoding attribut
- test: write the tests for the `alignall()` function
- aligner: Align the code on 80 car
- aligner: Make the alignall() function
- aligner: Let the user decide on wheter return the global alignement matrix or not
- minhashing: Export the demo of minhashing to the new api
- aligner: Remove useless arguments from findneighbours_clustering()
- aligner: clustering: Don't crash if sets are small.
- aligner,dataio: Export the results writing to a independant function
- test: Write the test for test_findneighbours_clustering
- dataio: Export some function to the dataio.py file
- test: add more tests
- align: Update API
- matrix: Make API closer to scipy.spatial and add metrics handling
- Cosmit
- minhashing: Modify API + change threshold handling
- normalize: Better tokenizer for unicode + stopwords
- Few corrections and add tests
- minhashing: Compute complexite on a huge file
- minhashing: plot complexity
- matrix: Let's the distance matrix API looks like scipy's one
- minhashing: Don't copy uselessly the signature matrix
- minhashing: Faster signaturing using numpy
- minhashing: rewrite main for testing purposes
- minhashing: Typo
- Try to optimize buckets computation in min hashing
- refactoring: First round of refactoring/review
- Add french_lemmas file
- aligner: add findneighbours docstring
- Add and delete some XXX
- aligner: Don't append and pop. Check before.
- aligner: Enable the user to give the signature matrix for minhashing
- demo: minibatch is faster
- aligner: Change the default value of k.
- Todo: Add a TODO file
- aligner: Handle any dimension for clustering and kdtree
- aligner: Continue to use 1xM matrices for KDTree
- demo: Display how much time the run took
- aligner: Instead of returning 1xN matrices, return MxN ones
- demo: Use kmeans instead of kdtree (for testing)
- aligner: Use lazy import for minhashing and kdtree
- aligner: Add kmeans to the available searchers list
- demo: For demo2, don't read the whole file
- aligner: Define autocasted as a global function
- demo: For testing purpose, run only the given demo
- demo: Use the sparql queries handling instead of csvvfile
- aligner: Handle sparql queries
- aligner: Makes parsefile works with unicode
- Let's make the tests and demo paths indepedant
- demo: Use the new implemantation of findneigbours()
- aligner: higher level implementation of KDTree and Minhashing
- demo: Add a new demo (with a kdtree)
- demo: add exemple on custom normalization function usage
- demo: Add a new demo of alignment usage
- normalize: Let's nltk be optional
- minhashing: Spelling mistake
- matrix: spelling mistakes
- distances: spelling mistakes
- aligner: Spelling mistakes
- aligner: Remove useless dependancies
- demo: Add comments
- aligner: Set the parsefile function into aligner module
- Add the demo file
- Extract the alignment process from the cube to be independant
- matrix: Cancel the 188 changset. Multiplying matrices was, in fact, a bad idea
- Correct some spelling
- minlsh: Use an iterator to compute the result set
- minlsh: Remove the useless rows in the signature matrix while searching
- distances: For the jaccard distance, consider the set of tokens
- Matrix: Remove the unused defaultvalue
- Align: don't use queries by lists, directly
- Matrix: Multiplying instead of adding
- Distance: The output unit of geographical distance can be precised
- API: Write results according to csv format
- API: Start the implemantation of the alignment API
- Minhashing: Give a thresdhold instead of a abstract "bandsize"
- Order imports
- Minhashing: Trained data can be saved and loaded
- distances: The planet radius for the geographical distance can be given
- distances: Don't concat two strings to know if there is a space in one of them. Make two tests instead
- typo: alignement --> alignment
- Matrix: Maximum distance computation delegated to max() method of numpy.matrix
- Minhash: Tests written
- Matrix: Improvement of the matched() method
- Matrix: Change lil_matrix for dense matrix
- Distance: Add geographical distance
- testing: make the alignment testing a little bit more cleaner
- Matrix: Adapt the globalalignmentmatrix computation to the previous changeset
- Matrix: Give weighting and normalization at the contruction of the matrix
- wip
- Minhashing: Really, really, really faster training
- Matrix: Compute the global alignement matrix
- Matrix: Can pass extra arguments to distance functions
- Matrix: Computation handles unknown values
- Test: Updated to the changement of simplify()
- Normalize: Add docstring to simplify()
- normalize: Add a stopword removing option to simplify()
- Minhashing: Api fonctionnelle
- minhashing: First try of minhashing (related to #129000)
- Matrix: Add basic operations such as add, mul sub, etc
- Matrix: Add __repr__ method()
- Matrix: Don't store inputs inside DistanceMatrix object
- Distance: Spaces are correctly supported by distances functions
- Matrix: Cannot use zip if it not a square matrix \!
- Matrix: Matched() return index and value, as tuples
- Matrix: Matched() has a lower complexity
- Matrix: Matrices are not symetric. Correct it
- Test: Assure distances are symetric
- Test: Add tests for matrix
- Test: Tests don't inherite anymore from CWTestCase by directly from unittest2 (be independant)
- Normalizer: Lematizer returns a string (better for comparison)
- Matrix: Enables normalization
- Test: Distance, test euclidean distance on strings too
- normalize: Using a class was a bad idea, I removed it
- Matrix: Compute a distance matrix
- Distance: Exchange 1 and 0 in the soundex distance, because we try to minimize the distance
- Distance: Temporal distance supports ambiguity and fuzzyness
- Normalizer: Add the format method  (related to #128998)
- Add LGPL to distance.py and normalize.py
- Normalizer: Add a normaliser (related to #128998)
- distances: Add an euclidean distance function between two numbers (closes #128982)
- distance: Add a new distance between dates (related #128982)
- distances: Add jaccard distance (related #128982)
- distances: Add the soundex distance (related #128982)
- distance: move soundex to soundexcode (related #128982)
- distances: Remove some trailing spaces (related #128982)
- distance: Start the iteration at 1, not 0 because we don't care about the first
- distances: Correct an IndexError in the soundex code (related #128982)
- distance: Soudex : if there is a vowel between two identical numbered
- test: Add some other tests to soudex, and some explanations too
- test: The test for soundex was false, I corrected it (related #128982)
- tests: Add tests for soundex and levenshtein (related #128982)
- distances: Add soundex code (related #128982)
- distance: add Levenshtein distance (related #128982)
- Initial commit


