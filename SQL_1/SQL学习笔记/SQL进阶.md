# 企业初级技术实操模拟题 — 答案解析

> 适用岗位：实施工程师 / 技术支持 / 数据库运维 / 初级开发
> 覆盖范围：SQL（DDL/DML/查询/聚合/JOIN/子查询） + Python基础 + Debug
> 难度定位：★ 入门级 / ★★ 基础级 / ★★★ 进阶级

---

# 一、SQL 实操复习题

## 0. 数据库背景说明

围绕"小型医院信息系统"，共四张表：

- `patient` 患者表
- `department` 科室表
- `doctor` 医生表
- `visit` 就诊记录表

---

## 第一部分：DDL（数据定义语言）

### SQL-01 ★ 创建 patient 表

**题目：** 创建患者表，含 patient_id（主键）、name（非空）、gender、age、department_id。

**答案：**

```sql
CREATE TABLE patient (
    patient_id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    gender VARCHAR(10),
    age INT,
    department_id INT
);
```

**解析：**
- `PRIMARY KEY`：主键，非空且唯一
- `NOT NULL`：该字段不允许为空值
- `VARCHAR(50)`：变长字符串，最大50字符
- `INT`：整数类型

---

### SQL-02 ★ 创建 department 表

**答案：**

```sql
CREATE TABLE department (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(50) NOT NULL
);
```

---

### SQL-03 ★ 创建 visit 表

**答案：**

```sql
CREATE TABLE visit (
    visit_id INT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    visit_date DATE,
    fee DECIMAL(10, 2)
);
```

**解析：**
- `DATE`：日期类型，格式如 `'2024-01-15'`
- `DECIMAL(10, 2)`：小数，共10位，其中小数点后2位（适合存金额）
- 也可以用 `FLOAT` 或 `NUMERIC`，但金额推荐 `DECIMAL` 避免精度丢失

---

### SQL-04 ★ 增加 phone 字段

**答案：**

```sql
ALTER TABLE patient ADD phone VARCHAR(20);
```

**解析：** `ALTER TABLE ... ADD ...` 用于向已有表添加新列。

---

### SQL-05 ★ 删除 phone 字段

**答案：**

```sql
ALTER TABLE patient DROP COLUMN phone;
```

**解析：** `DROP COLUMN` 删除列。注意：MySQL 用 `DROP COLUMN`，Oracle 也一样；部分数据库可简写 `DROP`。

---

### SQL-06 ★ 删除 visit 表

**答案：**

```sql
DROP TABLE visit;
```

**解析：** 区分三个易混淆概念：

| 语句 | 作用 | 删除对象 | 能否恢复 |
|------|------|----------|----------|
| `DELETE` | 删除表中的**数据行** | 数据 | 可回滚（事务内） |
| `DROP` | 删除整张**表结构** | 表（结构+数据） | 不能 |
| `TRUNCATE` | 清空表中所有数据 | 数据 | 不能 |

口诀：**DELETE删行，DROP删表，TRUNCATE清空。**

---

## 第二部分：DML（数据操作语言）

### SQL-07 ★ 插入科室数据

**答案：**

```sql
INSERT INTO department (department_id, department_name) VALUES
(1, '内科'),
(2, '外科'),
(3, '儿科'),
(4, '急诊科');
```

**解析：** 一条 `INSERT` 可以插入多行，用逗号分隔。也可以写四条单独的 INSERT。

---

### SQL-08 ★ 插入患者数据

**答案：**

```sql
INSERT INTO patient (patient_id, name, gender, age, department_id) VALUES
(1, '张三', '男', 25, 1),
(2, '李四', '女', 32, 2),
(3, '王五', '男', 17, 3),
(4, '赵六', '女', 65, 1),
(5, '钱七', '男', 45, 4);
```

---

### SQL-09 ★ 修改张三的年龄为26

**答案：**

```sql
UPDATE patient SET age = 26 WHERE name = '张三';
```

**⚠️ 重要提醒：** `UPDATE` 必须带 `WHERE`，否则会把全表所有行都改掉！这是生产环境最常见事故之一。

---

### SQL-10 ★ 修改王五的科室为急诊科

**答案：**

```sql
UPDATE patient SET department_id = 4 WHERE name = '王五';
```

---

### SQL-11 ★ 删除患者钱七

**答案：**

```sql
DELETE FROM patient WHERE name = '钱七';
```

---

### SQL-12 ★ 删除所有年龄小于18岁的患者

**答案：**

```sql
DELETE FROM patient WHERE age < 18;
```

**⚠️ 再次提醒：** `DELETE` 不带 `WHERE` = 删全表！写之前先 `SELECT * FROM ... WHERE ...` 确认一下删的是哪些行。

---

## 第三部分：SELECT 基础

### SQL-13 ★ 查询所有患者的姓名、性别、年龄

**答案：**

```sql
SELECT name, gender, age FROM patient;
```

---

### SQL-14 ★ 查询年龄大于60岁的患者

**答案：**

```sql
SELECT * FROM patient WHERE age > 60;
```

---

### SQL-15 ★ 查询所有女性患者

**答案：**

