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
        items.append({'type':'start','value':cmds.getAttr('defaultRenderGlobals.startFrame')})
        items.append({'type':'end','value':cmds.getAttr('defaultRenderGlobals.endFrame')})
        
        jobname = '.'.join(os.path.basename(scene_name).split('.')[0:-1])
        items.append({'type':'jobname','value':jobname})
        
        #additional data
        #items.append({'type':'Limit','value':'maya_render'})
        
        #saving scene before dialog
        cmds.file(save=True, force=True)

        return items