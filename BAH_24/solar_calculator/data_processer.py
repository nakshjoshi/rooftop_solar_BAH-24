import utils
from consts import *

def check_address(address):
    lat, long = utils.geocode(address)
    
    if MIN_LAT <= lat <= MAX_LAT and MIN_LONG <= long <= MAX_LONG:
        return True
    
    return False

