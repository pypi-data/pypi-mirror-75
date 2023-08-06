##############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
##############################################################################

##########################################################################
# THIS IS UNFINISHED
##########################################################################

from ...finutils.FinDayCount import FinDayCountTypes
from ...finutils.FinCalendar import FinCalendarTypes

##########################################################################


def FinLiborConventions(currencyName: str,
                        indexName: str = "LIBOR"):
    ''' This function is untested but returns country specific Libor-related
    conventions. '''

    if currencyName == "USD" and indexName == "LIBOR":
        spotLag = 2
        dayCountType = FinDayCountTypes.THIRTY_E_360_ISDA
        calendarType = FinCalendarTypes.TARGET
    elif currencyName == "EUR"and indexName == "EURIBOR":
        spotLag = 2
        dayCountType = FinDayCountTypes.THIRTY_E_360_ISDA
        calendarType = FinCalendarTypes.TARGET

    return (spotLag, dayCountType, calendarType)

###############################################################################
