from os.path import abspath, dirname, join
from Project import Project


class Webdriver(Project):

    def __init__(self):
        super().__init__()

    @property
    def base_folder(self):
        return join(self.root_path, "driver", "webdriver")

    def chrome_driver(self):
        from driver.webdriver.setup import Chrome
        return Chrome()


if __name__ == "__main__":
    pass
