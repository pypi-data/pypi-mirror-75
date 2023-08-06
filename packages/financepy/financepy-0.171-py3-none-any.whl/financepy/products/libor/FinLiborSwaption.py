##############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
##############################################################################

# TODO: Extend to allow term structure of volatility
# TODO: Extend to allow two fixed legs in underlying swap
# TODO: Cash settled swaptions

import numpy as np


from ...finutils.FinCalendar import FinCalendarTypes
from ...finutils.FinCalendar import FinBusDayAdjustTypes
from ...finutils.FinCalendar import FinDateGenRuleTypes
from ...finutils.FinDayCount import FinDayCountTypes
from ...finutils.FinFrequency import FinFrequencyTypes
from ...finutils.FinGlobalVariables import gDaysInYear
from ...finutils.FinMath import ONE_MILLION
from ...finutils.FinError import FinError
from ...finutils.FinHelperFunctions import labelToString, checkArgumentTypes
from ...finutils.FinDate import FinDate

from ...products.libor.FinLiborSwap import FinLiborSwap

from ...models.FinModelBlack import FinModelBlack
from ...models.FinModelBlackShifted import FinModelBlackShifted
from ...models.FinModelSABR import FinModelSABR
from ...models.FinModelSABRShifted import FinModelSABRShifted
from ...models.FinModelRatesHW import FinModelRatesHW
from ...models.FinModelRatesBK import FinModelRatesBK
from ...models.FinModelRatesBDT import FinModelRatesBDT

from ...finutils.FinOptionTypes import FinOptionTypes, FinOptionExerciseTypes
from ...finutils.FinOptionTypes import FinLiborSwaptionTypes

###############################################################################


class FinLiborSwaption():
    ''' This is the class for the European-style swaption, an option to enter
    into a swap (payer or receiver of the fixed coupon), that starts in the
    future and with a fixed maturity, at a swap rate fixed today. '''

    def __init__(self,
                 settlementDate: FinDate,
                 exerciseDate: FinDate,
                 maturityDate: FinDate,
                 swaptionType: FinLiborSwaptionTypes,
                 fixedCoupon: float,
                 fixedFrequencyType: FinFrequencyTypes,
                 fixedDayCountType: FinDayCountTypes,
                 notional: float = ONE_MILLION,
                 floatFrequencyType: FinFrequencyTypes = FinFrequencyTypes.QUARTERLY,
                 floatDayCountType: FinDayCountTypes = FinDayCountTypes.THIRTY_360,
                 calendarType: FinCalendarTypes = FinCalendarTypes.WEEKEND,
                 busDayAdjustType: FinBusDayAdjustTypes = FinBusDayAdjustTypes.FOLLOWING,
                 dateGenRuleType: FinDateGenRuleTypes = FinDateGenRuleTypes.BACKWARD):
        ''' Create a European-style swaption by defining the exercise date of
        the swaption, and all of the details of the underlying interest rate
        swap including the fixed coupon and the details of the fixed and the
        floating leg payment schedules. Bermudan style swaption should be
        priced using the FinLiborBermudanSwaption class. '''

        checkArgumentTypes(self.__init__, locals())

        if settlementDate > exerciseDate:
            raise FinError("Settlement date must be before expiry date")

        if exerciseDate > maturityDate:
            raise FinError("Exercise date must be before swap maturity date")

        self._settlementDate = settlementDate
        self._exerciseDate = exerciseDate
        self._maturityDate = maturityDate
        self._swaptionType = swaptionType

        self._fixedCoupon = fixedCoupon
        self._fixedFrequencyType = fixedFrequencyType
        self._fixedDayCountType = fixedDayCountType
        self._notional = notional
        self._floatFrequencyType = floatFrequencyType
        self._floatDayCountType = floatDayCountType

        self._calendarType = calendarType
        self._busDayAdjustType = busDayAdjustType
        self._dateGenRuleType = dateGenRuleType

        self._pv01 = None
        self._fwdSwapRate = None
        self._forwardDf = None
        self._underlyingSwap = None

