import wx
import UI_settings as UI

class threadStat(wx.Dialog):
    def __init__(self, pluginPath, corePath):
        self.pluginPath = pluginPath
        self.corePath = corePath

        wx.Dialog.__init__(self, None, title='MW Parameter guard', size=UI.WMAIN['size'],
                           style=wx.SYSTEM_MENU | # wx.CAPTION |  # ~wx.CLOSE_BOX |
                                 wx.TAB_TRAVERSAL | wx.STAY_ON_TOP) #| wx.RESIZE_BORDER)  # | wx.TRANSPARENT_WINDOW)

        self.SetMinSize((1, 1))
        self.SetSizeWH(50, 50)

        self.SetBackgroundColour(wx.Colour(UI.WCOLOR['BG'][0],
                                           UI.WCOLOR['BG'][1],
                                           UI.WCOLOR['BG'][2]))

        self.SetTransparent(220)
        self.Show()

    # ------------------------------------------------------------------------------------------------------------------
    def slicer_working(self):
        text = wx.StaticText(self,
                             style=wx.ALIGN_CENTRE,
                             label='S',
                             pos=(0, 0),
                             size=(50, 50)
                             )

        font = wx.Font(33, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        text.SetFont(font)

        text.SetForegroundColour(UI.TCOLOR['FG'])

    # ------------------------------------------------------------------------------------------------------------------
    def simulation_working(self):
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def close_TS(self):
        self.Destroy()

app = wx.App(False)
TS = threadStat('', '')
TS.slicer_working()
app.MainLoop()