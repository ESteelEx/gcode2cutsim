# # UI configuration file
# # define size and position of main window and all elements
#
########################################################################################################################
#                                               UI SETTINGS SECTION
########################################################################################################################
# MAIN WINDOW
# ----------------------------------------------------------------------------------------------------------------------
WMAIN = {'pos': (500, 500), 'size': (335, 800)}

# TEXT FIELDS
# ----------------------------------------------------------------------------------------------------------------------
THEADERSTART = {'pos': (20, 10),  'size': (), 'label': ''}

# EDIT FIELDS
# ----------------------------------------------------------------------------------------------------------------------
EBOX = {'pos': (200, 10),  'size': (100, 20)}

# CHECKBOX
# ----------------------------------------------------------------------------------------------------------------------
CBTODAY =     {'pos': (20, 240), 'label': 'Use todays date for daily versions on startup'}
CBCRYPT =     {'pos': (20, 260), 'label': 'Crypt my user data in config file. (recommended)'}
CBCPMACH =    {'pos': (20, 280), 'label': 'Always copy machine definitions after download'}
CBUPDATE =    {'pos': (20, 300), 'label': 'Proof for update on startup'}
CBAUTOSTART = {'pos': (20, 320), 'label': 'Start with Windows'}


# BUTTONS
# ----------------------------------------------------------------------------------------------------------------------
BCHOOSEF = {'pos': (280, 200), 'size': (30, 25)}
BCU =      {'pos': (280, 300), 'size': (30, 25)}
BSAVE =    {'pos': (220, 355), 'size': (100, 25)}
BEXPAND =  {'pos': (), 'size': (12, 12)}

########################################################################################################################
#                                                   COLOR SECTION
########################################################################################################################
#
# GROUP COLORS
# ----------------------------------------------------------------------------------------------------------------------
WCOLOR =     {'FG': (), 'BG': (90, 90, 90)}
TCOLOR =     {'FG': (255, 255, 255), 'BG': ()}
ECOLOR =     {'FG': (80, 80, 80), 'BG': (220, 220, 220)}
ECOLOR2 =    {'FG': (200, 200, 200), 'BG': (120, 120, 120)}
ECOLOR2CHANGE =    {'FG': (250, 250, 250), 'BG': (180, 180, 180)}
BCOLOR =     {'FG': (80, 80, 80), 'BG': (220, 220, 220)}
PARAMCOLOR = {'FG': (150, 150, 150), 'BG': (220, 220, 220)}