```sql
SELECT * FROM patient WHERE gender = '女';
```

---

### SQL-16 ★ 查询年龄在20～50岁之间（BETWEEN）

**答案：**

```sql
SELECT * FROM patient WHERE age BETWEEN 20 AND 50;
```

**解析：** `BETWEEN a AND b` 是**闭区间**，包含两端，等价于 `age >= 20 AND age <= 50`。

---

### SQL-17 ★ 查询姓名以"张"开头（LIKE）

**答案：**

```sql
SELECT * FROM patient WHERE name LIKE '张%';
```

**解析：** 通配符：
- `%`：匹配任意长度的任意字符（包括0个）
- `_`：匹配**单个**任意字符

例如：`'张_'` 只匹配"张三""张伟"，不匹配"张三丰"。

---

### SQL-18 ★ 查询年龄不是30岁的患者

**答案：**

```sql
SELECT * FROM patient WHERE age <> 30;
-- 或者
SELECT * FROM patient WHERE age != 30;
```

**解析：** `<>` 是 SQL 标准写法，所有数据库都支持；`!=` 是常见写法，MySQL、PostgreSQL、SQL Server 都支持，但严格来说 `<>` 更标准。

---

### SQL-19 ★ 查询年龄大于30岁的男性患者

**答案：**

```sql
SELECT * FROM patient WHERE age > 30 AND gender = '男';
```

**解析：** 多个条件用 `AND`（并且）或 `OR`（或者）连接。`AND` 的优先级高于 `OR`，复杂条件建议加括号。

---

### SQL-20 ★ 查询年龄最大的患者

**答案：**

```sql
SELECT * FROM patient WHERE age = (SELECT MAX(age) FROM patient);
```

或者简单写法（只能拿到年龄，拿不到完整信息）：

```sql
SELECT MAX(age) FROM patient;
```

---

### SQL-21 ★ 查询年龄最小的患者

**答案：**

```sql
SELECT * FROM patient WHERE age = (SELECT MIN(age) FROM patient);
```

---

### SQL-22 ★ 按年龄从大到小排序

**答案：**

```sql
SELECT * FROM patient ORDER BY age DESC;
```

**解析：**
- `ORDER BY ... ASC`：升序（默认，可省略）
- `ORDER BY ... DESC`：降序

---

### SQL-23 ★ 年龄最大的前三名患者

**答案（MySQL / PostgreSQL）：**

```sql
SELECT * FROM patient ORDER BY age DESC LIMIT 3;
```

**答案（SQL Server）：**

```sql
SELECT TOP 3 * FROM patient ORDER BY age DESC;
```

**答案（Oracle）：**

```sql
SELECT * FROM (SELECT * FROM patient ORDER BY age DESC) WHERE ROWNUM <= 3;
```

**解析：** 不同数据库的"取前N条"语法不同，这是面试常考点。

| 数据库 | 语法 |
|--------|------|
| MySQL / PostgreSQL | `LIMIT n` |
| SQL Server | `TOP n` |
| Oracle | `ROWNUM <= n` |

---

## 第四部分：聚合函数

### SQL-24 ★ 患者总人数

**答案：**

```sql
SELECT COUNT(*) FROM patient;
```

**解析：** `COUNT(*)` 统计行数，包括 NULL 值；`COUNT(列名)` 统计该列非空值的行数。

---

### SQL-25 ★ 平均年龄

**答案：**

```sql
SELECT AVG(age) FROM patient;
```

---

### SQL-26 ★ 最大年龄和最小年龄

**答案：**

```sql
SELECT MAX(age) AS 最大年龄, MIN(age) AS 最小年龄 FROM patient;
```

**解析：** `AS` 用于给列起别名，让结果更易读。

---

### SQL-27 ★ 年龄总和

**答案：**

```sql
SELECT SUM(age) FROM patient;
```

---

### SQL-28 ★★ 男性患者人数

**答案：**

```sql
SELECT COUNT(*) FROM patient WHERE gender = '男';
```

---

### SQL-29 ★★ 女性患者人数

**答案：**

```sql
SELECT COUNT(*) FROM patient WHERE gender = '女';
```

---

### SQL-30 ★★ 每个科室的患者数量

**答案：**

```sql
SELECT department_id, COUNT(*) AS 人数
FROM patient
GROUP BY department_id;
```

**解析：** `GROUP BY` 的黄金法则——**SELECT 后面的列，要么在 GROUP BY 里，要么被聚合函数包裹**。否则会报错或得到无意义的结果。

---

## 第五部分：GROUP BY + HAVING

### SQL-31 ★★ 患者人数超过2人的科室

**答案：**

```sql
SELECT department_id, COUNT(*) AS 患者人数
FROM patient
GROUP BY department_id
HAVING COUNT(*) > 2;
```

**解析：** `WHERE` vs `HAVING` 的区别是面试必考题：

| 子句 | 作用时机 | 过滤对象 | 能否用聚合函数 |
|------|----------|----------|----------------|
| `WHERE` | 分组**之前**过滤 | 行 | ❌ 不能 |
| `HAVING` | 分组**之后**过滤 | 分组 | ✅ 可以 |

