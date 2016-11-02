import wx, sys, time
from matplotlib.axes._base import _AxesBase

import guard
import UI_settings as UI
import key_stroke_timer
from Utilities import ini_worker
from screeninfo import get_monitors

class parameterGuardUI(wx.Dialog):
    def __init__(self, pluginPath, corePath, configFile):
        self.pluginPath = pluginPath
        self.corePath = corePath
        self.workingDir = sys.path[0]
        self.configFile = self.corePath + '\\' + configFile
        self.PGconfigFile = self.workingDir + '\\' + 'PG_config.ini'
        self.PGconfigFileCore = self.corePath + '\\' + 'PG_config.ini'
        self.PG_expanded = False
        self.current_y_pxpos_elem = 0
        self.param_dict = {}
        self.section_EC_stat = {}
        self.KST = key_stroke_timer.key_stroke_timer(self.configFile)
        self.MIN_SIZE_W = 20
        self.black_list = ['collapse', 'create', 'hideSection', 'show', 'filterStrategy', 'offsetType']

        self.GOC = guard.guard_of_changes(self)  # init observer thread
        self.GOC.start()  # start observer thread

        wx.Dialog.__init__(self, None, title='MW Parameter guard', size=UI.WMAIN['size'],
                           style=wx.SYSTEM_MENU | # wx.CAPTION |  # ~wx.CLOSE_BOX |
                                 wx.TAB_TRAVERSAL | wx.STAY_ON_TOP | wx.RESIZE_BORDER)  # | wx.TRANSPARENT_WINDOW)

        self.SetMinSize((1, 1))

        PG_XY = ini_worker.get_param_from_ini(self.PGconfigFileCore, 'UISETTINGS', 'lastWindowPosition')
        PG_XY = PG_XY.strip()[1:-1].split(',')
        PG_SIZE = ini_worker.get_param_from_ini(self.PGconfigFileCore, 'UISETTINGS', 'lastWindowSize')
        PG_SIZE = PG_SIZE.strip()[1:-1].split(',')


        self.MAIN_DISPLAY_SIZE = get_monitors()
        if len(self.MAIN_DISPLAY_SIZE) == 1:
            self.DISPLAY_SIZE = self.MAIN_DISPLAY_SIZE[0]
        else:
            self.DISPLAY_SIZE = self.MAIN_DISPLAY_SIZE[1]

        self.DISPLAY_SIZE = self.MAIN_DISPLAY_SIZE[0]

        #self.MoveXY(int(PG_XY[0]), int(PG_XY[1]))
        self.MoveXY(int(self.DISPLAY_SIZE.width)-10, 0)
        #self.SetSizeWH(int(PG_SIZE[0]), int(PG_SIZE[1]))
        self.SetSizeWH(int(PG_SIZE[0]), self.DISPLAY_SIZE.height)

        self.Bind(wx.EVT_SIZE, self.OnSize, self)
        # self.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver)
        # self.Bind(wx.EVT_LEAVE_WINDOW, self.onMouseLeave)
        # self.Bind(wx.EVT_LEFT_DOWN, self.onLMouseDown)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.onMouseEvents)

        atable = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_ESCAPE, wx.ID_EXIT)])
        self.SetAcceleratorTable(atable)
        wx.EVT_MENU(self, wx.ID_EXIT, self.OnExit)

        self.SetBackgroundColour(wx.Colour(UI.WCOLOR['BG'][0],
                                           UI.WCOLOR['BG'][1],
                                           UI.WCOLOR['BG'][2]))

        self.SetTransparent(220)
        self.Show()

        #fn = self.corePath + '\\bin\\images\\paramGuard.ico'
        #self.icon = wx.Icon(fn, wx.BITMAP_TYPE_ICO)
        #self.SetIcon(self.icon)

        self.section_list = ini_worker.get_sections_list_from_ini(self.configFile)  # list

        param_indentation = 10  # whitespace

        for section in self.section_list:

            self.section_EC_stat.update(
                {section: ini_worker.get_param_from_ini(self.configFile, section, 'collapse')})

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
                headline.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver)
                #headline.Bind(wx.EVT_LEAVE_WINDOW, self.onMouseLeave)

                button = wx.Button(self,
                                   name=section,
                                   label="",
                                   pos=(UI.BEXPAND['pos'][0], self.current_y_pxpos_elem + 11),
                                   size=UI.BEXPAND['size'])

                button.Bind(wx.EVT_BUTTON, self.expandCollapse)
                button.SetBackgroundColour(UI.BCOLOR['BG'])  # set color
                button.SetToolTipString('Click to expand/collapse section')
                button.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver)
                #button.Bind(wx.EVT_LEAVE_WINDOW, self.onMouseLeave)

                self.current_y_pxpos_elem += 20

                # params in sections (edit boxes)
                font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
                ui_elem_handler_dict = {}

                for param, value in section_params.iteritems():

                    if type(value) == str:
                        splitted_value = value.split(';')
                        if len(splitted_value) > 1:
                            if splitted_value[1].strip() == 'X':
                                self.black_list.append(param)

                    if param not in self.black_list:

                        text = wx.StaticText(self,
                                             label=param,
                                             pos=(UI.THEADERSTART['pos'][0] + param_indentation,
                                                  UI.THEADERSTART['pos'][1] + self.current_y_pxpos_elem))

                        text.SetForegroundColour(UI.PARAMCOLOR['FG'])  # set text color
                        text.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver)
                        #text.Bind(wx.EVT_LEAVE_WINDOW, self.onMouseLeave)

                        editbox = (wx.TextCtrl(self,
                                               name=section + ' - ' + param,
                                               value=str(value),
                                               pos=(UI.EBOX['pos'][0], UI.THEADERSTART['pos'][1] + self.current_y_pxpos_elem),
                                               size=UI.EBOX['size'],
                                               style=wx.TE_PROCESS_ENTER))

                        editbox.SetForegroundColour(UI.ECOLOR2['FG'])  # set color
                        editbox.SetBackgroundColour(UI.ECOLOR2['BG'])  # set color

                        editbox.Bind(wx.EVT_TEXT, self.EvtText)
                        editbox.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver)
                        #editbox.Bind(wx.EVT_LEAVE_WINDOW, self.onMouseLeave)


                        elem_dict = {param: [{'ebox': [editbox, value]},
                                             {'headline': headline},
                                             {'text': text},
                                             {'button': button}]}

                        ui_elem_handler_dict.update(elem_dict)

                        self.current_y_pxpos_elem += 20

                    self.param_dict[section].update(ui_elem_handler_dict)

        self.expandCollapse(None, refresh=True)
        self.refresh_UI()
        self.KST.start()

    # ------------------------------------------------------------------------------------------------------------------
    def refresh_UI(self):
        for section in self.section_list:
            section_params = ini_worker.get_section_from_ini(self.configFile, section)
            for param, value in section_params.iteritems():
                if param == 'hideSection':
                    hideSection = value

            if not hideSection:
                for param, value in section_params.iteritems():
                    if param == 'create':
                        if int(value):
                            keys = self.param_dict[section].keys()
                            self.param_dict[section][keys[0]][1]['headline'].SetForegroundColour(UI.TOK['FG'])
                            self.param_dict[section][keys[0]][1]['headline'].Hide()
                            self.param_dict[section][keys[0]][1]['headline'].Show()
                        else:
                            keys = self.param_dict[section].keys()
                            self.param_dict[section][keys[0]][1]['headline'].SetForegroundColour(UI.TERROR['FG'])
                            self.param_dict[section][keys[0]][1]['headline'].Hide()
                            self.param_dict[section][keys[0]][1]['headline'].Show()

                    if param not in self.black_list:
                        if self.param_dict[section][param][0]['ebox'][1] != value:
                            self.param_dict[section][param][0]['ebox'][0].SetForegroundColour(UI.ECOLOR2CHANGE['FG'])  # set color
                            self.param_dict[section][param][0]['ebox'][0].SetBackgroundColour(UI.ECOLOR2CHANGE['BG'])
                            self.param_dict[section][param][0]['ebox'][0].SetValue(str(value))
                            self.param_dict[section][param][0]['ebox'][1] = value

                            if self.section_EC_stat[section]:
                                self.param_dict[section][param][0]['ebox'][0].Hide()
                                self.param_dict[section][param][0]['ebox'][0].Show()

    # ------------------------------------------------------------------------------------------------------------------
    def EvtText(self, event):
        value = event.GetString()
        editbox_name = event.EventObject.GetName()

        section = editbox_name.split('-')[0].strip()
        param = editbox_name.split('-')[1].strip()

        self.GOC.inject_param_changed(str(param))

        self.KST.insert_last_key_stroke_time()
        self.KST.insert_parameter(section, param, value)

    # ------------------------------------------------------------------------------------------------------------------
    def expandCollapse(self, event, refresh=False):
        if not refresh:
            section_clicked = event.EventObject.GetName()
            if self.section_EC_stat[section_clicked]:
                self.section_EC_stat[section_clicked] = 0
                ini_worker.write_to_section(self.configFile, section_clicked, 'collapse', 0)
            else:
                self.section_EC_stat[section_clicked] = 1
                ini_worker.write_to_section(self.configFile, section_clicked, 'collapse', 1)

        self.GOC.inject_param_changed('collapse')

        self.current_y_pxpos_elem = 0
        param_indentation = 10
        headline_placed = False

        # for section, params in self.param_dict.iteritems():
        for section in self.section_list:
            if section in self.param_dict:
                for param, value in self.param_dict[section].iteritems():

                    if self.section_EC_stat[section]:
                        # value[0].ShowWithEffect(10, timeout=30)
                        if not headline_placed:
                            value[1]['headline'].SetPosition([UI.THEADERSTART['pos'][0],
                                                              UI.THEADERSTART['pos'][1] + self.current_y_pxpos_elem])
                            value[3]['button'].SetPosition([UI.BEXPAND['pos'][0],
                                                            UI.THEADERSTART['pos'][1] + self.current_y_pxpos_elem])
                            headline_placed = True
                            self.current_y_pxpos_elem += 20

                        value[0]['ebox'][0].Show()
                        value[1]['headline'].Show()
                        value[2]['text'].Show()
                        value[0]['ebox'][0].SetPosition([UI.EBOX['pos'][0],
                                                         UI.THEADERSTART['pos'][1] + self.current_y_pxpos_elem])
                        value[2]['text'].SetPosition([UI.THEADERSTART['pos'][0] + param_indentation,
                                                      UI.THEADERSTART['pos'][1] + self.current_y_pxpos_elem])

                        self.current_y_pxpos_elem += 20

                    else:
                        # value[0].HideWithEffect(10, timeout=30)
                        if not headline_placed:

                            value[1]['headline'].SetPosition([UI.THEADERSTART['pos'][0],
                                                              UI.THEADERSTART['pos'][1] + self.current_y_pxpos_elem])

                            value[3]['button'].SetPosition([UI.BEXPAND['pos'][0],
                                                            UI.THEADERSTART['pos'][1] + self.current_y_pxpos_elem])

                            headline_placed = True
                            self.current_y_pxpos_elem += 20

                        value[0]['ebox'][0].Hide()
                        value[2]['text'].Hide()

                headline_placed = False

    # ------------------------------------------------------------------------------------------------------------------
    def onMouseEvents(self, event):
        if event.LeftDown():
            M_POSITION = wx.GetMousePosition()
            self.X_DELTA = self.DISPLAY_SIZE.width - M_POSITION[0]
            # self.Y_DELTA = self.DISPLAY_SIZE.height - M_POSITION[1]

            M_POSITION = wx.GetMousePosition()
            PG_POSITION = self.GetScreenPosition()
            self.P_DELTA = M_POSITION - PG_POSITION

        if event.LeftIsDown():
            M_POSITION = wx.GetMousePosition()
            DS = self.GetSize()
            SP = self.GetScreenPosition()

            # if M_POSITION[0] + self.P_DELTA[0] > self.DISPLAY_SIZE.width - 10:
            #     self.SetSizeWH(DS[0], self.DISPLAY_SIZE.height + 10)
            #     # self.SetPosition((self.DISPLAY_SIZE.width - DS[0] + 10, 0))
            #     self.SetPosition((self.DISPLAY_SIZE.width - DS[0] + 10, 0))
            # else:
            #     self.SetPosition((M_POSITION[0] - self.P_DELTA[0], M_POSITION[1] - self.P_DELTA[1]))
            self.SetPosition((M_POSITION[0] - self.P_DELTA[0], M_POSITION[1] - self.P_DELTA[1]))

        elif event.Leaving():
            time.sleep(0.3)
            PG_SIZE = self.GetSize()
            M_POSITION = wx.GetMousePosition()
            PG_POSITION = self.GetScreenPosition()

            X_COLLAPSED = 10
            X_EXPAND = 335

            if self.PG_expanded:
                self.PG_expanded = False
                if M_POSITION[0] < PG_POSITION[0] or M_POSITION[0] > PG_POSITION[0] + PG_SIZE[0]:
                    self.SetSizeWH(self.MIN_SIZE_W, PG_SIZE[1])
                    NEW_PG_SIZE = self.GetSize()
                    NEW_PG_POSITION = self.GetScreenPosition()
                    X_DELTA = abs(335 - NEW_PG_SIZE[0])
                    self.SetPosition((NEW_PG_POSITION[0] + X_DELTA, NEW_PG_POSITION[1]))
                    return

                if M_POSITION[1] < PG_POSITION[1] or M_POSITION[1] > PG_POSITION[1] + PG_SIZE[1]:
                    self.SetSizeWH(18, PG_SIZE[1])
                    NEW_PG_SIZE = self.GetSize()
                    NEW_PG_POSITION = self.GetScreenPosition()
                    X_DELTA = abs(335 - NEW_PG_SIZE[0])
                    self.SetPosition((NEW_PG_POSITION[0] + X_DELTA, NEW_PG_POSITION[1]))
                    return
        else:
            M_POSITION = wx.GetMousePosition()
            PG_POSITION = self.GetScreenPosition()
            self.P_DELTA = M_POSITION - PG_POSITION

            PG_SIZE = self.GetSize()
            X_EXPAND = 335
            X_DELTA = X_EXPAND - PG_SIZE[0]
            self.PG_expanded = True
            self.SetSizeWH(X_EXPAND, PG_SIZE[1])
            self.SetPosition((PG_POSITION[0]-X_DELTA, PG_POSITION[1]))


    # ------------------------------------------------------------------------------------------------------------------
    def onMouseOver(self, event):

        if event.LeftIsDown():
            M_POSITION = wx.GetMousePosition()
            self.SetPosition((M_POSITION[0] - self.P_DELTA[0], M_POSITION[1] - self.P_DELTA[1]))
        else:
            M_POSITION = wx.GetMousePosition()
            PG_POSITION = self.GetScreenPosition()
            self.P_DELTA = M_POSITION - PG_POSITION

            PG_SIZE = self.GetSize()
            X_EXPAND = 335
            X_DELTA = X_EXPAND - PG_SIZE[0]
            self.PG_expanded = True
            # for x_plus in range(X_EXPAND):
            # self.SetSizeWH(X_EXPAND, PG_SIZE[1])
            self.SetSizeWH(X_EXPAND, PG_SIZE[1])
            self.SetPosition((PG_POSITION[0]-X_DELTA, PG_POSITION[1]))

    # ------------------------------------------------------------------------------------------------------------------
    def onMouseLeave(self, event):
        time.sleep(0.3)
        PG_SIZE = self.GetSize()
        M_POSITION = wx.GetMousePosition()
        PG_POSITION = self.GetScreenPosition()

        X_COLLAPSED = 10
        X_EXPAND = 335

        if self.PG_expanded:
            self.PG_expanded = False
            if M_POSITION[0] < PG_POSITION[0] or M_POSITION[0] > PG_POSITION[0] + PG_SIZE[0]:
                self.SetSizeWH(self.MIN_SIZE_W, PG_SIZE[1])
                NEW_PG_SIZE = self.GetSize()
                NEW_PG_POSITION = self.GetScreenPosition()
                X_DELTA = abs(335 - NEW_PG_SIZE[0])
                self.SetPosition((NEW_PG_POSITION[0] + X_DELTA, NEW_PG_POSITION[1]))
                return

            if M_POSITION[1] < PG_POSITION[1] or M_POSITION[1] > PG_POSITION[1] + PG_SIZE[1]:
                self.SetSizeWH(self.MIN_SIZE_W, PG_SIZE[1])
                NEW_PG_SIZE = self.GetSize()
                NEW_PG_POSITION = self.GetScreenPosition()
                X_DELTA = abs(335 - NEW_PG_SIZE[0])
                self.SetPosition((NEW_PG_POSITION[0] + X_DELTA, NEW_PG_POSITION[1]))
                return

            # self.Re
            # self.SetIcon('')


    # ------------------------------------------------------------------------------------------------------------------
    def OnSize(self, selff):
        PG_SIZE = self.GetSize()
        if PG_SIZE[0] > 335:
            self.SetSizeWH(335, PG_SIZE[1])

    # ------------------------------------------------------------------------------------------------------------------
    def OnExit(self, event):
        self.Destroy()
        self.GOC.inject_runstat(False)
        self.KST.kill_sheduler()
        PG_XY = self.GetScreenPosition()
        ini_worker.write_to_section(self.PGconfigFileCore, 'UISETTINGS', 'lastWindowPosition', str(PG_XY))
        PG_SIZE = self.GetSize()
        PG_SIZE[0] = self.MIN_SIZE_W
        ini_worker.write_to_section(self.PGconfigFileCore, 'UISETTINGS', 'lastWindowSize', str(PG_SIZE))

# ------------------------------------------------------------------------------------------------------------------
def main():
    """
    # pluginPath = 'D:\\MWAdditive'
    # corePath = 'D:\\MWAdditive'
    # configFile = 'Mesh.ini'
    # PG = parameterGuardUI(pluginPath, corePath, configFile)
    :return:
    """

    if len(sys.argv) >= 4:
        app = wx.App(False)
        PG = parameterGuardUI(sys.argv[1], sys.argv[2], sys.argv[3])  # pass absolute pathes here
        app.MainLoop()
    else:
        print 'Please pass plugin, core path and config file location.'
        print 'Trying to start with some default development params.'
        pluginPath = 'C:\\MWAdditive'
        corePath = 'C:\\MWAdditive'
        configFile = 'Mesh.ini'
        app = wx.App(False)
        PG = parameterGuardUI(pluginPath, corePath, configFile)
        app.MainLoop()

if __name__== "__main__":
    main()

