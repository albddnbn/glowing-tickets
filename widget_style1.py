from guizero import *

class widget_style:
    def __init__(self, widget, background=None, txt_color="black", txt_value="", when_click=""):
        self.widget = widget
        self.widget.bg = background
        self.widget.color = txt_color
        self.widget.value = txt_value
        self.widget.when_clicked = when_click
        self.return_widget()

    def return_widget(self):
        return self.widget



class full_button(PushButton):
    def __init__(self, btn_widget, backg, txt_color, padx, pady, size, mouse_enter, mouse_leave, command_dict):
        self.btn = btn_widget
        self.btn.bg = backg
        self.btn.text_color = txt_color
        if padx:
            self.btn.padx = padx
        if pady:
            self.btn.pady = pady
        if size:
            self.btn.size = size
        if command_dict != {}:
            self.btn.update_command(command_dict['function'], args=command_dict['args'])
        self.btn.when_mouse_enters = mouse_enter
        self.btn.when_mouse_leaves = mouse_leave
        self.return_button()

    def return_button(self):
        return self.btn

class padding:
    def __init__(self, master, leftpad="", rightpad="", toppad="", bottompad=""):
        Box(master, height="fill", width=leftpad, align="left")
        Box(master, height="fill", width=rightpad, align="right")
        if toppad:
            Box(master, height=toppad, width="fill", align="top")
        if bottompad:
            Box(master, height=bottompad, width="fill", align="bottom")
