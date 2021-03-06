# -*- coding: utf-8 -*-
"""Chapter 1 - 자동으로 모은 데이터는 분석하기 어렵다면서_ 자동으로 모은 중고 자동차 데이터를 분석해보자!(문제).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-KaDQgGqnMqXCAlyhnoXj7t8I7oJAOmM

# 주제 : 자동으로 모은 데이터는 분석하기 어렵다면서? 자동으로 모은 중고 자동차 데이터를 분석해보자!
----------

## 실습 가이드
    1. 데이터를 다운로드하여 Colab에 불러옵니다.
    2. 필요한 라이브러리는 모두 코드로 작성되어 있습니다.
    3. 코드는 위에서부터 아래로 순서대로 실행합니다.
    
    
## 데이터 소개
    - 이번 주제는 Used Cars Dataset을 사용합니다.
    - 파일은 한 개이며, 각각의 컬럼은 아래와 같습니다.
    
    - vehicles.csv
    id : 중고차 거래의 아이디
    url : 중고차 거래 페이지
    region : 해당 거래의 관리 지점
    region_url : 거래 관리 지점의 홈페이지
    price : 기입된 자동차의 거래가
    year : 거래가 기입된 년도
    manufacturer : 자동차를 생산한 회사
    model : 자동차 모델명
    condition : 자동차의 상태
    cylinders : 자동차의 기통 수
    fuel : 자동차의 연료 타입
    odometer : 자동차의 운행 마일 수
    title_status : 자동차의 타이틀 상태 (소유주 등록 상태)
    transmission : 자동차의 트랜스미션 종류
    vin : 자동차의 식별 번호 (vehicle identification number)
    drive : 자동차의 구동 타입
    size : 자동차 크기
    type : 자동차의 일반 타입 (세단, ...)
    paint_color : 자동차 색상
    image_url : 자동차 이미지
    description : 세부 설명
    county : 실수로 생성된 미사용 컬럼
    state : 거래가 업로드된 미 주
    lat : 거래가 업로드된 곳의 위도
    long : 거래가 업로드된 곳의 경도
    
    
- 데이터 출처: https://www.kaggle.com/austinreese/craigslist-carstrucks-data

## 최종 목표
    - 스크래핑된 dirty 데이터 클리닝 방법 이해
    - 다양한 종류의 데이터 정규화 방법 습득
    - 데이터 시각화를 통한 인사이트 습득 방법의 이해
    - Scikit-learn 기반의 모델 학습 방법 습득
    - XGBoost, LightGBM 기반의 모델 학습 방법 습득
    - 학습된 모델의 평가 방법 및 시각화 방법 습득

- 출제자 : 신제용 강사
---

## Step 0. 데이터 스크래핑이 대하여

### 스크래핑을 이용한 자동 데이터 습득

*   데이터의 형식을 예측 후 그대로 고정적으로 지정해서 가져옴 (데이터 구성이 예측이 벗어난 경우 (리뉴얼이나, 팝업창때메 평소랑 다름)는 동작이 잘 안될수 도 있다)
* 고로 스크래핑 데이터는 오류가 많을 수 밖에 없다 -> 데이터가 비어있거나 형식이 틀리고, 아웃라이어가 많다
(문자열 같은경우 앞뒤 공백이 많고, html 태그가 같이 포함되는경우가 많다, 인코딩에 의해 깨진 문자도 많다.)
(숫자같은 경우는 최대값이나 최소값으로 잘못기입되는 경우가 많다. 숫자대신 문자열이 들어가 분석에 차질이 생김)

### 스크래핑된 데이터에서 아웃라이어의 특징

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
# os.environ을 이용하여 Kaggle API Username, Key 세팅하기
os.environ['KAGGLE_USERNAME'] = 'samjinwang'
os.environ['KAGGLE_KEY'] = 'e808743bea20e4a89b105256b9d5941b'

"""### 문제 2. 데이터 다운로드 및 압축 해제하기

