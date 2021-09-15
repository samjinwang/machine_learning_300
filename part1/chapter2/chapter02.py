# -*- coding: utf-8 -*-
"""Chapter 02 - 우리 애는 머리는 좋은데, 공부를 안해서 그래요(해설).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZiMwGrXBSYUwCR4mW20BrCAo0aPVZAPO

# 주제 : <br>우리 애는 머리는 좋은데, 공부를 안해서 그래요 - 데이터로 살펴보는 우리 아이 학습 성공/실패 요소
----------

## 실습 가이드
    1. 데이터를 다운로드하여 Colab에 불러옵니다.
    2. 필요한 라이브러리는 모두 코드로 작성되어 있습니다.
    3. 코드는 위에서부터 아래로 순서대로 실행합니다.
    
    
## 데이터 소개
    - 이번 주제는 xAPI-Edu-Data 데이터셋을 사용합니다.
    
    - 다음 1개의 csv 파일을 사용합니다.
    xAPI-Edu-Data.csv
    
    - 각 파일의 컬럼은 아래와 같습니다.
    gender: 학생의 성별 (M: 남성, F: 여성)
    NationaliTy: 학생의 국적
    PlaceofBirth: 학생이 태어난 국가
    StageID: 학생이 다니는 학교 (초,중,고)
    GradeID: 학생이 속한 성적 등급
    SectionID: 학생이 속한 반 이름
    Topic: 수강한 과목
    Semester: 수강한 학기 (1학기/2학기)
    Relation: 주 보호자와 학생의 관계
    raisedhands: 학생이 수업 중 손을 든 횟수
    VisITedResources: 학생이 과목 공지를 확인한 횟수
    Discussion: 학생이 토론 그룹에 참여한 횟수
    ParentAnsweringSurvey: 부모가 학교 설문에 참여했는지 여부
    ParentschoolSatisfaction: 부모가 학교에 만족했는지 여부
    StudentAbscenceDays: 학생의 결석 횟수 (7회 이상/미만)
    Class: 학생의 성적 등급 (L: 낮음, M: 보통, H: 높음)
        
    
    
- 데이터 출처: https://www.kaggle.com/aljarah/xAPI-Edu-Data

## 최종 목표
    - 연구용 Tabular 데이터의 이해
    - 데이터 시각화를 통한 인사이트 습득 방법의 이해
    - Scikit-learn 기반의 모델 학습 방법 습득
    - Logistic Regression, XGBoost 기반의 모델 학습 방법 습득
    - 학습된 모델의 평가 방법 및 시각화 방법 습득

- 출제자 : 신제용 강사
---

## Step 0. 연구용 데이터에 관하여

### 연구용 데이터의 목적
목적: 연구의 결과를 이용해 논문을 쓰기 위함 
데이터가 잘 정리되어 있는게 장점 -> 데이터가 다루는게 주목적이 아니라 데이터가 어떻게 취득되었고 데이터를 이용해서 주장하는 바를 가설을 잘 설명하기 위함이다.
즉 분석방법은 간단하게 설명해주고 논문을 잘 설득력있게 해야함 -> 데이터를 잘 정리하고 데이터를 분석할때 쓴 코드를 잘 써야한다. 
이런걸 reproducable 이라함. 어떤과정을 통해 연구를 뒷받침할 수 있게 해야함. 데이터가 좋고 코드를 쉽게 잘 정리해서 공신력을 높인다. 
인용도 잘 해야함.출처를 잘 밝혀줘야함

### 연구용 데이터의 인용

## Step 1. 데이터셋 준비하기
"""

!pip list

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""### 문제 1. Colab Notebook에 Kaggle API 세팅하기

"""

import os

# os.environ을 이용하여 Kaggle API Username, Key 세팅하기
os.environ['KAGGLE_USERNAME'] = 'samjinwang'
os.environ['KAGGLE_KEY'] = 'dbac5e87a67bab917de88fbc54568ec8'

"""### 문제 2. 데이터 다운로드 및 압축 해제하기

