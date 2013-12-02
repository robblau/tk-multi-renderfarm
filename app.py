"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------

"""

import sys
import os
import platform

from tank.platform import Application

class AboutTank(Application):
    
    def init_app(self):
        """
        Called as the application is being initialized
        """
        # import using special tank import mechanism
        _app = self.import_module("tk_multi_renderfarm")
        # create a callback to run when our command is launched.
        # pass the app object as a parameter.
        cb = lambda : _app.show_dialog(self)
        # add stuff to main menu
        self.engine.register_command("Render Farm", cb)