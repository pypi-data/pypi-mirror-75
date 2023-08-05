from backtester.trading_system_parameters import TradingSystemParameters
from backtester.features.feature import Feature
from backtester.dataSource.yahoo_data_source import YahooStockDataSource
from backtester.timeRule.custom_time_rule import CustomTimeRule
from backtester.executionSystem.simple_execution_system import SimpleExecutionSystem
from backtester.orderPlacer.backtesting_order_placer import BacktestingOrderPlacer
from backtester.trading_system import TradingSystem
from backtester.constants import *

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from datetime import timedelta

class MomentumTradingParams(TradingSystemParameters):

    def __init__(self, tradingFunctions):
        self.__tradingFunctions = tradingFunctions
        super().__init__()
        self.__dataSetId = 'equity_data'
        self.__instrumentIds = self.__tradingFunctions.getSymbolsToTrade()
        self.__startDate = self.__tradingFunctions.start_date
        self.__endDate = self.__tradingFunctions.end_date

    def getDataParser(self):
        '''
        Returns an instance of class DataParser. Source of data for instruments
        '''
        instrumentIds = self.__tradingFunctions.getSymbolsToTrade()
        return YahooStockDataSource(
            cachedFolderName = 'historicalData/',
            dataSetId = self.__dataSetId,
            instrumentIds = instrumentIds,
            startDateStr = self.__startDate,
            endDateStr = self.__endDate,
        )
        
    def getTimeRuleForUpdates(self):
        return CustomTimeRule(
            startDate = self.__startDate, 
            endDate = self.__endDate, 
            frequency = 'D', 
            sample = '30'
        )

    def getFrequencyOfFeatureUpdates(self):
        return timedelta(days = 1)

    def getStartingCapital(self):
        if len(self.__tradingFunctions.getSymbolsToTrade()) > 0:
            return 1000*len(self.__tradingFunctions.getSymbolsToTrade())
        else:
            return 30000

    def getCustomFeatures(self):
        '''
        This is a way to use any custom features you might have made.
        Returns a dictionary where:
        
        key: featureId to access this feature (Make sure this doesnt conflict with any of the pre defined feature Ids)
        value: Your custom Class which computes this feature. The class should be an instance of Feature
        
        Eg. if your custom class is MyCustomFeature, and you want to access this via featureId='my_custom_feature',
        you will import that class, and return this function as {'my_custom_feature': MyCustomFeature}
        '''
        return {
            'prediction': TrainingPredictionFeature,
            'zero_fees': FeesCalculator,
            'benchmark_PnL': BuyHoldPnL,
            'score': ScoreFeature
        }

    def getInstrumentFeatureConfigDicts(self):
        '''
        Returns an array of instrument feature config dictionaries instrument feature config Dictionary has the 
        following keys:
        
        featureId: a string representing the type of feature you want to use
        featureKey: a string representing the key you will use to access the value of this feature
        params: A dictionary with which contains other optional params if needed by the feature
        '''

        predictionDict = {
            'featureKey': 'prediction',
            'featureId': 'prediction',
            'params': {'tradingFunctions':self.__tradingFunctions}}

        feesConfigDict = {
            'featureKey': 'fees',
            'featureId': 'zero_fees',
            'params': {}
        }
        profitlossConfigDict = {
            'featureKey': 'pnl',
            'featureId': 'pnl',
            'params': {
                'price': self.getPriceFeatureKey(),
                'fees': 'fees'
            }
        }
        capitalConfigDict = {
            'featureKey': 'capital',
            'featureId': 'capital',
            'params': {
                'price': 'adjClose',
                'fees': 'fees',
                'capitalReqPercent': 0.95
            }
        }
        benchmarkDict = {
            'featureKey': 'benchmark',
            'featureId': 'benchmark_PnL',
            'params': {'pnlKey': 'pnl'}
        }
        scoreDict = {
            'featureKey': 'score',
            'featureId': 'score',
            'params': {
                'featureName1': 'pnl',
                'featureName2':'benchmark'
            }
        }

        stockFeatureConfigs = self.__tradingFunctions.getInstrumentFeatureConfigDicts()

        return {
            INSTRUMENT_TYPE_STOCK: stockFeatureConfigs + [
                predictionDict,
                feesConfigDict,
                profitlossConfigDict,
                capitalConfigDict,
                benchmarkDict, 
                scoreDict
            ]
        }

    def getMarketFeatureConfigDicts(self):
        '''
        Returns an array of market feature config dictionaries having the following keys:
        
        featureId: a string representing the type of feature you want to use
        featureKey: a string representing the key you will use to access the value of this feature
        params: A dictionary with which contains other optional params if needed by the feature
        '''
        scoreDict = {
            'featureKey': 'score',
            'featureId': 'score_ll',
            'params': {
                'featureName': self.getPriceFeatureKey(),
                'instrument_score_feature': 'score'
            }
        }
        
        return [scoreDict]

    def getPrediction(self, time, updateNum, instrumentManager):
        predictions = pd.Series(index = self.__instrumentIds)
        predictions = self.__tradingFunctions.getPrediction(time, updateNum, instrumentManager, predictions)
        return predictions

    def getExecutionSystem(self):
        '''
        Returns the type of execution system we want to use. Its an implementation of the class ExecutionSystem
        It converts prediction to intended positions for different instruments.
        '''
        
        return SimpleExecutionSystem(
            enter_threshold = 0.7,
            exit_threshold = 0.55,
            longLimit = 1,
            shortLimit = 1,
            capitalUsageLimit = 0.10*self.getStartingCapital(),
            enterlotSize = 1, 
            exitlotSize = 1,
            limitType = 'L', 
            price = 'adjClose'
        )

    def getOrderPlacer(self):
        '''
        Returns the type of order placer we want to use. It's an implementation of the class OrderPlacer.
        It helps place an order, and also read confirmations of orders being placed.
        For Backtesting, you can just use the BacktestingOrderPlacer, which places the order which you want, and 
        automatically confirms it too.
        '''
        
        return BacktestingOrderPlacer()

    def getLookbackSize(self):
        '''
        Returns the amount of lookback data you want for your calculations. The historical market features and instrument features are only
        stored upto this amount.
        This number is the number of times we have updated our features.
        '''
        
        return 120

    def getPriceFeatureKey(self):
        '''
        The name of column containing the instrument price
        '''
        
        return 'adjClose'

    def getInstrumentsIds(self):
        '''
        Get all instrument ids
        '''
        
        return self.__instrumentIds


