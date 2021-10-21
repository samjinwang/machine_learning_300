# -*- coding: utf-8 -*-
"""Chapter 3. 우리나라의 행복지수는 몇 위_ 아니, 행복지수가 도대체 뭔데_(문제).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sK3UaIyu30iizjAFx1riNqBWMKZtYfGp

# 주제 : 우리나라의 행복지수는 몇 위? 아니, 행복지수가 도대체 뭔데?
----------

## 실습 가이드
    1. 데이터를 다운로드하여 Colab에 불러옵니다.
    2. 필요한 라이브러리는 모두 코드로 작성되어 있습니다.
    3. 코드는 위에서부터 아래로 순서대로 실행합니다.
    
    
## 데이터 소개
    - 이번 주제는 World Happiness Report up to 2020을 사용합니다.
    
    - 다음 6개의 csv 파일을 사용합니다.
    2015.csv
    2016.csv
    2017.csv
    2018.csv
    2019.csv
    2020.csv
    
    - 각 파일의 컬럼은 아래와 같습니다.
    Country: 국가
    Region: 국가의 지역
    Happiness Rank: 행복지수 순위
    Happiness Score: 행복지수 점수
    GDP per capita: 1인당 GDP
    Healthy Life Expectancy: 건강 기대수명
    Social support: 사회적 지원
    Freedom to make life choices: 삶에 대한 선택의 자유
    Generosity: 관용
    Corruption Perception: 부정부패
    Dystopia + Residual: 그 외

    
- 데이터 출처: https://www.kaggle.com/mathurinache/world-happiness-report

## 최종 목표
    - 전문가에 의해 작성된 데이터 분석해보기
    - 시간적으로 변하는 데이터의 Plot 방법 이해
    - 데이터 시각화를 통한 인사이트 습득 방법의 이해
    - 학습된 모델로 부터의 인사이트 획득 방법 습득

- 출제자 : 신제용 강사
---

## Step 0. 행복지수 데이터에 대하여

### 전문가에 의해 작성된 데이터
- 전문가에 의해 통계처리가 완료된 데이터
- survey기관 (여론조사기관)등에서 모집단을 sampling통해 적절한 통계치를 구해 신뢰도 95퍼센트 이내에서 적적한 평균오차를 가진 데이터를 얻음

### 행복지수 점수의 구성에 대하여
- 0~10점으로 구성된 캔드릴 사다리에서 점수가 되어잇음
- dystopia + residual : 각 국가별로 2.0이라는 residual을 받고 6개 항목에 해당안되는 여러가지 요소를 dystopia 점수로 내어 합친것
- 이것들을 합치면 happiness score

## Step 1. 데이터셋 준비하기
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""### 문제 1. Colab Notebook에 Kaggle API 세팅하기

"""

import os

# os.environ을 이용하여 Kaggle API Username, Key 세팅하기
os.environ['KAGGLE_USERNAME'] = 'samjinwang'
os.environ['KAGGLE_KEY'] = "275e30bb4ec266131f19681443d436b8"

"""### 문제 2. 데이터 다운로드 및 압축 해제하기

"""

# Linux 명령어로 Kaggle API를 이용하여 데이터셋 다운로드하기 (!kaggle ~)
# Linux 명령어로 압축 해제하기

!rm *.*
!kaggle datasets download -d mathurinache/world-happiness-report
!unzip '*.zip'

"""### 문제 3. Pandas 라이브러리로 csv파일 읽어들이기

"""

df = dict()
df['2015'] = pd.read_csv('2015.csv')
df['2016'] = pd.read_csv('2016.csv')
df['2017'] = pd.read_csv('2017.csv')
df['2018'] = pd.read_csv('2018.csv')
df['2019'] = pd.read_csv('2019.csv')
df['2020'] = pd.read_csv('2020.csv')

df['2020'].head()

"""## Step 2. 데이터프레임 구성하기

### 문제 4. 년도별 데이터 표준화하기
"""

for key in df:
  print(key, df[key].columns) # 각 데이터프레임의 컬럼 확인

# 각 년도별로 다른 정보를 가진 데이터 프레임의 Column을 동일하게 표준화하기
cols = ['country', 'score', 'economy', 'family', 'health', 'freedom', 'generosity', 'trust', 'residual']

df['2015'].drop(['Region', 'Happiness Rank', 'Standard Error'], axis=1, inplace=True) # generosity, trust 순서 반대
df['2016'].drop(['Region', 'Happiness Rank', 'Lower Confidence Interval',
                 'Upper Confidence Interval'], axis=1, inplace=True) # generosity, trust 순서 반대
df['2017'].drop(['Happiness.Rank', 'Whisker.high', 'Whisker.low'], axis=1, inplace=True) 
df['2018'].drop(['Overall rank'], axis=1, inplace=True) # residual 없음
df['2019'].drop(['Overall rank'], axis=1, inplace=True) # residual 없음
df['2020'].drop(['Regional indicator', 'Standard error of ladder score', 
                 'upperwhisker', 'lowerwhisker', 'Logged GDP per capita',
                 'Social support', 'Healthy life expectancy',
                 'Freedom to make life choices', 'Generosity',
                 'Perceptions of corruption', 'Ladder score in Dystopia'], axis=1, inplace=True)

