from os.path import abspath, dirname, join
import sys


class Project:

    def __init__(self):
        pass

    @property
    def root_path(self):
        return abspath(join(dirname(__file__), ".."))

    @property
    def lib_path(self):
        return join(self.root_path, "lib")

    @property
    def python_site_package_path(self):
        return join(self.lib_path, "site-packages")
    
    @property
    def script_path(self):
        return join(self.root_path, "script")

    def path_initialize(self):
        paths = [self.root_path,
                 self.lib_path,
                 self.python_site_package_path,
                 self.script_path]

        for path in paths:
            if path not in sys.path:
                sys.path.append(path)

if __name__ == "__main__":
    pass
