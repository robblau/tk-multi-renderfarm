# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import os

import nuke

import tank
from tank import Hook
from tank import TankError

class PostSubmitHook(Hook):
    
    def execute(self,app,outputs, **kwargs):
        '''
        
        app:        main class app
        outputs:    list of dicts with the following keys:
                
                    jobname:    String
                                Jobname from UI.
                                
                    priority:   Int
                                Priority value from UI.
                                
                    start:      Int
                                Start frame from UI.
                                
                    end:        Int
                                End frame from UI.
                                
                    limit:      String
                                Limit from UI.
                    
                    work_file:  String
                                Path to work file.
                    
                    output:     Dict
                                Dictionary with all data from the outputs:
                                
                                name:         String
                                              Name of output in the environment.
                                
                                tank_type:    String
                                              Tank type specified in the environment.
        
        '''
        
        print 'Post Render Hook!!!!!!'
        self.app=app
        self.outputs=outputs
        
        print 'app:'
        print self.app
        #print self.app.sgtk.templates["maya_shot_work"]
        
        print 'outputs:'
        for output in self.outputs:
            
            print output  
            
            
            
            
            