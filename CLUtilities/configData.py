from Utilities import ini_worker

class configData():
    def __init__(self, configFile):
        self.configFile = configFile

    # ------------------------------------------------------------------------------------------------------------------
    def get_simulation_data(self):
        sim_params = ini_worker.get_section_from_ini(self.configFile, 'SIMULATION')

        return sim_params
