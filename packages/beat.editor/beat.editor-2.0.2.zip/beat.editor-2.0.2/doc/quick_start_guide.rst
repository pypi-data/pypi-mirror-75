.. vim: set fileencoding=utf-8 :

.. Copyright (c) 2020 Idiap Research Institute, http://www.idiap.ch/          ..
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


.. _beat-editor-quick-start-guide:

===========================
 Quick Start Guide
===========================

This quick start guide gives an overview of the development workflow using this
editor.

Installation
============

Follow the same `installation`_ procedure as other beat packages to setup a
conda environment ready for development.  Activate the conda environment (e.g.
named "beat").

.. code-block:: sh

   $ conda activate beat
   (beat) $

.. note::

   In these instructions ``(beat) $`` corresponds to your own shell prompt,
   which can be different.  The actual command(s) to type comes after the ``$``
   marker.

All further instructions assume you have the environment where BEAT packages
are installed properly activated.


Work flow
=========

The BEAT editor allows you to implement and test your solution locally on
either a reduced or different dataset.  Once you have everything working as
expected, push the resulting code to the platform and execute it there, for
validation.

The following steps describe the procedure to start from an **existing**
experiment and build on that.

#. Get (or pull) the reference experience you would like to base your work on:

   .. code-block:: sh

      (beat) $ beat pull <experiment-author>/<experiments>/<toolchain-author>/<toolchain-name>/<toolchain-version>/<experiment>

   This will pull the experiment as well as all its dependencies from the
   platform so that it can be edited (and run) locally.

   .. note::

      Values within angle brackets (``<`` and ``>``) will depend on the asset
      name.  Replace these values by appropriate actual values.

#. Create your own fork of the experiment:

    .. code-block:: sh

        (beat) $ beat experiment fork <experiment-author>/<experiments>/<toolchain-author>/<toolchain-name>/<toolchain-version>/<experiment> <your-beat-user-id>/<experiments>/<toolchain-author>/<toolchain-name>/<toolchain-version>/<experiment-name>

#. Create your own fork from an algorithm you want to modify:

    .. code-block:: sh

        (beat) $ beat algorithm fork <author>/<algorithm>/<version> <your-beat-user-id>/<algorithm>/<version>

    This will allow you to use your own modified algorithm for your fork.

    .. note::

        You will have to update your experiment fork in order to use your own
        algorithm(s).

    .. note::

        You do not need to fork an algorithm, you can use a different one as
        long as its inputs and outputs match the one you want to replace.

#. Edit the code:

   .. code-block:: sh

      (beat) $ beat algorithm edit <author>/<algorithm>/<version>

   This will open your default configured editor to edit the code of the
   algorithm passed in parameter.

#. To edit any other asset, just start the editor, optionally pointing to the
   prefix of interest:

   .. code-block:: sh

      (beat) $ beat --prefix <path/to/prefix> editor start

   This will start the BEAT editor so that you will have an easy access to all
   locally available assets.  You'll be able to edit them visually. The editor
   also allows to start your favorite editor for code or documentation
   modification.

#. Once the editing is done, you can run an experiment **locally** like this:

   .. code-block:: sh

      $ beat exp run <experiment-author>/experiments/<toolchain-author>/<toolchain-name>/<toolchain-version>/<experiment-name>

#. Once the experiment runs successfully on your machine, you can upload it to
   the online platform and run it there.

    .. code-block:: sh

       $ beat exp push <experiment-author>/experiments/<toolchain-author>/<toolchain-name>/<toolchain-version>/<experiment-name>
       $ beat exp start <experiment-author>/experiments/<toolchain-author>/<toolchain-name>/<toolchain-version>/<experiment-name>

    You can monitor the execution of your experiment at any moment with:

    .. code-block::

       $ beat exp monitor <experiment-author>/experiments/<toolchain-author>/<toolchain-name>/<toolchain-version>/<experiment-name>

.. include:: links.rst
