# Tableau A/B Test 대시보드 구현

- 결괏값은 다를 수 있습니다.
---

## 1. 목표

`ab_cube_daily.csv`를 활용하여 **A/B Test 결과를 비교 및 해석할 수 있는 Tableau Dashboard를 구성한다.**

---

## 2. 데이터 연결

- `ab_cube_daily.csv`를 Tableau에 연결한다.

---

## 3. 계산 필드 생성

다음 계산 필드를 생성하시오.

### (1) CTR
- SUM(clicks) / SUM(impressions)

### (2) CVR
- SUM(purchases) / SUM(users)

---

## 4. 시각화 구성

---

### (1) KPI 비교 – CTR

#### 요구사항
- Chart Type: Bar Chart

#### 구성
- Columns: `variant_id`
- Rows: `CTR`
- Marks:
  - Color → `variant_id`

---

### (2) KPI 비교 – Revenue

#### 요구사항
- Chart Type: Bar Chart

#### 구성
- Columns: `variant_id`
- Rows: `SUM(revenue)`
- Marks:
  - Color → `variant_id`

---

### (3) Revenue Trend 분석

#### 요구사항
- Chart Type: Line Chart

#### 구성
- Columns: `event_date`
- Rows: `SUM(revenue)`
- Marks:
  - Color → `variant_id`

#### 추가 요구사항
- `event_date`는 연도가 포함된 월 기준으로 설정
- 날짜는 Continuous(연속형)으로 설정

---

### (4) Segment 분석 (Gender)

#### 요구사항
- Chart Type:  Table

#### 구성
- Columns: `variant_id`
- Rows: `Gender`
- Marks:
  - Color → `variant_id`
  - Table → `SUM(revenue)`

---

### (6) Dashboard 구성

다음 시트를 하나의 Dashboard에 배치하시오.

- CTR 비교
- Revenue 비교
- Revenue Trend
- Gender Segment 분석

---

## 5. 제출물

- Tableau Dashboard (스크린샷 또는 `.twb` 파일)