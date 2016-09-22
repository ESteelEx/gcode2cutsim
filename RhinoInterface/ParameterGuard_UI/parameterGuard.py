import wx, threading
import guard
import UI_settings as UI
from Utilities import ini_worker

class parameterGuardUI(wx.Dialog):
    def __init__(self, pluginPath, corePath, configFile):
        self.pluginPath = pluginPath
        self.corePath = corePath
        self.configFile = self.corePath + '\\' + configFile
        self.current_y_pxpos_elem = 0

        wx.Dialog.__init__(self, None, title='MW Parameter guard', size=UI.WMAIN['size'],
                           style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX |
                                 wx.TAB_TRAVERSAL | wx.STAY_ON_TOP | wx.RESIZE_BORDER)

        atable = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_ESCAPE, wx.ID_EXIT)])
        self.SetAcceleratorTable(atable)
        wx.EVT_MENU(self, wx.ID_EXIT, self.OnExit)

        self.SetBackgroundColour(wx.Colour(UI.WCOLOR['BG'][0],
                                           UI.WCOLOR['BG'][1],
                                           UI.WCOLOR['BG'][2]))

        self.Centre()
        self.Show()



        section_list = ini_worker.get_sections_list_from_ini(self.configFile)

        param_indentation = 10

        self.editbox = []

        for section in section_list:

            if section != 'GCODE' and section != 'MESH':

                font = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
                text = wx.StaticText(self,
                              label=section,
                              pos=(UI.THEADERSTART['pos'][0],
                                   UI.THEADERSTART['pos'][1] + self.current_y_pxpos_elem ))

                text.SetForegroundColour(UI.TCOLOR['FG'])  # set text color
                text.SetFont(font)

                self.current_y_pxpos_elem += 20
                section_params = ini_worker.get_section_from_ini(self.configFile, section)

                font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

                for param, value in section_params.iteritems():
                    text = wx.StaticText(self,
                                  label=param,
                                  pos=(UI.THEADERSTART['pos'][0] + param_indentation,
                                       UI.THEADERSTART['pos'][1] + self.current_y_pxpos_elem))

                    text.SetForegroundColour(UI.PARAMCOLOR['FG'])  # set text color

                    self.editbox.append(wx.TextCtrl(self,
                                value=str(value),
                                pos=(UI.EBOX['pos'][0], UI.THEADERSTART['pos'][1] + self.current_y_pxpos_elem),
                                size=UI.EBOX['size'],
                                style=wx.TE_PROCESS_ENTER))

                    self.editbox[-1].SetForegroundColour(UI.ECOLOR2['FG'])  # set color
                    self.editbox[-1].SetBackgroundColour(UI.ECOLOR2['BG'])  # set color

                    self.current_y_pxpos_elem += 20

        #self.scroll = wx.ScrolledWindow(self, 1)
        #self.scroll.SetScrollbars(0, 1, 0, 1000)

    # ------------------------------------------------------------------------------------------------------------------
    def OnExit(self, event):
        self.Destroy()


def main():
    app = wx.App(False)
    pluginPath = 'C:\\MWAdditive'
    corePath = 'C:\\MWAdditive'
    configFile = 'Mesh.ini'
    PG = parameterGuardUI('C:\\MWAdditive', 'C:\\MWAdditive', 'Mesh.ini')
    GOC = guard.guard_of_changes(pluginPath, corePath, PG)
    GOC.start()
    app.MainLoop()



if __name__== "__main__":
    main()

