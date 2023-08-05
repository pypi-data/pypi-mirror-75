# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from enum import Enum

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# --------------------------------------------------------- class: TimeInterval ---------------------------------------------------------- #

class TimeInterval(Enum):
    NOW     = 'now'
    DAY     = 'day'
    WEEK    = 'week'
    MONTH   = 'month'
    YEAR    = 'year'
    ALL     = 'all'


# ---------------------------------------------------------------------------------------------------------------------------------------- #