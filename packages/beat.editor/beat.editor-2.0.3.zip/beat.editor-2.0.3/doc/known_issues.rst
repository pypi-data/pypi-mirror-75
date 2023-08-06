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


.. _beat-editor-knownissues:

=============================
 Known issues on beat.editor
=============================

This documents lists the current important issues and gives a pointer to the
complete list of issues on the Gitlab repository.


Experiment editor
=================

    - The algorithm selection currently does not check for dataformat compatibility
      between blocks.
      See (`Issue 185`_)
    - No preview of the toolchain currently available.
      See (`Issue 185`_)
    - Smart mapping/filtering to enable smarter algorithm selection based on matching
      input and outputs is not available yet. However the algorithms provided
      are matching the inputs and outputs in terms of its numbers.
      See (`Issue 185`_)


Gitlab Issues
=============

All issues can be found on our `Gitlab issue tracker`_

.. _Issue 185: https://gitlab.idiap.ch/beat/beat.editor/issues/185
.. _Gitlab issue tracker: https://gitlab.idiap.ch/beat/beat.editor/issues/
