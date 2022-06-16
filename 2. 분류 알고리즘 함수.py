# 패키지 임포트
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose


# 2011년 1 ~ 12월
train_features_2011 = train_features_type[('2011-01-01' <= train_features_type['Date']) & (train_features_type['Date'] < '2012-01-01')]
df_2011 = train_features_2011
def make_Q_Type_df(store,dept):

    try:
        if train_features[('2011-01-01' <= train_features['Date']) & (train_features['Date'] < '2012-01-01')]['Date'].nunique() == 52:
            dataframe = train_features[train_features['Store']==store]
    except:
        pass
    
                                ##############
                                #  전체 판매량  #
                                ##############


    train_features_2011 = dataframe[('2011-01-01' <= dataframe['Date']) & (dataframe['Date'] < '2012-01-01')]   
    total_sales = df_2011['Weekly_Sales'].sum()
    total_sales_avg = total_sales / df_2011['Dept'].nunique()

    store_sales = train_features_2011['Weekly_Sales'].sum()
    store_dept_count = train_features_2011['Dept'].nunique()
    store_sales_avg = train_features_2011['Weekly_Sales'].sum() / store_dept_count
    
    store_dept_sales = train_features_2011[train_features_2011['Dept']==dept]['Weekly_Sales'].sum()
    # store_dept_sales = train_features_2011[train_features_2011['Dept']==dept]['Weekly_Sales'].sum() / train_features_2011['Dept'].nunique()

    Q = []

    store_LQ_A_per = store_sales * 0.020701433011128367 #* (store_sales / total_sales)
    store_HQ_A_per = store_sales * 0.0237844480210703#* (store_sales / total_sales)
    
    store_LQ_B_per = store_sales * 0.020701433011128367 #* (store_sales / total_sales)
    store_HQ_B_per = store_sales * 0.0237844480210703#* (store_sales / total_sales)
    
    store_LQ_C_per = store_sales * 0.020701433011128367# * (store_sales / total_sales)
    store_HQ_C_per = store_sales * 0.0237844480210703#* (store_sales / total_sales)

#     store_LQ_A_per = store_sales * 0.020701433011128367  * (store_sales_avg / total_sales_avg)
#     store_HQ_A_per = store_sales * 0.0237844480210703 * (store_sales_avg / total_sales_avg)

#     store_LQ_B_per = store_sales * 0.020701433011128367  * (store_sales_avg / total_sales_avg)
#     store_HQ_B_per = store_sales * 0.0237844480210703 * (store_sales_avg / total_sales_avg)
    
#     store_LQ_C_per = store_sales * 0.020701433011128367  * (store_sales_avg / total_sales_avg)
#     store_HQ_C_per = store_sales * 0.0237844480210703 * (store_sales_avg / total_sales_avg)
    
    # print("상점 판매량 :",store_sales)
    # print("상점 판매량 x HQ 경계 :",store_sales * 0.0237844480210703)
    # print("상점 판매량 x HQ 경계 x ST/T :",store_sales * 0.0237844480210703 * (store_sales / total_sales))
    # print("상점 판매량 x HQ 경계 x ST(평균)/T(평균) :",store_sales * 0.0237844480210703 * (store_sales_avg / total_sales_avg))
    # print("상점/부서 판매량",store_dept_sales)

    if store in train_features_2011[train_features_2011['Type']=='A']['Store'].unique():
        if store_dept_sales <= store_LQ_A_per:
            Q = "LQ"
        else:
            Q = "HQ"
    
    if store in train_features_2011[train_features_2011['Type']=='B']['Store'].unique():
        if store_dept_sales <= store_LQ_B_per:
            Q = "LQ"
        else:
            Q = "HQ"
            
    if store in train_features_2011[train_features_2011['Type']=='C']['Store'].unique():
        if store_dept_sales <= store_LQ_C_per:
            Q = "LQ"
        else:
            Q = "HQ"

    return '{}'.format(Q)




                                ##############
                                #   변동계수   #
                                ##############
