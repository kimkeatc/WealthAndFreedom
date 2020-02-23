import os
from os.path import abspath, dirname, exists, join
from sys import path

_PROJECT_BASE_PATH = abspath(join(dirname(__file__), ".."))
     

class ProjectPath:

    def __init__(self, root):
        self.root = root
        self.add_sys_path()

    def add_sys_path(self):
        plist = [self.etc, self.lib, self.lib_site_packages]
        for p in plist:
            if p not in path:
                path.insert(1, p)

    def bin_fldr(self):
        return "bin"
    def database_fldr(self):
        return "fldr"
    def doc_fldr(self):
        return "doc"
    def driver_fldr(self):
        return "driver"
    def etc_fldr(self):
        return "etc"
    def history_fldr(self):
        return "history"
    def lib_fldr(self):
        return "Lib"
    def lib_site_package_fldr(self):
        return join(self.lib_fldr(), "site-packages")
    def log_fldr(self):
        return "log"

    @property
    def bin(self):
        return join(self.root, self.bin_fldr())
    @property
    def database(self):
        return join(self.root, self.database_fldr())
    @property
    def doc(self):
        return join(self.root, self.doc_fldr())
    @property
    def driver(self):
        return join(self.root, self.driver_fldr())
    @property
    def etc(self):
        return join(self.root, self.etc_fldr())
    @property
    def history(self):
        return join(self.root, self.history_fldr())
    @property
    def lib(self):
        return join(self.root, self.lib_fldr())
    @property
    def lib_site_packages(self):
        return join(self.root, self.lib_site_package_fldr())
    @property
    def log(self):
        return join(self.root, self.log_fldr())


class CollateralsPath(ProjectPath):

    def __init__(self, root):
        super(CollateralsPath, self).__init__(root)
        
    def create_path(self, _path, create_if_not_exists=False):
        if not exists(_path):
            if create_if_not_exists:
                os.mkdir(_path)
                return self.create_path(_path)
            else:
                return 1
        return 0
            
        
    def get_path(self, fnc):
        """ To ensure specific item is existing.

        Args:-
         - fnc : Class attribute function

        Output:-
         - ipath   : Specific item path directory

        Usage:-
         p = CollateralsPath(_PROJECT_BASE_PATH)
         f = p.get_path((p.holiday_excel_file_path))
         print(f)

        """
        
        ipath = fnc()
        if not exists(ipath):
            print("Missing Item - %s" % ipath)
            raise FileNotFoundError
        return ipath

    def holiday_excel_file(self):
        return "holidays.xlsx"
    def holiday_excel_file_path(self):
        return join(self.bin, self.holiday_excel_file())

    def webdriver_chrome(self):
        return "chromedriver.exe"
    def webdriver_chrome_path(self):
        return join(self.driver, "webdriver", "chrome", "77.0.3865.40", self.webdriver_chrome())
    
    def daily_log_path(self, date):
        return join(self.log, date)
        
def _ppath():
    return CollateralsPath(_PROJECT_BASE_PATH)