df['2019'].columns

#residual 추가
df['2018']['residual'] = df['2018']['Score'] - df['2018'][['Country or region', 'Score', 'GDP per capita', 'Social support',
       'Healthy life expectancy', 'Freedom to make life choices', 'Generosity',
       'Perceptions of corruption']].sum(axis = 1) #axis =1 를 넣어줌으로 각 axis별로 합을 구할수 있게됨

df['2019']['residual'] = df['2018']['Score'] - df['2018'][['Country or region', 'Score', 'GDP per capita', 'Social support',
       'Healthy life expectancy', 'Freedom to make life choices', 'Generosity',
       'Perceptions of corruption']].sum(axis = 1)

df['2016'].columns

df['2015'] = df['2015'][['Country', 'Happiness Score', 'Economy (GDP per Capita)', 'Family',
       'Health (Life Expectancy)', 'Freedom', 'Generosity', 'Trust (Government Corruption)',
       'Dystopia Residual']]
df['2016'] = df['2016'][['Country', 'Happiness Score', 'Economy (GDP per Capita)', 'Family',
       'Health (Life Expectancy)', 'Freedom', 'Generosity', 'Trust (Government Corruption)',
       'Dystopia Residual']]

for key in df:
  print(key, df[key].columns) # 각 데이터프레임의 컬럼 확인

for col_name in df:
  df[col_name].columns = cols
# 각 컬럼을 통일된 이름으로 만들어줌

df['2016']

"""### 문제 5. 하나의 데이터프레임으로 합치기

"""

# 아래 셀과 동일한 데이터프레임으로 결합하기
df_all = pd.concat(df, axis = 0)
df_all.index.names = ['year','rank'] #각 연도랑 각각의 rank로 만들어줌

df_all

# 이 셀의 출력 내용이 사라지지 않게 조심하세요.

"""### 문제 6. 원하는 형태로 데이터프레임 정리하기"""

# 아래 셀과 동일한 데이터프레임으로 변형하기
df_all.reset_index(inplace = True)

df_all['rank'] += 1

df_all

# 이 셀의 출력 내용이 사라지지 않게 조심하세요.

"""### 문제 7. Pivot을 이용하여 데이터프레임 재구성하기"""

# 아래 셀과 동일한 데이터프레임 구성하기
# Hint) DataFrame의 pivot() 메소드 활용
rank_table = df_all.pivot(index = 'country',columns = ['year'],values ='rank') #country 기준 pivot이라 abc 순이다
# 모든 국가가 rank가 되어잇는게 아니라 nan 값도 있다
rank_table.sort_values('2020', inplace = True)

rank_table.head(10)

# 이 셀의 출력 내용이 사라지지 않게 조심하세요.

"""## Step 3. 데이터 시각화 수행하기

### 문제 8. 년도별 순위 변화 시각화하기
"""

# 아래 셀과 동일하게 년도별 순위 변화를 시각화하기
# Hint) plt.plot을 이용하고, 필요한 경우 데이터프레임을 변형하면서 그리시오.

fig = plt.figure(figsize = (10,50))
rank2020 = rank_table['2020'].dropna()
for c in rank_table['2020'].dropna().index: #nan 값을뺀 나머지 국가들의 순위를 하나씩 돌려줌
  t = rank_table.loc[c].dropna() # 각국가별로 연도별 랭크를 보여주게됨 #중간에 등수가 빠진 나라는 빼고 해서 그래프가 끊어지는걸 방지
  plt.plot(t.index, t, '.-') #x축:연도 , y축: 연도별 랭킹, 선중간마다 점
  

plt.xlim(['2015','2020']) #15년도 부터 20년도를 딱 끝에맞춤
plt.ylim([0, rank_table.max().max()+1]) #맥스하나면 #연도별 최하위권, 두개면 그중 최고 하위권, +1 은 그냥 위아래 공간 확보
plt.yticks(rank2020, rank2020.index) #각 나라의 랭크를 나라이름으로 바꿔줌
ax = plt.gca()
ax.invert_yaxis() # y축 순서를 거꾸로 뒤집어줌
ax.yaxis.set_label_position('right')
ax.yaxis.tick_right() #y축을 우측으로 옮겨줌
plt.tight_layout()
plt.show()

# 이 셀의 출력 내용이 사라지지 않게 조심하세요.

"""### 문제 9. 분야별로 나누어 점수 시각화하기"""

# sns.barplot()을 이용하여 아래 셀과 동일하게 시각화하기
# Hint) 필요에 따라 데이터프레임을 수정하여 사용하시오. 적절한 수정을 위해 누적합(pd.cumsum())을 활용하시오.

fig = plt.figure(figsize = (6,8))
data = df_all[df_all['year']== '2020']
data = data.loc[data.index[:20]] #2020년 상위20등까지 가져오기

d = data[data.columns[4:]].cumsum(axis = 1) #같은 나라별로 수치끼리 누적그래프 바 만들기
d = d[d.columns[::-1]]  #residual부터(누적합이 가장많이 쌓인곳부터) 그리기
d['country'] = data['country']