记忆口诀：**WHERE筛行，HAVING筛组。**

---

### SQL-32 ★★ 平均年龄超过40岁的科室

**答案：**

```sql
SELECT department_id, AVG(age) AS 平均年龄
FROM patient
GROUP BY department_id
HAVING AVG(age) > 40;
```

---

### SQL-33 ★★ 每个科室的最大年龄

**答案：**

```sql
SELECT department_id, MAX(age) AS 最大年龄
FROM patient
GROUP BY department_id;
```

---

### SQL-34 ★★ 每个科室平均年龄，从高到低

**答案：**

```sql
SELECT department_id, AVG(age) AS 平均年龄
FROM patient
GROUP BY department_id
ORDER BY AVG(age) DESC;
```

**解析：** 执行顺序：`FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY`。所以 `ORDER BY` 可以用 SELECT 里定义的别名。

---

### SQL-35 ★★ 患者人数最多的科室

**答案：**

```sql
SELECT department_id, COUNT(*) AS 患者人数
FROM patient
GROUP BY department_id
ORDER BY COUNT(*) DESC
LIMIT 1;
```

---

## 第六部分：JOIN

### SQL-36 ★★ 查询患者姓名和科室名称

**答案：**

```sql
SELECT p.name AS 患者姓名, d.department_name AS 科室名称
FROM patient p
JOIN department d ON p.department_id = d.department_id;
```

**解析：**
- `JOIN` 或 `INNER JOIN`：内连接，只返回两边都匹配的行
- `p` 和 `d` 是表别名，简化写法
- `ON` 后面写连接条件

---

### SQL-37 ★★ 男性患者的姓名和科室名称

**答案：**

```sql
SELECT p.name, d.department_name
FROM patient p
JOIN department d ON p.department_id = d.department_id
WHERE p.gender = '男';
```

---

### SQL-38 ★★ 年龄大于50岁的患者姓名、年龄、科室名称

**答案：**

```sql
SELECT p.name, p.age, d.department_name
FROM patient p
JOIN department d ON p.department_id = d.department_id
WHERE p.age > 50;
```

---

### SQL-39 ★★ 查询患者姓名和医生姓名（三表关联）

**答案：**

```sql
SELECT p.name AS 患者姓名, doc.doctor_name AS 医生姓名
FROM patient p
JOIN visit v ON p.patient_id = v.patient_id
JOIN doctor doc ON v.doctor_id = doc.doctor_id;
```

**解析：** 三表 JOIN 的连接思路：找"中间表"。`visit` 表同时关联了患者和医生，是典型的中间表/关联表。

---

### SQL-40 ★★ 张三的所有就诊记录

**答案：**

```sql
SELECT p.name AS 患者姓名, doc.doctor_name AS 医生姓名, 
       v.visit_date AS 就诊日期, v.fee AS 费用
FROM patient p
JOIN visit v ON p.patient_id = v.patient_id
JOIN doctor doc ON v.doctor_id = doc.doctor_id
WHERE p.name = '张三';
```

---

### SQL-41 ★★ 每个医生接诊了多少名患者

**答案：**

```sql
SELECT doc.doctor_name, COUNT(DISTINCT v.patient_id) AS 患者人数
FROM doctor doc
JOIN visit v ON doc.doctor_id = v.doctor_id
GROUP BY doc.doctor_name;
```

**解析：** 这里用 `COUNT(DISTINCT patient_id)` 而不是 `COUNT(*)`。

- `COUNT(*)`：统计就诊**次数**（同一个患者看同一个医生多次会算多次）
- `COUNT(DISTINCT patient_id)`：统计**不同患者人数**（去重）

题目问的是"接诊了多少名患者"，应该用 `DISTINCT` 去重。

---

### SQL-42 ★★ 每个科室接诊患者数量

**答案：**

```sql
SELECT d.department_name, COUNT(DISTINCT v.patient_id) AS 接诊人数
FROM department d
JOIN doctor doc ON d.department_id = doc.department_id
JOIN visit v ON doc.doctor_id = v.doctor_id
GROUP BY d.department_name;
```

**解析：** 三表关联路径：`department` → `doctor` → `visit`

---

## 第七部分：子查询 / EXISTS

### SQL-43 ★★ 年龄高于平均年龄的患者

**答案：**

```sql
SELECT * FROM patient
WHERE age > (SELECT AVG(age) FROM patient);
```

**解析：** 子查询放在 `WHERE` 后面，先执行子查询算出平均年龄，再用这个值过滤外层。

---

### SQL-44 ★★ 没有任何就诊记录的患者

**方法一：NOT EXISTS**

```sql
SELECT * FROM patient p
WHERE NOT EXISTS (
    SELECT 1 FROM visit v WHERE v.patient_id = p.patient_id
);
```

**方法二：LEFT JOIN + IS NULL**

```sql
SELECT p.*
FROM patient p
LEFT JOIN visit v ON p.patient_id = v.patient_id
WHERE v.visit_id IS NULL;
```