"""

# Li# Linux 명령어로 Kaggle API를 이용하여 데이터셋 다운로드하기 (!kaggle ~)
# Linux 명령어로 압축 해제하기
!rm *.* #모든 파일 삭제 추후 다시 실행시 파일을 엎어쓰는지 선택을 안해도 됨
!kaggle datasets download -d austinreese/craigslist-carstrucks-data
!unzip '*.zip'

"""### 문제 3. Pandas 라이브러리로 csv파일 읽어들이기

"""

df = pd.read_csv('vehicles.csv')

"""## Step 2. EDA 및 데이터 기초 통계 분석

### 문제 4. 불필요한 데이터 데이터프레임에서 제거하기
"""

# DataFrame에서 제공하는 메소드를 이용하여 각 데이터프레임의 구조 분석하기 (head(), info(), describe())
# 데이터프레임에서 불필요한 컬럼 제거하기

df.head()
#year을 age로환산해서 만든다
#범주형 데이터 cylinder fuel 은 누락된 데이터가 있을 확률이 높아보임
#odometer은 정확히 적혀잇는 정도가 다 다를것같아보임
#VIN 은 별로 안중요해보임

df.info() #



df.isna().sum() #null이 빠져있는 값들이 많아보인다
#condition은 중요한정보인데 많이 빠져있다
#주요한 요소들로 예상되는데 비어있는 값들이 많다

df.describe()

df.columns

df.drop([ 'id', 'url', 'region_url', 'VIN',
         'image_url', 'description', 'state', 'lat','county' 
         'long', 'posting_date'], axis=1, inplace=True) #머신러닝에 분석이 어렵거나 비어있는 값이 많은 경우는 빼버림

df['age'] = 2021 - df['year']
df.drop('year', axis=1, inplace=True) #year를 age(차의 나이)로 바꾼다 _> 분석에 더 적합

df.columns



"""### 문제 5. 범주형 데이터의 통계 분석하기

"""

df.columns

# 범주형 데이터의 값의 범위, 기초 통계 분석하기


len(df['manufacturer'].value_counts()) #총 43개의 종류
df['manufacturer'].value_counts()

fig = plt.figure(figsize=(8, 10))
#팔린 차의 제조사 별로 팔린횟수 기준으로 내림차순한다
sns.countplot(y='manufacturer', data=df.fillna('n/a'), order=df.fillna('n/a')['manufacturer'].value_counts().index)

#모든 차의 모델을 다 출력해본다 ->굉장히 많음
for model, num in zip(df['model'].value_counts().index, df['model'].value_counts()):
  print(model, num)

  # num 이 1인 값 즉 한번밖에 안된값은 제대로 스크랩된 데이터가 대부분 아니다

# new 도 na에 포함할지 생각해 봐야함
sns.countplot(y='condition', data=df.fillna('n/a'), order=df.fillna('n/a')['condition'].value_counts().index)

# 
sns.countplot(y='cylinders', data=df.fillna('n/a'), order=df.fillna('n/a')['cylinders'].value_counts().index)

#웬만하면 gas 차 휘발유
sns.countplot(y='fuel', data=df.fillna('n/a'), order=df.fillna('n/a')['fuel'].value_counts().index)

# 자동기어인 애들이 주로다

sns.countplot(y='transmission', data=df.fillna('n/a'), order=df.fillna('n/a')['transmission'].value_counts().index)

#4개가 다 비슷해서 그대로 써도 무난할듯
sns.countplot(y='drive', data=df.fillna('n/a'), order=df.fillna('n/a')['drive'].value_counts().index)

sns.countplot(y='size', data=df.fillna('n/a'), order=df.fillna('n/a')['size'].value_counts().index)

sns.countplot(y='type', data=df.fillna('n/a'), order=df.fillna('n/a')['type'].value_counts().index)

sns.countplot(y='paint_color', data=df.fillna('n/a'), order=df.fillna('n/a')['paint_color'].value_counts().index)

"""### 문제 6. 수치형 데이터의 통계 분석하기"""