# 2011년 1 ~ 12월
def make_CV_Type_df(store,dept):    


    dataframe = train_features[train_features['Store']==store]
    train_features_2011 = dataframe[('2011-01-01' <= dataframe['Date']) & (dataframe['Date'] < '2012-01-01')]   

    CV = []

    temp_df = pd.DataFrame()
    temp_df2 = pd.DataFrame()
    for i in train_features_2011['Dept'].unique():
        temp = pd.DataFrame(train_features_2011[train_features_2011['Dept']==i]['Weekly_Sales'].groupby(train_features_2011['Date']).mean())
        temp_df = pd.concat([temp_df,temp],axis=1)
    x = pd.concat([temp_df,temp_df2],axis=1)
    x.columns = [i for i in train_features_2011['Dept'].unique()]
    x = x.fillna(method='bfill')

    all_sds_df = pd.DataFrame(columns=['Dept','CV'])
    for idx,i in zip(x.columns,range(len(x.T))):
        all_sds_df = all_sds_df.append(pd.DataFrame([[idx,np.std(x.iloc[:,i])/np.mean(x.iloc[:,i])]],
                                              columns=['Dept','CV']),ignore_index=True)
    all_sds_df.set_index('Dept',inplace=True)

    if all_sds_df.loc[dept][0] > 0.25:
        CV = "HV"
    elif all_sds_df.loc[dept][0] >= 0.1:
        CV = "MV"
    else:
        CV = "LV"

    return CV


# 2011년 1 ~ 12월
def make_Q_CV_df(store,dept):    
                                #######################
                                #  전체 판매량 & 변동계수  #
                                #######################

    dataframe = train_features[train_features['Store']==store]
    train_features_2011 = dataframe[('2011-01-01' <= dataframe['Date']) & (dataframe['Date'] < '2012-01-01')]   
    store_sales = train_features_2011['Weekly_Sales'].sum()   
    store_dept_sales = train_features_2011[train_features_2011['Dept']==dept]['Weekly_Sales'].sum()

    Q = []

    store_LQ_per = store_sales * 0.020701433011128367 
    store_HQ_per = store_sales * 0.0237844480210703

    if store in train_features_2011['Store'].unique():
        if store_dept_sales <= store_LQ_per:
            Q = "LQ"
        else:
            Q = "HQ"
            
            
      
    CV = []

    temp_df = pd.DataFrame()
    temp_df2 = pd.DataFrame()
    temp = pd.DataFrame(train_features_2011[train_features_2011['Dept']==i]['Weekly_Sales'].groupby(train_features_2011['Date']).mean())
    temp_df = pd.concat([temp_df,temp],axis=1)
    x = pd.concat([temp_df,temp_df2],axis=1)
    x.columns = [i for i in train_features_2011['Dept'].unique()]
    x = x.fillna(method='bfill')

    all_sds_df = pd.DataFrame(columns=['Dept','CV'])
    for idx,i in zip(x.columns,range(len(x.T))):
        all_sds_df = all_sds_df.append(pd.DataFrame([[idx,np.std(x.iloc[:,i])/np.mean(x.iloc[:,i])]],
                                              columns=['Dept','CV']),ignore_index=True)
    all_sds_df.set_index('Dept',inplace=True)

    if all_sds_df.loc[dept][0] > 0.25:
        CV = "HV"
    elif all_sds_df.loc[dept][0] >= 0.1:
        CV = "MV"
    else:
        CV = "LV"



    return '{}_{}'.format(Q,CV)




                                ##############
                                #  분기판매량   #
                                ##############