**解析：**
- `LEFT JOIN`：左表全部保留，右表没有匹配的填 NULL
- 然后用 `WHERE 右表主键 IS NULL` 找出"没匹配上的"
- `NOT EXISTS` 性能通常更好，尤其是数据量大的时候

---

### SQL-45 ★★★ 从未去过"内科"的患者

**答案：**

```sql
SELECT * FROM patient p
WHERE NOT EXISTS (
    SELECT 1 FROM visit v
    JOIN doctor doc ON v.doctor_id = doc.doctor_id
    JOIN department d ON doc.department_id = d.department_id
    WHERE v.patient_id = p.patient_id
      AND d.department_name = '内科'
);
```

**另一种写法：NOT IN**

```sql
SELECT * FROM patient
WHERE patient_id NOT IN (
    SELECT v.patient_id FROM visit v
    JOIN doctor doc ON v.doctor_id = doc.doctor_id
    JOIN department d ON doc.department_id = d.department_id
    WHERE d.department_name = '内科'
);
```

---

### SQL-46 ★★★ 至少就诊过两次的患者

**答案：**

```sql
SELECT p.name AS 患者姓名, COUNT(*) AS 就诊次数
FROM patient p
JOIN visit v ON p.patient_id = v.patient_id
GROUP BY p.patient_id, p.name
HAVING COUNT(*) >= 2;
```

---

### SQL-47 ★★★ 就诊次数超过3次的患者

**答案：**

```sql
SELECT p.name AS 患者姓名, COUNT(*) AS 就诊次数
FROM patient p
JOIN visit v ON p.patient_id = v.patient_id
GROUP BY p.patient_id, p.name
HAVING COUNT(*) > 3;
```

---

## 第八部分：综合 SQL

### SQL-48 ★★★ 年龄超过50岁且就诊过的患者

**答案：**

```sql
SELECT p.name AS 姓名, p.age AS 年龄, COUNT(*) AS 就诊次数
FROM patient p
JOIN visit v ON p.patient_id = v.patient_id
WHERE p.age > 50
GROUP BY p.patient_id, p.name, p.age;
```

---

### SQL-49 ★★★ 每个科室的患者数量和平均年龄

**答案：**

```sql
SELECT d.department_name AS 科室名称,
       COUNT(p.patient_id) AS 患者数量,
       AVG(p.age) AS 平均年龄
FROM department d
LEFT JOIN patient p ON d.department_id = p.department_id
GROUP BY d.department_id, d.department_name;
```

**解析：** 用 `LEFT JOIN` 而不是 `INNER JOIN`，因为即使某个科室没有患者，也应该显示出来（患者数量为0）。

---

### SQL-50 ★★★ 就诊总费用超过1000元的患者

**答案：**

```sql
SELECT p.name AS 患者姓名, SUM(v.fee) AS 总费用
FROM patient p
JOIN visit v ON p.patient_id = v.patient_id
GROUP BY p.patient_id, p.name
HAVING SUM(v.fee) > 1000
ORDER BY SUM(v.fee) DESC;
```

---

### SQL-51 ★★★ 就诊次数最多的患者

**答案：**

```sql
SELECT p.name AS 姓名, COUNT(*) AS 就诊次数
FROM patient p
JOIN visit v ON p.patient_id = v.patient_id
GROUP BY p.patient_id, p.name
ORDER BY COUNT(*) DESC
LIMIT 1;
```

**注意：** 如果有多人并列第一，`LIMIT 1` 只返回一个。要返回所有并列第一的，需要子查询。

---

### SQL-52 ★★★ 没有任何患者的科室

**答案：**

```sql
SELECT d.department_name
FROM department d
LEFT JOIN patient p ON d.department_id = p.department_id
WHERE p.patient_id IS NULL;
```

**解析：** 这是面试经典题。为什么用 `LEFT JOIN` 而不是 `INNER JOIN`？

- `INNER JOIN`：只返回两边都有的行 → 没有患者的科室会被过滤掉，永远查不到
- `LEFT JOIN`：左表（科室）全部保留，没有患者的地方填 NULL → 用 `IS NULL` 就能找出来

一句话总结：**要找"没有的"，用 LEFT JOIN + IS NULL。**

---

# 二、Python 基础编程复习题

## 第一阶段：变量 / 输入输出

### PY-01 ★ 输入姓名，输出问候

**答案：**

```python
name = input("请输入姓名：")
print(f"你好，{name}")
```

**解析：** `input()` 返回的是字符串。`f"..."` 是 f-string 格式化，Python 3.6+ 支持。

---

### PY-02 ★ 输入两个整数，输出和差积商

**答案：**

```python
a = int(input("请输入第一个整数："))
b = int(input("请输入第二个整数："))

print(f"和：{a + b}")
print(f"差：{a - b}")
print(f"积：{a * b}")
print(f"商：{a / b}")
```

**解析：**
- `int()` 把字符串转成整数
- `/` 是真除法（返回 float），`//` 是整除（返回整数）

---

### PY-03 ★ 判断奇数偶数

**答案：**

```python
n = int(input("请输入一个整数："))
if n % 2 == 0:
    print("偶数")
else:
    print("奇数")
```

**解析：** `%` 是取模运算符，`n % 2 == 0` 表示能被2整除。

