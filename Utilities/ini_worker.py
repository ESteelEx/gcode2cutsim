

# ------------------------------------------------------------------------------------------------------------------
def get_section_from_ini(fileName, section):
    """
    :param fileName: pass relative ini-file location as string
    :param section: pass INI section as string to read
    :return: dict of all params in ini section. If possible values are stored as float
    """
    with open(fileName) as fh:
        ini_content = fh.readlines()
        for i, j in zip(ini_content, range(len(ini_content))):
            if i.strip().find('[') == 0:
                if i.find(section) != -1:
                    section_dict = {}
                    for ii in ini_content[j+1:]:
                        if ii.strip().find('[') == 0 or ii.strip().find('=') == -1:
                            section_end = True
                            break
                        key = ii[:ii.strip().find('=')].strip()
                        value = ii[ii.strip().find('=')+1:].strip()
                        try:
                            value = float(value)
                        except:
                            pass
                        section_dict[key] = value
                    if section_end:
                        break

    return section_dict