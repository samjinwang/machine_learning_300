# -*- coding: utf-8 -*-
"""Chapter01 - 데이터 분석으로 심부전증을 예방할 수 있을까(해설).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iX9VwvZ9TOTwWlSoUv7bKpbxOu9Vdzvg

# 주제 : 데이터 분석으로 심부전증을 예방할 수 있을까?
----------

## 실습 가이드
    1. 데이터를 다운로드하여 Colab에 불러옵니다.
    2. 필요한 라이브러리는 모두 코드로 작성되어 있습니다.
    3. 코드는 위에서부터 아래로 순서대로 실행합니다.
    
    
## 데이터 소개
    - 이번 주제는 Heart Failure Prediction 데이터셋을 사용합니다.
    
    - 다음 1개의 csv 파일을 사용합니다.
    heart_failure_clinical_records_dataset.csv
    
    - 각 파일의 컬럼은 아래와 같습니다.
    age: 환자의 나이
    anaemia: 환자의 빈혈증 여부 (0: 정상, 1: 빈혈)
    creatinine_phosphokinase: 크레아틴키나제 검사 결과
    diabetes: 당뇨병 여부 (0: 정상, 1: 당뇨)
    ejection_fraction: 박출계수 (%)
    high_blood_pressure: 고혈압 여부 (0: 정상, 1: 고혈압)
    platelets: 혈소판 수 (kiloplatelets/mL)
    serum_creatinine: 혈중 크레아틴 레벨 (mg/dL)
    serum_sodium: 혈중 나트륨 레벨 (mEq/L)
    sex: 성별 (0: 여성, 1: 남성)
    smoking: 흡연 여부 (0: 비흡연, 1: 흡연)
    time: 관찰 기간 (일)
    DEATH_EVENT: 사망 여부 (0: 생존, 1: 사망)
    
    
    
- 데이터 출처: https://www.kaggle.com/andrewmvd/heart-failure-clinical-data


## 최종 목표
    - 의료 데이터와 그 분석에 대한 이해
    - Colab 및 Pandas 라이브러리 사용법 이해
    - 데이터 시각화를 통한 인사이트 습득 방법의 이해
    - Scikit-learn 기반의 모델 학습 방법 습득
    - Classification 모델의 학습과 평가 방법 이해

- 출제자 : 신제용 강사
---

## Step 0. 의료 데이터셋에 대하여

### 의료 데이터의 수집
데이터 3법으로 의료데이터를 민간연구자가 쓸 수 있게 되었다

### 의료 데이터 분석의 현재

### Accuracy, Precision, 그리고 Recall

Confusion Matrix를 통해 정답 true/false 예측결과 true/fase를 table로 해서 TP(t,t),FP(f,t),FN(t,f), TN (f,f) 로 나눈다. (정답,예측결과)

Accuracy: TP + TN / TP + FP + FN + TN (모든 케이스 중에 제대로 맞출 확률)
Precision: TP / TP + FP (True라고 예측한것 중에 실제로 True를 맞출 확률)
Recall (재현률): TP / TP + FN (실제 True라고 하는것들중에 얼마나 맞췄는지에대한 확률)

의료데이터 중에는 recall이 제일 중요 -> 실제로 병걸린 사람중에 얼마나 제대로 맞췄는지를 찾는게 중요하다) -> Recall 값이 좋아야 진단이 좋아짐
-> 리콜을 100프로로 유지하면 precision이 0이 되므로 0.95이상을 유지하는게 가장 이상적이다)

-> t/f를 구분짓는 threshold를 잘 조절하면서 recall값에대해 precision 값을 최대치로 만드는것이 목표이다

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
os.environ['KAGGLE_KEY'] = '86abde4641deb4585043c243d9d68b99'

!kaggle -h

"""### 문제 2. 데이터 다운로드 및 압축 해제하기

"""

# Linux 명령어로 Kaggle API를 이용하여 데이터셋 다운로드하기 (!kaggle ~)
# Linux 명령어로 압축 해제하기
!kaggle datasets download -d andrewmvd/heart-failure-clinical-data
!unzip '*.zip'

!ls

"""### 문제 3. Pandas 라이브러리로 csv파일 읽어들이기

"""

# pd.read_csv()로 csv파일 읽어들이기
df = pd.read_csv('heart_failure_clinical_records_dataset.csv')

df

"""## Step 2. EDA 및 데이터 기초 통계 분석

### 문제 4. 데이터프레임의 각 컬럼 분석하기
"""

# DataFrame에서 제공하는 메소드를 이용하여 컬럼 분석하기 (head(), info(), describe())
df.head(5)
# df.head(-5) #뒤에 5개까지 보여줌

df.info()
# datatype, non-null count를 잘 볼것. 각 column에 대한 data type을 확인한다
# non-null: 값이 비는지 확인

df.describe() #수치적 데이터의 통계적 값
# mean: 0이나 1 로 치우치면 imbalance하다고 볼 수 있음
# max나 min이 과도하게 크거나 작은지 확인해본다 둘의 차이가 많이 나는지, 그 사이의 증가량이 어떤지 -> 둘중 하나가 너무 크거나 작으면 outlier 를 생각해봐야함
# column간의 collerate한지 여부도 봐야함

"""### 문제 5. 수치형 데이터의 히스토그램 그리기