---

### PY-04 ★ 年龄段判断

**答案：**

```python
age = int(input("请输入年龄："))

if age < 18:
    print("未成年")
elif age <= 59:
    print("成年人")
else:
    print("老年人")
```

**解析：** `elif` = else if，多分支条件判断。注意顺序很重要，是从上往下匹配的。

---

## 第二阶段：if / for / while

### PY-05 ★ 输出 1～100

**答案：**

```python
for i in range(1, 101):
    print(i)
```

**解析：** `range(1, 101)` 生成 1 到 100 的序列（左闭右开，右边不包含）。

---

### PY-06 ★ 输出 1～100 所有偶数

**答案：**

```python
for i in range(2, 101, 2):
    print(i)
```

或者：

```python
for i in range(1, 101):
    if i % 2 == 0:
        print(i)
```

**解析：** `range(start, end, step)` 的第三个参数是步长。

---

### PY-07 ★ 计算 1+2+...+100

**答案：**

```python
total = 0
for i in range(1, 101):
    total += i
print(total)
```

**答案（高斯公式，一行搞定）：**

```python
print((1 + 100) * 100 // 2)
```

---

### PY-08 ★ 计算 1～100 所有偶数的和

**答案：**

```python
total = 0
for i in range(2, 101, 2):
    total += i
print(total)
```

---

### PY-09 ★ 计算 1² + 2² + ... + n²

**答案：**

```python
n = int(input("请输入n："))
total = 0
for i in range(1, n + 1):
    total += i * i
print(total)
```

---

### PY-10 ★★ 判断质数

**答案：**

```python
n = int(input("请输入一个整数："))

if n < 2:
    print("不是质数")
else:
    is_prime = True
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            is_prime = False
            break
    if is_prime:
        print("是质数")
    else:
        print("不是质数")
```

**解析：**
- 质数定义：大于1的自然数，除了1和自身外不能被其他数整除
- 优化：只需要检查到 √n 即可（因为如果 n 有因数 a，那一定有对应的 n/a，其中一个 ≤ √n）
- `break`：跳出当前循环

---

## 第三阶段：列表

### PY-11 ★ 找出列表最大值（不用 max()）

**答案：**

```python
nums = [3, 7, 2, 9, 5, 1]

max_val = nums[0]
for num in nums:
    if num > max_val:
        max_val = num

print(max_val)
```

**思路：** 假设第一个元素是最大值，然后遍历，遇到更大的就更新。

---

### PY-12 ★ 找出最小值（不用 min()）

**答案：**

```python
nums = [3, 7, 2, 9, 5, 1]

min_val = nums[0]
for num in nums:
    if num < min_val:
        min_val = num

print(min_val)
```

---

### PY-13 ★ 计算列表元素之和（不用 sum()）

**答案：**

```python
nums = [3, 7, 2, 9, 5, 1]

total = 0
for num in nums:
    total += num

print(total)
```

---

### PY-14 ★ 统计列表中有多少个偶数

**答案：**

```python
nums = [3, 7, 2, 9, 5, 1]

count = 0
for num in nums:
    if num % 2 == 0:
        count += 1

print(count)
```

---

### PY-15 ★★ 删除列表中的所有负数

**答案（推荐：创建新列表）：**

```python
nums = [3, -1, 5, -2, 7]

result = []
for num in nums:
    if num >= 0:
        result.append(num)

print(result)
```

**⚠️ 易错点：** 不要在遍历列表的同时删除元素，会导致索引错乱（见 DEBUG-01）。

---

### PY-16 ★★ 找出列表中第二大的数字

**答案：**

```python
nums = [3, 7, 2, 9, 5, 1]

first = second = float('-inf')
for num in nums:
    if num > first:
        second = first
        first = num
    elif num > second and num != first:
        second = num

print(second)
```

**解析：** 一次遍历，维护两个变量。时间复杂度 O(n)，比排序后取第二高效。

---

### PY-17 ★★ 去掉列表中的重复元素

**答案（最简单，用 set）：**

```python
nums = [1, 2, 2, 3, 3, 3, 4]
result = list(set(nums))
print(result)
```

**答案（保持顺序，不使用 set）：**

```python
nums = [1, 2, 2, 3, 3, 3, 4]

result = []
for num in nums:
    if num not in result:
        result.append(num)

print(result)
```

**解析：** `set` 是集合，自动去重，但会打乱顺序。如果要保持原顺序，用第二种方法。

---

## 第四阶段：字符串

### PY-18 ★ 统计字符串长度

**答案：**

```python
s = "hello world"
print(len(s))
```

---

### PY-19 ★ 统计字符串中有多少个数字

**答案：**

```python
s = "abc123def45"

count = 0
for c in s:
    if c.isdigit():
        count += 1

print(count)
```

**解析：** `str.isdigit()` 判断字符是否是数字字符。也可以用 `'0' <= c <= '9'`。

---

### PY-20 ★★ 统计每个字符出现的次数

**答案（经典写法）：**

```python
s = "hello"

result = {}
for c in s:
    if c in result:
        result[c] += 1
    else:
        result[c] = 1

for char, count in result.items():
    print(f"{char}: {count}")
```

