import platform
import getpass

def on_wsl() -> bool:
    """ Function that will detect if the program is runned on wsl

    Returns
    -------
    isOnWSL : bool
        Boolean value that indicates if the program is on wsl
    """
    isOnWSL=False
    
    uname=platform.uname()
    system=uname[0]
    release=uname[2]

    if system.lower() == 'linux' and 'microsoft' in release.lower():
        isOnWSL=True
    return isOnWSL

def get_platform_name() -> str:
    """ Gets the name of the platform in lowercase

    Returns
    -------
    system : str
        Name of the platform (lowercase)
    """
    return platform.system().lower()

def get_user_name() -> str:
    """ Gets the username of the device

    Returns
    -------
    username : str
        Username of the device
    """
    return getpass.getuser()