"""

# Linux 명령어로 Kaggle API를 이용하여 데이터셋 다운로드하기 (!kaggle ~)
# Linux 명령어로 압축 해제하기
!kaggle datasets download -d aljarah/xAPI-Edu-Data
!unzip "*.zip"

"""### 문제 3. Pandas 라이브러리로 csv파일 읽어들이기

"""

# pd.read_csv()로 csv파일 읽어들이기
df = pd.read_csv('xAPI-Edu-Data.csv')

df
# 카테고리컬 데이터들이 0,1이아닌 클래스 이름으로 되어있다

"""## Step 2. EDA 및 데이터 기초 통계 분석

### 문제 4. 데이터프레임의 각 컬럼 분석하기
"""

# DataFrame에서 제공하는 메소드를 이용하여 컬럼 분석하기 (head(), info(), describe())
df.head()

df.info()
#dtype 클래스 이름으로 되어잇어서 object로 되어있다

df.describe()
#raisehands min부터 max까지 uniform 함
# 그외의 데이터들도 상당히 uniform 함

df.columns
#EDA를 하기위해 어떤 데이터들이 잇는지 확인

df['gender'].value_counts()
# M,F의 분포를 볼수 잇다

df['NationalITy'].value_counts()
#대소문자가 섞여서 있긴하다

df['PlaceofBirth'].value_counts() #위에 국적과 약간의 차이가있다

"""### 문제 5. 수치형 데이터의 히스토그램 그리기

"""

df.columns

# seaborn의 histplot, jointplot, pairplot을 이용해 히스토그램 그리기
#sns.histplot(x= 'raisedhands', data=df) #쌍봉형 데이터이다
#sns.histplot(x='raisedhands', data=df, hue='Class', hue_order=['L', 'M', 'H']) #클래스가 섞여있어서 l,m,n으로 나눈다
sns.histplot(x='raisedhands', data=df, hue='Class', hue_order=['L', 'M', 'H'], kde=True)
#Low는 raisedhand가 낮은쪽에 분포가 많다
#MId는 raisedhadn 쌍봉에 전반적으로 있고
#High는 raisedhand의 높은쪽에 몰려있다
#상당히 유용해보인다 -> low 나 high의 학생들은 잘 가를수 있으나 학생이 middle에 대한건 좀더 볼 필요가 있어보인다 
#->손을 잘들면 성적이 좋을 확률이 높다고 상관성을 볼 수 있다

sns.histplot(x='VisITedResources', data=df, hue='Class', hue_order=['L', 'M', 'H'], kde=True)
# 성적이 낮으면 확인한횟수가 적다
# 성적이 중간이나 높으면 확인한 횟수가 많고, 특히 high인 학생들이 좀더 많이 몰려있다
# rasiedhand와 비슷한 양상이지만 mid 학생들이 확인한 횟수가 좀더 많은곳에 몰려있다 -> 수업 참여정도에 비해 수업외 리소스를 보는 것은 성적에 조금 더 영향을 주는것으로 보여짐
# 수업 참여도와 달리 수업외 리소스를 참고하는 학생들이 성적이 low 갈 확률이 적다

sns.jointplot(x='VisITedResources', y='raisedhands', data=df, hue='Class', hue_order=['L', 'M', 'H'])
# 이 둘이 성적이 상중하로 잘 갈라주기때문에 joint 플랏을 때려봄
# 2D상으로 보면 mid와 high는 구분이 살짝 모호하지만, low와 middle은 구분이 잘 되어보임

sns.histplot(x='AnnouncementsView', data=df, hue='Class', hue_order=['L', 'M', 'H'], kde=True)
# 성적이 낮은 학생들은 공지확인도 잘 안함
# 성적이 mid,high인 학생들은 잘 연관이 없어보임 -> 꼭 공지 확인 잘한다고 성적이 좋은게 아님
# 그래도 공지를 확인을 많이 할 수록 성적이 좋은쪽에 있는건 맞는거 같음

sns.histplot(x='Discussion', data=df, hue='Class', hue_order=['L', 'M', 'H'], kde=True)
# 성적이 low 한애들이 다른 지표들에 비해 discussion에선 높게나옴
# 성적이 높은 학생들도 discussion에 참여 하거나 안하거나 비슷함 (쌍봉형)
# mid는 참가를 안한쪽에 더 몰려있다
# 다른 데이터에 비해 경향성이 좀 덜해 보인다 (discussion참여도와 성적이 크게 관련이 없어보인다)
# 수업에 대한 리소스 참고가 가장 영향이 좋아 보인다

sns.pairplot(df, hue='Class', hue_order=['L', 'M', 'H']) #모든 경우의 수에대한 조인트플랏
#sns.pairplot(df. hue+'Class', hue_order= ['L',"M","H"])
# jointplot이 일자로 나오면 나올수록 상관성이 높은데, 네모모양으로 펼쳐지만 상관성이 낮다고 볼 수 있다
# visited Resource 랑 raisedhand는 각각 상관성이 높아보이지만 실제로 joint 해보면 네모모양임 -> 상관성이 높지가 않다
# 둘이 각각은 상관성이 있어보이지만 같이 있을때는 상관성이 없어보인다 -> 이 두가지가 서로 다른 축에서 데이터를 나눠줄 수 가 있다 -> 두가지를 동시에 보는게 굉장히 유용해 보인다
# 비슷한거 두개를 겹쳐놓고 보는거 보다 비슷한거 두개인데 둘 다 좋은 거면 좋은거 두개로 하는게 더 좋다
# 두개다 좋은 feature가 잇는데 붙였을때 correlation이 낮으면 이 넓게 펼쳐진게 서로를 잘 분리하는데 도움이 된다고 할 수가 있다
# feature 두개가 correlation이 낮을 수록 좋다. 다만, 분석하고자 하는 대상이랑 correlation이 높으면 좋은다. feature끼리는 낮아야 서로를 분리해 조사할 수 있이서 correlation낮아야 좋다
# 디스커션은 플랫하고 별로 상관성도 없다 -> 디스커션이랑 같이 raisedhand를 같이 붙여놓앗을때 별로 좋은 결과가 안나온다

"""### 문제 6. Countplot을 이용하여 범주별 통계 확인하기

