import bpy
import math
from bpy.props import BoolProperty

bl_info = {
    'name': 'Timer increaser',
    'description': 'Timer Text effect for font objects',
    'author': 'Giuseppe Marzio Zermo',
    'version': (0, 1),
    'blender': (2, 7, 9),
    'location': 'Properties Editor, Text Context',
    'url': 'https://github.com/gmarzioz/blender-texttimer-addon',
    'category': 'Text'}


def countdown_timer(scene):
    timers = [ob.data for ob in scene.objects if ob.type == 'FONT' and ob.data.is_timer]
    for font in timers:
        secs = font["timer"]
        countdown_frames = secs * scene.render.fps / scene.render.fps_base
        frame = countdown_frames + scene.frame_current + 1
        if frame < 0:
            continue
        ts = float(frame * scene.render.fps_base ) / float(scene.render.fps)
        t = 0
        th = ts
        
        th %= 24
        hours = ts // 3600
        
        
        
        tm = ts / 60
        tm %= 60
        minutes = tm
        
        ts %= 60
        seconds = ts
        
        tsc = ts
        
        
        
        font.body = "%02d:%02d:%02d" % (hours,minutes,seconds)
    return None
def is_timer(self,context):
    if self.is_timer:
        if "timer" not in self.keys():
            self["timer"] = 10
    return None
class TimerPanel(bpy.types.Panel):
    """Timer Panel"""
    bl_label = "Timer increase"
    bl_idname = "FONT_PT_timer"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    
    @classmethod
    def poll(cls, context):
        return (context.object and context.object.type in {'FONT'} and context.curve)
    def draw_header(self, context):
        font = context.object.data
        
        self.layout.prop(font, "is_timer", text="")
    def draw(self, context):
        font = context.object.data
        layout = self.layout
        if font.is_timer:
            row = layout.row()
            row.prop(font,'["timer"]', text="Seconds")
def register():
    bpy.types.TextCurve.is_timer = BoolProperty(default=False, update=is_timer, description="Make countdown timer")
    
    bpy.app.handlers.frame_change_pre.append(countdown_timer)
    bpy.utils.register_class(TimerPanel)
    
def unregister():
    bpy.utils.unregister_class(TimerPanel)
    bpy.app.handlers.frame_change_pre.pop()
    
if __name__ == "__main__":
    register()