# 수치형 데이터의 값의 범위, 기초 통계 분석하기
# 수치형 데이터의 값의 범위, 기초 통계 분석하기
#box플랏으로 봣을때 좋은 결과가 안나옴
#
fig = plt.figure(figsize=(8, 2))
sns.rugplot(x='price', data=df, height=1)

fig = plt.figure(figsize=(8, 2))
#outlier가 많아서 rugplot으로 해본다
sns.rugplot(x='odometer', data=df, height=1)

sns.histplot(x='age', data=df, bins=18, kde=True) #이건 무난하게 시각화가 됨



"""## Step 3. 데이터 클리닝 수행하기

### 문제 7. 범주형 데이터 시각화하여 분석하기
"""

# Boxplot 계열로 범주형 데이터를 시각화하여 분석하기
df.columns

sns.boxplot(x='manufacturer', y = 'price', data=df.fillna('n/a')) #알아보기 힘듬

sns.boxplot(x='fuel', y = 'price', data=df.fillna('n/a')) #아웃라이어가 너무 많음

"""### 문제 8. 범주형 데이터 클리닝하기"""

# 범주형 데이터를 아래 방법 중 적절히 판단하여 처리하기
df.columns

# 1. 결손 데이터가 포함된 Row를 제거
df['manufacturer'].fillna('others').value_counts() # 전체 기준을 제조사로 함

col = 'manufacturer'
counts = df[col].fillna('others').value_counts() #결손값을 기타로 채운후 '제조사' 컬럼의 요소들 갯수를 파악
plt.plot(range(len(counts)),counts) #차가 많이 팔린 제조사로 내림 차운으로 선그래프가 나타남 (x축은 많이팔린 순위),(y축은 팔린 댓수)

n_categorical = 10
counts.index[n_categorical:] #많이 팔린 상위 n개 그룹을 제외한 나머지
df[col] = df[col].apply(lambda s : s if str(s) not in counts.index[n_categorical:] else 'others')

df[col].value_counts()

#같은 방식
col = 'region'
counts = df[col].fillna('others').value_counts()
plt.plot(range(len(counts)),counts) #5부터 급격한 감소

n_categorical = 5
df[col] = df[col].apply(lambda s : s if str(s) not in counts.index[n_categorical:] else 'others')

df[col].value_counts()

col = 'model'
counts = df[col].fillna('others').value_counts()
plt.plot(range(len(counts[:20])),counts[:20]) #상위 10개만 해도 될듯

n_categorical = 10
others =  counts.index[n_categorical:]
df[col] = df[col].apply(lambda s : s if str(s) not in others else 'others') #30000개를 일일이 처리하려면 힘드니 others를 따로 만들어서 한다

df[col].value_counts()

col = 'condition'
counts = df[col].fillna('others').value_counts()
plt.plot(range(len(counts)),counts) #5부터 급격한 감소

n_categorical = 3
others =  counts.index[n_categorical:]
df[col] = df[col].apply(lambda s : s if str(s) not in others else 'others')

col = 'cylinders'
counts = df[col].fillna('others').value_counts()
plt.plot(range(len(counts)),counts)
n_categorical = 4
others =  counts.index[n_categorical:]
df[col] = df[col].apply(lambda s : s if str(s) not in others else 'others')

col = 'fuel'
counts = df[col].fillna('others').value_counts()
plt.plot(range(len(counts)),counts)
n_categorical = 2
others =  counts.index[n_categorical:]
df[col] = df[col].apply(lambda s : s if str(s) not in others else 'others')

# col = 'title_status'
# counts = df[col].fillna('others').value_counts()
# plt.plot(range(len(counts)),counts)
# n_categorical = 2
# others =  counts.index[n_categorical:]
df.drop('title_status',axis = 1, inplace = True)

col = 'transmission'
counts = df[col].fillna('others').value_counts()
plt.plot(range(len(counts)),counts)

n_categorical = 2
others =  counts.index[n_categorical:]
df[col] = df[col].apply(lambda s : s if str(s) not in others else 'others')

col = 'drive'
counts = df[col].fillna('others').value_counts()
plt.plot(range(len(counts)),counts)
#수정할 필요 없어보임
df[col].fillna('others').value_counts() #그래도 결측값은 확실히 추가해 놓는다