###############################################################################

    def value(self,
              valuationDate,
              discountCurve,
              model):
        ''' Valuation of a Libor European-style swaption using a choice of
        models on a specified valuation date. Models include FinModelBlack,
        FinModelBlackShifted, '''

        floatSpread = 0.0
        payFixedFlag = True

        swap = FinLiborSwap(self._exerciseDate,
                            self._maturityDate,
                            self._fixedCoupon,
                            self._fixedFrequencyType,
                            self._fixedDayCountType,
                            self._notional,
                            floatSpread,
                            self._floatFrequencyType,
                            self._floatDayCountType,
                            payFixedFlag,
                            self._calendarType,
                            self._busDayAdjustType,
                            self._dateGenRuleType)

        k = self._fixedCoupon
        pv01 = swap.pv01(valuationDate, discountCurve)
        s = swap.parCoupon(valuationDate, discountCurve)
        texp = (self._exerciseDate - self._settlementDate) / gDaysInYear

        # Discounting is done via the PV01 annuity so no discounting in Black
        df = 1.0

        if isinstance(model, FinModelBlack):

            if self._swaptionType == FinLiborSwaptionTypes.PAYER:
                swaptionPrice = model.value(s, k, texp, df,
                                            FinOptionTypes.EUROPEAN_CALL)
            elif self._swaptionType == FinLiborSwaptionTypes.RECEIVER:
                swaptionPrice = model.value(s, k, texp, df,
                                            FinOptionTypes.EUROPEAN_PUT)

        elif isinstance(model, FinModelBlackShifted):

            if self._swaptionType == FinLiborSwaptionTypes.PAYER:
                swaptionPrice = model.value(s, k, texp, df,
                                            FinOptionTypes.EUROPEAN_CALL)
            elif self._swaptionType == FinLiborSwaptionTypes.RECEIVER:
                swaptionPrice = model.value(s, k, texp, df,
                                            FinOptionTypes.EUROPEAN_PUT)

        elif isinstance(model, FinModelSABR):

            if self._swaptionType == FinLiborSwaptionTypes.PAYER:
                swaptionPrice = model.value(s, k, texp, df,
                                            FinOptionTypes.EUROPEAN_CALL)
            elif self._swaptionType == FinLiborSwaptionTypes.RECEIVER:
                swaptionPrice = model.value(s, k, texp, df,
                                            FinOptionTypes.EUROPEAN_PUT)

        elif isinstance(model, FinModelSABRShifted):

            if self._swaptionType == FinLiborSwaptionTypes.PAYER:
                swaptionPrice = model.value(s, k, texp, df,
                                            FinOptionTypes.EUROPEAN_CALL)
            elif self._swaptionType == FinLiborSwaptionTypes.RECEIVER:
                swaptionPrice = model.value(s, k, texp, df,
                                            FinOptionTypes.EUROPEAN_PUT)

        elif isinstance(model, FinModelRatesHW):

            cpnTimes = [texp]
            cpnFlows = [0.0]

            # The first flow is always the previous coupon date
            numFlows = len(swap._adjustedFixedDates)

            for iFlow in range(1, numFlows):
                flowDate = swap._adjustedFixedDates[iFlow]
                cpnTime = (flowDate - valuationDate) / gDaysInYear
                cpnFlow = swap._fixedFlows[iFlow-1] / self._notional
                cpnTimes.append(cpnTime)
                cpnFlows.append(cpnFlow)

            cpnTimes = np.array(cpnTimes)
            cpnFlows = np.array(cpnFlows)

            dfTimes = discountCurve._times
            dfValues = discountCurve._dfValues

            if np.any(cpnTimes < 0.0):
                raise FinError("No coupon times can be before the value date.")

            swaptionPx = model.europeanBondOption_Jamshidian(texp, 1.0,
                                                             1.0, cpnTimes,
                                                             cpnFlows,
                                                             dfTimes, dfValues)

            if self._swaptionType == FinLiborSwaptionTypes.PAYER:
                swaptionPrice = swaptionPx['put']
            elif self._swaptionType == FinLiborSwaptionTypes.RECEIVER:
                swaptionPrice = swaptionPx['call']
            else:
                raise FinError("Unknown swaption option type" +
                               str(self._optionType))

            # Cancel the multiplication at the end below
            swaptionPrice /= pv01

        elif isinstance(model, FinModelRatesBK):

            print("** USE WITH CAUTION AS TREE MAY NEED TWEAKS FOR ACCRUED **")
            cpnTimes = [texp]
            cpnFlows = [0.0]

            # The first flow is always the previous coupon date
            numFlows = len(swap._adjustedFixedDates)

            for iFlow in range(1, numFlows):
                flowDate = swap._adjustedFixedDates[iFlow]
                cpnTime = (flowDate - valuationDate) / gDaysInYear
                cpnFlow = swap._fixedFlows[iFlow-1] / self._notional
                cpnTimes.append(cpnTime)
                cpnFlows.append(cpnFlow)

            cpnTimes = np.array(cpnTimes)
            cpnFlows = np.array(cpnFlows)

            dfTimes = discountCurve._times
            dfValues = discountCurve._dfValues

            if np.any(cpnTimes < 0.0):
                raise FinError("No coupon times can be before the value date.")

            tmat = (self._maturityDate - valuationDate) / gDaysInYear

            model.buildTree(tmat, dfTimes, dfValues)
            swaptionPx = model.bermudanSwaption(texp,
                                                tmat, 1.0, 1.0,
                                                cpnTimes,
                                                cpnFlows,
                                                FinOptionExerciseTypes.EUROPEAN)

            if self._swaptionType == FinLiborSwaptionTypes.PAYER:
                swaptionPrice = swaptionPx['pay']
            elif self._swaptionType == FinLiborSwaptionTypes.RECEIVER:
                swaptionPrice = swaptionPx['rec']

            swaptionPrice /= pv01

        elif isinstance(model, FinModelRatesBDT):

            print("** USE WITH CAUTION AS TREE MAY NEED TWEAKS FOR ACCRUED **")
            cpnTimes = [texp]
            cpnFlows = [0.0]

            # The first flow is always the previous coupon date
            numFlows = len(swap._adjustedFixedDates)

            for iFlow in range(1, numFlows):
                flowDate = swap._adjustedFixedDates[iFlow]
                cpnTime = (flowDate - valuationDate) / gDaysInYear
                cpnFlow = swap._fixedFlows[iFlow-1] / self._notional
                cpnTimes.append(cpnTime)
                cpnFlows.append(cpnFlow)

            cpnTimes = np.array(cpnTimes)
            cpnFlows = np.array(cpnFlows)

            dfTimes = discountCurve._times
            dfValues = discountCurve._dfValues

            if np.any(cpnTimes < 0.0):
                raise FinError("No coupon times can be before the value date.")

            tmat = (self._maturityDate - valuationDate) / gDaysInYear

            model.buildTree(tmat, dfTimes, dfValues)
            swaptionPx = model.bermudanSwaption(texp, tmat, 1.0, 1.0,
                                                cpnTimes, cpnFlows,
                                                FinOptionExerciseTypes.EUROPEAN)

            if self._swaptionType == FinLiborSwaptionTypes.PAYER:
                swaptionPrice = swaptionPx['pay']
            elif self._swaptionType == FinLiborSwaptionTypes.RECEIVER:
                swaptionPrice = swaptionPx['rec']

            swaptionPrice /= pv01
        else:
            raise FinError("Unknown swaption model " + str(model))

        self._pv01 = pv01
        self._fwdSwapRate = s
        self._forwardDf = discountCurve.df(self._exerciseDate)
        self._underlyingSwap = swap

        # The exchange of cash occurs on the settlement date
        dfSettle = discountCurve.df(self._settlementDate)
        swaptionPrice = swaptionPrice * pv01 * self._notional / dfSettle

        return swaptionPrice

