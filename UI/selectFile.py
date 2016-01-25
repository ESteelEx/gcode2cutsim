import wx

def get_file_list():
    # ask user which file to open
    """
    :rtype : list with file names
    """
    wapp = wx.PySimpleApp()

    openFileDialog = wx.FileDialog(None, "Choose GCODE file", "", "",
                                   "GCODE files (*.gcode)|*.gcode",
                                   wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE | wx.FD_PREVIEW)

    if openFileDialog.ShowModal() == wx.ID_OK:
        image_directory = openFileDialog.GetDirectory()
        list_file_name = openFileDialog.GetFilenames()
    else:
        list_file_name = None
        image_directory = None

    return image_directory, list_file_name