"""

# seaborn의 countplot()을 사용
# Hint) x와 hue를 사용하여 범주별 Class 통계 확인

sns.countplot(x='Class', data=df, order=['L', 'M', 'H'])

sns.countplot(x='gender', data=df, hue='Class', hue_order=['L', 'M', 'H'])

df.columns

sns.countplot(x='NationalITy', data=df, hue='Class', hue_order=['L', 'M', 'H'])
plt.xticks(rotation=90)
plt.show()

sns.countplot(x='ParentAnsweringSurvey', data=df, hue='Class', hue_order=['L', 'M', 'H'])

sns.countplot(x='ParentschoolSatisfaction', data=df, hue='Class', hue_order=['L', 'M', 'H'])

sns.countplot(x='Topic', data=df, hue='Class', hue_order=['L', 'M', 'H'])
plt.xticks(rotation=90)
plt.show()

"""### 문제 7. 범주형 대상 Class 컬럼을 수치로 바꾸어 표현하기"""

# L, M, H를 숫자로 바꾸어 표현하기 (eg. L: -1, M: 0, H:1)
# Hint) DataFrame의 map() 메소드를 사용

df['Class_value'] = df['Class'].map(dict(L=-1, M=0, H=1))
df.head()

# 숫자로 바꾼 Class_value 컬럼을 이용해 다양한 시각화 수행하기
gb = df.groupby('gender').mean()['Class_value']
plt.bar(gb.index, gb)

gb = df.groupby('Topic').mean()['Class_value'].sort_values()
plt.barh(gb.index, gb)

gb = df.groupby('StudentAbsenceDays').mean()['Class_value'].sort_values(ascending=False)
plt.bar(gb.index, gb)