col = 'size'
counts = df[col].fillna('others').value_counts()
plt.plot(range(len(counts)),counts)

n_categorical = 2
others =  counts.index[n_categorical:]
df[col] = df[col].apply(lambda s : s if str(s) not in others else 'others')

col = 'type'
counts = df[col].fillna('others').value_counts()
plt.plot(range(len(counts)),counts)
n_categorical = 8
others =  counts.index[n_categorical:]

df[col] = df[col].apply(lambda s : s if str(s) not in others else 'others')

df.loc[df[col]=='other',col] = 'others'
df[col].value_counts() #other과 others를 합쳐준다

col = 'paint_color'
counts = df[col].fillna('others').value_counts()
plt.plot(range(len(counts)),counts)
n_categorical = 7
others =  counts.index[n_categorical:]
df[col] = df[col].apply(lambda s : s if str(s) not in others else 'others')

# 2. 결손 데이터를 others 범주로 변경하기

# 3. 지나치게 소수로 이루어진 범주를 others 범주로 변경하기

#(4. Classifier를 학습해서 결손 데이터 추정하여 채워넣기)

"""### 문제 9. 수치형 데이터 시각화하여 분석하기"""

# Seaborn을 이용하여 범주형 데이터를 시각화하여 분석하기
# Hint) 값의 범위가 너무 넓을 경우 histplot() 등이 잘 동작하지 않으므로, rugplot을 활용
fig = plt.figure(figsize=(8, 2))
sns.rugplot(x='price', data=df, height=1)

fig = plt.figure(figsize=(8, 2))
sns.rugplot(x='odometer', data=df, height=1)

fig = plt.figure(figsize=(8, 2))
sns.histplot(x='age', data=df, bins = 18,kde = True)

"""### 문제 10. 수치형 데이터 클리닝하기"""

# quantile() 메소드를 이용하여 outlier 제거하고 시각화하여 확인하기

p1 = df['price'].quantile(0.99) #상위  1퍼센트 수치값 66995
 
p2 = df['price'].quantile(0.1) #하위 10퍼센트 500
p1,p2

df = df[(p1 >df['price']) &(p2 <df['price'])]

o1 = df['odometer'].quantile(0.99) #상위  1퍼센트 수치값 280000
 
o2 = df['odometer'].quantile(0.1) #하위 10퍼센트 14939

o1,o2

df = df[(o1 >df['odometer']) &(o2 <df['odometer'])]

df.describe()

plt.figure(figsize = (10,5))
sns.boxplot(x='manufacturer', y = 'price', data=df) #더 잘보임
# 값의 범위가 비슷함 (아웃라이어 포함) -> 얼마나 유용할지는 두고봐야할듯
# 그래도 상/하위 25프로(박스자체)만 볼때는 유용해 보이기도 함 통계적으로는

plt.figure(figsize = (10,5))
sns.boxplot(x='model', y = 'price', data=df) #제조사보다 좀더 다이내믹함
#비싼보델일수록 확실히 높은 구간에 있음

"""### 문제 11. 컬럼간의 Correlation Heatmap으로 시각화하기"""

sns.heatmap(df.corr(), annot = True, cmap= 'YlOrRd') 
#odometer 와 차의 나이가 값에 악영향을 줌을 알 수 있다 
#odometer 와 age가 상관관계가 있어보임 -> 둘의 콜라보는 좋지 않을지 몰라도 좋은 feature로서의 역할은 하긴할듯

"""## Step 4. 모델 학습을 위한 데이터 전처리

### 문제 12. StandardScaler를 이용해 수치형 데이터 표준화하기
"""

from sklearn.preprocessing import StandardScaler

# StandardScaler를 이용해 수치형 데이터를 표준화하기
X_num = df[['odometer','age']]
scalar = StandardScaler()
scalar.fit(X_num)
X_scaled = scalar.transform(X_num)
X_scaled = pd.DataFrame(X_scaled, index = X_num.index, columns=X_num.columns)