class TrainingPredictionFeature(Feature):
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        tf = featureParams['tradingFunctions']
        predictions = tf.getPrediction(time, updateNum, instrumentManager, pd.Series(index = tf.getSymbolsToTrade()))
        return predictions

class FeesCalculator(Feature):
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        return pd.Series(0, index = instrumentManager.getAllInstrumentsByInstrumentId())

class BuyHoldPnL(Feature):
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()

        priceData = instrumentLookbackData.getFeatureDf('adjClose')
         
        if len(priceData) < 2:
            return pd.Series(0, index = instrumentManager.getAllInstrumentsByInstrumentId())
        else:
            bhpnl = instrumentLookbackData.getFeatureDf(featureKey).iloc[-1]
            bhpnl += priceData.iloc[-1] - priceData.iloc[-2]

        return bhpnl

class ScoreFeature(Feature):
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        if len(instrumentLookbackData.getFeatureDf(featureParams['featureName1'])) > 0:
            feature1 = instrumentLookbackData.getFeatureDf(featureParams['featureName1']).iloc[-1]
            feature2 = instrumentLookbackData.getFeatureDf(featureParams['featureName2']).iloc[-1]
            
            for instrumentId in feature1.index:
                pnls = instrumentLookbackData.getFeatureDf('pnl')[instrumentId]
                positions = instrumentLookbackData.getFeatureDf('position')[instrumentId]
                
                print(instrumentId)
                print('pnl: %.2f'%pnls[-1])
                if len(positions) > 2 and np.abs(positions[-1] - positions[-2]) > 0:
                    print('Position changed to: %.2f'%positions[-1])
            
            toRtn = (feature1 - feature2) / feature2.abs()
            toRtn[toRtn.isnull()] = 0
            toRtn[toRtn == np.Inf] = 0
        else:
            toRtn=0

        return toRtn