###############################################################################

    def cashSettledValue(self,
                         valuationDate: FinDate,
                         discountCurve,
                         swapRate: float,
                         model):
        ''' Valuation of a Libor European-style swaption using a cash settled
        approach which is a market convention that used Black's model and that
        discounts all of the future payments at a flat swap rate. Note that the
        Black volatility for this valuation should in general not equal the
        Black volatility for the standard arbitrage-free valuation. '''

        floatSpread = 0.0
        payFixedFlag = True

        swap = FinLiborSwap(self._exerciseDate,
                            self._maturityDate,
                            self._fixedCoupon,
                            self._fixedFrequencyType,
                            self._fixedDayCountType,
                            self._notional,
                            floatSpread,
                            self._floatFrequencyType,
                            self._floatDayCountType,
                            payFixedFlag,
                            self._calendarType,
                            self._busDayAdjustType,
                            self._dateGenRuleType)

        k = self._fixedCoupon
        s = swapRate

        pv01 = swap.cashSettledPV01(valuationDate,
                                    swapRate,
                                    self._fixedFrequencyType)

        texp = (self._exerciseDate - self._settlementDate) / gDaysInYear

        # Discounting is done via the PV01 annuity so no discounting in Black
        df = 1.0

        if isinstance(model, FinModelBlack):

            if self._swaptionType == FinLiborSwaptionTypes.PAYER:
                swaptionPrice = model.value(s, k, texp, df,
                                            FinOptionTypes.EUROPEAN_CALL)
            elif self._swaptionType == FinLiborSwaptionTypes.RECEIVER:
                swaptionPrice = model.value(s, k, texp, df,
                                            FinOptionTypes.EUROPEAN_PUT)

        else:

            raise FinError("Cash settled swaptions must be priced using"
                           + " Black's model.")

        self._fwdSwapRate = swapRate
        self._forwardDf = discountCurve.df(self._exerciseDate)
        self._underlyingSwap = swap
        # The annuity needs to be discounted to today using the correct df
        self._pv01 = pv01 * self._forwardDf

        # The exchange of cash occurs on the settlement date
        dfSettle = discountCurve.df(self._settlementDate)
        swaptionPrice = swaptionPrice * self._pv01 * self._notional / dfSettle

        return swaptionPrice