"""

# seaborn의 histplot, jointplot, pairplot을 이용해 히스토그램 그리기
#sns.histplot(x='age', data=df)
sns.histplot(x='age', data=df, hue='DEATH_EVENT', kde=True) #사망한 사람들은 비교적 나이대가 고루게 분포되어있고, 사망하지 않은 사람들은 젊은쪽이 많다

#sns.histplot(df['creatinine_phosphokinase']) #3000 이상은 outlyer로 보는게 좋아보임
sns.histplot(data=df.loc[df['creatinine_phosphokinase'] < 3000, 'creatinine_phosphokinase']) #통계적 특성이 잘 안보여서 유용해 보이지 않음

#sns.histplot(x='ejection_fraction', data=df) #중간에 빈게 있다 -> bins로 조절해본다
sns.histplot(x='ejection_fraction', data=df, bins=13, hue='DEATH_EVENT', kde=True) #ejection fraction이 낮은사람이 사망률이 높고 높으면 낮다.
#비율의 차이는 크지만 사망자수가 한쪽에 분포가 많다 -> precision은 잘 나올지는 몰라도 recall 값을 구하기 안좋아보임

#sns.histplot(x='platelets', data=df) #통계적으로는 잘 분포되어 보임
sns.histplot(x='platelets', data=df, hue='DEATH_EVENT') #근데 death event와는 관련이 잘 없어보임

sns.histplot(x='time', data=df, hue='DEATH_EVENT', kde=True)

sns.jointplot(x='platelets', y='creatinine_phosphokinase', hue='DEATH_EVENT', data=df, alpha=0.3) #두값을 이용해 scatter를 만들고 death event따라 색을 나눠줌 -> 많이 뭉쳐있어서 안좋아보임
# alpha 값을 주면 더 뭉친곳이 더 진하게 보임

sns.jointplot(x='ejection_fraction', y='serum_creatinine', data=df, hue='DEATH_EVENT') #러닝후 가장 도드라 지는 두개를 join로 비교해서 본다 -> 어느정도 구분되는 영역이 보인다

"""### 문제 6. Boxplot 계열을 이용하여 범주별 통계 확인하기

"""

# 수치형 데이터 말고 boxplot으로 범주별로 따로 통계를 확인해봄
# seaborn의 Boxplot 계열(boxplot(), violinplot(), swarmplot())을 사용
# Hint) hue 키워드를 사용하여 범주 세분화 가능
sns.boxplot(x='DEATH_EVENT', y='ejection_fraction', data=df)
# 박스의 높낮이로 평균값의 차이를 알 수 있음
# 위아래 선으로 전체적인 값들의 범위를 볼 수 있음
# 자동적으로 outlier될만한 값들이 위아래 점들로 표기됨
# 많은 데이터로 헷갈리면 boxplot으로 일목요연하게 볼 수 있음
# 경영층이 애용하므로 경영층과 얘기할때 쓰면 좋다

sns.boxplot(x='smoking', y='ejection_fraction', data=df) #스모킹 여부에 따른 ejection 여부
# 흡연자가 ejection fraction값이 좁은걸 볼 수 있다

sns.violinplot(x='DEATH_EVENT', y='ejection_fraction', data=df)
# 박스 플랏의 variation
# 가운데 줄로 박스플랏의 내용을 볼 수잇고. 양옆으로 나온값을 보고 histogramd에서 볼 수 있는 값들을 볼 수 있다
# 위아래 얇은 걸로 outlier알 수 있다
# 데이터를 더 잘보고싶을때 쓰지 보고용으로는 잘 안씀

#sns.violinplot(x='DEATH_EVENT', y='ejection_fraction', hue = 'smoking', data=df) # 스모킹과 데스이벤트에따라 4가지를 볼 수 있다

#sns.swarmplot(x='DEATH_EVENT', y='platelets', data=df) #데이터가 일정갯수 잇으면 점으로 표현 -> boxplot처럼 통계정보는 없다. 시각적으로 좋지만 통계적인것은 알기 힘듬

sns.swarmplot(x='DEATH_EVENT', y='platelets', hue='smoking', data=df) #스모킹에 관한것이 시각적으로 얼마나 영향을 주는지 볼 수 있다 ->둘이 갈라져 있으면 스모킹이 영향을 잘 준다는걸 알 숭 있다
# 바이올린 플랏에서 좀 더 나아간 버전

"""## Step 3. 모델 학습을 위한 데이터 전처리

