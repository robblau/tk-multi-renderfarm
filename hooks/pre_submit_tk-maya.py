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

import maya.cmds as cmds

import tank
from tank import Hook
from tank import TankError

class PreSubmitHook(Hook):
    
    def execute(self, **kwargs):
                
        items = []
        
        # get the main scene:
        scene_name = cmds.file(query=True, sn=True)
        if not scene_name:
            raise TankError("Please Save your file before Rendering")
                 
        items.append({"type": "work_file", "value": scene_name})
        
        #scan scene for starting information
        items.append({'type':'start','value':cmds.playbackOptions(query=True, minTime=True)})
        items.append({'type':'end','value':cmds.playbackOptions(query=True, maxTime=True)})
        items.append({'type':'limit','value':'shave_render'})
        
        jobname = '.'.join(os.path.basename(scene_name).split('.')[0:-1])
        items.append({'type':'jobname','value':jobname})

        return items