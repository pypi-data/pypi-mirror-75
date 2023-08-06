##############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
##############################################################################

# TODO Fix this

import numpy as np

from ..finutils.FinMath import N
from ..finutils.FinHelperFunctions import labelToString
from ..finutils.FinOptionTypes import FinOptionTypes
from ..finutils.FinError import FinError

###############################################################################
# TODO: Use Numba ?
###############################################################################


class FinModelBlack():
    ''' Black's Model which prices call and put options in the forward
    measure according to the Black-Scholes equation. '''

    def __init__(self, volatility, implementation=0):
        ''' Create FinModel black using parameters. '''
        self._volatility = volatility
        self._implementation = 0
        self._numSteps = 0
        self._seed = 0
        self._param1 = 0
        self._param2 = 0

###############################################################################

    def value(self,
              forwardRate,   # Forward rate F
              strikeRate,    # Strike Rate K
              timeToExpiry,  # Time to Expiry (years)
              df,            # Discount Factor to expiry date
              callOrPut):    # Call or put
        ''' Price a derivative using Black's model which values in the forward
        measure following a change of measure. '''

        if strikeRate < 0.0:
            raise FinError("Strike must not be negative")

        if timeToExpiry < 0.0:
            raise FinError("Time to expiry is negative.")

        if self._volatility < 0.0:
            raise FinError("Volatility is negative.")

        f = forwardRate
        t = timeToExpiry
        k = strikeRate
        sqrtT = np.sqrt(t)
        vol = self._volatility

        if abs(t) < 1e-10:
            t = 1e-10
            sqrtT = np.sqrt(t)

        if abs(vol) < 1e-10:
            vol = 1e-10

        if abs(k) < 1e-10:
            k = 1e-10

        d1 = (np.log(f/k) + vol * vol * t / 2.0) / (vol * sqrtT)
        d2 = d1 - vol*sqrtT

        print(f, k, d1, d2)

        if callOrPut == FinOptionTypes.EUROPEAN_CALL:
            v = df * (f * N(d1) - k * N(d2))
        elif callOrPut == FinOptionTypes.EUROPEAN_PUT:
            v = df * (k * N(-d2) - f * N(-d1))
        else:
            raise FinError("Option type must be a European Call or Put")

 #       print(f,t,k,vol,df,v)

        return v

###############################################################################

    def __repr__(self):
        s = "FINMODELBLACK"
        s += labelToString("VOLATILITY", self._volatility)
        s += labelToString("IMPLEMENTATION", self._implementation)
        s += labelToString("NUMSTEPS", self._numSteps)
        return s

###############################################################################
