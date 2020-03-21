from os.path import abspath, dirname, join
from pathlib import Path
import sys

_REPO = abspath(Path(__file__).absolute().parents[1])


class Project:

    def __init__(self):
        self._path = _REPO

    @property
    def path(self):
        return self._path

    @property
    def bin(self):
        return bin()

    @property
    def data(self):
        return data()

    @property
    def driver(self):
        return driver()

    @property
    def etc(self):
        return etc()

    @property
    def Lib(self):
        return Lib()

    @property
    def script(self):
        return script()


class bin(Project):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_classname(cls):
        return cls.__name__

    @property
    def name(self):
        return self.get_classname()

    @property
    def path(self):
        return join(super().path, self.name)


class data(Project):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_classname(cls):
        return cls.__name__

    @property
    def name(self):
        return self.get_classname()

    @property
    def path(self):
        return join(super().path, self.name)


class driver(Project):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_classname(cls):
        return cls.__name__

    @property
    def name(self):
        return self.get_classname()

    @property
    def path(self):
        return join(super().path, self.name)

    @property
    def webdriver(self):
        return webdriver()


class etc(Project):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_classname(cls):
        return cls.__name__

    @property
    def name(self):
        return self.get_classname()

    @property
    def path(self):
        return join(super().path, self.name)


class Lib(Project):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_classname(cls):
        return cls.__name__

    @property
    def name(self):
        return self.get_classname()

    @property
    def path(self):
        return join(super().path, self.name)


class script(Project):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_classname(cls):
        return cls.__name__

    @property
    def name(self):
        return self.get_classname()

    @property
    def path(self):
        return join(super().path, self.name)


class webdriver:

    def __init__(self):
        pass

    @classmethod
    def get_classname(cls):
        return cls.__name__

    @property
    def name(self):
        return self.get_classname()

    @property
    def path(self):
        return join(driver().path, self.name)

    @property
    def Chrome(self):
        return Webdriver_Chrome()


class Webdriver_Chrome:

    latest_version = "77.0.3865.40"

    def __init__(self):
        pass

    @property
    def name(self):
        return "Chrome"

    @property
    def path(self):
        return join(webdriver().path, self.name)

    @property
    def driver(self):
        return "chromedriver.exe"

    def driver_path(self, version=None):
        if not version:
            version = self.latest_version
        version = str(version)
        path = join(self.path, version, self.driver)
        return path


def sys_path_initialize():
    project = Project()
    paths = [project.path, project.Lib.path, project.script.path]
    for path in paths:
        if path not in sys.path:
            sys.path.append(path)


if __name__ == "__main__":
    sys_path_initialize()
