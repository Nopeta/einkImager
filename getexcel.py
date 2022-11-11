import pandas
import os

path = os.path.dirname(__file__) + '/'
df = pandas.read_excel(path + 'data_test.xlsx')
print("Columns")
print(df[df['date'] == '2022-11-11'])
