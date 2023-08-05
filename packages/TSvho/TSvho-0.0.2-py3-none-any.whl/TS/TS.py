import pandas as pd
from matplotlib import pyplot
import math
import numpy as np


def MeanAll(file_name,TS_attribute):
    df = pd.read_csv(file_name)
    MeanTotal = 0
    for i in range(1,df.__len__()):
        MeanTotal = MeanTotal + df.iloc[i][TS_attribute]
    mean = MeanTotal / int(df.__len__())
    return mean

def Mariance(file_name,TS_attribute):
    VarianceTotal = 0
    df = pd.read_csv(file_name)
    mean=TS_mean(file_name, TS_attribute)
    for i in range(1,df.__len__()):
        VarianceTotal = VarianceTotal + ((df.iloc[i][TS_attribute] - mean) ** 2)
    VarianceTotal = VarianceTotal / df.__len__()
    return VarianceTotal

def List(file_name,TS_attribute):
    df = pd.read_csv(file_name)
    for i in range(1,df.__len__()):
        print(df.iloc[i][TS_attribute])

def StandardDeviation(file_name,TS_attribute):
    return math.sqrt(TS_variance(file_name,TS_attribute))

def MeanAbsoluteDeviation(file_name,TS_attribute):
    total = 0
    MAD = 0
    df = pd.read_csv(file_name)
    for i in range(1,df.__len__()):
        total = total + df.iloc[i][TS_attribute]
    avg= total / df.__len__()
    for i in range(1,df.__len__()):
        MAD = MAD + df.iloc[i][TS_attribute] - avg
    return MAD

def Mean(file_name, time_step_N, TS_attribute):
    VarianceTotal = 0
    df = pd.read_csv(file_name)
    mean=TS_mean(file_name, TS_attribute)
    for i in range(1,df.__len__()):
        VarianceTotal = VarianceTotal + ((df.iloc[time_step_N][TS_attribute] - mean) ** time_step_N)
    VarianceTotal = VarianceTotal / df.__len__()
    return VarianceTotal

def Skewness(file_name, time_step_N, TS_attribute):
    skewness_g = 0
    df = pd.read_csv(file_name)
    skewness_g = math.sqrt(df.__len__()) * TS_Mean(file_name, time_step_N, TS_attribute) / TS_Mean(file_name, time_step_N-1, TS_attribute) ** (time_step_N/(time_step_N-1))
    return skewness_g

def Kurtosis(file_name, time_step_N, TS_attribute):
    kurtosis_g = 0
    df = pd.read_csv(file_name)
    kurtosis_g = df.__len__() * TS_Mean(file_name, time_step_N+2, TS_attribute) / TS_Mean(file_name, time_step_N, TS_attribute) ** 2 - (time_step_N+1)
    return kurtosis_g

def ZeroCrossingRate(file_name, TS_attribute):
    ZCR_total = 0
    df = pd.read_csv(file_name)
    for i in range(2, df.__len__()):
        ZCR_total = ZCR_total + abs(np.sign(df.iloc[i][TS_attribute]) - np.sign(df.iloc[i-1][TS_attribute]))
    ZCR_total = ZCR_total / 2
    return ZCR_total

def MeanCrossingRate(file_name, TS_attribute):
    MCR_total = 0
    df = pd.read_csv(file_name)
    for i in range(2, df.__len__()):
        MCR_total = MCR_total + abs(np.sign(df.iloc[i][TS_attribute]-TS_mean(file_name, TS_attribute)) - np.sign(df.iloc[i-1][TS_attribute])-TS_mean(file_name, TS_attribute))
    MCR_total = MCR_total / 2
    return MCR_total

def Covariance(file_name, time_step_N, TS_attribute_A, TS_attribute_B):
    Covariance_Total = 0
    df = pd.read_csv(file_name)
    for i in range(1, df.__len__()):
        Covariance_Total = Covariance_Total + abs((df.iloc[i][TS_attribute_A] - TS_mean(file_name, TS_attribute_A)) * (df.iloc[i][TS_attribute_B] - TS_mean(file_name, TS_attribute_B)))
    Covariance_Total = Covariance_Total / df.__len__()
    return Covariance_Total

