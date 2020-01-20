import wx
from types import ModuleType
from math import ceil

import Settings
import AutoSelfieTaker


class MyFrame(wx.Frame):

    def __init__(self, var_dict=None, title='', rows=0, columns=2):
        super().__init__(parent=None, title=title, style=wx.STAY_ON_TOP | wx.MAXIMIZE_BOX | wx.CLIP_CHILDREN | wx.CAPTION)
        rows = int(ceil(len(var_dict)))
        self.__buildUI(rows, columns)
        self.__initUI(var_dict)
        self.__show()


    def __buildUI(self, rows=1, columns=2):
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(wx.Colour(160,200,240))
        self.box_sizer = wx.BoxSizer(wx.VERTICAL)       
        self.grid_sizer = wx.FlexGridSizer(rows, columns, 1,1)
        self.grid_sizer.AddGrowableCol(0)
        self.grid_sizer.AddGrowableCol(1)
        self.box_sizer.Add(self.grid_sizer, flag=wx.EXPAND | wx.ALL, border=5)
        button_grid = wx.GridSizer(1, 4, 1, 1)
        self.start_btn = wx.Button(self.panel, label='Start Application')
        self.start_btn.Bind(wx.EVT_BUTTON, self.on_start)
        self.write_btn = wx.Button(self.panel, label='Write Values')
        self.write_btn.Bind(wx.EVT_BUTTON, self.on_write)
        self.reset_btn = wx.Button(self.panel, label='Reset Values')
        self.reset_btn.Bind(wx.EVT_BUTTON, self.on_reset)
        self.close_btn = wx.Button(self.panel, label='Close Application')
        self.close_btn.Bind(wx.EVT_BUTTON, self.on_close)
        button_grid.Add(self.start_btn, flag=wx.EXPAND | wx.ALL, border=5)
        button_grid.Add(self.write_btn, flag=wx.EXPAND | wx.ALL, border=5)
        button_grid.Add(self.reset_btn, flag=wx.EXPAND | wx.ALL, border=5)
        button_grid.Add(self.close_btn, flag=wx.EXPAND | wx.ALL, border=5)
        self.box_sizer.Add(button_grid, flag=wx.EXPAND | wx.ALL, border=5)
        self.panel.SetSizerAndFit(self.box_sizer)


    def __initUI(self, var_dict):
        offset = len(max(var_dict.keys(), key=len)) * 7
        self.var_dict = var_dict
        self.text_ctrl_dict = dict()
        self.label_value_dict = dict()

        for var, val in var_dict.items():
            if isinstance(val, dict):
                if val['_EDITABLE']:
                    parent_sizer = wx.BoxSizer(wx.HORIZONTAL)
                    dict_sizer = wx.BoxSizer(wx.VERTICAL)
                    var_sizer = wx.BoxSizer(wx.VERTICAL)
                    val_sizer = wx.BoxSizer(wx.VERTICAL)

                    label = wx.StaticText(self.panel, label=var)
                    variable = wx.Choice(self.panel, choices=[val for val in val.keys() if not val.startswith('_')])
                    variable.Insert('Select', 0)
                    variable.Append('Add New Range')
                    variable.SetSelection(0)
                    value = wx.TextCtrl(self.panel, value=val['_PLACEHOLDER'])
                    dict_sizer.Add(label, flag=wx.EXPAND | wx.ALL, border=10)
                    var_sizer.Add(variable, flag=wx.EXPAND | wx.ALL, border=10)
                    val_sizer.Add(value, flag=wx.EXPAND | wx.ALL, border=10)

                    size = dict_sizer.GetSize().Get()
                    dict_sizer.SetMinSize(wx.Size(size[0]+offset, size[1]))
                    size = var_sizer.GetSize().Get()
                    var_sizer.SetMinSize(wx.Size(size[0]+150, size[1]))
                    size = val_sizer.GetSize().Get()
                    val_sizer.SetMinSize(wx.Size(size[0]+250, size[1]))

                    parent_sizer.Add(dict_sizer, flag=wx.EXPAND)
                    parent_sizer.Add(var_sizer, flag=wx.EXPAND)
                    parent_sizer.Add(val_sizer, flag=wx.EXPAND)

                    self.grid_sizer.Add(parent_sizer, flag=wx.EXPAND)

                    self.text_ctrl_dict[value.GetId()] = str(val)
                    self.label_value_dict[label.GetId()] = value.GetId()

            else:
                parent_sizer = wx.BoxSizer(wx.HORIZONTAL)
                var_sizer = wx.BoxSizer(wx.VERTICAL)
                val_sizer = wx.BoxSizer(wx.VERTICAL)

                label = wx.StaticText(self.panel, label=var)
                value = wx.TextCtrl(self.panel, value=str(val))
                var_sizer.Add(label, flag=wx.EXPAND | wx.ALL, border=10)
                val_sizer.Add(value, flag=wx.EXPAND | wx.ALL, border=10)

                size = var_sizer.GetSize().Get()
                var_sizer.SetMinSize(wx.Size(size[0]+offset, size[1]))
                size = val_sizer.GetSize().Get()
                val_sizer.SetMinSize(wx.Size(size[0]+400, size[1]))

                parent_sizer.Add(var_sizer, flag=wx.EXPAND)
                parent_sizer.Add(val_sizer, flag=wx.EXPAND)

                self.grid_sizer.Add(parent_sizer, flag=wx.EXPAND)

                self.text_ctrl_dict[value.GetId()] = str(val)
                self.label_value_dict[label.GetId()] = value.GetId()


    def __show(self):
        width = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        height = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)
        dimensions = self.box_sizer.ComputeFittingWindowSize(self).Get()
        pos=((width/2) - (dimensions[0]/2), (height/2) - (dimensions[1]/2))
        self.SetMinSize(self.box_sizer.ComputeFittingWindowSize(self))
        self.SetMaxSize(self.box_sizer.ComputeFittingWindowSize(self))
        self.SetPosition(wx.Point(pos[0], pos[1]))
        # print (self.text_ctrl_dict)
        self.Show()


    def on_start(self, event):
        self.Hide()
        AutoSelfieTaker.main(True)


    def on_write(self, event):
        for label_id, value_id in self.label_value_dict.items():
            label = self.FindWindowById(label_id).GetLabel()
            value = self.FindWindowById(value_id).GetValue()
            self.var_dict[label] = value

            # print (f'{label} = {value}')

            try:
                float(value)                
                cmd_str = f'Settings.{label} = {value}'
            except ValueError:
                try:
                    cmd_str = f'Settings.{label} = \"{value}\"'
                except SyntaxError:
                    cmd_str = f'Settings.{label} = \"{value}\"'

            exec(cmd_str)

            cmd_str = f'print (type(Settings.{label}))'
            cmd_str = f'print (Settings.{label})'
            exec(cmd_str)

        print (type(Settings.blur_threshold))


    def on_reset(self, event):
        for ctrl_id, ctrl_val in self.text_ctrl_dict.items():
            text_ctrl = self.FindWindowById(ctrl_id)
            text_ctrl.SetValue(ctrl_val)


    def on_close(self, event):
        self.Close(True)
        self.Destroy()


if __name__ == '__main__':

    variables = {key:value for key, value in vars(Settings).items() if not key.startswith('__') and not isinstance(value, ModuleType)}

    app = wx.App()
    frame = MyFrame(variables)
    app.MainLoop()