sns.set_color_codes('muted') #톤 다운된 색깔로 변경
colors = ['r', 'g','b','c','m','y','purple'][::-1] #각 요소별로 색깔 배정
for idx, c in enumerate(d.columns[:-1]):
  sns.barplot(x=c, y = 'country', data = d, label = c, color = colors[idx])

plt.legend(loc = 'lower right')
plt.title('Top 20 Happiness Scores in Detail')
plt.xlabel('Happiness Score')
sns.despine(left=True, bottom= True) #프레임 제거

# 이 셀의 출력 내용이 사라지지 않게 조심하세요.

"""### 문제 10. Column간의 상관성 시각화하기"""

# 상관성 Heatmap, Pairplot 등으로 상관성을 시각화하기
sns.heatmap(df_all.drop('rank', axis=1).corr(), annot=True, cmap='YlOrRd')

sns.pairplot(df_all.drop('rank',axis = 1))

"""## Step 4. 모델 학습을 위한 데이터 전처리

### 문제 11. 모델의 입력과 출력 정의하기
"""

# 학습할 모델의 입출력을 정의하시오. Column의 의미를 고려하여 선정하시오.
# 이미 행복 지수 자체는 요소들의 합이니까 다른 방식으로 학습해야함
col_input_list = ['economy','family','health','freedom','generosity','trust']
col_out = 'score'

"""### 문제 12. 학습데이터와 테스트데이터 분리하기

"""

# 2015년 ~ 2019년도 데이터를 학습 데이터로, 2020년도 데이터를 테스트 데이터로 분리하기
df_train = df_all[df_all['year'] != '2020']
df_test = df_all[df_all['year'] == '2020']

X_train = df_train[col_input_list]
y_train = df_train[col_out]
X_test = df_test[col_input_list]
y_test = df_test[col_out]

"""### 문제 13. StandardScaler를 이용해 학습 데이터 표준화하기

"""

from sklearn.preprocessing import StandardScaler

# StandardScaler를 이용해 학습 데이터를 표준화하기
scaler = StandardScaler()
scaler.fit(X_train) #X를 scaler에 그냥 넣은 것과는 달리 x_train 을 fit함 -> x_test대해 완전히 blind로 가는것. (테스트를 넣어야할지 상황을 보고 하면됨)

X_norm = scaler.transform(X_train)
X_train = pd.DataFrame(X_norm,index = X_train.index, columns = X_train.columns)

X_norm = scaler.transform(X_test)
X_test = pd.DataFrame(X_norm,index = X_test.index, columns = X_test.columns)

"""## Step 5. Regression 모델 학습하기

### 문제 14. Linear Regression 모델 학습하기
"""

from sklearn.linear_model import LinearRegression

#Trust가 0점이라 데이터가 nan으로 되어있는 나라들이 있다 -> 0으로 바꿔줘야함
X_train.fillna(0,inplace = True)

# LinearRegression 모델 생성/학습
model_lr = LinearRegression()
model_lr.fit(X_train, y_train)

"""### 문제 15. 모델 학습 결과 평가하기"""

from sklearn.metrics import mean_absolute_error, mean_squared_error
from math import sqrt

# Predict를 수행하고 mean_absolute_error, rmse 결과 출력하기
pred = model_lr.predict(X_test)
print(mean_absolute_error(y_test,pred))
print(sqrt(mean_squared_error(y_test,pred)))

"""### 문제 16. XGBoost Regression 모델 학습하기"""

from xgboost import XGBRegressor

# XGBRegressor 모델 생성/학습
model_xgb = XGBRegressor()
model_xgb.fit(X_train,y_train)

pred = model_xgb.predict(X_test)
print(mean_absolute_error(y_test,pred))
print(sqrt(mean_squared_error(y_test,pred)))

"""### 문제 17. 모델 학습 결과 평가하기"""

# Predict를 수행하고 mean_absolute_error, rmse 결과 출력하기
pred =

"""## Step 6. 모델 학습 결과 심화 분석하기

### 문제 18. 실제 값과 추측 값의 Scatter plot 시각화하기
"""

# y_test vs. pred Scatter 플랏으로 시각적으로 분석하기

plt.scatter(x=y_test, y = pred)
plt.plot([0,9],[0,9], 'r-')
plt.show()
#15~19년도 데이터로 20년 데이터를 예측해본것 -> 상당히 결과가 잘 나왔다

"""### 문제 19. LinearRegression 모델의 Coefficient 시각화하기

"""

# model_lr.coef_ 시각화하기

plt.bar(X_train.columns, model_lr.coef_)


#econmoy가 가장큰 영향력을 준다
#현재 standard dev로 보는것이고 이코노미의 편차가 크기때문에 영향력이 높다고 볼 수 있는부분
#generesoity가 낮게 나온건 국가들이 generosity 점수가 크게 안변한다고 볼 수 잇음

"""### 문제 20. XGBoost 모델의 Feature Importance 시각화하기

"""

# model_xgb.feature_importance_ 시각화하기

plt.bar(X_train.columns, model_xgb.feature_importances_)