**答案（进阶，用 dict.get）：**

```python
s = "hello"
result = {}
for c in s:
    result[c] = result.get(c, 0) + 1
print(result)
```

**解析：** 这是 Python 面试最高频的基础题之一，必须熟练掌握。核心思路是用字典做"计数器"。

---

### PY-21 ★★ 判断回文字符串

**答案（双指针法，推荐）：**

```python
s = "abcba"

left = 0
right = len(s) - 1
is_palindrome = True

while left < right:
    if s[left] != s[right]:
        is_palindrome = False
        break
    left += 1
    right -= 1

print("是回文" if is_palindrome else "不是回文")
```

**答案（Python 一行流）：**

```python
s = "abcba"
if s == s[::-1]:
    print("是回文")
else:
    print("不是回文")
```

**解析：** `s[::-1]` 是 Python 字符串反转的切片写法。面试时如果要展示算法思维，推荐双指针法。

---

### PY-22 ★★ 统计句子中的单词数量

**答案：**

```python
sentence = "hello world python"
words = sentence.split()
print(len(words))
```

**解析：** `split()` 不带参数时，按任意空白字符（空格、制表符、换行等）分割，并且自动忽略首尾空格。

---

## 第五阶段：字典

### PY-23 ★ 创建字典并输出

**答案：**

```python
person = {
    "姓名": "张三",
    "年龄": 20,
    "专业": "计算机科学"
}

print(person["姓名"])
print(person["年龄"])
print(person["专业"])
```

---

### PY-24 ★★ 计算平均成绩

**答案：**

```python
students = {
    "张三": 80,
    "李四": 90,
    "王五": 70
}

total = 0
for score in students.values():
    total += score

average = total / len(students)
print(average)
```

---

### PY-25 ★★ 找出成绩最高的学生

**答案：**

```python
students = {
    "张三": 80,
    "李四": 90,
    "王五": 70
}

best_name = ""
best_score = 0

for name, score in students.items():
    if score > best_score:
        best_score = score
        best_name = name

print(f"{best_name} {best_score}")
```

---

### PY-26 ★★★ 统计列表中每个元素出现的次数

**答案：**

```python
nums = [1, 2, 2, 3, 3, 3]

result = {}
for num in nums:
    if num in result:
        result[num] += 1
    else:
        result[num] = 1

for num, count in result.items():
    print(f"{num} → {count}")
```

**解析：** 这道题和 PY-20 本质一样，都是"计数器模式"。是 Python 基础面试最经典的题目之一，一定要能手写出来。

---

## 第六阶段：函数

### PY-27 ★ 定义加法函数

**答案：**

```python
def add(a, b):
    return a + b

# 测试
print(add(1, 2))  # 输出 3
```

**解析：** `return` 返回结果并结束函数。没有 `return` 的函数返回 `None`。

---

### PY-28 ★ 判断偶数函数

**答案：**

```python
def is_even(n):
    return n % 2 == 0

# 测试
print(is_even(4))  # True
print(is_even(5))  # False
```

---

### PY-29 ★★ 判断质数函数

**答案：**

```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# 测试
print(is_prime(7))   # True
print(is_prime(10))  # False
```

---

### PY-30 ★★ 统计元音字母数量

**答案：**

```python
def count_vowels(s):
    vowels = "aeiouAEIOU"
    count = 0
    for c in s:
        if c in vowels:
            count += 1
    return count

# 测试
print(count_vowels("hello"))  # 2
```

---

## 第七阶段：文件操作

### PY-31 ★★ 写入并读取文件

**答案：**

```python
# 写入
with open("test.txt", "w", encoding="utf-8") as f:
    f.write("第一行\n")
    f.write("第二行\n")
    f.write("第三行\n")

# 读取
with open("test.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)
```

**解析：**
- `with open(...)` 是推荐写法，自动关闭文件，不需要手动 `f.close()`
- `"w"`：写入模式（会覆盖原有内容）
- `"r"`：读取模式
- `encoding="utf-8"`：指定编码，避免中文乱码

---

### PY-32 ★★ 统计文件行数

**答案：**

```python
with open("test.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    print(len(lines))
```

或者逐行读取（适合大文件）：

```python
count = 0
with open("test.txt", "r", encoding="utf-8") as f:
    for line in f:
        count += 1
print(count)
```

---

### PY-33 ★★ 统计文件中的单词数量

**答案：**

```python
with open("test.txt", "r", encoding="utf-8") as f:
    content = f.read()
    words = content.split()
    print(len(words))
```

---

### PY-34 ★★ 统计日志级别出现次数

**答案：**

```python
counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}

with open("test.txt", "r", encoding="utf-8") as f:
    for line in f:
        for level in counts:
            if level in line:
                counts[level] += 1

for level, count in counts.items():
    print(f"{level}: {count}")
```

---

### PY-35 ★★★ 找出所有包含 ERROR 的行

**答案：**

```python
with open("test.txt", "r", encoding="utf-8") as f:
    for line in f:
        if "ERROR" in line:
            print(line.strip())
```

