"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------

"""


def show_dialog(app):
    # defer imports so that the app works gracefully in batch modes
    from .dialog import AppDialog
    # show the dialog window using the engine's show_dialog method
    app.engine.show_dialog("Render Farm", app, AppDialog, app)
