import os

import maya.cmds as cmds

import tank
from tank import Hook
from tank import TankError


class PreSubmitHook(Hook):
    def execute(self, **kwargs):
        attrs = []

        # get the main scene:
        scene_name = cmds.file(query=True, sn=True)
        if not scene_name:
            raise TankError("Please Save your file before Rendering")

        attrs.append({'type': 'work_file', 'value': scene_name})

        #scan scene for starting information
        attrs.append({'type': 'start', 'value': int(cmds.getAttr('defaultRenderGlobals.startFrame'))})
        attrs.append({'type': 'end', 'value': int(cmds.getAttr('defaultRenderGlobals.endFrame'))})
        attrs.append({'type': 'by', 'value': 1})

        jobname = '.'.join(os.path.basename(scene_name).split('.')[0:-1])
        attrs.append({'type': 'jobname', 'value': jobname})

        #additional data
        #items.append({'type':'Limit','value':'maya_render'})

        #saving scene before dialog
        cmds.file(save=True, force=True)

        return attrs