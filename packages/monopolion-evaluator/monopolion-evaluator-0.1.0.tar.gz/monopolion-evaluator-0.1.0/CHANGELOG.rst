
Changelog
=========

0.1.0 (2020-08-03)
------------------

* Changed CLI to sub-commands. `monopolion-evaluator` is now `monopolion-evaluator train`.
* Added predict sub-command.
* Added `--output` arg to `train`, to save the model.

0.0.6 (2020-07-29)
------------------

* Added command line arguments to customize classifier

0.0.5 (2020-07-28)
------------------

* Fix 'File already exists' build error, caused by competing build artifacts
* Fix missing wheel in build

0.0.4 (2020-07-28)
------------------

* Added continuous deployment using Travis

0.0.3 (2020-07-28)
------------------

* Added Classifier

0.0.2 (2020-07-26)
------------------

* Parses GameOutcome protobuf
* Converts protobuf to Pandas DataFrame

0.0.1 (2020-07-25)
------------------

* Removed requirements.io to let build pass on Travis.
* Removed support for Python <= 3.5.

0.0.0 (2020-07-24)
------------------

* First release on PyPI.
