import log

try:
    import colorama
    addLevelName(
        INFO,
        colorama.Fore.GREEN + getLevelName(INFO) + colorama.Style.RESET_ALL)
    addLevelName(
        DEBUG,
        colorama.Fore.WHITE + getLevelName(DEBUG) + colorama.Style.RESET_ALL)
    addLevelName(WARNING, colorama.Fore.YELLOW + getLevelName(WARNING) +
                 colorama.Style.RESET_ALL)
    addLevelName(
        ERROR,
        colorama.Fore.RED + getLevelName(ERROR) + colorama.Style.RESET_ALL)
    addLevelName(
        CRITICAL,
        colorama.Fore.RED + getLevelName(ERROR) + colorama.Style.RESET_ALL)
except ImportError:
    pass

log.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s", level=log.INFO)
