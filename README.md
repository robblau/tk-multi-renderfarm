App for Shotgun Toolkit, to submit files to a render farm.

Configuration example:

tk-multi-renderfarm:
 hook_post_submit: shot_post_submit_tk_maya
 hook_pre_submit: shot_pre_submit_tk_maya
 location: {path: 'https://github.com/baitstudio/tk-multi-renderfarm.git',type: git, version: v0.0.2}
 outputs:
  - {description: Sends Ass export and Arnold render to the farm., display_group: Render, display_name: Arnold Render, icon: icons/arnold.png, name: arnold_render, required: false, selected: false, tank_type: Arnold Render}
  - {description: Send Maya render to the farm., display_group: Render, display_name: Maya Render, icon: icons/maya.png, name: maya_render, required: false, selected: false, tank_type: Maya Render}
  - {description: Exports Ass locally and sends Arnold render to the farm., display_group: Render, display_name: ASS Render, icon: icons/ass.png, name: ass_render, required: false, selected: false, tank_type: Arnold Render}
