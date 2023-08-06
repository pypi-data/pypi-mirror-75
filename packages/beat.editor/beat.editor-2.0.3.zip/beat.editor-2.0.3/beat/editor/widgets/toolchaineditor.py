# vim: set fileencoding=utf-8 :
###############################################################################
#                                                                             #
# Copyright (c) 2019 Idiap Research Institute, http://www.idiap.ch/           #
# Contact: beat.support@idiap.ch                                              #
#                                                                             #
# This file is part of the beat.editor module of the BEAT platform.           #
#                                                                             #
# Commercial License Usage                                                    #
# Licensees holding valid commercial BEAT licenses may use this file in       #
# accordance with the terms contained in a written agreement between you      #
# and Idiap. For further information contact tto@idiap.ch                     #
#                                                                             #
# Alternatively, this file may be used under the terms of the GNU Affero      #
# Public License version 3 as published by the Free Software and appearing    #
# in the file LICENSE.AGPL included in the packaging of this file.            #
# The BEAT platform is distributed in the hope that it will be useful, but    #
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY  #
# or FITNESS FOR A PARTICULAR PURPOSE.                                        #
#                                                                             #
# You should have received a copy of the GNU Affero Public License along      #
# with the BEAT platform. If not, see http://www.gnu.org/licenses/.           #
#                                                                             #
###############################################################################

from enum import Enum
from functools import partial

import simplejson as json

from beat.backend.python.algorithm import Algorithm
from PyQt5.QtCore import QFile
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import QRect
from PyQt5.QtCore import QRectF
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPainterPath
from PyQt5.QtGui import QPen
from PyQt5.QtGui import QTransform
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtWidgets import QGraphicsPathItem
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from ..backend.asset import Asset
from ..backend.asset import AssetType
from ..backend.assetmodel import AssetModel
from ..backend.resourcemodels import AlgorithmResourceModel
from ..backend.resourcemodels import DatasetResourceModel
from ..backend.resourcemodels import experiment_resources
from ..decorators import frozen
from .editor import AbstractAssetEditor
from .toolchainscene import ToolchainScene
from .validatedhelpers import NameLineEdit


class BasePin(QGraphicsObject):
    """Base class for pin graphics"""

    dataChanged = pyqtSignal()

    def __init__(self, parent, pin, block, pin_brush, pin_pen):

        super().__init__(parent=parent)

        # Highlight
        self.setAcceptHoverEvents(True)

        # Storage
        self.pin_type = None
        self.pin = pin
        self.block = block
        self.brush = pin_brush
        self.pen = pin_pen
        self.block_object = parent

    def shape(self):
        """Define the circle shape of a Pin object"""

        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def paint(self, painter, option, widget):
        """Paint the Pin"""

        painter.setBrush(self.brush)
        painter.setPen(self.pen)

        painter.drawEllipse(self.boundingRect())

    def mousePressEvent(self, event):
        """Painting connection initiated"""

        self.new_connection = Connection(self.block_object.connection_style)
        self.block_object.scene().addItem(self.new_connection)

    def mouseMoveEvent(self, event):
        """Painting connection in progress"""

        # Only one single connection allowed from input pin
        if isinstance(self, InputPin):
            # Check if connection exist and remove if it does
            for connection in self.block_object.toolchain.connections:
                if (
                    connection.end_block == self.block_object
                    and connection.end_pin == self
                ):
                    self.block_object.toolchain.connections.remove(connection)
                    self.block_object.scene().removeItem(connection)
                    self.dataChanged.emit()

        mouse_position = self.mapToScene(event.pos())
        self.new_connection.set_new_connection_pins_coordinates(self, mouse_position)

    def mouseReleaseEvent(self, event):
        """Painting connection ended - validation required"""

        self.block_object.scene().removeItem(self.new_connection)
        target = self.block_object.scene().itemAt(
            event.scenePos().toPoint(), QTransform()
        )

        if isinstance(target, BasePin):

            if isinstance(self, OutputPin):
                start = self
                end = target
            else:
                start = target
                end = self

            if Connection(self.block_object.connection_style).check_validity(
                start, end
            ):

                # Find the corresponding channel
                connection_settings = {}
                if start.block_object.type == BlockType.DATASETS:
                    connection_settings["channel"] = start.block_object.name
                else:
                    connection_settings[
                        "channel"
                    ] = start.block_object.synchronized_channel

                if end.block_object.synchronized_channel is None:
                    end.block_object.synchronized_channel = connection_settings[
                        "channel"
                    ]
                # Create the connection
                connection_settings["from"] = start.block + "." + start.pin
                connection_settings["to"] = end.block + "." + end.pin

                channel_colors = self.block_object.toolchain.json_object[
                    "representation"
                ]["channel_colors"]

                connection = Connection(self.block_object.connection_style)
                connection.load(
                    self.block_object.toolchain, connection_settings, channel_colors
                )

                self.dataChanged.emit()

                self.block_object.toolchain.connections.append(connection)
                self.block_object.toolchain.scene.addItem(connection)

    def get_center_point(self):
        """Get the center coordinates of the Pin(x,y)"""

        rect = self.boundingRect()
        pin_center_point = QPointF(
            rect.x() + rect.width() / 2.0, rect.y() + rect.height() / 2.0
        )

        return self.mapToScene(pin_center_point)


class InputPin(BasePin):
    def __init__(self, parent, pin, block, pin_brush, pin_pen):

        super().__init__(parent, pin, block, pin_brush, pin_pen)

    def boundingRect(self):
        """Bounding rect around pin object"""

        height = self.block_object.height / 2.0
        width = height

        x = -(width / 2.0)

        if self.block_object.type == BlockType.LOOPS:
            _idx = None
            if self.pin in self.block_object.processor_inputs:
                _idx = self.block_object.processor_inputs.index(self.pin)
            elif self.pin in self.block_object.evaluator_inputs:
                _idx = self.block_object.evaluator_inputs.index(self.pin) + len(
                    self.block_object.processor_inputs
                )
            if _idx is not None:
                y = self.block_object.height + _idx * self.block_object.pin_height
            else:
                y = self.block_object.height
        else:
            y = (
                self.block_object.height
                + self.block_object.inputs.index(self.pin)
                * self.block_object.pin_height
            )

        rect = QRectF(QRect(x, y, width, height))
        return rect


class OutputPin(BasePin):
    def __init__(self, parent, pin, block, pin_brush, pin_pen):

        super().__init__(parent, pin, block, pin_brush, pin_pen)

    def boundingRect(self):
        """ bounding rect width by height.
        """

        height = self.block_object.height / 2.0
        width = height

        x = self.block_object.custom_width - (width / 2.0)
        if self.block_object.type == BlockType.LOOPS:
            _idx = None
            if self.pin in self.block_object.processor_outputs:
                _idx = self.block_object.processor_outputs.index(self.pin)
            elif self.pin in self.block_object.evaluator_outputs:
                _idx = self.block_object.evaluator_outputs.index(self.pin) + len(
                    self.block_object.processor_outputs
                )

            if _idx is not None:
                y = self.block_object.height + _idx * self.block_object.pin_height
            else:
                y = self.block_object.height
        else:
            y = (
                self.block_object.height
                + self.block_object.outputs.index(self.pin)
                * self.block_object.pin_height
            )

        rect = QRectF(QRect(x, y, width, height))
        return rect


