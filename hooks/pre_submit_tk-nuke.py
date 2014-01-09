import nuke

import tank
from tank import Hook
from tank import TankError

class PreSubmitHook(Hook):
    
    def execute(self, **kwargs):
                
        items = []
        
        # get the main scene:
        scene_name = nuke.root()['name'].value()
        if not scene_name:
            raise TankError("Please Save your file before Rendering")
                 
        items.append({"type": "work_file", "value": scene_name})
        
        #scan scene for starting information
        items.append({'type':'start','value': nuke.root()['first_frame'].value()})
        items.append({'type':'end','value': nuke.root()['last_frame'].value()})
        
        jobname = '.'.join(os.path.basename(scene_name).split('.')[0:-1])
        items.append({'type':'jobname','value':jobname})
        
        #adding extra attributes
        #items.append({'type':'Limit','value':'nuke_render'})
        
        #saving scene before dialog
        nuke.scriptSave()

        return items