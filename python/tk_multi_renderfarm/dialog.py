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
from .output_item import OutputItem
from .output import PublishOutput

class AppDialog(QtGui.QWidget):

    
    def __init__(self, app):
        QtGui.QWidget.__init__(self)
        self._app = app
        
        self._outputs=[]
        
        #fail safe for unsaved work
        try:
            self._pre_submit()
            
            self.show_render_dlg()
            
            self.create_connections()
            
            self._outputs=[PublishOutput(self._app, output) for output in self._app.get_setting("outputs")]
            
            self._populate_output_list()
                
        except TankError, e:
            QtGui.QMessageBox.information(None, "Unable To Render!", "%s" % e)
    
    def create_connections(self):
        
        self.ui.submit_btn.released.connect(self.submit_btn_released)
        self.ui.cancel_btn.released.connect(self.cancel_btn_released)
    
    def cancel_btn_released(self):
        
        self.close()
    
    def submit_btn_released(self):
        
        #collecting output data            
        outputs=[]
        
        for item in self.ui.contents.children():
            
            if isinstance(item,OutputItem):
                
                if item.selected:
                    
                    data={}
                    
                    data['output']={}
                    data['output']['name']=item._output.name
                    data['output']['tank_type']=item._output.tank_type
                    
                    data['jobname']=self.ui.jobname_lineEdit.text()
                    data['priority']=self.ui.priority_spinBox.value()
                    data['start']=self.ui.start_spinBox.value()
                    data['end']=self.ui.end_spinBox.value()
                    data['limit']=self.ui.limit_lineEdit.text()
                    data['work_file']=self.work_file
                    
                    outputs.append(data)
        
        #executing hook
        if len(outputs)!=0:
            self._app.execute_hook("hook_post_submit",app=self._app,outputs=outputs)
            
            self.close()
        else:
            QtGui.QMessageBox.information(None, "Unable To Render!", "No items were selected to submit!")

    def show_render_dlg(self):
        
        # set up the UI
        self.ui = Ui_Dialog() 
        self.ui.setupUi(self)
        
        #setting start information
        self.ui.jobname_lineEdit.setText(self.jobname)
        self.ui.priority_spinBox.setValue(self.priority)
        self.ui.start_spinBox.setValue(self.start)
        self.ui.end_spinBox.setValue(self.end)
        self.ui.limit_lineEdit.setText(self.limit)
    
    def _populate_output_list(self):
        """
        Build the main task list for selection of outputs, items, etc.
        """

        # clear existing widgets:
        task_scroll_widget = self.ui.task_scroll.widget()
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
        
        # add vertical stretch:
        layout.addStretch(1)
    
    def _pre_submit(self):
        
        #getting start information
        self.jobname='default'
        self.ctx=self._app.context
        self.user=sgtk.util.get_current_user(self._app.sgtk)
        self.start=0
        self.end=0
        self.priority=50
        self.limit='default'
        self.work_file=None
        
        for item in self._app.execute_hook("hook_pre_submit"):
            
            if item['type']=='start':
                self.start=item['value']
            
            if item['type']=='end':
                self.end=item['value']
            
            if item['type']=='jobname':
                self.jobname=item['value']
            
            if item['type']=='limit':
                self.limit=item['value']
            
            if item['type']=='work_file':
                self.work_file=item['value']