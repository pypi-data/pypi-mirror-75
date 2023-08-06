import sys
from datetime import datetime

def info(*args):                                                                      
    pref = datetime.now().strftime('[%y%m%d %H:%M:%S]')
    print(pref, *args, file=sys.stdout)
