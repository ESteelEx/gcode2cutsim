import os


def sim_files(gcodef, simf):
    update_flg = False
    if os.path.isfile(gcodef) and os.path.isfile(simf):
        gcodet = os.path.getmtime(gcodef)
        simt = os.path.getmtime(simf)
        gcodes = os.path.getsize(gcodef)
        sims = os.path.getsize(simf)

        if simt - gcodet > 0:
            print 'Simulation file ' + simf + ' is up to date.'
            if gcodes > sims:
                print 'Sim file seems to be incomplete. Recalculation needed.'
                update_flg = True
        else:
            print 'Recalculating simulation files'
            update_flg = True
    else:
        update_flg = True

    return update_flg