from cli.interpreter import Interpreter
from pystemd.systemd1 import Unit
from pystemd.dbusexc import DBusInvalidArgsError
from cli.print_utils import error


if __name__ == "__main__":
    unit = Unit(b'docker.service', _autoload=True)
    try:
        if unit.Unit.ActiveState == b"inactive":
            error("Docker is not running. Try `sudo service docker start`")
        else:
            zsc_interpreter = Interpreter()
            zsc_interpreter.start()
    except DBusInvalidArgsError:
        error("Docker is not installed. Try `sudo apt install docker.io`")