def make_quarter(dataframe):

    # 4분기를 구하려면 8개의 주기가 필요하기때문에 2010년,2011년 자료 사용
    '''
    date range : 2010 ~ 2011 (구하려고 하는 년도 + 이전 년도의 수치 필요)
    '''

    q_df = dataframe[(dataframe['Date'] >= '2010-04-01') & (dataframe['Date'] < '2012-01-01')]
    q1_2010 = dataframe[dataframe['Date'] < '2010-04-01']

    x = pd.DataFrame(q_df.set_index('Date').resample('QS')['Weekly_Sales'].mean())
    x.loc['2010-01-01'] = q1_2010['Weekly_Sales'].mean()
    x = x.fillna(0)
    x = x.reset_index()
    pd.to_datetime(x['Date'])
    x = x.sort_values(by='Date')
    x = x.set_index('Date')
    
    result_add_q = seasonal_decompose(x,model='additive')

    if result_add_q.seasonal[0] > result_add_q.seasonal[1] > result_add_q.seasonal[2] > result_add_q.seasonal[3]:
        return "q1234"
    elif result_add_q.seasonal[0] > result_add_q.seasonal[1] > result_add_q.seasonal[3] > result_add_q.seasonal[2]:
        return "q1243"
    elif result_add_q.seasonal[0] > result_add_q.seasonal[2] > result_add_q.seasonal[1] > result_add_q.seasonal[3]:
        return "q1324"
    elif result_add_q.seasonal[0] > result_add_q.seasonal[2] > result_add_q.seasonal[3] > result_add_q.seasonal[1]:
        return "q1342"        
    elif result_add_q.seasonal[0] > result_add_q.seasonal[3] > result_add_q.seasonal[1] > result_add_q.seasonal[2]:
        return "q1423"
    elif result_add_q.seasonal[0] > result_add_q.seasonal[3] > result_add_q.seasonal[2] > result_add_q.seasonal[1]:
        return "q1432"

    elif result_add_q.seasonal[1] > result_add_q.seasonal[0] > result_add_q.seasonal[2] > result_add_q.seasonal[3]:
        return "q2134"
    elif result_add_q.seasonal[1] > result_add_q.seasonal[0] > result_add_q.seasonal[3] > result_add_q.seasonal[2]:
        return "q2143"
    elif result_add_q.seasonal[1] > result_add_q.seasonal[2] > result_add_q.seasonal[0] > result_add_q.seasonal[3]:
        return "q2314"
    elif result_add_q.seasonal[1] > result_add_q.seasonal[2] > result_add_q.seasonal[3] > result_add_q.seasonal[0]:
        return "q2341"
    elif result_add_q.seasonal[1] > result_add_q.seasonal[3] > result_add_q.seasonal[0] > result_add_q.seasonal[2]:
        return "q2413"
    elif result_add_q.seasonal[1] > result_add_q.seasonal[3] > result_add_q.seasonal[2] > result_add_q.seasonal[0]:
        return "q2431"

    elif result_add_q.seasonal[2] > result_add_q.seasonal[0] > result_add_q.seasonal[1] > result_add_q.seasonal[3]:
        return "q3124"
    elif result_add_q.seasonal[2] > result_add_q.seasonal[0] > result_add_q.seasonal[3] > result_add_q.seasonal[1]:
        return "q3142"
    elif result_add_q.seasonal[2] > result_add_q.seasonal[1] > result_add_q.seasonal[0] > result_add_q.seasonal[3]:
        return "q3214"
    elif result_add_q.seasonal[2] > result_add_q.seasonal[1] > result_add_q.seasonal[3] > result_add_q.seasonal[0]:
        return "q3241"
    elif result_add_q.seasonal[2] > result_add_q.seasonal[3] > result_add_q.seasonal[0] > result_add_q.seasonal[1]:
        return "q3412"

    elif result_add_q.seasonal[2] > result_add_q.seasonal[3] > result_add_q.seasonal[1] > result_add_q.seasonal[0]:
        return "q3421"

    elif result_add_q.seasonal[3] > result_add_q.seasonal[0] > result_add_q.seasonal[1] > result_add_q.seasonal[2]:
        return "q4123"
    elif result_add_q.seasonal[3] > result_add_q.seasonal[0] > result_add_q.seasonal[2] > result_add_q.seasonal[1]:
        return "q4132"
    elif result_add_q.seasonal[3] > result_add_q.seasonal[1] > result_add_q.seasonal[0] > result_add_q.seasonal[2]:
        return "q4213"
    elif result_add_q.seasonal[3] > result_add_q.seasonal[1] > result_add_q.seasonal[2] > result_add_q.seasonal[0]:
        return "q4231"
    elif result_add_q.seasonal[3] > result_add_q.seasonal[2] > result_add_q.seasonal[0] > result_add_q.seasonal[1]:
        return "q4312"
    elif result_add_q.seasonal[3] > result_add_q.seasonal[2] > result_add_q.seasonal[1] > result_add_q.seasonal[0]:
        return "q4321"