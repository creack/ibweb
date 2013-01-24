#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Strategy:

    __prices__ = []
    __macds__ = []
    score = 0

    def addPrice(self, price):
        self.__prices__.append(price)

    __prev_ema__ = {}
    def getEma(self, data, period):
        k = 2. / (1. + period)

        try:
            self.__prev_ema__[period]
        except KeyError:
            self.__prev_ema__[period] = 0

        if len(data) < period - 1:
            return 0
        elif len(data) == period:
            total = 0
            for i in data:
                total += i
            self.__prev_ema__[period] = round(i / period, 4)
        else:
            self.__prev_ema__[period] =  round(k * (data[-1] - self.__prev_ema__[period]) + self.__prev_ema__[period], 4)

        return self.__prev_ema__[period]

    def getScore(self):
        return self.score

    def getMacd(self):

        if len(self.__prices__) >= 11:
            ema12 = self.getEma(self.__prices__, 12)

        if (len(self.__prices__) >= 25):
            ema26 = self.getEma(self.__prices__, 26)
            macd = round(ema26 - ema12, 4)
            self.__macds__.append(macd)

        if len(self.__prices__) >= 26 + 9:
            signal_line = self.getEma(self.__macds__, 9)
            signal = signal_line == macd

            self.score = self.score - 1 if signal_line - macd < 0 else self.score + 1

            return {"12": ema12, "26":ema26, "macd":macd, "signal": signal_line, "sig": "SIIIIGGNNALLLLL" if signal else "", "st": "BUY" if signal_line < macd else "SELL"}

        return {"12": 0, "26": 0, "macd": 0, "singal": 0, "sig": 0}