###############################################################################

    def printSwapFixedLeg(self):

        if self._underlyingSwap is None:
            raise FinError("Underlying swap has not been set. Do a valuation.")

        self._underlyingSwap.printFixedLeg()

###############################################################################

    def printSwapFloatLeg(self):

        if self._underlyingSwap is None:
            raise FinError("Underlying swap has not been set. Do a valuation.")

        self._underlyingSwap.printFloatLeg()

###############################################################################

    def __repr__(self):
        ''' Function to allow us to print the swaption details. '''

        s = labelToString("SETTLEMENT DATE", self._settlementDate)
        s += labelToString("EXERCISE DATE", self._exerciseDate)
        s += labelToString("SWAPTION TYPE", str(self._swaptionType))
        s += labelToString("MATURITY DATE", self._maturityDate)
        s += labelToString("SWAP NOTIONAL", self._notional)
        s += labelToString("FIXED COUPON", self._fixedCoupon * 100)
        s += labelToString("FIXED FREQUENCY", str(self._fixedFrequencyType))
        s += labelToString("FIXED DAY COUNT", str(self._fixedDayCountType))
        s += labelToString("FLOAT FREQUENCY", str(self._floatFrequencyType))
        s += labelToString("FLOAT DAY COUNT", str(self._floatDayCountType))

        if self._pv01 is not None:
            s += labelToString("PV01", self._pv01)
            s += labelToString("FWD SWAP RATE", self._fwdSwapRate*100)
            s += labelToString("FWD DF TO EXPIRY", self._forwardDf, "")

        return s

###############################################################################

    def print(self):
        ''' Alternative print method. '''

        print(self)

###############################################################################
