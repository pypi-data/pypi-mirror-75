##############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
##############################################################################

from ...finutils.FinDate import FinDate
from ...finutils.FinFrequency import FinFrequency, FinFrequencyTypes
from ...finutils.FinCalendar import FinCalendarTypes
from ...finutils.FinSchedule import FinSchedule
from ...finutils.FinCalendar import FinBusDayAdjustTypes
from ...finutils.FinCalendar import FinDateGenRuleTypes
from ...finutils.FinDayCount import FinDayCount, FinDayCountTypes
from ...finutils.FinError import FinError
from ...finutils.FinHelperFunctions import checkArgumentTypes, labelToString


###############################################################################


class FinBondAnnuity(object):
    ''' An annuity is a vector of dates and flows generated according to ISDA
    standard rules which starts on the next date after the start date
    (effective date) and runs up to an end date with no principal repayment.
    Dates are then adjusted according to a specified calendar. '''

    def __init__(self,
                 maturityDate: FinDate,
                 coupon: float,
                 frequencyType: FinFrequencyTypes,
                 calendarType: FinCalendarTypes = FinCalendarTypes.WEEKEND,
                 busDayAdjustType: FinBusDayAdjustTypes = FinBusDayAdjustTypes.FOLLOWING,
                 dateGenRuleType: FinDateGenRuleTypes = FinDateGenRuleTypes.BACKWARD,
                 dayCountConventionType: FinDayCountTypes = FinDayCountTypes.ACT_360,
                 face: float = 100.0):

        checkArgumentTypes(self.__init__, locals())

        self._maturityDate = maturityDate
        self._coupon = coupon
        self._frequencyType = frequencyType
        self._frequency = FinFrequency(frequencyType)

        # ISDA Style conventions
        self._calendarType = calendarType
        self._busDayAdjustType = busDayAdjustType
        self._dateGenRuleType = dateGenRuleType
        self._dayCountConventionType = dayCountConventionType

        self._face = face
        self._par = 100.0

        self._flowDates = []
        self._settlementDate = FinDate(1, 1, 1900)
        self._accruedInterest = None
        self._accruedDays = 0.0
        self._alpha = 0.0

###############################################################################

    def cleanPriceFromDiscountCurve(self, settlementDate, discountCurve):
        ''' Calculate the bond price using some discount curve to present-value
        the bond's cashflows. '''

        fullPrice = self.fullPriceFromDiscountCurve(settlementDate,
                                                    discountCurve)
        accrued = self._accruedInterest * self._par / self._face
        cleanPrice = fullPrice - accrued
        return cleanPrice

###############################################################################

    def fullPriceFromDiscountCurve(self, settlementDate, discountCurve):
        ''' Calculate the bond price using some discount curve to present-value
        the bond's cashflows. '''

        self.calculateFlowDatesPayments(settlementDate)
        pv = 0.0

        numFlows = len(self._flowDates)

        for i in range(1, numFlows):
            dt = self._flowDates[i]
            df = discountCurve.df(dt)
            flow = self._flowAmounts[i]
            pv = pv + flow * df

        return pv * self._par / self._face

###############################################################################

    def calculateFlowDatesPayments(self, settlementDate):

        # No need to generate flows if settlement date has not changed
        if settlementDate == self._settlementDate:
            return

        if settlementDate == self._maturityDate:
            raise FinError("Settlement date is maturity date.")

        self._settlementDate = settlementDate
        calendarType = FinCalendarTypes.NONE
        busDayRuleType = FinBusDayAdjustTypes.NONE
        dateGenRuleType = FinDateGenRuleTypes.BACKWARD

        self._flowDates = FinSchedule(settlementDate,
                                      self._maturityDate,
                                      self._frequencyType,
                                      calendarType,
                                      busDayRuleType,
                                      dateGenRuleType).generate()

        self._pcd = self._flowDates[0]
        self._ncd = self._flowDates[1]
        self._calcAccruedInterest(settlementDate)

        self._flowAmounts = [0.0]
        basis = FinDayCount(self._dayCountConventionType)

        prevDt = self._pcd

        for nextDt in self._flowDates[1:]:
            alpha = basis.yearFrac(prevDt, nextDt)
            flow = self._coupon * alpha * self._face
            self._flowAmounts.append(flow)
            prevDt = nextDt

###############################################################################

    def _calcAccruedInterest(self, settlementDate):
        ''' Calculate the amount of coupon that has accrued between the
        previous coupon date and the settlement date. '''

        if settlementDate != self._settlementDate:
            self.calculateFlowDatesPayments(settlementDate)

        if len(self._flowDates) == 0:
            raise FinError("Accrued interest - not enough flow dates.")

        dc = FinDayCount(self._dayCountConventionType)

        if self._dayCountConventionType == FinDayCountTypes.ACT_ACT_ICMA:
            accFactor = dc.yearFrac(self._pcd, settlementDate, self._ncd)
            alpha = 1.0 - accFactor
            accFactor = accFactor/self._frequency
        else:
            accFactor = dc.yearFrac(self._pcd, settlementDate)
            alpha = 1.0 - accFactor

        self._accruedInterest = accFactor * self._face * self._coupon
        self._alpha = alpha
        self._accruedDays = settlementDate - self._pcd

        return self._accruedInterest

###############################################################################

    def printFlows(self, settlementDate):
        ''' Print a list of the unadjusted coupon payment dates used in
        analytic calculations for the bond. '''

        self.calculateFlowDatesPayments(settlementDate)

        numFlows = len(self._flowDates)
        for i in range(1, numFlows):
            dt = self._flowDates[i]
            flow = self._flowAmounts[i]
            print(dt, ",", flow)

###############################################################################

    def __repr__(self):
        ''' Print a list of the unadjusted coupon payment dates used in
        analytic calculations for the bond. '''

        s = labelToString("MATURITY DATE", self._maturityDate)
        s += labelToString("FREQUENCY", self._frequencyType)
        s += labelToString("CALENDAR", self._calendarType)
        s += labelToString("BUSDAYRULE", self._busDayAdjustType)
        s += labelToString("DATEGENRULE", self._dateGenRuleType)

        return s

###############################################################################

    def print(self):
        ''' Simple print function for backward compatibility. '''
        print(self)


###############################################################################
