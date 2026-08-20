# SQL 数据库操作与建表常用数据类型

## 一、数据库命名规范

创建 database 时，习惯使用反引号 `` ` `` 包裹名称，可以避免名字与 SQL 关键字冲突时报错。

---

## 二、数据库基础操作：CREATE / SHOW / DROP

### 1. 创建数据库

```sql
CREATE DATABASE `database_name`;
```

### 2. 查看所有数据库

```sql
SHOW DATABASES;
```

### 3. 删除数据库

```sql
DROP DATABASE `database_name`;
```

---

## 三、SQL 建表常用 6 种数据类型

最常用：`int`、`varchar`、`char`、`text`、`decimal`、`datetime`

### 建表示例

```sql
CREATE TABLE demo_test (
    id INT,                     -- 整数
    username VARCHAR(50),       -- 可变长度字符串
    gender CHAR(2),             -- 定长短字符串
    salary DECIMAL(10,2),       -- 小数 / 金额
    article TEXT,               -- 大文本
    create_time DATETIME        -- 日期时间
);
```

---

### 1. INT —— 整数类型

- **用途**：存储整数，如 ID、年龄、数量
- **范围**：大约 ±21 亿
- **常用场景**：自增主键

```sql
id INT PRIMARY KEY AUTO_INCREMENT
```

---

### 2. VARCHAR(n) —— 可变长度字符串

- **用途**：存储长度不固定的短文本，如用户名、标题、URL
- **说明**：`n` 表示最大字符数；实际数据短则占用更少空间
- **地位**：日常字符串首选类型

```sql
username VARCHAR(50)   -- 最多 50 个字符
```

---

### 3. CHAR(n) —— 定长字符串

- **用途**：存储长度固定的极短字符串，如性别、手机号、状态码
- **说明**：长度不足时自动补空格，查询效率略高于 VARCHAR

```sql
gender CHAR(2)   -- 存"男" / "女"
```

---

### 4. DECIMAL(总位数, 小数位) —— 精确小数

- **用途**：存储金额、价格等需要精确计算的小数
- **重要原则**：**金额必用 DECIMAL，绝对不要用 FLOAT**（浮点误差）
- **示例**：`DECIMAL(10,2)` —— 共 10 位，其中 2 位小数，最大值为 `99999999.99`

```sql
salary DECIMAL(10,2)
```

---

### 5. TEXT —— 长文本类型

- **用途**：存储大段文本内容，如文章、备注、描述
- **特点**：不设置长度限制，不能用于索引
- **选用原则**：短文字用 VARCHAR，大段文本才用 TEXT

```sql
article TEXT
```

---

### 6. DATETIME —— 日期时间类型

- **用途**：存储日期 + 时间，如创建时间、更新时间、做题时间
- **格式**：`2026-08-13 22:10:00`

```sql
create_time DATETIME
```

---

## 四、数据类型速查表

| 类型 | 用途 | 典型示例 |
|------|------|----------|
| INT | 整数数字 | id, age, count |
| VARCHAR | 普通短字符串 | 用户名, URL |
| CHAR | 固定极短字符 | 性别, 状态码 |
| DECIMAL | 金钱 / 精确小数 | 薪资, 价格 |
| TEXT | 大段文本 | 文章, 备注 |
| DATETIME | 日期时间 | 创建时间 |

---

## 五、易错点提醒

1. 存时间不要用 VARCHAR 存字符串，优先用 `DATETIME`
2. 存金额绝对不要用 FLOAT / DOUBLE，会有浮点误差，必须用 `DECIMAL`
3. 短字符串优先 VARCHAR，超长文本才用 TEXT

---

## 六、DESCRIBE / DROP / ALTER —— 查看、删除、修改表结构

### 1. DESCRIBE —— 查看表结构

- **作用**：查看一张表有哪些列、每列的数据类型、是否为主键等信息
- **简写**：`DESC 表名`

```sql
DESCRIBE `student`;
DESC `student`;   -- 简写，效果一样
```

---

### 2. DROP TABLE —— 删除整张表

- **作用**：把整张表连同数据一起删掉，不可恢复
- **注意**：删除的是**表结构 + 全部数据**，不是只删数据

```sql
DROP TABLE `student`;
```

---

### 3. ALTER TABLE —— 修改表结构

- **作用**：在已存在的表上**增加列 / 删除列 / 修改列**，不影响已有数据

#### ① 增加一列

```sql
ALTER TABLE `student` ADD `gpa` DECIMAL(3,2);
```

#### ② 删除一列

```sql
ALTER TABLE `student` DROP COLUMN `gpa`;
```

---

## 七、INSERT INTO —— 插入数据

- **作用**：往表里新增一行数据

### 标准写法：按建表顺序依次插入

```sql
INSERT INTO `student` VALUES(1, '小白', '历史');
INSERT INTO `student` VALUES(2, '小黑', '生物');
INSERT INTO `student` VALUES(3, '小绿', NULL);   -- 某列没数据，写 NULL
```

> 注意：VALUES 后面的值顺序，必须和建表时列的顺序完全一致。

---

### 自定义列顺序写法（推荐，更灵活）

在表名后面用括号写明：**我要给哪些列赋值、按什么顺序赋值**

```sql
INSERT INTO `student`(`name`, `major`, `student_id`) 
VALUES('小蓝', '英语', 4);
```

**好处：**
1. 不用记建表时的列顺序，自己指定顺序
2. 只想给部分列赋值时，可以只写需要的列，其他列自动为 NULL / 默认值

---

## 八、约束（CONSTRAINT）—— 给列加规则

约束就是给字段立规矩，插入/修改数据时必须遵守，否则报错。

### 1. NOT NULL —— 非空约束

- **作用**：该列不允许为空，插入时必须给值

```sql
user_name VARCHAR(32) NOT NULL
```

---

### 2. UNIQUE —— 唯一约束

- **作用**：该列所有行的值不能重复
- **注意**：主键天然就是唯一的；UNIQUE 可以给非主键列加

```sql
salary DECIMAL(10,2) UNIQUE   -- 每个人工资不能一样（仅举例）
```

---

### 3. DEFAULT —— 默认值

- **作用**：插入数据时如果没给该列赋值，自动填入默认值

```sql
major VARCHAR(20) DEFAULT '历史'   -- 不填专业时，默认是"历史"
```

---

### 4. AUTO_INCREMENT —— 自增

- **作用**：主键自动 +1，插入数据时不用手动写 id
- **注意**：只能用于整数类型的主键

```sql
student_id INT AUTO_INCREMENT PRIMARY KEY
```

插入时可以不写 id，数据库自动分配：

```sql
INSERT INTO `student`(`name`, `major`) VALUES('小蓝', '英语');
-- student_id 自动变成下一个数字，不用手动写
```

---

### 完整建表 + 约束示例

```sql
CREATE TABLE `student` (
    `student_id` INT AUTO_INCREMENT,
    `name` VARCHAR(20),
    `major` VARCHAR(20) DEFAULT '历史',
    PRIMARY KEY(`student_id`)
);
```

---

## 九、UPDATE & DELETE —— 修改和删除数据

### 准备测试数据

```sql
CREATE TABLE `student` (
    `student_id` INT,
    `name` VARCHAR(20),
    `major` VARCHAR(20),
    `score` INT,
    PRIMARY KEY(`student_id`)
);

