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
        self.param_dict = {}
        self.section_EC_stat = {}

        self.GOC = guard.guard_of_changes(self)  # init observer thread
        self.GOC.start()  # start observer thread

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
        fn = self.corePath + '\\bin\\images\\paramGuard.ico'
        self.icon = wx.Icon(fn, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        self.section_list = ini_worker.get_sections_list_from_ini(self.configFile)  # list

        param_indentation = 10 # whitespace

        for section in self.section_list:

            self.section_EC_stat.update({section: 1})

            section_params = ini_worker.get_section_from_ini(self.configFile, section)
            for param, value in section_params.iteritems():
                if param == 'hideSection':
                    hideSection = value

            if not hideSection:

                self.param_dict[section] = {}

                font = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)

                headline = wx.StaticText(self,
                                     label=section,
                                     pos=(UI.THEADERSTART['pos'][0],
                                          UI.THEADERSTART['pos'][1] + self.current_y_pxpos_elem))

                headline.SetForegroundColour(UI.TCOLOR['FG'])  # set text color
                headline.SetFont(font)

                button = wx.Button(self,
                                   name=section,
                                   label="",
                                   pos=(2, self.current_y_pxpos_elem + 11),
                                   size=UI.BEXPAND['size'])

                button.Bind(wx.EVT_BUTTON, self.expandCollapse)
                button.SetBackgroundColour(UI.BCOLOR['BG'])  # set color
                button.SetToolTipString('Click to expand/collapse section')

                self.current_y_pxpos_elem += 20

                # params in sections (edit boxes)
                font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
                ui_elem_handler_dict = {}
                for param, value in section_params.iteritems():

                    text = wx.StaticText(self,
                                         label=param,
                                         pos=(UI.THEADERSTART['pos'][0] + param_indentation,
                                              UI.THEADERSTART['pos'][1] + self.current_y_pxpos_elem))

                    text.SetForegroundColour(UI.PARAMCOLOR['FG'])  # set text color

                    editbox = (wx.TextCtrl(self,
                                           name=section + ' - ' + param,
                                           value=str(value),
                                           pos=(UI.EBOX['pos'][0], UI.THEADERSTART['pos'][1] + self.current_y_pxpos_elem),
                                           size=UI.EBOX['size'],
                                           style=wx.TE_PROCESS_ENTER))

                    editbox.SetForegroundColour(UI.ECOLOR2['FG'])  # set color
                    editbox.SetBackgroundColour(UI.ECOLOR2['BG'])  # set color

                    editbox.Bind(wx.EVT_TEXT, self.EvtText)

                    elem_dict = {param: [{'ebox': [editbox, value]},
                                         {'headline': headline},
                                         {'text': text}]}

                    ui_elem_handler_dict.update(elem_dict)

                    self.current_y_pxpos_elem += 20

                self.param_dict[section].update(ui_elem_handler_dict)

        # self.scroll = wx.ScrolledWindow(self, 1)
        # self.scroll.SetScrollbars(0, 1, 0, 1000)

    # ------------------------------------------------------------------------------------------------------------------
    def refresh_UI(self):

        # section_list = ini_worker.get_sections_list_from_ini(self.configFile)  # list
        for section in self.section_list:

            section_params = ini_worker.get_section_from_ini(self.configFile, section)
            for param, value in section_params.iteritems():
                if param == 'hideSection':
                    hideSection = value

            if not hideSection:
                for param, value in section_params.iteritems():
                    if self.param_dict[section][param][1] != value:
                        self.param_dict[section][param][0].SetForegroundColour(UI.ECOLOR2CHANGE['FG'])  # set color
                        self.param_dict[section][param][0].SetBackgroundColour(UI.ECOLOR2CHANGE['BG'])
                        self.param_dict[section][param][0].SetValue(str(value))

                    self.param_dict[section][param][1] = value

    # ------------------------------------------------------------------------------------------------------------------
    def EvtText(self, event):
        value = event.GetString()
        editbox_name = event.EventObject.GetName()

        ini_worker.write_to_section(self.configFile, editbox_name.split('-')[0].strip(), editbox_name.split('-')[1].strip(), value)

    # ------------------------------------------------------------------------------------------------------------------
    def expandCollapse(self, event):
        section_clicked = event.EventObject.GetName()
        if self.section_EC_stat[section_clicked]:
            self.section_EC_stat[section_clicked] = 0
        else:
            self.section_EC_stat[section_clicked] = 1

        self.current_y_pxpos_elem = 20
        param_indentation = 10

        # for section, params in self.param_dict.iteritems():
        for section in self.section_list:
            if section in self.param_dict:
                for param, value in self.param_dict[section].iteritems():

                    if self.section_EC_stat[section]:
                        # value[0].ShowWithEffect(10, timeout=30)
                        value[0]['ebox'][0].Show()
                        value[1]['headline'].Show()
                        value[2]['text'].Show()
                        value[0]['ebox'][0].SetPosition([UI.EBOX['pos'][0],
                                              UI.THEADERSTART['pos'][1] + self.current_y_pxpos_elem])

                        value[1]['headline'].SetPosition([UI.THEADERSTART['pos'][0], UI.THEADERSTART['pos'][1] + self.current_y_pxpos_elem])
                        value[2]['text'].SetPosition([UI.THEADERSTART['pos'][0] + param_indentation , UI.THEADERSTART['pos'][1] + self.current_y_pxpos_elem])

                        self.current_y_pxpos_elem += 20
                    else:
                        # value[0].HideWithEffect(10, timeout=30)
                        value[0]['ebox'][0].Hide()
                        value[1]['headline'].Hide()
                        value[2]['text'].Hide()


                self.current_y_pxpos_elem += 20

    # ------------------------------------------------------------------------------------------------------------------
    def OnExit(self, event):
        self.Destroy()
        self.GOC.inject_runstat(False)


def main():
    app = wx.App(False)
    pluginPath = 'C:\\MWAdditive'
    corePath = 'C:\\MWAdditive'
    configFile = 'Mesh.ini'
    PG = parameterGuardUI(pluginPath, corePath, configFile)
    app.MainLoop()


if __name__== "__main__":
    main()

