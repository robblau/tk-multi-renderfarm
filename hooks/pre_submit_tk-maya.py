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

        attrs.append({'type': 'submit_file', 'value': str(scene_name),'gui':False})

        attrs.append({'type': 'start', 'value': int(cmds.getAttr('defaultRenderGlobals.startFrame')),'gui':True})
        attrs.append({'type': 'end', 'value': int(cmds.getAttr('defaultRenderGlobals.endFrame')),'gui':True})
        attrs.append({'type': 'by', 'value': 1})

        jobname = os.path.splitext(os.path.basename(scene_name))[0]
        attrs.append({'type': 'jobname', 'value': str(jobname),'gui':True})
        attrs.append({'type': 'queue', 'value': ['high', 'mid', 'low'],'gui':True})
        attrs.append({'type': 'submit', 'value': True,'gui':True})

        #saving scene before dialog
        cmds.file(save=True, force=True)

        return attrs