### 문제 7. StandardScaler를 이용하여 데이터 전처리하기
"""

from sklearn.preprocessing import StandardScaler #평균을 0으로 stand_dev를 1로 바꿔주는 작업

df.columns

# 수치형 입력 데이터, 범주형 입력 데이터, 출력 데이터로 구분하기
# x-num에 전체 데이터중 수치에 관련된 데이터만 모은다
# x-categorical = 위에서 안뺀것중에 나머지인 범주형데이터를 모은다
X_num = df[['age', 'creatinine_phosphokinase','ejection_fraction', 'platelets','serum_creatinine', 'serum_sodium']]
X_cat = df[['anaemia', 'diabetes', 'high_blood_pressure', 'sex', 'smoking']]
y = df['DEATH_EVENT'] #출력 데이터

# 수치형 입력 데이터를 전처리하고 입력 데이터 통합하기
scaler = StandardScaler() #
scaler.fit(X_num)
X_scaled = scaler.transform(X_num) #standardscaler와 transform을 통해 numpy 값으로 바꾼다 -> 데이터 프레임이 아니어서 index와 column정보가 빠짐
X_scaled = pd.DataFrame(data=X_scaled, index=X_num.index, columns=X_num.columns) #데이터 프레임을 씌우는 작업을 함
X = pd.concat([X_scaled, X_cat], axis=1) # axis =1 을해서 column과 row를 안붙이도록 함

X.head() #수치값들끼리 column이 붙어있고, 0과1로 나누어진 cateogory 값들이 붙어있다

"""### 문제 8. 학습데이터와 테스트데이터 분리하기

"""

from sklearn.model_selection import train_test_split

# train_test_split() 함수로 학습 데이터와 테스트 데이터 분리하기 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1) #shuffle은 true. testsize = 0.3 70프로가 트레인용으로 쓰임. 
#random_state = 1트레인과 테스트를 랜덤으로 나눠주는 시드
# 순차적으로 학습해야할경우 shuffle 을 false로 함

"""## Step 4. Classification 모델 학습하기

### 문제 9. Logistic Regression 모델 생성/학습하기
"""

from sklearn.linear_model import LogisticRegression

# LogisticRegression 모델 생성/학습
model_lr = LogisticRegression(max_iter=1000)
# model_lr = LogisticRegression(max_iter=1000, verbose = 1) #verbose 값으로 학습하는 과정을 보여줌
model_lr.fit(X_train, y_train)

"""### 문제 10. 모델 학습 결과 평가하기

"""

from sklearn.metrics import classification_report

# Predict를 수행하고 classification_report() 결과 출력하기
pred = model_lr.predict(X_test)
print(classification_report(y_test, pred))

"""### 문제 11. XGBoost 모델 생성/학습하기
가장 많이쓰는 모델

"""

from xgboost import XGBClassifier

# XGBClassifier 모델 생성/학습
model_xgb = XGBClassifier()
model_xgb.fit(X_train, y_train)

"""### 문제 12. 모델 학습 결과 평가하기

"""

# Predict를 수행하고 classification_report() 결과 출력하기
pred = model_xgb.predict(X_test)
print(classification_report(y_test, pred))

"""### 문제 13. 특징의 중요도 확인하기

"""

# XGBClassifier 모델의 feature_importances_를 이용하여 중요도 plot
plt.bar(X.columns, model_xgb.feature_importances_) #이것만 출력하면 선그래프로 나옴 가장 두드러지는 feature정도는 확인 가능
# 근데 time은 분석하기 적절하지 못한 수치라 수치형 데이터 x_num에서 time을 배제하고 다시학습후 결과를 보는게 좋다
plt.xticks(rotation=90) #컬럼 이름들이 겹치는것을 돌려서 나눠보여줌
plt.show()

"""## Step5 모델 학습 결과 심화 분석하기

### 문제 14. Precision-Recall 커브 확인하기
"""

from sklearn.metrics import plot_precision_recall_curve

# 두 모델의 Precision-Recall 커브를 한번에 그리기 (힌트: fig.gca()로 ax를 반환받아 사용)
# precision을 1부터해서 recall 증가시킬때 어떻게 요동치는지 보임.
# 리콜을 증가시킬때 precision이 잘 유지됨 -> AP 값이 높아짐 -> 1에 가까울 수록 좋음
fig = plt.figure()
ax = fig.gca() # 동일한 x에대가 plot을 같이 그릴수 있음
plot_precision_recall_curve(model_lr, X_test, y_test, ax=ax)
plot_precision_recall_curve(model_xgb, X_test, y_test, ax=ax) #이게 lr 보다 대체적으로 좋은 값을 가짐

"""### 문제 15. ROC 커브 확인하기"""

from sklearn.metrics import plot_roc_curve

# 두 모델의 ROC 커브를 한번에 그리기 (힌트: fig.gca()로 ax를 반환받아 사용)
# false positive를 낮게 유지시키는게 목적  -> FP의 값을 올리면서 TP의 값이 얼마나 빨리 1에 도달하는지 본다. -> 즉, fp가 낮을때 1에 먼저 도달하는게 좋은 값
# AUC (area under curve) #아래영역이 더 큰게 좋음
fig = plt.figure()
ax = fig.gca()
plot_roc_curve(model_lr, X_test, y_test, ax=ax)
plot_roc_curve(model_xgb, X_test, y_test, ax=ax)

