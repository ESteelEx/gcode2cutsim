import time
from threading import Thread
from Utilities import ini_worker

class key_stroke_timer(Thread):
    def __init__(self, configFile, time_init=time.time()):
        Thread.__init__(self)
        self.configFile = configFile
        self.time_init = time_init
        self.last_key_stroke = None
        self.section = None
        self.param = None
        self.value = None
        self.time_interval = 3
        self.running = 1

    # ------------------------------------------------------------------------------------------------------------------
    def run(self):
        while self.running:
            while self.last_key_stroke == None:
                if not self.running:
                    break
            if not self.running:
                break

            # time.sleep(self.time_interval)
            time_delta = 0
            while time_delta <= self.time_interval:
                time_delta = time.time() - self.last_key_stroke

            if str(ini_worker.get_param_from_ini(self.configFile, self.section, self.param)) != str(self.value):
                ini_worker.write_to_section(self.configFile,
                                            self.section,
                                            self.param,
                                            self.value)

            self.last_key_stroke = None

        print '--|X|-- key guard unplugged'

    # ------------------------------------------------------------------------------------------------------------------
    def insert_parameter(self, section, param, value):
        self.section = section
        self.param = param
        self.value = value

    # ------------------------------------------------------------------------------------------------------------------
    def insert_last_key_stroke_time(self):
        self.last_key_stroke = time.time()

    # ------------------------------------------------------------------------------------------------------------------
    def kill_sheduler(self):
        """
        Kill key stroke timer with bool 0
        :return:
        """
        self.running = 0