

# ------------------------------------------------------------------------------------------------------------------
def get_section_from_ini(fileName, section):
    """
    :param fileName: pass relative ini-file location as string
    :param section: pass INI section as string to read
    :return: dict of all params in ini section. If possible values are stored as float
    """
    with open(fileName) as fh:
        ini_content = fh.readlines()
        section_dict = {}
        for i, j in zip(ini_content, range(len(ini_content))):
            if i.strip().find('[') == 0:
                # if i.find(section) != -1:
                if i[1:-2] == section:
                    section_end = False
                    for ii in ini_content[j+1:]:
                        if len(ii.strip()) != 0:
                            if ii.strip()[0] != ';':
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

# ------------------------------------------------------------------------------------------------------------------
def get_sections_list_from_ini(fileName):
    """
    :param fileName: pass relative ini-file location as string
    :return: all sections in ini file as list of strings
    """
    with open(fileName) as fh:
        ini_content = fh.readlines()
        sections_list = []
        for i, j in zip(ini_content, range(len(ini_content))):
            if i.strip().find('[') == 0:
                sections_list += [i[1:-2].strip()]

    return sections_list

# ------------------------------------------------------------------------------------------------------------------
def get_comments_by_section(fileName, section):
    """

    :param fileName:
    :param section:
    :return:
    """
    with open(fileName) as fh:
        ini_content = fh.readlines()
        comment_dict = {}
        for i, j in zip(ini_content, range(len(ini_content))):
            if i.strip().find('[') == 0:
                if i[1:-2] == section:
                    section_end = False
                    for ii, jj in zip(ini_content[j+1:], range(len(ini_content[j+1]))):
                        if ii.strip().find('[') == 0:
                            section_end = True
                            break
                        if len(ii.strip()) != 0:
                            if ii.strip()[0] == ';':
                                for iii in ini_content[jj+j+1:]:
                                    if iii.strip().find('=') > 1:
                                        key = iii.split('=')[0]

                                comment = ii[ii.strip().find(';')+1:].strip()
                                comment_dict[key] = comment

                    if section_end:
                        break

    return comment_dict

# ------------------------------------------------------------------------------------------------------------------
def write_to_section(fileName, section, param, param_value):
    """

    :param fileName:
    :param section:
    :return:
    """
    with open(fileName) as fh:
        ini_content = fh.readlines()
        section_end = False
        for i, j in zip(ini_content, range(len(ini_content))):
            if section_end:
                break
            if i.strip().find('[') == 0:
                if i[1:-2] == section:

                    for ii, jj in zip(ini_content[j+1:], range(len(ini_content[j+1]))):
                        if section_end:
                            break
                        if len(ii.strip()) != 0:
                            for iii, jjj in zip(ini_content[jj+j+1:], range(len(ini_content[jj+j+1:])) ):
                                if iii.strip().find('[') == 0:
                                    section_end = True
                                    break
                                if iii.strip().find('=') > 1:
                                    key = iii.split('=')[0]
                                    if key == param:
                                        ini_content[jj+j+jjj+1] = key + '=' + str(param_value) + '\n'

    fh = open(fileName, 'w')
    for line in ini_content:
        fh.write(line)

    fh.close()
