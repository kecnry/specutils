from ..ui.widgets.plugin import Plugin
from ..third_party.qtpy.QtWidgets import *
from ..third_party.qtpy.QtCore import *
from ..third_party.qtpy.QtGui import *
from ..core.comms import Dispatch, DispatchHandle
import qtawesome as qta
from ..ui.widgets.utils import ICON_PATH


class DataListPlugin(Plugin):
    name = "Data List"

    def setup_ui(self):
        self.layout_vertical.setContentsMargins(11, 11, 11, 11)

        # List widget for the data sets
        self.list_widget_data_list = QListWidget(self)

        # Label box to show when no data set has been loaded
        self.label_unopened = QLabel(self)
        self.label_unopened.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)
        self.label_unopened.setText("Click the folder icon to open a data set")
        self.label_unopened.setWordWrap(True)
        self.label_unopened.setStyleSheet("""
        QLabel {
            color: #8a6d3b;
            background-color: #fcf8e3;
            padding: 10px;
            border: 1px solid #faebcc;
            border-radius: 4px;
        }""")

        self.layout_vertical.addWidget(self.label_unopened)
        self.layout_vertical.addWidget(self.list_widget_data_list)

        self.layout_horizontal = QHBoxLayout()

        self.button_open_data = QToolButton(self)
        self.button_open_data.setIcon(QIcon(os.path.join(
            ICON_PATH, "Open Folder-48.png")))
        self.button_open_data.setIconSize(QSize(25, 25))

        self.button_create_sub_window = QToolButton(self)
        self.button_create_sub_window.setIcon(QIcon(os.path.join(
            ICON_PATH, "Open in Browser-50.png")))
        self.button_create_sub_window.setIconSize(QSize(25, 25))
        self.button_create_sub_window.setEnabled(False)

        self.button_add_to_sub_window = QToolButton(self)
        self.button_add_to_sub_window.setIcon(QIcon(os.path.join(
            ICON_PATH, "Change Theme-50.png")))
        self.button_add_to_sub_window.setIconSize(QSize(25, 25))
        self.button_add_to_sub_window.setEnabled(False)

        self.button_remove_data = QToolButton(self)
        self.button_remove_data.setIcon(QIcon(os.path.join(
            ICON_PATH, "Delete-48.png")))
        self.button_remove_data.setEnabled(False)
        self.button_remove_data.setIconSize(QSize(25, 25))

        self.layout_horizontal.addWidget(self.button_open_data)
        self.layout_horizontal.addWidget(self.button_create_sub_window)
        self.layout_horizontal.addWidget(self.button_add_to_sub_window)
        self.layout_horizontal.addStretch()
        self.layout_horizontal.addWidget(self.button_remove_data)

        self.layout_vertical.addLayout(self.layout_horizontal)

    def setup_connections(self):
        # Enable/disable buttons depending on selection
        self.list_widget_data_list.itemSelectionChanged.connect(
            lambda: self.toggle_buttons(self.current_data_item))

        # Connect the create new sub window button
        self.button_create_sub_window.clicked.connect(
            lambda: Dispatch.on_add_window.emit(data=self.current_data))

        # Connect the add to current plot window button
        self.button_add_to_sub_window.clicked.connect(
            lambda: Dispatch.on_add_to_window.emit(
                data=self.current_data))

        # When the layer list delete button is pressed
        self.button_remove_data.clicked.connect(
            lambda: Dispatch.on_remove_data.emit(
            self.current_data))

        # Open file dialog
        self.button_open_data.clicked.connect(
            lambda: Dispatch.on_file_open.emit())

    @property
    def current_data(self):
        """
        Returns the currently selected data object from the data list widget.

        Returns
        -------
        data : specviz.core.data.Data
            The `Data` object of the currently selected row.
        """
        data_item = self.list_widget_data_list.currentItem()

        if data_item is not None:
            data = data_item.data(Qt.UserRole)
            return data

    @property
    def current_data_item(self):
        return self.list_widget_data_list.currentItem()

    @DispatchHandle.register_listener("on_added_data")
    def add_data_item(self, data):
        """
        Adds a `Data` object to the loaded data list widget.

        Parameters
        ----------
        data : specviz.core.data.Data
            The `Data` object to add to the list widget.
        """
        new_item = QListWidgetItem(data.name, self.list_widget_data_list)
        new_item.setFlags(new_item.flags() | Qt.ItemIsEditable)

        new_item.setData(Qt.UserRole, data)

        self.list_widget_data_list.setCurrentItem(new_item)

    @DispatchHandle.register_listener("on_removed_data")
    def remove_data_item(self, data):
        data_item = self.get_data_item(data)

        self.list_widget_data_list.takeItem(
            self.list_widget_data_list.row(data_item))

    def get_data_item(self, data):
        for i in range(self.list_widget_data_list.count()):
            data_item = self.list_widget_data_list.item(0)

            if data_item.data(Qt.UserRole) == data:
                return data_item

    def toggle_buttons(self, data_item):
        if data_item is not None:
            self.label_unopened.hide()
            self.button_remove_data.setEnabled(True)
            self.button_create_sub_window.setEnabled(True)
            self.button_add_to_sub_window.setEnabled(True)
        else:
            self.label_unopened.show()
            self.button_remove_data.setEnabled(False)
            self.button_create_sub_window.setEnabled(False)
            self.button_add_to_sub_window.setEnabled(False)


