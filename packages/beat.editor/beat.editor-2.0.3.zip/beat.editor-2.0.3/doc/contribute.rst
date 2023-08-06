.. vim: set fileencoding=utf-8 :

.. Copyright (c) 2019 Idiap Research Institute, http://www.idiap.ch/          ..
.. Contact: beat.support@idiap.ch                                             ..
..                                                                            ..
.. This file is part of the beat.editor module of the BEAT platform.             ..
..                                                                            ..
.. Commercial License Usage                                                   ..
.. Licensees holding valid commercial BEAT licenses may use this file in      ..
.. accordance with the terms contained in a written agreement between you     ..
.. and Idiap. For further information contact tto@idiap.ch                    ..
..                                                                            ..
.. Alternatively, this file may be used under the terms of the GNU Affero     ..
.. Public License version 3 as published by the Free Software and appearing   ..
.. in the file LICENSE.AGPL included in the packaging of this file.           ..
.. The BEAT platform is distributed in the hope that it will be useful, but   ..
.. WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY ..
.. or FITNESS FOR A PARTICULAR PURPOSE.                                       ..
..                                                                            ..
.. You should have received a copy of the GNU Affero Public License along     ..
.. with the BEAT platform. If not, see http://www.gnu.org/licenses/.          ..


.. _beat-editor-contribute:

===========================
 Contribute to beat.editor
===========================

Development environment setup
=============================

Follow the same procedure as other beat package to setup a conda environment
ready for development.

#. Setup conda environment: ::

   $ /path/to/bob.admin/conda/conda-bootstrap.py --overwrite --python=3.6 beat_editor_env

#. Setup development environment: ::

   $ buildout -c development.cfg

#. Install the ``pre-commit`` package: ::

   $ conda install pre_commit

#. Setup ``pre-commit`` package: ::

   $ pre-commit install

#. You can run the pre-commit hooks at any time by calling: ::

    $ pre-commit run --all-files


beat.editor needs the following dependencies for its pre-commit hooks:

    - black
    - flake8
    - bandit


| black is currently available through Idiap's conda channel.
| flake8 is available through conda's defaults channel.
| bandit is not yet available on either so it must be installed using pip:

::

    $ pip install bandit

If you would like to install them all using pip you can call: ::

    $ pip install -r pre-commit-dependencies.txt


Development
===========

Writing code
------------

beat.editor is a python application or rather Qt Python application. It will use
the `QtWidgets`_ module for the GUI part.

The current implementation will use `PyQt`_ as `Qt for Python`_ is not yet
available on conda.

While the code is written in Python the API is mostly the same as the C++
framework minus some pythonism that can be found in the `PyQt documentation`_.


Writing tests
-------------

beat.editor uses pytest as its testing framework because of the `pytest-qt`_
module that provides support for testing Qt based application.

An example of tests is shown here:

.. literalinclude:: ../beat/editor/test/test_editors.py


Tests can fall in to categories:

- Automatic tests
- Manual tests

Automatic tests are tests that can be fully automated using pytest and pytest-qt
while manual tests are tests than requires that a person takes a look at the
output of said test. For example check that the rendering of some GUI element is
the expected output. This kind of test may require writing a minimal application
that will be as automated as possible in order for the operator to only have to
do the manual check(s) required.


Run tests
---------

beat.editor uses pytest to run its test suite. ::

    $ pytest -sv

Will run all the tests verbosely and not capture the outputs of the test. The
`-s` option is mandatory if there's a need to brake in the code using python's
debugger.

If you have built your packages using `buildout.cfg` and wish to transition to a development stage using `development.cfg`
first make sure you have removed `beat.core`, `beat.cmdline` and `beat.backend.python` from your conda environment ::

    $ conda list # check
    $ conda remove <package>

Then rebuild all packages (you can delete the bin/ folder to make sure it's rebuilt): ::

    $ buildout -c development.cfg

Now running your tests would require pytest to use the current environment and use your dependency packages: ::

    $ ./bin/python -m pytest -sv

Coding guidelines
=================

Coding style
------------

PEP8 rules should be followed when writing code for this module.

In order to avoid having to nitpick about code style. black for python as well
as flake8 will be used to ensure that formatting is enforced and doesn't let
the developer wondering if he did it the right way.

Pre-commit hooks will be run to ensure that.

While developing, the hooks can be manually called: ::

    $ pre-commit run --all-files

This command will run the hooks on the whole repository. However more fine
grained control can be applied.

Commit guidelines
=================

Commit content
--------------

Commits should be atomic. What atomic means is that one commit should target
one specific change.

For example:

#. Introduce new API with corresponding tests
#. Implement use of new API in module1 with corresponding tests
#. Implement use of new API in module2 with corresponding tests

The same goes for fixes in, for example, the documentation. If the change is not
related to code changes committed at the same time, then it should be a separate
commit. This will avoid confusion and also allow for easier refactoring if
needed.

Commit message format
---------------------

The commit message format is the following:

One summary line with the concerned module in brackets
One blank line
Longer multi-line description of what change and why it was changed.
One blank line
Meta information like bug fixed by the commit

Example: ::

    [widgets] Automatically update json preview

    The preview content was only loaded at the same time as the file parsed.
    Now changes to the file are automatically detected and the preview
    refreshed.

    Fixes #10


If the change is trivial like fixing a typo in a variable name, the long
description may be omitted.

Commit message must be meaningful.

For example: ::

    [dependencies] Updated version

is not acceptable as it doesn't provide any useful information beside "something
has been update". This means that any developer going through the
history log will have to open that specific commit to see exactly what changed
and may only guess why it has changed.

On the other hand: ::

    [dependencies] Updated minimal foo version to X.Y.Z

    Needed because of bug XXXXX

is concise and makes it clear what happened and why.


Branching guidelines
====================

Branching must be used for new features as well as bug fixes. Unless an
exceptional circumstance occurs, one branch should implement one feature or
one bug fix. If bug fixes or features depend on one of these branch, then a
new branch should be created from there and then rebased as soon as the base
branch was merged into master.

Before merging occurs, each branch should be rebased on the latest master.

As for the naming, branches should have meaningful names also.

For example: ::

   issue_20_fix_wrong_index
   implement_dataformat_editor

A branch doesn't need to be one commit, it can be but it can also span as many
commits as needed in order to implement a feature or bug fix.

Note that it may also happen that one branch contains fixes for several issues
as they might be related.


Merge message
-------------

Merge messages should again be meaningful and concise about the what and the
why.

.. include:: links.rst