# get_dummies를 이용해 범주형 데이터를 one-hot 벡터로 변경하기
X_cat = df.drop(['price','odometer','age'],axis = 1)
X_cat = pd.get_dummies(X_cat) #linear regression은 안하므로 drop first는 안한다

# 입출력 데이터 통합하기
X = pd.concat([X_scaled, X_cat],axis =1 )
y = df['price']

X.head()

X.shape

X.isna().sum()
#age가 결측값이 있음
X.fillna(0.0,inplace=True) #age가 이미 표준화된 값이라 굳이 평균값을 안집어넣어도됨

"""### 문제 13. 학습데이터와 테스트데이터 분리하기

"""

from sklearn.model_selection import train_test_split

# train_test_split() 함수로 학습 데이터와 테스트 데이터 분리하기
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state = 1)

"""## Step 5. Regression 모델 학습하기

### 문제 14. XGBoost Regression 모델 학습하기
"""

from xgboost import XGBRegressor

# XGBRegressor 모델 생성/학습
model_reg = XGBRegressor()
model_reg.fit(X_train, y_train)

"""### 문제 15. 모델 학습 결과 평가하기"""

from sklearn.metrics import mean_absolute_error, mean_squared_error
from math import sqrt

# Predict를 수행하고 mean_absolute_error, rmse 결과 출력하기
pred = model_reg.predict(X_test)
print(mean_absolute_error(y_test,pred)) 
print(sqrt(mean_squared_error(y_test,pred))) #에러값 제곱하고 평균을 낸후 루트를 씌움 (rmse)
#에러값들이 상당히 크다

"""## Step 6. 모델 학습 결과 심화 분석하기

### 문제 16. 실제 값과 추측 값의 Scatter plot 시각화하기
"""

# y_test vs. pred Scatter 플랏으로 시각적으로 분석하기
# Hint) Scatter로 시각적 확인이 어려울 경우, histplot 등 활용

plt.scatter(x=y_test,y=pred,alpha = 0.005) #alpha를 조절해서 겹치는게 적은 부분을 옅게표현
plt.plot([0,60000],[0,60000],'r-')

#값이 낮은 차들은 y = x축에 잘 형성된걸보니 잘 분석이 되었다
#근데 실제로 아주 값이 작은 차는 학습모델에선 매우 비싸게 예측됨
#그리고 차가 비쌀때 (4만불이상)은 실제보다 가격이 낮다고 측정됨

sns.histplot(x=y_test,y=pred)
plt.plot([0,60000],[0,60000],'r-')

"""### 문제 17. 에러 값의 히스토그램 확인하기

"""

# err의 히스토그램으로 에러율 히스토그램 확인하기
err = (pred - y_test) / y_test *100
sns.histplot(err[err<600]) #에러율이 6보다 작은애들
plt.xlabel('error(%)')
plt.xlim(-100,100)
plt.grid()

#값이 0보다 약간 왼쪽으로 치우져져있다 -> underestimated 되어있다
#예상 보다 낮게 측정될때는 -100%까지 가진 않는다
#예상 보다 높게 측정될때는 +100%를 웃도는 경우도 있다 -> 에러율이 아주높은 애들이 있다

plt.show()

#에러율 0근처에 값이 몰려있을수록 잘학습된 모델이다
#안좋을수록 좌우로 퍼짐

err = (pred - y_test)
sns.histplot(err) #에러율이 6보다 작은애들
plt.xlabel('error($)')

plt.grid()

#에러값 자체로만 봤을 땐 0기준으로 정돈되어 나타나 있다

#성능개선 아이디어
# 범주형 데이터 클리닝시 
# model의 경우 이름이 다양하니까 대문자,소문자 둘중하나로 다 맞춘후 other로 빠지는 값을 최대한 줄여본다
# 또는 model명을 표준화해서 조금씩 다르게 표현된 모델명을 하나로 맞춰주는 작업을 해줘도 좋을듯
# 가격을 표준화를 많이 시켜서 저가,고가로 나누는게 아니라 좀더 잘 나눴으면 좋앗을지도