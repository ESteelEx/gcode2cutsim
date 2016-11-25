import os


def sim_files(gcodef, simf):
    update_flg = False
    gcodet = os.path.getmtime(gcodef)
    simt = os.path.getmtime(simf)
    gcodes = os.path.getsize(gcodef)
    sims = os.path.getsize(simf)

    if simt - gcodet > 0:
        print 'Sim file is newer then G-Code. Up to date.'
        if gcodes > sims:
            print 'Sim file seems to be incomplete. Recalculation needed.'
            update_flg = True
    else:
        print 'Recalculate sim file'
        update_flg = True

    return update_flg