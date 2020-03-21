from script.Project import Project
from script import Bursa
import sys

__filename__ = "fiavest"


def main():

    project = Project()
    project.path_initialize()

    return


if __name__ == "__main__":
    print("Execute script %s" % __filename__ )
    returncode = main()
    sys.exit(returncode)
