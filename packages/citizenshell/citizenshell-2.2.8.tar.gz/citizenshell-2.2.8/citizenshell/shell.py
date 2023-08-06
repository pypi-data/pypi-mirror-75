from .parseduri import ParsedUri
from .telnetshell import TelnetShell
from .localshell import LocalShell
from .secureshell import SecureShell
from .adbshell import AdbShell
from .serialshell import SerialShell

def Shell(uri=None, **kwargs):
    if not uri:
        return LocalShell(**kwargs)

    parsed_uri = ParsedUri(uri, **kwargs)
    if parsed_uri.scheme == "telnet":
        return TelnetShell(hostname=parsed_uri.hostname, username=parsed_uri.username, 
                           password=parsed_uri.password, port=parsed_uri.port, **parsed_uri.kwargs)
    elif parsed_uri.scheme == "ssh":
        return SecureShell(hostname=parsed_uri.hostname, username=parsed_uri.username, 
                           password=parsed_uri.password, port=parsed_uri.port, **parsed_uri.kwargs)
    elif parsed_uri.scheme == "adb":
        return AdbShell(hostname=parsed_uri.hostname, port=parsed_uri.port, **parsed_uri.kwargs)
    elif parsed_uri.scheme == "serial":
        return SerialShell(port=parsed_uri.port, username=parsed_uri.username, 
                           password=parsed_uri.password, baudrate=parsed_uri.baudrate, **parsed_uri.kwargs)
            
    raise RuntimeError("unknwon scheme '%s'" % parsed_uri.scheme)
