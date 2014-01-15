"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------
"""
import tank
import platform
import unicodedata
import os
import sys
import pprint
import threading

import sgtk
from tank.platform.qt import QtCore, QtGui
from tank import TankError
from .ui.dialog import Ui_Dialog
from ui.results import Ui_PublishResultForm
from .output_item import OutputItem
from .output import PublishOutput


class AppDialog(QtGui.QWidget):
    '''Extra Attributes supported:
        - int
        - string
        - bool
    '''

    def __init__(self, app):
        QtGui.QWidget.__init__(self)

        self._app = app
        self._outputs = []

        #fail safe for unsaved work
        try:
            self._pre_submit()
            self.show_render_dlg()
            self._outputs = [PublishOutput(self._app, output) for output in self._app.get_setting("outputs")]
            self._populate_output_list()
        except TankError, e:
            QtGui.QMessageBox.information(None, "Unable To Render!", "%s" % e)
        except Exception as e:
            print(e)

    def submit_btn_released(self):
        #collecting output data
        self.data_outputs = []

        for item in self.ui.contents.children():
            if isinstance(item, OutputItem):
                if item.selected:
                    data = {}

                    data['output'] = {}
                    data['output']['name'] = item._output.name
                    data['output']['tank_type'] = item._output.tank_type

                    data['jobname'] = self.ui.jobname_lineEdit.text()
                    data['priority'] = self.ui.priority_spinBox.value()
                    data['start'] = self.ui.start_spinBox.value()
                    data['end'] = self.ui.end_spinBox.value()
                    data['work_file'] = self.work_file

                    for item in self.additionalInfo:
                        widget = item['widget']
                        if isinstance(widget, QtGui.QLineEdit):
                            data[item['type']] = widget.text()
                        elif isinstance(widget, QtGui.QCheckBox):
                            data[item['type']] = widget.isChecked()
                        elif isinstance(widget, QtGui.QSpinBox):
                            data[item['type']] = widget.value()

                    self.data_outputs.append(data)

        #is anything selected?
        if len(self.data_outputs) != 0:
            #showing progress page
            self.ui.central_stackedWidget.setCurrentWidget(self.ui.progress_page)

            #execute hook
            QtCore.QTimer.singleShot(1, self.execute_post_hook)
        else:
            QtGui.QMessageBox.information(None, "Unable To Render!", "No items were selected to submit!")

    def execute_post_hook(self):
        #execute hook
        errors = self._app.execute_hook("hook_submit",
                                        app=self._app,
                                        outputs=self.data_outputs,
                                        widget=self.ui)

        #success or failure?
        if len(errors) == 0:
            self.ui.central_stackedWidget.setCurrentWidget(self.ui.success_page)
        else:
            self.ui.central_stackedWidget.setCurrentWidget(self.ui.failure_page)

            #generate errors report
            report = ''
            for output in errors:
                for error in output['errors']:
                    report += error + '\n'

            self.ui.failure_details.setText(report)

    def show_render_dlg(self):
        # set up the UI
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        #setting start information
        self.ui.jobname_lineEdit.setText(self.jobname)
        self.ui.priority_spinBox.setValue(self.priority)
        self.ui.start_spinBox.setValue(self.start)
        self.ui.end_spinBox.setValue(self.end)

        #making sure submit page is showing
        self.ui.central_stackedWidget.setCurrentWidget(self.ui.submit_page)

        #generate ui for extra attributes
        gridLayout = self.ui.gridLayout_additional

        #removing additionalInfo label
        if len(self.additionalInfo) != 0:
            gridLayout.removeWidget(self.ui.additionalInfo_label)
            self.ui.additionalInfo_label.setParent(None)

        #populate additional info ui
        row = 0
        for item in self.additionalInfo:
            # additionalItem = QtGui.QWidget()
            # layout = QtGui.QHBoxLayout(additionalItem)
            # layout.setContentsMargins(0, 0, 0, 0)

            label = QtGui.QLabel(item['type'] + ':')
            # layout.addWidget(label)
            gridLayout.addWidget(label, row, 0, 1, 1)

            widget = None
            if isinstance(item['value'], str):
                widget = QtGui.QLineEdit(item['value'])
            elif isinstance(item['value'], bool):
                widget = QtGui.QCheckBox()
                widget.setChecked(item['value'])
            elif isinstance(item['value'], int):
                widget = QtGui.QSpinBox()
                widget.setValue(item['value'])

            if widget:
                gridLayout.addWidget(widget, row, 2, 1, 1)

            # layout.addStretch(1)

                item['widget'] = widget
            # groupLayout.addWidget(additionalItem)

            row += 1

        self.ui.submit_btn.released.connect(self.submit_btn_released)
        self.ui.cancel_btn.released.connect(self.close)
        self.ui.success_close_btn.released.connect(self.close)
        self.ui.failure_close_btn.released.connect(self.close)

    def _populate_output_list(self):
        """Build the main task list for selection of outputs, items, etc.
        """
        # clear existing widgets
        # task_scroll_widget = self.ui.task_scroll.widget()
        #TODO

        if len(self._outputs) == 0:
            # no tasks so show no tasks text:
            self.ui.renders_stacked_widget.setCurrentWidget(self.ui.no_renders_page)
            return
        else:
            self.ui.renders_stacked_widget.setCurrentWidget(self.ui.renders_page)

        layout = QtGui.QVBoxLayout(self.ui.contents)

        for output in self._outputs:
            item = OutputItem(output, self.ui.contents)
            layout.addWidget(item)

        layout.addStretch(1)

    def _pre_submit(self):
        #getting start information
        self.jobname = 'default'
        self.ctx = self._app.context
        self.user = sgtk.util.get_current_user(self._app.sgtk)
        self.start = 0
        self.end = 0
        self.priority = 50
        self.work_file = None

        self.additionalInfo = []
        for item in self._app.execute_hook("hook_pre_submit"):
            if item['type'] == 'start':
                self.start = item['value']
            elif item['type'] == 'end':
                self.end = item['value']
            elif item['type'] == 'jobname':
                self.jobname = item['value']
            elif item['type'] == 'work_file':
                self.work_file = item['value']
            else:
                self.additionalInfo.append(item)