class Connection(QGraphicsPathItem):
    def __init__(self, style):

        super().__init__()

        self.start_block_name = None
        self.start_pin_name = None
        self.start_pin_center_point = None
        self.end_block_name = None
        self.end_pin_name = None
        self.end_pin_center_point = None
        self.channel = None

        self.connection_color = []

        self.set_style(style)

    def itemChange(self, change, value):
        if change == self.ItemSelectedChange:
            if value:
                color = QColor("red")
            else:
                color = QColor(*self.connection_color)
            pen = self.pen()
            pen.setColor(color)
            self.setPen(pen)
        return QGraphicsItem.itemChange(self, change, value)

    def set_style(self, config):

        # Highlight
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

        # Geometry and color settings
        self.connection_color = config["color"]

        self.connection_pen = QPen()
        self.connection_pen.setColor(QColor(*self.connection_color))
        self.connection_pen.setWidth(config["width"])

    def drawCubicBezierCurve(self):

        self.setPen(self.connection_pen)

        path = QPainterPath()
        middle_point_x = (
            self.end_pin_center_point.x() - self.start_pin_center_point.x()
        ) / 2.0
        middle_point_y = (
            self.end_pin_center_point.y() - self.start_pin_center_point.y()
        ) / 2.0
        second_middle_point_y = (
            self.end_pin_center_point.y() - self.start_pin_center_point.y()
        ) / 4.0
        control_point = QPointF(middle_point_x, middle_point_y)
        second_control_point = QPointF(middle_point_x, second_middle_point_y)
        path.moveTo(self.start_pin_center_point)
        path.cubicTo(
            self.start_pin_center_point + control_point,
            self.end_pin_center_point - second_control_point,
            self.end_pin_center_point,
        )

        self.setPath(path)

    def set_moved_block_pins_coordinates(self):
        self.start_pin_center_point = self.start_pin.get_center_point()
        self.end_pin_center_point = self.end_pin.get_center_point()

        self.drawCubicBezierCurve()

    def set_new_connection_pins_coordinates(self, selected_pin, mouse_position):

        if isinstance(selected_pin, OutputPin):
            self.start_block_name = selected_pin.block
            self.start_pin_name = selected_pin.pin
            self.start_pin = selected_pin
            self.start_pin_center_point = self.start_pin.get_center_point()
            self.end_pin_center_point = mouse_position
        if isinstance(selected_pin, InputPin):
            self.end_block_name = selected_pin.block
            self.end_pin_name = selected_pin.pin
            self.end_pin = selected_pin
            self.end_pin_center_point = self.end_pin.get_center_point()
            self.start_pin_center_point = mouse_position

        self.drawCubicBezierCurve()

    def check_validity(self, start, end):

        # remove input-input and output-output connection
        if type(start) == type(end):
            return False

        # remove connection to same block object
        if start.block_object == end.block_object:
            return False

        # check if end block pin is free
        toolchain = end.block_object.toolchain
        for connection in toolchain.connections:
            if connection.end_block == end.block_object and connection.end_pin == end:
                return False

        return True

    def load(self, toolchain, connection_details, channel_colors):

        self.start_block_name = connection_details["from"].split(".")[0]
        self.start_pin_name = connection_details["from"].split(".")[1]
        self.end_block_name = connection_details["to"].split(".")[0]
        self.end_pin_name = connection_details["to"].split(".")[1]
        self.channel = connection_details["channel"]

        if self.channel is None:
            warning = QMessageBox()
            warning.setIcon(QMessageBox.Warning)
            warning.setWindowTitle(toolchain.tr("Connection creation"))
            warning.setInformativeText(
                toolchain.tr("No dataset synchronization channel connection found!")
            )
            warning.setStandardButtons(QMessageBox.Ok)
            warning.exec_()

        else:
            hexadecimal = "000000"

            if self.channel != "":
                if self.channel not in channel_colors:
                    toolchain.web_representation["channel_colors"][
                        self.channel
                    ] = "#000000"
                channel_colors = toolchain.web_representation["channel_colors"]
                hexadecimal = channel_colors[self.channel].lstrip("#")

            hlen = len(hexadecimal)
            self.connection_color = list(
                int(hexadecimal[i : i + hlen // 3], 16)
                for i in range(0, hlen, hlen // 3)
            )
            self.connection_color.append(255)
            self.connection_pen.setColor(QColor(*self.connection_color))

        self.blocks = toolchain.blocks

        for block in self.blocks:
            if block.name == self.start_block_name:
                self.start_block = block
            elif block.name == self.end_block_name:
                self.end_block = block

        if self.start_block.type == BlockType.LOOPS:
            if self.start_pin_name in self.start_block.pins["outputs"]["processor"]:
                self.start_pin = self.start_block.pins["outputs"]["processor"][
                    self.start_pin_name
                ]
            else:
                self.start_pin = self.start_block.pins["outputs"]["evaluator"][
                    self.start_pin_name
                ]
        else:
            self.start_pin = self.start_block.pins["outputs"][self.start_pin_name]

        if self.end_block.type == BlockType.LOOPS:
            if self.end_pin_name in self.end_block.pins["inputs"]["processor"]:
                self.end_pin = self.end_block.pins["inputs"]["processor"][
                    self.end_pin_name
                ]
            else:
                self.end_pin = self.end_block.pins["inputs"]["evaluator"][
                    self.end_pin_name
                ]
        else:
            self.end_pin = self.end_block.pins["inputs"][self.end_pin_name]

        self.start_pin_center_point = self.start_pin.get_center_point()
        self.end_pin_center_point = self.end_pin.get_center_point()

        self.drawCubicBezierCurve()

        self.start_block.blockMoved.connect(self.set_moved_block_pins_coordinates)
        self.end_block.blockMoved.connect(self.set_moved_block_pins_coordinates)


class LoopWidget(QDialog):
    """Class holder for the various libraries"""

    dataChanged = pyqtSignal()
    selectionChanged = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor"""

        super().__init__(parent)

        self.setMinimumHeight(200)

        # Layouts
        layout = QHBoxLayout(self)

        self.sequential_loop_processor_listwidget = QListWidget()
        self.autonomous_loop_processor_listwidget = QListWidget()
        self.sequential_loop_evaluator_listwidget = QListWidget()
        self.autonomous_loop_evaluator_listwidget = QListWidget()

        for listwidget, title in [
            (
                self.sequential_loop_processor_listwidget,
                self.tr("Sequential Loop Processor"),
            ),
            (
                self.autonomous_loop_processor_listwidget,
                self.tr("Autonomous Loop Processor"),
            ),
            (
                self.sequential_loop_evaluator_listwidget,
                self.tr("Sequential Loop Evaluator"),
            ),
            (
                self.autonomous_loop_evaluator_listwidget,
                self.tr("Autonomous Loop Evaluator"),
            ),
        ]:
            vbox_layout = QVBoxLayout()
            vbox_layout.addWidget(QLabel(title))
            vbox_layout.addWidget(listwidget)
            layout.addLayout(vbox_layout)

            self._setup_listwidget(listwidget, [])

            listwidget.itemSelectionChanged.connect(self.selectionChanged)

    def _setup_listwidget(self, listwidget, algorithms):
        listwidget.clear()
        if algorithms:
            listwidget.addItems(algorithms)
        else:
            invalid_item = QListWidgetItem(self.tr("No valid algorithm found"))
            invalid_item.setFlags(Qt.NoItemFlags)
            listwidget.addItem(invalid_item)

    def set_sequential_loop_processor_list(self, algorithms):
        self.sequential_loop_processor_list = algorithms
        self._setup_listwidget(self.sequential_loop_processor_listwidget, algorithms)

    def set_autonomous_loop_processor_list(self, algorithms):
        self.autonomous_loop_processor_list = algorithms
        self._setup_listwidget(self.autonomous_loop_processor_listwidget, algorithms)

    def set_sequential_loop_evaluator_list(self, algorithms):
        self.sequential_loop_evaluator_list = algorithms
        self._setup_listwidget(self.sequential_loop_evaluator_listwidget, algorithms)

    def set_autonomous_loop_evaluator_list(self, algorithms):
        self.sequential_loop_evaluator_list = algorithms
        self._setup_listwidget(self.autonomous_loop_evaluator_listwidget, algorithms)

    def get_processor_evaluator_loops(self):
        selected_loops = {}

        selected_sequential_loop_processor = (
            self.sequential_loop_processor_listwidget.selectedItems()
        )
        selected_autonomous_loop_processor = (
            self.autonomous_loop_processor_listwidget.selectedItems()
        )
        selected_sequential_loop_evaluator = (
            self.sequential_loop_evaluator_listwidget.selectedItems()
        )
        selected_autonomous_loop_evaluator = (
            self.autonomous_loop_evaluator_listwidget.selectedItems()
        )

        sequential_loop_processor = None
        if selected_sequential_loop_processor:
            sequential_loop_processor = selected_sequential_loop_processor[0].text()

        autonomous_loop_processor = None
        if selected_autonomous_loop_processor:
            autonomous_loop_processor = selected_autonomous_loop_processor[0].text()

        sequential_loop_evaluator = None
        if selected_sequential_loop_evaluator:
            sequential_loop_evaluator = selected_sequential_loop_evaluator[0].text()

        autonomous_loop_evaluator = None
        if selected_autonomous_loop_evaluator:
            autonomous_loop_evaluator = selected_autonomous_loop_evaluator[0].text()

        selected_loops["sequential_loop_processor"] = sequential_loop_processor
        selected_loops["autonomous_loop_processor"] = autonomous_loop_processor
        selected_loops["sequential_loop_evaluator"] = sequential_loop_evaluator
        selected_loops["autonomous_loop_evaluator"] = autonomous_loop_evaluator

        return selected_loops


class LoopDialog(QDialog):
    """Dialog to edit a block"""

    def __init__(self, toolchain, parent=None):
        """Constructor

        :param block: current block
        :param parent QWidget: parent widget
        """

        super().__init__(parent)
        self.setWindowTitle(self.tr("Add Loop"))

        layout = QVBoxLayout(self)

        # Layouts Widget
        self.loop_widget = LoopWidget()
        layout.addWidget(self.loop_widget)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        )
        self.buttons.button(QDialogButtonBox.Ok).setEnabled(False)
        layout.addWidget(self.buttons)

        # Signals/Slots connection
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.loop_widget.selectionChanged.connect(self.__updateUi)

    @pyqtSlot()
    def __updateUi(self):
        loops_dict = self.value()
        self.buttons.button(QDialogButtonBox.Ok).setEnabled(all(loops_dict.values()))

    def value(self):
        """Returns the value selected"""

        return self.loop_widget.get_processor_evaluator_loops()

    def set_lists(
        self,
        sequential_loop_processor_list,
        autonomous_loop_processor_list,
        sequential_loop_evaluator_list,
        autonomous_loop_evaluator_list,
    ):

        self.loop_widget.set_sequential_loop_processor_list(
            sequential_loop_processor_list
        )
        self.loop_widget.set_autonomous_loop_processor_list(
            autonomous_loop_processor_list
        )
        self.loop_widget.set_sequential_loop_evaluator_list(
            sequential_loop_evaluator_list
        )
        self.loop_widget.set_autonomous_loop_evaluator_list(
            autonomous_loop_evaluator_list
        )

    @staticmethod
    def getLoops(
        toolchain,
        sequential_loop_processor_list,
        autonomous_loop_processor_list,
        sequential_loop_evaluator_list,
        autonomous_loop_evaluator_list,
        parent=None,
    ):
        """Static method to create the dialog and return qdialog accepted/spinbox value

        :param block: current block
        :param parent QWidget: parent widget
        """

        dialog = LoopDialog(toolchain, parent)
        dialog.set_lists(
            sequential_loop_processor_list,
            autonomous_loop_processor_list,
            sequential_loop_evaluator_list,
            autonomous_loop_evaluator_list,
        )
        result = dialog.exec_()
        value = None

        if result == QDialog.Accepted:
            value = dialog.value()

        return (value, result)


class BlockEditionDialog(QDialog):
    """Dialog to edit a block"""

    def __init__(self, block, parent=None):
        """Constructor

        :param block: current block
        :param parent QWidget: parent widget
        """

        super().__init__(parent)

        toolchain = block.toolchain
        self.setWindowTitle(self.tr("Block Edition"))
        self.name_lineedit = NameLineEdit(block.name)
        self.color = "#000000"
        self.channel_combobox = QComboBox()
        no_channel_label = QLabel(self.tr("No input connections yet!"))
        no_dataset_channel_label = QLabel(self.tr("No synchronization for datasets"))

        layout = QFormLayout(self)
        layout.addRow(self.tr("Name:"), self.name_lineedit)

        channels = []

        if block.type == BlockType.DATASETS:
            channel_color_button = QPushButton("Channel color", self)
            channel_color_button.setToolTip("Opens color dialog")
            channel_color_button.clicked.connect(self.on_color_click)
            layout.addRow(self.tr("Channel:"), no_dataset_channel_label)
            layout.addRow(self.tr("Channel color:"), channel_color_button)
        elif block.synchronized_channel is None:
            layout.addRow(self.tr("Channel:"), no_channel_label)
        else:
            for connection in toolchain.connections:
                if connection.end_block == block and connection.channel not in channels:
                    channels.append(connection.channel)
            self.channel_combobox.addItems(channels)
            # set current channel if exists
            index = self.channel_combobox.findText(
                str(block.synchronized_channel), Qt.MatchFixedString
            )
            if index >= 0:
                self.channel_combobox.setCurrentIndex(index)

            layout.addRow(self.tr("Channel:"), self.channel_combobox)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        )
        # layout.addWidget(self.buttons)
        layout.addRow(self.buttons)

        # Signals/Slots connection
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    @pyqtSlot()
    def on_color_click(self):
        self.colorDialog()

    def colorDialog(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.color = color.name().capitalize()

    def value(self):
        """Returns the value selected"""

        return {
            "name": self.name_lineedit.text(),
            "channel": self.channel_combobox.currentText(),
            "color": self.color,
        }

    @staticmethod
    def getNewBlockSettings(block, parent=None):
        """Static method to create the dialog and return qdialog accepted/spinbox value

        :param block: current block
        :param parent QWidget: parent widget
        """

        dialog = BlockEditionDialog(block, parent)
        result = dialog.exec_()
        value = None

        if result == QDialog.Accepted:
            value = dialog.value()

        return (value, result)


class BlockType(Enum):
    """All possible block types"""

    BLOCKS = "blocks"
    ANALYZERS = "analyzers"
    DATASETS = "datasets"
    LOOPS = "loops"

    @classmethod
    def from_name(cls, name):
        try:
            return cls[name.upper()]
        except KeyError:
            raise KeyError("{} is not a valid block type".format(name))


BLOCKTYPE_PROPERTY = "__block_type__"


class Block(QGraphicsObject):
    """Block item"""

    dataChanged = pyqtSignal()
    blockMoved = pyqtSignal()

    def __init__(self, block_type, style, connection_style):
        super().__init__()

        # Block information
        self.type = block_type
        self.name = ""

        if self.type == BlockType.LOOPS:
            self.processor_inputs = []
            self.processor_outputs = []
            self.evaluator_inputs = []
            self.evaluator_outputs = []
        else:
            if self.type == BlockType.DATASETS:
                self.inputs = None
            else:
                self.inputs = []

            if self.type == BlockType.ANALYZERS:
                self.outputs = None
            else:
                self.outputs = []

        self.synchronized_channel = None

        self.style = style
        self.connection_style = connection_style

        self.position = QPointF(0, 0)
        self.pins = dict()
        self.pins["inputs"] = dict()
        self.pins["outputs"] = dict()

        if self.type == BlockType.LOOPS:
            self.pins["inputs"]["processor"] = dict()
            self.pins["outputs"]["processor"] = dict()
            self.pins["inputs"]["evaluator"] = dict()
            self.pins["outputs"]["evaluator"] = dict()

        self.set_style(style)

    def load(self, toolchain, block_details):
        self.toolchain = toolchain

        if "name" in block_details:
            self.name = block_details["name"]

        if self.type == BlockType.LOOPS:
            self.processor_inputs = block_details["processor_inputs"]
            self.processor_outputs = block_details["processor_outputs"]
            self.evaluator_inputs = block_details["evaluator_inputs"]
            self.evaluator_outputs = block_details["evaluator_outputs"]
        else:
            if self.type != BlockType.DATASETS and self.type != BlockType.LOOPS:
                self.inputs = block_details["inputs"]

            if self.type != BlockType.ANALYZERS and self.type != BlockType.LOOPS:
                self.outputs = block_details["outputs"]

        if "synchronized_channel" in block_details:
            self.synchronized_channel = block_details["synchronized_channel"]

        self.set_style(self.style)
        self.create_pins()

    def create_pins(self):

        if self.type == BlockType.LOOPS:
            for pin_name in self.processor_inputs:
                input_pin = InputPin(
                    self, pin_name, self.name, self.pin_brush, self.pin_pen
                )
                self.pins["inputs"]["processor"][pin_name] = input_pin

                input_pin.dataChanged.connect(self.dataChanged)

            for pin_name in self.processor_outputs:
                output_pin = OutputPin(
                    self, pin_name, self.name, self.pin_brush, self.pin_pen
                )
                self.pins["outputs"]["processor"][pin_name] = output_pin

                output_pin.dataChanged.connect(self.dataChanged)

            for pin_name in self.evaluator_inputs:
                input_pin = InputPin(
                    self, pin_name, self.name, self.pin_brush, self.pin_pen
                )
                self.pins["inputs"]["evaluator"][pin_name] = input_pin

                input_pin.dataChanged.connect(self.dataChanged)

            for pin_name in self.evaluator_outputs:
                output_pin = OutputPin(
                    self, pin_name, self.name, self.pin_brush, self.pin_pen
                )
                self.pins["outputs"]["evaluator"][pin_name] = output_pin

                output_pin.dataChanged.connect(self.dataChanged)
        else:
            if self.inputs is not None:
                for pin_name in self.inputs:
                    input_pin = InputPin(
                        self, pin_name, self.name, self.pin_brush, self.pin_pen
                    )
                    self.pins["inputs"][pin_name] = input_pin

                    input_pin.dataChanged.connect(self.dataChanged)

            if self.outputs is not None:
                for pin_name in self.outputs:
                    output_pin = OutputPin(
                        self, pin_name, self.name, self.pin_brush, self.pin_pen
                    )
                    self.pins["outputs"][pin_name] = output_pin

                    output_pin.dataChanged.connect(self.dataChanged)

    def set_style(self, config):

        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable)

        # Geometry settings
        self.width = config["width"]
        self.height = config["height"]
        self.border = config["border"]
        self.radius = config["radius"]
        self.pin_height = config["pin_height"]

        self.text_font = QFont(config["font"], config["font_size"], QFont.Bold)
        self.pin_font = QFont(config["pin_font"], config["pin_font_size"], QFont.Normal)

        metrics = QFontMetrics(self.text_font)
        text_width = metrics.boundingRect(self.name).width() + 24

        if self.type == BlockType.LOOPS:
            if len(self.processor_inputs) > 0:
                self.max_processor_inputs_width = (
                    metrics.boundingRect(max(self.processor_inputs, key=len)).width()
                    + 24
                )
            else:
                self.max_processor_inputs_width = 24

            if len(self.evaluator_inputs) > 0:
                self.max_evaluator_inputs_width = (
                    metrics.boundingRect(max(self.evaluator_inputs, key=len)).width()
                    + 24
                )
            else:
                self.max_evaluator_inputs_width = 24

            self.max_inputs_width = max(
                self.max_processor_inputs_width, self.max_evaluator_inputs_width
            )

            if len(self.processor_outputs) > 0:
                self.max_processor_outputs_width = (
                    metrics.boundingRect(max(self.processor_outputs, key=len)).width()
                    + 24
                )
            else:
                self.max_processor_outputs_width = 24

            if len(self.evaluator_outputs) > 0:
                self.max_evaluator_outputs_width = (
                    metrics.boundingRect(max(self.evaluator_outputs, key=len)).width()
                    + 24
                )
            else:
                self.max_evaluator_outputs_width = 24

            self.max_outputs_width = max(
                self.max_processor_outputs_width, self.max_evaluator_outputs_width
            )
        else:
            if self.inputs is not None and len(self.inputs) > 0:
                self.max_inputs_width = (
                    metrics.boundingRect(max(self.inputs, key=len)).width() + 24
                )
            else:
                self.max_inputs_width = 24

            if self.outputs is not None and len(self.outputs) > 0:
                self.max_outputs_width = (
                    metrics.boundingRect(max(self.outputs, key=len)).width() + 24
                )
            else:
                self.max_outputs_width = 24

        self.custom_width = max(
            self.max_outputs_width + self.max_inputs_width, text_width
        )

        self.custom_height = self.height

        self.center = QPointF()
        self.center.setX(self.custom_width / 2.0)
        self.center.setY(self.height / 2.0)

        self.background_brush = QBrush()
        self.background_brush.setStyle(Qt.SolidPattern)

        self.background_color_datasets = QColor(*config["background_color_datasets"])
        self.background_color_analyzers = QColor(*config["background_color_analyzers"])
        self.background_color_blocks = QColor(*config["background_color_blocks"])
        self.background_color_loops = QColor(*config["background_color_loops"])

        self.background_brush.setColor(self.background_color_blocks)

        self.background_pen = QPen()
        self.background_pen.setStyle(Qt.SolidLine)
        self.background_pen.setWidth(0)
        self.background_pen.setColor(QColor(*config["background_color"]))

        self.border_pen = QPen()
        self.border_pen.setStyle(Qt.SolidLine)
        self.border_pen.setWidth(self.border)
        self.border_pen.setColor(QColor(*config["border_color"]))

        self.selection_border_pen = QPen()
        self.selection_border_pen.setStyle(Qt.SolidLine)
        self.selection_border_pen.setWidth(self.border)
        self.selection_border_pen.setColor(QColor(*config["selection_border_color"]))

        self.text_pen = QPen()
        self.text_pen.setStyle(Qt.SolidLine)
        self.text_pen.setColor(QColor(*config["text_color"]))

        self._pin_brush = QBrush()
        self._pin_brush.setStyle(Qt.SolidPattern)

        self.pin_pen = QPen()
        self.pin_pen.setStyle(Qt.SolidLine)

        self.pin_brush = QBrush()
        self.pin_brush.setStyle(Qt.SolidPattern)
        self.pin_brush.setColor(QColor(*config["pin_color"]))

    def boundingRect(self):
        """Bounding rect of the block object width by height"""
        metrics = QFontMetrics(self.text_font)
        text_height = metrics.boundingRect(self.name).height() + 24

        if self.type == BlockType.LOOPS:
            max_pin_height = max(
                len(self.processor_inputs) + len(self.evaluator_inputs),
                len(self.processor_outputs) + len(self.evaluator_outputs),
            )
        else:
            if self.inputs is not None and self.outputs is not None:
                max_pin_height = max(len(self.inputs), len(self.outputs))
            elif self.inputs is not None and self.outputs is None:
                max_pin_height = len(self.inputs)
            elif self.inputs is None and self.outputs is not None:
                max_pin_height = len(self.outputs)
            else:
                max_pin_height = 0

        if max_pin_height == 0:
            self.custom_width = 55
            self.height = 55

        self.custom_height = (
            text_height + self.height + max_pin_height * self.pin_height
        )
        rect = QRect(0, -text_height, self.custom_width, self.custom_height)
        rect = QRectF(rect)
        return rect

    def draw_pins_name(self, painter, _type, data, offset):
        """Paint pin with name"""
        offset = offset * self.pin_height
        if offset != 0:
            # add processor/evaluator separator line
            painter.setPen(self.pin_pen)
            separator_height = self.height - self.radius + offset
            painter.drawLine(
                self.border, separator_height, self.custom_width, separator_height
            )
        for pin_name in data:
            # Pin rect
            painter.setBrush(self.background_brush)
            painter.setPen(self.background_pen)
            painter.setFont(self.pin_font)

            coord_x = self.border / 2
            alignement = Qt.AlignLeft

            max_width = self.max_inputs_width
            if _type == "output":
                coord_x = self.custom_width - self.max_outputs_width - self.border / 2
                max_width = self.max_outputs_width
                alignement = Qt.AlignRight

            rect = QRect(
                coord_x, self.height - self.radius + offset, max_width, self.pin_height
            )

            textRect = QRect(
                rect.left() + self.radius,
                rect.top() + self.radius,
                rect.width() - 2 * self.radius,
                rect.height(),
            )

            painter.setPen(self.pin_pen)
            painter.drawText(textRect, alignement, pin_name)

            offset += self.pin_height

    def mouseMoveEvent(self, event):
        """Update connections due to new block position"""

        super(Block, self).mouseMoveEvent(event)

        self.position = self.scenePos()

        self.blockMoved.emit()
        self.dataChanged.emit()

    def mouseDoubleClickEvent(self, event):
        """Update block information"""
        value = None
        ok = False
        block_updated = False

        value, ok = BlockEditionDialog.getNewBlockSettings(self)

        old_name = self.name
        old_channel = self.synchronized_channel

        if ok:
            if self.name != value["name"]:
                old_name = self.name
                self.name = value["name"]
                if self.type == BlockType.DATASETS:
                    self.toolchain.web_representation["channel_colors"][
                        self.name
                    ] = self.toolchain.web_representation["channel_colors"].pop(
                        old_name
                    )

                block_updated = True
            if (
                self.synchronized_channel != value["channel"]
                and self.type != BlockType.DATASETS
            ):
                self.synchronized_channel = value["channel"]
                block_updated = True
            if self.type == BlockType.DATASETS:
                self.toolchain.web_representation["channel_colors"][self.name] = value[
                    "color"
                ]
                block_updated = True

        if block_updated:
            block_item = {}
            if self.type == BlockType.LOOPS:
                block_item["processor_inputs"] = self.processor_inputs
                block_item["processor_outputs"] = self.processor_outputs
                block_item["evaluator_inputs"] = self.evaluator_inputs
                block_item["evaluator_outputs"] = self.evaluator_outputs
            # Update blocks
            else:
                block_item["inputs"] = self.inputs
                block_item["outputs"] = self.outputs
            block_item["name"] = self.name
            block_item["synchronized_channel"] = self.synchronized_channel

            self.toolchain.blocks.remove(self)
            self.scene().removeItem(self)

            self.load(self.toolchain, block_item)
            self.dataChanged.connect(self.toolchain.dataChanged)
            self.toolchain.blocks.append(self)
            self.toolchain.scene.addItem(self)

            # if type is dataset: update sync channels everywhere
            if self.type == BlockType.DATASETS:
                for block in self.toolchain.blocks:
                    if (
                        block.type != BlockType.DATASETS
                        and block.synchronized_channel == old_name
                    ):
                        block.synchronized_channel = self.name

            # Update connections
            for connection in self.toolchain.connections:
                # Name update
                if connection.start_block_name == old_name:
                    connection.start_block_name = self.name
                if connection.end_block_name == old_name:
                    connection.end_block_name = self.name
                if connection.channel == old_name:
                    connection.channel = self.name

                # color update
                self.toolchain.scene.removeItem(connection)

                # Find the corresponding channel
                connection_settings = {}
                connection_settings["channel"] = connection.channel
                # Create the connection
                connection_settings["from"] = (
                    connection.start_block_name + "." + connection.start_pin_name
                )
                connection_settings["to"] = (
                    connection.end_block_name + "." + connection.end_pin_name
                )

                channel_colors = self.toolchain.json_object.get(
                    "representation", {}
                ).get("channel_colors")
                connection.load(self.toolchain, connection_settings, channel_colors)

                self.toolchain.scene.addItem(connection)

            # Complete toolchain channel update from current block
            if old_channel != self.synchronized_channel:
                self.toolchain.update_channel_path(
                    self, old_channel, self.synchronized_channel
                )

            # Update representation
            web_representation = self.toolchain.web_representation
            for key, value in web_representation.items():
                for sub_key, sub_value in web_representation[key].items():
                    if sub_key == old_name:
                        # blocks and channel_colors
                        new_sub_key = sub_key.replace(old_name, self.name)
                        web_representation[key][new_sub_key] = web_representation[
                            key
                        ].pop(sub_key)
                    elif "/" in sub_key:
                        # connections
                        new_sub_key = sub_key
                        left_part = sub_key.split("/")[0]
                        right_part = sub_key.split("/")[1]

                        if left_part.split(".")[0] == old_name:
                            new_sub_key = (
                                self.name
                                + "."
                                + left_part.split(".")[1]
                                + "/"
                                + right_part
                            )
                        if right_part.split(".")[0] == old_name:
                            new_sub_key = (
                                left_part
                                + "/"
                                + self.name
                                + "."
                                + right_part.split(".")[1]
                            )
                        if new_sub_key != sub_key:
                            web_representation[key][new_sub_key] = web_representation[
                                key
                            ].pop(sub_key)

            self.dataChanged.emit()

    def paint(self, painter, option, widget):
        """Paint the block"""

        # Design tools
        if self.type == BlockType.DATASETS:
            self.background_brush.setColor(self.background_color_datasets)
        elif self.type == BlockType.ANALYZERS:
            self.background_brush.setColor(self.background_color_analyzers)
        elif self.type == BlockType.LOOPS:
            self.background_brush.setColor(self.background_color_loops)

        painter.setBrush(self.background_brush)
        painter.setPen(self.border_pen)

        if self.type == BlockType.LOOPS:
            max_pin_height = max(
                len(self.processor_inputs) + len(self.evaluator_inputs),
                len(self.processor_outputs) + len(self.evaluator_outputs),
            )
        else:
            if self.inputs is not None and self.outputs is not None:
                max_pin_height = max(len(self.inputs), len(self.outputs))
            elif self.inputs is not None and self.outputs is None:
                max_pin_height = len(self.inputs)
            elif self.inputs is None and self.outputs is not None:
                max_pin_height = len(self.outputs)
            else:
                max_pin_height = 0

        if self.isSelected():
            self.selection_border_pen.setWidth(3)
            painter.setPen(self.selection_border_pen)
        else:
            self.border_pen.setWidth(0)
            painter.setPen(self.border_pen)

        if max_pin_height == 0:
            self.custom_width = 55
            self.height = 55

        painter.drawRoundedRect(
            0,
            0,
            self.custom_width,
            self.height + max_pin_height * self.pin_height,
            self.radius,
            self.radius,
        )

        # Block name
        painter.setPen(self.text_pen)
        painter.setFont(self.text_font)

        metrics = QFontMetrics(painter.font())
        text_width = metrics.boundingRect(self.name).width() + 24
        text_height = metrics.boundingRect(self.name).height() + 24
        margin = (text_width - self.custom_width) * 0.5
        text_rect = QRect(-margin, -text_height, text_width, text_height)

        painter.drawText(text_rect, Qt.AlignCenter, self.name)

        # Pin
        if self.type == BlockType.LOOPS:
            self.draw_pins_name(painter, "input", self.processor_inputs, 0)
            self.draw_pins_name(
                painter, "input", self.evaluator_inputs, len(self.processor_inputs)
            )
            self.draw_pins_name(painter, "output", self.processor_outputs, 0)
            self.draw_pins_name(
                painter, "output", self.evaluator_outputs, len(self.processor_outputs)
            )
        else:
            if self.inputs is not None:
                self.draw_pins_name(painter, "input", self.inputs, 0)
            if self.outputs is not None:
                self.draw_pins_name(painter, "output", self.outputs, 0)


class ToolchainView(QGraphicsView):
    def __init__(self, toolchain):
        super().__init__()

        self.toolchain = toolchain

    def wheelEvent(self, event):
        """In/Out zoom view using the mouse wheel"""

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        factor = (event.angleDelta().y() / 120) * 0.1
        self.scale(1 + factor, 1 + factor)

    def keyPressEvent(self, event):
        """Focus on the toolchain when F key pressed"""
        if event.key() == Qt.Key_F:
            self.custom_focus()
        if event.key() == Qt.Key_Backspace or event.key() == Qt.Key_Delete:
            self.delete_blocks()

    def custom_focus(self):
        """Custom focus on toolchain"""

        selected_blocks = self.scene().selectedItems()
        if selected_blocks:
            x_list = []
            y_list = []
            width_list = []
            height_list = []
            for block in selected_blocks:
                x_list.append(block.scenePos().x())
                y_list.append(block.scenePos().y())
                width_list.append(block.boundingRect().width())
                height_list.append(block.boundingRect().height())
                min_x = min(x_list)
                min_y = min(y_list) + block.boundingRect().y()
                max_width = max(x_list) + max(width_list) - min_x
                max_height = max(y_list) + max(height_list) - min_y
            rect = QRectF(QRect(min_x, min_y, max_width, max_height))
            toolchain_focus = rect
        else:
            toolchain_focus = self.scene().itemsBoundingRect()

        self.fitInView(toolchain_focus, Qt.KeepAspectRatio)

    def delete_blocks(self):
        """Custom deletion on toolchain"""

        selected_items = self.scene().selectedItems()
        if selected_items:
            for item in selected_items:
                if isinstance(item, Connection):
                    self.toolchain.connections.remove(item)
                    self.scene().removeItem(item)
                    self.toolchain.dataChanged.emit()
                elif isinstance(item, Block):
                    num_connections = 0
                    for connection in self.toolchain.connections:
                        if (
                            item.name == connection.start_block_name
                            or item.name == connection.end_block_name
                        ):
                            num_connections += 1
                    if num_connections > 0:
                        warning = QMessageBox()
                        warning.setIcon(QMessageBox.Warning)
                        warning.setWindowTitle(self.tr("Deleting connected block"))
                        warning.setInformativeText(
                            self.tr("You can't delete a connected block!")
                        )
                        warning.setStandardButtons(QMessageBox.Ok)
                        warning.exec_()
                    else:
                        if item.type == BlockType.DATASETS:
                            if (
                                item.name
                                in self.toolchain.web_representation["channel_colors"]
                            ):
                                self.toolchain.web_representation["channel_colors"].pop(
                                    item.name
                                )
                        self.toolchain.web_representation["blocks"].pop(item.name)

                        self.toolchain.blocks.remove(item)
                        self.scene().removeItem(item)
                        self.toolchain.dataChanged.emit()


class ToolchainWidget(QWidget):
    """Toolchain designer"""

    dataChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.json_object = {}

        self.sequential_loop_processor_list = []
        self.autonomous_loop_processor_list = []
        self.sequential_loop_evaluator_list = []
        self.autonomous_loop_evaluator_list = []

        config_data = {}
        file_ = QFile(":/resources/toolchain_style_config")
        if file_.open(QFile.ReadOnly | QFile.Text):
            config_data = json.loads(file_.readAll().data().decode("utf-8"))

        scene_config = config_data["toolchainscene_config"]
        self.scene = ToolchainScene(scene_config)

        self.block_config = config_data["block_config"]
        self.connection_config = config_data["connection_config"]

        self.view = ToolchainView(self)
        self.view.setScene(self.scene)

        self.toolbar = QToolBar()

        self.loop_button = QPushButton()
        self.loop_button.setToolTip("Loop")
        self.loop_button.setIcon(QIcon(":/resources/loop"))
        self.loop_button.clicked.connect(self.add_loop_block)

        self.dataset_button = QPushButton()
        self.dataset_button.setToolTip("Dataset")
        self.dataset_button.setIcon(QIcon(":/resources/dataset"))
        self.dataset_edit_menu = QMenu(self)
        self.dataset_edit_menu.setProperty(BLOCKTYPE_PROPERTY, BlockType.DATASETS)

        self.block_button = QPushButton()
        self.block_button.setToolTip("Block")
        self.block_button.setIcon(QIcon(":/resources/block"))
        self.block_edit_menu = QMenu(self)
        self.block_edit_menu.setProperty(BLOCKTYPE_PROPERTY, BlockType.BLOCKS)

        self.analyzer_button = QPushButton()
        self.analyzer_button.setToolTip("Analyzer")
        self.analyzer_button.setIcon(QIcon(":/resources/analyzer"))
        self.analyzer_edit_menu = QMenu(self)
        self.analyzer_edit_menu.setProperty(BLOCKTYPE_PROPERTY, BlockType.ANALYZERS)

        self.toolbar.addWidget(self.dataset_button)
        self.toolbar.addWidget(self.block_button)
        self.toolbar.addWidget(self.analyzer_button)
        self.toolbar.addWidget(self.loop_button)

        self.toolbar.setOrientation(Qt.Vertical)

        layout = QHBoxLayout(self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.view)

        for menu in [
            self.dataset_edit_menu,
            self.block_edit_menu,
            self.analyzer_edit_menu,
        ]:
            self.__setup_menu(menu, [])

    def __setup_menu(self, menu, item_list):
        menu.clear()
        block_type = menu.property(BLOCKTYPE_PROPERTY)
        if item_list:
            for item in item_list:
                menu.addAction(
                    item, partial(self.button_item_selected, block_type, item)
                )
        else:
            action = menu.addAction(
                self.tr("No valid {} found".format(block_type.name.lower()))
            )
            action.setEnabled(False)

    def add_loop_block(self):
        loops, ok = LoopDialog.getLoops(
            self,
            self.sequential_loop_processor_list,
            self.autonomous_loop_processor_list,
            self.sequential_loop_evaluator_list,
            self.autonomous_loop_evaluator_list,
        )

        if ok:
            sequential_loop_processor = loops["sequential_loop_processor"]
            autonomous_loop_processor = loops["autonomous_loop_processor"]
            sequential_loop_evaluator = loops["sequential_loop_evaluator"]
            autonomous_loop_evaluator = loops["autonomous_loop_evaluator"]

            if sequential_loop_processor is None and autonomous_loop_processor is None:
                raise ValueError("No processor selected!")
            elif (
                sequential_loop_evaluator is None and autonomous_loop_evaluator is None
            ):
                raise ValueError("No evaluator selected!")
            elif (
                sequential_loop_processor is not None
                and autonomous_loop_processor is not None
            ):
                raise ValueError("Two processors selected!")
            elif (
                sequential_loop_evaluator is not None
                and autonomous_loop_evaluator is not None
            ):
                raise ValueError("Two evaluators selected!")
            else:
                processor_asset = None
                evaluator_asset = None

                processor_inputs = []
                processor_outputs = []
                evaluator_inputs = []
                evaluator_outputs = []

                if sequential_loop_processor is not None:
                    processor_asset = Asset(
                        self.prefix_path, AssetType.ALGORITHM, sequential_loop_processor
                    )
                else:
                    processor_asset = Asset(
                        self.prefix_path, AssetType.ALGORITHM, autonomous_loop_processor
                    )

                if sequential_loop_evaluator is not None:
                    evaluator_asset = Asset(
                        self.prefix_path, AssetType.ALGORITHM, sequential_loop_evaluator
                    )
                else:
                    evaluator_asset = Asset(
                        self.prefix_path, AssetType.ALGORITHM, autonomous_loop_evaluator
                    )

                processor_declaration = processor_asset.declaration
                evaluator_declaration = evaluator_asset.declaration

                block_item = {}
                for group in processor_declaration["groups"]:
                    if "inputs" in group:
                        for key in group["inputs"].keys():
                            processor_inputs.append(key)
                        block_item["processor_inputs"] = processor_inputs
                    if "outputs" in group:
                        for key in group["outputs"].keys():
                            processor_outputs.append(key)
                        block_item["processor_outputs"] = processor_outputs

                for group in evaluator_declaration["groups"]:
                    if "inputs" in group:
                        for key in group["inputs"].keys():
                            evaluator_inputs.append(key)
                        block_item["evaluator_inputs"] = evaluator_inputs
                    if "outputs" in group:
                        for key in group["outputs"].keys():
                            evaluator_outputs.append(key)
                        block_item["evaluator_outputs"] = evaluator_outputs

                init_name_count = 0
                init_name = self.tr("CHANGE_ME")
                for block in self.blocks:
                    if block.name.find(init_name) > -1:
                        init_name_count += 1
                new_block_name = init_name + "_" + str(init_name_count)
                block_item["name"] = new_block_name

                block = Block(
                    BlockType.LOOPS, self.block_config, self.connection_config
                )
                block.load(self, block_item)

                block.dataChanged.connect(self.dataChanged)
                block.dataChanged.emit()
                self.blocks.append(block)
                self.scene.addItem(block)

    def update_channel_path(self, block, old_channel, new_channel):
        # check if current block is synchronized on old_channel
        for connection in self.connections:
            if (
                block.name == connection.start_block_name
                and connection.channel == old_channel
            ):
                # update connection channel
                connection.channel = new_channel

                self.scene.removeItem(connection)

                # Find the corresponding channel
                connection_settings = {}
                connection_settings["channel"] = connection.channel
                # Create the connection
                connection_settings["from"] = (
                    connection.start_block_name + "." + connection.start_pin_name
                )
                connection_settings["to"] = (
                    connection.end_block_name + "." + connection.end_pin_name
                )

                channel_colors = self.json_object.get("representation", {}).get(
                    "channel_colors"
                )
                connection.load(self, connection_settings, channel_colors)
                self.scene.addItem(connection)

    def button_item_selected(self, block_type, name):
        inputs = []
        outputs = []

        if block_type == BlockType.DATASETS:
            inputs = None
            name_split = name.split("/")
            database_name = name_split[0] + "/" + name_split[1]
            asset = Asset(self.prefix_path, AssetType.DATABASE, database_name)
            for protocol in asset.declaration["protocols"]:
                if protocol["name"] == name_split[2]:
                    if "sets" in protocol:
                        for _set in protocol["sets"]:
                            if _set["name"] == name_split[3]:
                                for key in _set["outputs"].keys():
                                    outputs.append(key)
                    else:
                        protocol_name = protocol["template"]
                        sub_asset = Asset(
                            self.prefix_path, AssetType.PROTOCOLTEMPLATE, protocol_name
                        )
                        for _set in sub_asset.declaration["sets"]:
                            if _set["name"] == name_split[3]:
                                for key in _set["outputs"].keys():
                                    outputs.append(key)

        else:
            if block_type == BlockType.ANALYZERS:
                outputs = None
            asset = Asset(self.prefix_path, AssetType.ALGORITHM, name)
            declaration = asset.declaration
            for group in declaration["groups"]:
                if "inputs" in group:
                    for key in group["inputs"].keys():
                        inputs.append(key)
                if "outputs" in group:
                    for key in group["outputs"].keys():
                        outputs.append(key)

        block_item = {}
        block_item["inputs"] = inputs
        block_item["outputs"] = outputs
        init_name_count = 0
        init_name = self.tr("CHANGE_ME")
        for block in self.blocks:
            if block.name.find(init_name) > -1:
                init_name_count += 1
        new_block_name = init_name + "_" + str(init_name_count)
        block_item["name"] = new_block_name

        if block_type == BlockType.DATASETS:
            self.web_representation["channel_colors"][new_block_name] = "#000000"

        block = Block(block_type, self.block_config, self.connection_config)
        block.load(self, block_item)

        block.dataChanged.connect(self.dataChanged)
        block.dataChanged.emit()
        self.blocks.append(block)
        self.scene.addItem(block)

    def set_prefix_databases_algorithms_lists(
        self,
        prefix_path,
        dataset_list,
        algorithm_list,
        sequential_loop_processor_list,
        autonomous_loop_processor_list,
        sequential_loop_evaluator_list,
        autonomous_loop_evaluator_list,
        analyzer_list,
    ):
        self.prefix_path = prefix_path

        for menu, item_list in [
            (self.dataset_edit_menu, dataset_list),
            (self.block_edit_menu, algorithm_list),
            (self.analyzer_edit_menu, analyzer_list),
        ]:
            self.__setup_menu(menu, item_list)

        self.dataset_button.setMenu(self.dataset_edit_menu)
        self.block_button.setMenu(self.block_edit_menu)
        self.analyzer_button.setMenu(self.analyzer_edit_menu)

        self.sequential_loop_processor_list = sequential_loop_processor_list
        self.autonomous_loop_processor_list = autonomous_loop_processor_list
        self.sequential_loop_evaluator_list = sequential_loop_evaluator_list
        self.autonomous_loop_evaluator_list = autonomous_loop_evaluator_list

    def clear_space(self):
        self.scene.clear()
        self.scene.items().clear()
        self.blocks = []
        self.connections = []
        self.channels = []

    def load(self, json_object):
        """Parse the json in parameter and generates a graph"""

        self.json_object = json_object

        self.web_representation = self.json_object.get("representation")

        self.clear_space()

        # Get datasets, blocks, analyzers, loops
        for block_type in BlockType:
            for block_item in self.json_object.get(block_type.value, {}):
                block = Block(block_type, self.block_config, self.connection_config)
                block.load(self, block_item)
                # Place blocks (x,y) if information is given
                if self.web_representation["blocks"] is not None:
                    # if block.name in self.web_representation:
                    if block.name in self.web_representation["blocks"]:
                        block.setPos(
                            self.web_representation["blocks"][block.name]["col"],
                            self.web_representation["blocks"][block.name]["row"],
                        )
                        block.position = block.scenePos()
                block.dataChanged.connect(self.dataChanged)
                self.blocks.append(block)
                self.scene.addItem(block)

        # Display connections
        connections = self.json_object.get("connections", [])
        channel_colors = self.json_object.get("representation", {}).get(
            "channel_colors"
        )

        for connection_item in connections:
            connection = Connection(self.connection_config)
            connection.load(self, connection_item, channel_colors)
            self.connections.append(connection)
            self.scene.addItem(connection)

    def dump(self):
        """Returns the json used to load the widget"""

        data = {}

        if self.web_representation is not None:
            data["representation"] = self.web_representation

        has_loops = False

        for block_type in BlockType:
            block_type_list = []
            for block in self.blocks:
                block_data = {}
                if block.type == block_type:
                    block_data["name"] = block.name
                    if block.synchronized_channel is not None:
                        block_data["synchronized_channel"] = block.synchronized_channel
                    if block.type == BlockType.LOOPS:
                        block_data["processor_inputs"] = block.processor_inputs
                        block_data["evaluator_inputs"] = block.evaluator_inputs
                        block_data["processor_outputs"] = block.processor_outputs
                        block_data["evaluator_outputs"] = block.evaluator_outputs
                        has_loops = True
                    else:
                        if block.inputs is not None:
                            block_data["inputs"] = block.inputs
                        if block.outputs is not None:
                            block_data["outputs"] = block.outputs

                    block_type_list.append(block_data)
                data["representation"]["blocks"][block.name] = {
                    "col": int(block.position.x()),
                    "row": int(block.position.y()),
                    "width": int(block.custom_width),
                    "height": int(block.custom_height),
                }

            if block_type == BlockType.LOOPS:
                if has_loops:
                    data[block_type.value] = block_type_list
            else:
                data[block_type.value] = block_type_list

        connection_list = []
        for connection in self.connections:
            connection_data = {}
            connection_data["channel"] = connection.channel
            connection_data["from"] = (
                connection.start_block_name + "." + connection.start_pin_name
            )
            connection_data["to"] = (
                connection.end_block_name + "." + connection.end_pin_name
            )
            connection_list.append(connection_data)

        data["connections"] = connection_list

        if has_loops:
            data["schema_version"] = 2

        return data


@frozen
class ToolchainEditor(AbstractAssetEditor):
    def __init__(self, parent=None):
        super().__init__(AssetType.TOOLCHAIN, parent)
        self.setObjectName(self.__class__.__name__)
        self.set_title(self.tr("Toolchain"))

        self.toolchain_model = AssetModel()
        self.toolchain_model.asset_type = AssetType.TOOLCHAIN

        self.toolchain = ToolchainWidget()
        self.layout().addWidget(self.toolchain, 2)
        self.layout().addStretch()

        self.algorithm_list = []
        self.analyzer_list = []
        self.dataset_list = []
        self.sequential_loop_processor_list = []
        self.autonomous_loop_processor_list = []
        self.sequential_loop_evaluator_list = []
        self.autonomous_loop_evaluator_list = []

        self.toolchain.dataChanged.connect(self.dataChanged)
        self.contextChanged.connect(self.__reloadData)

    @pyqtSlot()
    def __reloadData(self):
        # ensure the experiments related data are up to date
        experiment_resources.refresh()

        algorithm_model = AlgorithmResourceModel()
        algorithm_model.setAnalyzerEnabled(False)
        algorithm_model.setTypes([Algorithm.SEQUENTIAL, Algorithm.AUTONOMOUS])
        dataset_model = DatasetResourceModel()

        self.dataset_list = [
            dataset_model.index(i, 0).data() for i in range(dataset_model.rowCount())
        ]
        self.algorithm_list = [
            algorithm_model.index(i, 0).data()
            for i in range(algorithm_model.rowCount())
        ]

        algorithm_model.setAnalyzerEnabled(True)
        self.analyzer_list = [
            algorithm_model.index(i, 0).data()
            for i in range(algorithm_model.rowCount())
        ]

        algorithm_model.setAnalyzerEnabled(False)
        algorithm_model.setTypes([Algorithm.SEQUENTIAL_LOOP_PROCESSOR])
        self.sequential_loop_processor_list = [
            algorithm_model.index(i, 0).data()
            for i in range(algorithm_model.rowCount())
        ]

        algorithm_model.setTypes([Algorithm.AUTONOMOUS_LOOP_PROCESSOR])
        self.autonomous_loop_processor_list = [
            algorithm_model.index(i, 0).data()
            for i in range(algorithm_model.rowCount())
        ]

        algorithm_model.setTypes([Algorithm.SEQUENTIAL_LOOP_EVALUATOR])
        self.sequential_loop_evaluator_list = [
            algorithm_model.index(i, 0).data()
            for i in range(algorithm_model.rowCount())
        ]

        algorithm_model.setTypes([Algorithm.AUTONOMOUS_LOOP_EVALUATOR])
        self.autonomous_loop_evaluator_list = [
            algorithm_model.index(i, 0).data()
            for i in range(algorithm_model.rowCount())
        ]

        self.toolchain.set_prefix_databases_algorithms_lists(
            self.prefix_path,
            self.dataset_list,
            self.algorithm_list,
            self.sequential_loop_processor_list,
            self.autonomous_loop_processor_list,
            self.sequential_loop_evaluator_list,
            self.autonomous_loop_evaluator_list,
            self.analyzer_list,
        )

    def refresh(self):
        """Reimpl"""

        super().refresh()
        self.__reloadData()

    def _asset_models(self):
        """Returns a list of all asset models used"""

        return [self.toolchain_model]

    def _load_json(self, json_object):
        """Load the json object passed as parameter"""

        self.toolchain.load(json_object)

    def _dump_json(self):
        """Returns the json representation of the asset"""

        return self.toolchain.dump()
