import os

import nuke

import tank
from tank import Hook
from tank import TankError


class PreSubmitHook(Hook):
    def execute(self, **kwargs):
        attrs = []

        # get the main scene:
        scene_name = nuke.root()['name'].value()
        if not scene_name:
            raise TankError("Please Save your file before Rendering")

        attrs.append({"type": "work_file", "value": scene_name})

        #scan scene for starting information
        attrs.append({'type': 'start', 'value': nuke.root()['first_frame'].value()})
        attrs.append({'type': 'end', 'value': nuke.root()['last_frame'].value()})

        jobname = '.'.join(os.path.basename(scene_name).split('.')[0:-1])
        attrs.append({'type': 'jobname', 'value': jobname})

        #adding extra attributes
        #items.append({'type':'Limit','value':'nuke_render'})

        #saving scene before dialog
        nuke.scriptSave()

        return attrs