def Correlation(file_name, time_step_N, TS_attribute_A, TS_attribute_B):
    Correlation_Total = 0
    df = pd.read_csv(file_name)
    TS_Covariance(file_name, time_step_N, TS_attribute_A, TS_attribute_B) / (TS_StandardDeviation(file_name,TS_attribute_A) * TS_StandardDeviation(file_name,TS_attribute_B))
    df = pd.read_csv(file_name)
    for i in range(1, df.__len__()):
        Correlation_Total = Correlation_Total + (df.iloc[i][TS_attribute_A] - TS_mean(file_name, TS_attribute_A)) * (df.iloc[i][TS_attribute_B] - TS_mean(file_name, TS_attribute_B))
    Correlation_Total = Correlation_Total / df.__len__()
    return Correlation_Total

def AverageResultantAcceleration(file_name, TS_attribute_Total):
    ARA_Total = 0
    df = pd.read_csv(file_name)
    for i in range(1, TS_attribute_Total):
        value_tmp = 0
        for j in range(1, TS_attribute_Total):
            value_tmp = value_tmp + df.iloc[i][j] ** 2
        ARA_Total = ARA_Total + math.sqrt(value_tmp)
    ARA_Total = ARA_Total / TS_attribute_Total
    return ARA_Total

def Magnitude(file_name, TS_attribute_Total):
    Magnitude_Total = 0
    df = pd.read_csv(file_name)
    for i in range(1, TS_attribute_Total):
        for j in range(1, TS_attribute_Total):
            Magnitude_Total = Magnitude_Total + df.iloc[i][j] ** 2
    Magnitude_Total = math.sqrt(Magnitude_Total)
    return Magnitude_Total

def AverageAbsoluteDifference(file_name, TS_attribute_Total_N):
    AAD_Total = 0
    df = pd.read_csv(file_name)
    for i in range(2, df.__len__()):
        AAD_Total = AAD_Total + abs(df.iloc[i][TS_attribute_Total_N] - df.iloc[i-1][TS_attribute_Total_N])
    AAD_Total = AAD_Total / df.__len__()
    return AAD_Total

def AverageAbsoluteValue(file_name, TS_attribute_Total_N):
    AAV_Total = 0
    df = pd.read_csv(file_name)
    for i in range(1, df.__len__()):
        AAV_Total = AAV_Total + abs(df.iloc[i][TS_attribute_Total_N])
    AAV_Total = AAV_Total / df.__len__()
    return AAV_Total

def RootMeanSquare(file_name, TS_attribute_Total_N):
    RMS_Total = 0
    df = pd.read_csv(file_name)
    for i in range(1, df.__len__()):
        RMS_Total = RMS_Total + df.iloc[i][TS_attribute_Total_N] ** 2
    RMS_Total = RMS_Total / df.__len__()
    return RMS_Total


# file='_visitors.csv'
#
# print('TS_mean:', TS_mean(file,1))
# print('TS_variance:', TS_variance(file,1))
# print('TS_list:', TS_list(file,1))
# print('TS_StandardDeviation:', TS_StandardDeviation(file,1))
# print('TS_MeanAbsoluteDeviation:', TS_MeanAbsoluteDeviation(file,1))
# print('TS_Mean:', TS_Mean(file, 5, 1))
# print('TS_Skewness:', TS_Skewness(file, 5, 1))
# print('TS_Kurtosis:', TS_Kurtosis(file, 5, 1))
# print('TS_ZeroCrossingRate:', TS_ZeroCrossingRate(file, 1))
# print('TS_MeanCrossingRate:', TS_MeanCrossingRate(file, 1))
# print('TS_Covariance:', TS_Covariance(file, 5, 1, 2))
# print('TS_Correlation:', TS_Correlation(file, 5, 1, 2))
# print('TS_AverageResultantAcceleration:', TS_AverageResultantAcceleration(file, 3))
# print('TS_Magnitude:', TS_Magnitude(file, 3))
# print('TS_AverageAbsoluteDifference:', TS_AverageAbsoluteDifference(file, 1))
# print('TS_AverageAbsoluteValue:', TS_AverageAbsoluteValue(file, 1))
# print('TS_RootMeanSquare:', TS_RootMeanSquare(file, 1))
#


# groups = df.groupby(pd.Grouper(freq='A'))
# years = pd.DataFrame()
# for name, group in groups:
#     years[name,year] = group.values
# years.plot()
#df.hist()
#df.plot(kind='kde')
#df.plot(style='-',subplots=True,legend=False)
#df.boxplot()
#pyplot.matshow(date, interpolation=None, aspect='auto')
#pyplot.show()

# print(df)
# print(df.__len__())

# df = pd.read_csv('_visitors.csv')
# count = df.__len__()

