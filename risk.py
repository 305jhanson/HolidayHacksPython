import pandas as pd
import matplotlib as plt


def getConditionGroups():
    data = pd.read_csv('COVID_data.csv')
    return data['Condition Group']