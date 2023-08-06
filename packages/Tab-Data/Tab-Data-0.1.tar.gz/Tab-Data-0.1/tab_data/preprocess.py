import numpy as np
import pandas as pd
from sklearn import preprocessing
from scipy import stats

def tab_le(*args, cate_feature):
	for col_tmp in cate_feature:
		le_tmp = preprocessing.LabelEncoder()
		value_tmp = []
		for df_tmp in args:
			df_tmp[pd.isnull(df_tmp)]  = 'NaN'
			if col_tmp in df_tmp:
				value_tmp.extend(list(df_tmp[col_tmp].unique()))
		le_tmp.fit(value_tmp)
		for df_tmp in args:
			if col_tmp in df_tmp:
				df_tmp[col_tmp] = le_tmp.transform(list(df_tmp[col_tmp]))
	if len(args) > 1:
		return args
	else:
		return args[0]

def tab_stat(df):
	print(f"Dataset Shape: {df.shape}")
	desc = pd.DataFrame(df.dtypes,columns=['dtypes'])
	desc = desc.reset_index()
	desc['Name'] = desc['index']
	desc = desc[['Name','dtypes']]
	desc['Missing'] = df.isnull().sum().values	
	desc['Uniques'] = df.nunique().values
	desc['1st value'] = df.loc[0].values
	desc['2nd value'] = df.loc[1].values
	desc['3rd value'] = df.loc[2].values

	# for name in summary['Name'].value_counts().index:
	# 	summary.loc[summary['Name'] == name, 'Entropy'] = round(stats.entropy(df[name].value_counts(normalize=True), base=2),2) 

	return desc.T


	
