# stores.csv
This file contains anonymized information about the 45 stores, indicating the type and size of store.
(45개의 상점에 대한 유형과 크기)

# train.csv
This is the historical training data, which covers to 2010-02-05 to 2012-11-01. Within this file you will find the following fields:
(2010-02-05 ~ 2012-11-01 기간의 데이터)
* Store - the store number (상점번호)
* Dept - the department number (부서번호)
* Date - the week (한 주의 시작날짜)
* Weekly_Sales -  sales for the given department in the given store (해당매장에서 해당부서의 일주일 판매량)
* IsHoliday - whether the week is a special holiday week (특별휴일주간 , 일요일 제외)

# test.csv
This file is identical to train.csv, except we have withheld the weekly sales. You must predict the sales for each triplet of store, department, and date in this file.
(train.csv에서 Weekly_Sales를 뺀 데이터셋, Weekly_Sales를 타겟으로 잡는다.)

# features.csv
This file contains additional data related to the store, department, and regional activity for the given dates. It contains the following fields:
(상점, 부서, 지역활동과 관련된 데이터셋)
* Store - the store number (상점번호)
* Date - the week (한 주의 시작날짜)
* Temperature - average temperature in the region (해당 지역의 평균 기온)
* Fuel_Price - cost of fuel in the region (해당 지역의 연료 비용)
* MarkDown1-5 - anonymized data related to promotional markdowns that Walmart is running. MarkDown data is only available after Nov 2011, and is not available for all stores all the time. Any missing value is marked with an NA.
* (월마트에서 진행하는 특별 할인 행사)
* CPI - the consumer price index (소비자 물가 지수)
* Unemployment - the unemployment rate (실업률)
* IsHoliday - whether the week is a special holiday week (특별휴일주간, 일요일 제외)

For convenience, the four holidays fall within the following weeks in the dataset (not all holidays are in the data):
Super Bowl: 12-Feb-10, 11-Feb-11, 10-Feb-12, 8-Feb-13
Labor Day: 10-Sep-10, 9-Sep-11, 7-Sep-12, 6-Sep-13
Thanksgiving: 26-Nov-10, 25-Nov-11, 23-Nov-12, 29-Nov-13
Christmas: 31-Dec-10, 30-Dec-11, 28-Dec-12, 27-Dec-13