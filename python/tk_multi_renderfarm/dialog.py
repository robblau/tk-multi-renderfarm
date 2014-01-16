"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------
"""
import tank
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
            self.attributes = self._app.execute_hook('hook_pre_submit')
            self.show_render_dlg()
            self._outputs = [PublishOutput(self._app, output) for output in self._app.get_setting("outputs")]
            self._populate_output_list()
        except TankError, e:
            QtGui.QMessageBox.information(None, "Unable To Submit!", "%s" % e)
        except Exception as e:
            print(e)

    def submit_btn_released(self):
        self.data_outputs = []

        for item in self.ui.contents.children():
            if isinstance(item, OutputItem):
                if item.selected:
                    data = {}

                    data['output'] = {}
                    data['output']['name'] = item._output.name
                    data['output']['tank_type'] = item._output.tank_type

                    for item in self.attributes:
                        
                        if item['gui']:
                            
                            widget = item['widget']
                            if isinstance(widget, QtGui.QLineEdit):
                                data[item['type']] = widget.text()
                            elif isinstance(widget, QtGui.QCheckBox):
                                data[item['type']] = widget.isChecked()
                            elif isinstance(widget, QtGui.QSpinBox):
                                data[item['type']] = widget.value()
                            elif isinstance(widget, QtGui.QComboBox):
                                data[item['type']] = widget.currentText()
                        else:
                            data[item['type']] = item['value']

                    self.data_outputs.append(data)

        #is anything selected?
        if len(self.data_outputs) != 0:
            #showing progress page
            self.ui.central_stackedWidget.setCurrentWidget(self.ui.progress_page)

            #execute hook
            QtCore.QTimer.singleShot(1, self.execute_submit_hook)
        else:
            QtGui.QMessageBox.information(None, "Unable To Submit!", "No items were selected to submit!")

    def execute_submit_hook(self):
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

        #making sure submit page is showing
        self.ui.central_stackedWidget.setCurrentWidget(self.ui.submit_page)

        #populate job attributes
        row = 0
        for item in self.attributes:
            
            if item['gui']:
            
                label = QtGui.QLabel(item['type'] + ':')
                self.ui.gridLayout.addWidget(label, row, 0, 1, 1)
    
                widget = None
                if isinstance(item['value'], str):
                    widget = QtGui.QLineEdit(item['value'])
                elif isinstance(item['value'], bool):
                    widget = QtGui.QCheckBox()
                    widget.setChecked(item['value'])
                elif isinstance(item['value'], int):
                    widget = QtGui.QSpinBox()
                    widget.setValue(item['value'])
                elif isinstance(item['value'], list):
                    widget = QtGui.QComboBox()
                    for i in item['value']:
                        widget.addItem(i)
    
                if widget:
                    self.ui.gridLayout.addWidget(widget, row, 2, 1, 1)
                    item['widget'] = widget
    
                row += 1
        
        #connecting buttons to methods
        self.ui.submit_btn.released.connect(self.submit_btn_released)
        self.ui.cancel_btn.released.connect(self.close)
        self.ui.success_close_btn.released.connect(self.close)
        self.ui.failure_close_btn.released.connect(self.close)

    def _populate_output_list(self):
        """Build the main task list for selection of outputs, items, etc.
        """
        if len(self._outputs) == 0:
            self.ui.renders_stacked_widget.setCurrentWidget(self.ui.no_renders_page)
            return
        else:
            self.ui.renders_stacked_widget.setCurrentWidget(self.ui.renders_page)

        layout = QtGui.QVBoxLayout(self.ui.contents)

        for output in self._outputs:
            item = OutputItem(output, self.ui.contents)
            layout.addWidget(item)

        layout.addStretch(1)
