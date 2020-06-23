import logging
import logging.handlers

def init():
    logging.basicConfig()
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    filehandler = logging.FileHandler(filename="log/log.log")
    format = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    filehandler.setFormatter(format)
    filehandler.suffix = "%Y-%m-%d.log"
    root.addHandler(filehandler)