**解析：** 这是最贴近实际运维工作的题目——日志过滤。`strip()` 去掉首尾空白和换行符。

---

## 第八阶段：异常处理

### PY-36 ★ 处理输入非整数的情况

**答案：**

```python
try:
    n = int(input("请输入整数："))
    print(f"你输入的是：{n}")
except ValueError:
    print("请输入整数")
```

**解析：** `try-except` 是 Python 异常处理机制。`ValueError` 是类型转换失败时抛出的异常。

---

### PY-37 ★★ 除法函数处理除零

**答案：**

```python
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "除数不能为0"

# 测试
print(divide(10, 2))   # 5.0
print(divide(10, 0))   # 除数不能为0
```

---

## 第九阶段：代码阅读

### PY-38 ★★ 列表引用问题

**代码：**

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)
```

**答案：** 输出 `[1, 2, 3, 4]`

**解析：** Python 中列表是**可变对象**，`b = a` 只是让 b 指向同一个列表对象（引用赋值），不是复制。所以通过 b 修改，a 也会变。

如果要真正复制：
- `b = a.copy()`
- `b = list(a)`
- `b = a[:]`

---

### PY-39 ★★ if-else 分支

**代码：**

```python
x = 10
if x > 5:
    x = x + 10
else:
    x = x - 10
print(x)
```

**答案：** 输出 `20`

**解析：** 10 > 5 为真，执行 x = 10 + 10 = 20。

---

### PY-40 ★★ for 循环累加

**代码：**

```python
total = 0
for i in range(1, 6):
    total += i
print(total)
```

**答案：** 输出 `15`

**解析：** `range(1, 6)` 是 1, 2, 3, 4, 5，累加 = 1+2+3+4+5 = 15。

---

### PY-41 ★★ 遍历列表输出偶数

**代码：**

```python
nums = [1, 2, 3, 4, 5]
for n in nums:
    if n % 2 == 0:
        print(n)
```

**答案：** 输出：
```
2
4
```

---

### PY-42 ★★★ 字典计数

**代码：**

```python
d = {}
for x in [1, 2, 2, 3, 3, 3]:
    if x not in d:
        d[x] = 1
    else:
        d[x] += 1
print(d)
```

**答案：** 输出 `{1: 1, 2: 2, 3: 3}`

**解析：** 这就是经典的"计数器模式"。遍历列表，字典的 key 存元素，value 存出现次数。

---

# 三、代码 Debug 题

## DEBUG-01 ★★ 遍历列表时删除元素

**问题代码：**

```python
nums = [1, 2, 3, 4, 5]

for i in range(len(nums)):
    if nums[i] % 2 == 0:
        nums.remove(nums[i])

print(nums)
```

**1. 问题：** 会报 `IndexError`（索引越界），或者结果不正确。

**2. 原因：** 在遍历列表的同时删除元素，列表长度会变短，但 `range(len(nums))` 是在循环开始前就计算好的。当删除元素后，后面的元素会往前移，导致跳过某些元素，甚至索引越界。

**举个例子：**
- 初始：[1, 2, 3, 4, 5]，i=0 → 1 不删
- i=1 → 2 被删，列表变成 [1, 3, 4, 5]
- i=2 → 此时 nums[2] 是 4（而不是原来的 3），3 被跳过了

**3. 修改方案：**

**方案一（推荐）：创建新列表**

```python
nums = [1, 2, 3, 4, 5]
result = [n for n in nums if n % 2 != 0]
print(result)
```

**方案二：倒序遍历**

```python
nums = [1, 2, 3, 4, 5]
for i in range(len(nums) - 1, -1, -1):
    if nums[i] % 2 == 0:
        nums.pop(i)
print(nums)
```

---

## DEBUG-02 ★★ 函数没有 return

**问题代码：**

```python
def add(a, b):
    print(a + b)

result = add(1, 2)
print(result + 3)
```

**问题：** 报错 `TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'`

**原因：** 函数 `add` 用了 `print` 而不是 `return`。没有 `return` 的函数默认返回 `None`。所以 `result` 是 `None`，`None + 3` 就报错了。

**修改：**

```python
def add(a, b):
    return a + b

result = add(1, 2)
print(result + 3)  # 输出 6
```

---

## DEBUG-03 ★★ 字典 key 不存在

**问题代码：**

```python
users = {
    "zhangsan": 20,
    "lisi": 25
}

print(users["wangwu"])
```

**问题：** 报 `KeyError: 'wangwu'`，因为 key 不存在。

**修改方案：**

**方案一：用 get() 方法**

```python
print(users.get("wangwu", "不存在"))
```

**方案二：先判断**

```python
if "wangwu" in users:
    print(users["wangwu"])
else:
    print("不存在")
```

**方案三：try-except**

```python
try:
    print(users["wangwu"])
except KeyError:
    print("不存在")
```

---

## DEBUG-04 ★★ 文件未关闭

**问题代码：**

```python
f = open("test.txt", "r")
data = f.read()
print(data)
```

**问题：** 文件打开后没有调用 `f.close()`。虽然程序结束时文件会被操作系统自动关闭，但如果程序中途异常退出，可能导致资源泄漏。在长时间运行的程序中这会造成文件句柄耗尽。

