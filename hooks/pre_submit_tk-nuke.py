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

        attrs.append({'type': 'work_file', 'value': scene_name})

        attrs.append({'type': 'start', 'value': nuke.root()['first_frame'].value()})
        attrs.append({'type': 'end', 'value': nuke.root()['last_frame'].value()})
        attrs.append({'type': 'by', 'value': 1})

        jobname = '.'.join(os.path.basename(scene_name).split('.')[0:-1])
        attrs.append({'type': 'jobname', 'value': jobname})
        attrs.append({'type': 'queue', 'value': ['high', 'mid', 'low']})
        attrs.append({'type': 'submit', 'value': True})

        #saving scene before dialog
        nuke.scriptSave()

        return attrs