"""## Step 3. 모델 학습을 위한 데이터 전처리

### 문제 8. get_dummies()를 이용하여 범주형 데이터 전처리하기
"""

df.columns

# pd.get_dummies()를 이용해 범주형 데이터를 one-hot 벡터로 변환하기
# Hint) Multicollinearity를 피하기 위해 drop_first=True로 설정

X = pd.get_dummies(df.drop(['ParentschoolSatisfaction', 'Class', 'Class_value'], axis=1),
                   columns=['gender', 'NationalITy', 'PlaceofBirth',
                            'StageID', 'GradeID','SectionID', 'Topic',
                            'Semester', 'Relation', 'ParentAnsweringSurvey',
                            'StudentAbsenceDays'], #부모만족도는 뺌
                   drop_first=True) #logistic regression 에서 true를 해야 더 값이 잘나옴(MUlticollinearity)
y = df['Class']

X

"""### 문제 9. 학습데이터와 테스트데이터 분리하기

"""

from sklearn.model_selection import train_test_split

# train_test_split() 함수로 학습 데이터와 테스트 데이터 분리하기
#x_trian, x_test, y_train, y_test = train_test_split(x,y,test_size =0.3, random_state=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

"""## Step 4. Classification 모델 학습하기

### 문제 10. Logistic Regression 모델 생성/학습하기
"""

from sklearn.linear_model import LogisticRegression

# LogisticRegression 모델 생성/학습
model_lr = LogisticRegression(max_iter=10000)
model_lr.fit(X_train, y_train)

"""### 문제 11. 모델 학습 결과 평가하기

"""

from sklearn.metrics import classification_report

# Predict를 수행하고 classification_report() 결과 출력하기
pred = model_lr.predict(X_test)
print(classification_report(y_test, pred))

"""### 문제 12. XGBoost 모델 생성/학습하기

"""

from xgboost import XGBClassifier

# XGBClassifier 모델 생성/학습
model_xgb = XGBClassifier()
model_xgb.fit(X_train, y_train)

"""### 문제 13. 모델 학습 결과 평가하기

"""

# Predict를 수행하고 classification_report() 결과 출력하기
pred = model_xgb.predict(X_test)
print(classification_report(y_test, pred))

"""## Step5 모델 학습 결과 심화 분석하기

### 문제 14. Logistic Regression 모델 계수로 상관성 파악하기
"""

model_lr.classes_

model_lr.coef_.shape #59: 학습에 쓰고있는 feature의 갯수, 3: class 갯수 ("H","L","M") -> 첫번째 것을 출력해보면 성적을 좋게하는 요소를 확인 가능

# Logistic Regression 모델의 coef_ 속성을 plot하기
fig = plt.figure(figsize=(15, 8))
plt.bar(X.columns, model_lr.coef_[0, :]) # 
plt.xticks(rotation=90)
plt.show()
#math가 성적으로  보면 낮은데 여러 feature와 어울렸을때 성적이 상위권인데와는 상관성이 높아보임
#출석일수, 책임자가 엄마, 부모의 설베이 참여가 좋은 영향
#사우디아라비아 학생들의 성적이 높아보임

# Logistic Regression 모델의 coef_ 속성을 plot하기
fig = plt.figure(figsize=(15, 8))
plt.bar(X.columns, model_lr.coef_[1, :])
plt.xticks(rotation=90)
plt.show()
#디스커션의 잦은 참여가 좋은 영향을 주진 않음
#chem을 선택한 학생들이 성적이 안좋음 -> 상관성만 보자

"""### 문제 15. XGBoost 모델로 특징의 중요도 확인하기"""

# XGBoost 모델의 feature_importances_ 속성을 plot하기
fig = plt.figure(figsize=(15, 8))
plt.bar(X.columns, model_xgb.feature_importances_)
plt.xticks(rotation=90)
plt.show()
#여기서도 성실성, 책임자가 어머니엿을때, 리소스 참고

