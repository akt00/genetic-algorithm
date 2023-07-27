# available outside of "ga" package (from)
from . import genome
# only available inside "ga" package (import)
import os


if os.getenv('PYCHARM_HOSTED'):
    print('ga package init')