INSERT INTO `student` VALUES(1, '小白', '历史', 50);
INSERT INTO `student` VALUES(2, '小黑', '生物', 60);
INSERT INTO `student` VALUES(3, '小绿', '化学', 70);
INSERT INTO `student` VALUES(4, '小黄', '语文', 90);
INSERT INTO `student` VALUES(5, '小蓝', '数学', 70);
```

---

### 1. UPDATE —— 修改数据

**语法：**
```sql
UPDATE 表名
SET 列1=新值, 列2=新值
WHERE 条件;
```

> ⚠ **必须写 WHERE！** 不写 WHERE 会把整张表所有行都改掉。

#### ① 修改单列

```sql
UPDATE `student`
SET `major` = '英语文学'
WHERE `major` = '数学';
```

#### ② 同时修改多列（逗号隔开）

```sql
UPDATE `student`
SET `name` = '小灰', `major` = '物理'
WHERE `student_id` = 1;
```

#### ③ 多条件修改（OR / AND）

```sql
UPDATE `student`
SET `major` = '文化'
WHERE `major` = '语文' OR `major` = '英语文学';
```

> 等价优化写法：`WHERE major IN ('语文', '英语文学')`

---

### 2. DELETE —— 删除数据

**语法：**
```sql
DELETE FROM 表名
WHERE 条件;
```

> ⚠ **必须写 WHERE！** 不写 WHERE 会清空整张表。

#### ① 按条件删除一行

```sql
DELETE FROM `student`
WHERE `student_id` = 5;
```

#### ② 多条件删除

```sql
DELETE FROM `student`
WHERE `name` = '小灰' AND `major` = '物理';
```

#### ③ 清空整张表（危险操作）

```sql
DELETE FROM `student`;
```

---

## 十、易错点汇总（新手高频踩坑）

| 错误 | 原因 | 正确写法 |
|------|------|----------|
| 中文分号 `；` | 标点用了中文 | 必须用英文半角 `;` |
| 反引号不成对 `` `major` `` | 少了左边或右边反引号 | `` `字段名` `` 成对出现 |
| UPDATE 不写 WHERE | 忘了加条件 | 整张表被改掉，必须加 WHERE |
| DELETE 不写 WHERE | 忘了加条件 | 整张表被清空，必须加 WHERE |
| INSERT 列顺序错乱 | 没写列名，值顺序不对 | 推荐写清楚列名：`INSERT INTO 表(列1,列2) VALUES(...)` |
| 金额用 FLOAT | 浮点误差 | 必须用 DECIMAL |
