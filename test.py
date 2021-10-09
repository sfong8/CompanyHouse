import pandas as pd

chouse = pd.read_csv('BasicCompanyData-2021-10-01-part1_6.csv')
chouse=chouse[[' CompanyNumber']]

x = chouse.sample(1001)
x.columns =['chouse_num']
x.to_csv('chouse_num_sample.csv',index=None)