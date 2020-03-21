from os.path import abspath, dirname, join
import sys

PROJECT_ROOT_PATH = abspath(join(dirname(__file__), ".."))


class ProjectPath:

    def __init__(self, root):
        self.root = root

    @property
    def bin(self):
        return "bin"
    @property
    def database(self):
        return "db"
    @property
    def documents(self):
        return "docs"
    @property
    def driver(self):
        return "driver"
    @property
    def history(self):
        return "history"
    @property
    def lib(self):
        return "lib"
    @property
    def logs(self):
        return "logs"
    @property
    def script(self):
        return "script"

    def bin_folder(self):
        return join(self.root, self.bin)
    def database_folder(self):
        return join(self.root, self.database)
    def documents_folder(self):
        return join(self.root, self.documents)
    def driver_folder(self):
        return join(self.root, self.driver)
    def history_folder(self):
        return join(self.root, self.history)
    def lib_folder(self):
        return join(self.root, self.lib)
    def logs_folder(self):
        return join(self.root, self.logs)
    def script_folder(self):
        return join(self.root, self.script)
    def site_packages_folder(self):
        return join(self.lib_folder(), "site-packages")

    def initialize(self):
        paths = [self.script_folder(), self.lib_folder(), self.site_packages_folder(), self.root]

        for index, path in enumerate(paths):
            if path not in sys.path:
                sys.path.insert(1, path)

class Tool:

    def __init__(self):
        self.cls = project_path()

    def ChromeWebdriver(self):
        return self.Webdriver().Webdriver().getChromeDriver("75.0.3770.140")

    def Webdriver(self):
        from driver.webdriver import setup
        return setup

def project_path():
    cls = ProjectPath(PROJECT_ROOT_PATH)
    try:
        cls.initialize()
    except Exception as e:
        print(e)
        raise Exception("Project path initialization failure.")
    return cls