**修改（推荐 with 语句）：**

```python
with open("test.txt", "r", encoding="utf-8") as f:
    data = f.read()
    print(data)
```

**解析：** `with` 语句会在代码块结束时自动关闭文件，即使发生异常也会关闭。这是 Python 操作文件的标准最佳实践。

---

# 四、实操模拟题（完整模拟）

## 模拟题一：SQL — 选修超过3门课的学生

**表结构：** `student`（学生）、`course`（课程）、`sc`（选课表，含 student_id, course_id, score）

**答案：**

```sql
SELECT s.name, COUNT(sc.course_id) AS 课程数量
FROM student s
JOIN sc ON s.student_id = sc.student_id
GROUP BY s.student_id, s.name
HAVING COUNT(sc.course_id) > 3;
```

---

## 模拟题二：SQL — 没有选修任何课程的学生

**答案：**

```sql
SELECT s.*
FROM student s
LEFT JOIN sc ON s.student_id = sc.student_id
WHERE sc.course_id IS NULL;
```

或者用 NOT EXISTS：

```sql
SELECT * FROM student s
WHERE NOT EXISTS (
    SELECT 1 FROM sc WHERE sc.student_id = s.student_id
);
```

---

## 模拟题三：SQL — 每门课程的平均成绩，从高到低

**答案：**

```sql
SELECT c.course_name, AVG(sc.score) AS 平均成绩
FROM course c
JOIN sc ON c.course_id = sc.course_id
GROUP BY c.course_id, c.course_name
ORDER BY AVG(sc.score) DESC;
```

---

## 模拟题四：SQL — employee 表完整操作

**答案：**

```sql
-- 1. 创建表
CREATE TABLE employee (
    id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INT,
    department VARCHAR(50),
    salary DECIMAL(10, 2)
);

-- 2. 插入3条数据
INSERT INTO employee (id, name, age, department, salary) VALUES
(1, '张三', 28, '技术部', 8000),
(2, '李四', 32, '市场部', 9500),
(3, '王五', 25, '技术部', 7000);

-- 3. 修改其中一人的工资
UPDATE employee SET salary = 10000 WHERE name = '李四';

-- 4. 删除一人
DELETE FROM employee WHERE name = '王五';

-- 5. 查询工资最高的人
SELECT * FROM employee 
WHERE salary = (SELECT MAX(salary) FROM employee);
-- 或者
SELECT * FROM employee ORDER BY salary DESC LIMIT 1;
```

---

## 模拟题五：Python — 统计列表数字出现次数

**答案：**

```python
nums = [3, 5, 2, 3, 8, 5, 3, 9]

counts = {}
for num in nums:
    if num in counts:
        counts[num] += 1
    else:
        counts[num] = 1

print(counts)
```

---

## 模拟题六：Python — 找出成绩最高的学生

**答案：**

```python
students = [
    {"name": "张三", "score": 85},
    {"name": "李四", "score": 92},
    {"name": "王五", "score": 78},
    {"name": "赵六", "score": 95}
]

best = students[0]
for s in students:
    if s["score"] > best["score"]:
        best = s

print(f"{best['name']} {best['score']}")
```

---

## 模拟题七：Python — 读取日志打印 ERROR 行

**答案：**

```python
with open("log.txt", "r", encoding="utf-8") as f:
    for line in f:
        if "ERROR" in line:
            print(line.strip())
```

---

# 五、复习重点速查表

## SQL 优先级排序（按你现在的情况）

| 优先级 | 知识点 | 掌握标准 |
|--------|--------|----------|
| 🔴 最高 | DDL（CREATE/ALTER/DROP） | 能独立写建表语句 |
| 🔴 最高 | DML（INSERT/UPDATE/DELETE） | 记得带 WHERE |
| 🟠 高 | JOIN（INNER/LEFT） | 理解左连接和内连接区别 |
| 🟠 高 | GROUP BY + HAVING | 能区分 WHERE 和 HAVING |
| 🟡 中 | 子查询 / NOT EXISTS | 能写"没有XX的XX" |
| 🟢 低 | 基础 SELECT/WHERE | 你已经比较熟了 |

## Python 优先级排序

| 优先级 | 知识点 | 掌握标准 |
|--------|--------|----------|
| 🔴 最高 | 列表 + 字典操作 | 能手写计数器 |
| 🔴 最高 | for / if 基础 | 熟练不卡顿 |
| 🟠 高 | 函数定义 | 会写 return |
| 🟠 高 | 文件操作 | 会用 with open |
| 🟡 中 | 字符串处理 | 回文、统计次数 |
| 🟢 低 | 异常处理 | 知道 try-except |

## 面试必背的 SQL 口诀

1. **DELETE 删行，DROP 删表**
2. **WHERE 筛行，HAVING 筛组**
3. **要找"没有的"，LEFT JOIN + IS NULL**
4. **GROUP BY 黄金法则：SELECT 的列要么分组要么聚合**
5. **COUNT(*) 统计行数，COUNT(DISTINCT) 去重统计**

---