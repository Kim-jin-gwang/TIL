# Spark SQL을 활용한 데이터 조인 실습 Skeleton 파일
# 아래의 빈칸(____)을 채운 후 PySpark 환경에서 실행하세요.
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("SparkSQLJoinPractice").getOrCreate()

# 1. 데이터 준비
employee_data = [
    (1, "Alice", "Data Science"),
    (2, "Bob", "Machine Learning"),
    (3, "Charlie", "Data Engineering"),
    (4, "David", "Data Science")
]
salary_data = [
    (1, 4000),
    (2, 5000),
    (3, 4500),
    (5, 5500)
]

employee_df = spark.createDataFrame(employee_data, ["EmpID", "Name", "Department"])
salary_df = spark.createDataFrame(salary_data, ["EmpID", "Salary"])

# 2. Temporary View 등록
employee_df.createOrReplaceTempView("employee")
salary_df.createOrReplaceTempView("salary")

# 3. Inner Join - 공통된 EmpID만 조회
print("INNER JOIN 결과:")
spark.sql("""
    SELECT e.EmpID, e.Name, e.Department, s.Salary
    FROM employee e
    INNER JOIN salary s 
    ON e.EmpID = s.EmpID
""").show()

# 4. Left Join - 모든 직원 정보 + 급여가 없는 경우도 포함
print("LEFT JOIN 결과:")
spark.sql("""
    SELECT e.EmpID, e.Name, e.Department, s.Salary
    FROM employee e
    LEFT JOIN salary s 
    ON e.EmpID = s.EmpID
""").show()

# 5. Right Join - 급여는 있는데 직원 정보가 없는 경우 확인
print("RIGHT JOIN 결과:")
spark.sql("""
    SELECT e.EmpID, e.Name, e.Department, s.Salary
    FROM employee e
    RIGHT JOIN salary s 
    ON e.EmpID = s.EmpID
""").show()

# 6. Full Outer Join - 어느 한 쪽이라도 누락된 경우 포함
print("FULL JOIN 결과:")
spark.sql("""
    SELECT e.EmpID, e.Name, e.Department, s.Salary
    FROM employee e
    FULL OUTER JOIN salary s 
    ON e.EmpID = s.EmpID
""").show()
