create database `sql_advanced`;
use `sql_advanced`;
show databases;

-- 1.建表
create table `employee`(
	`emp_id` int primary key,
    `name` varchar(20),
    `birth_date` date,
    `sex` varchar(1),
    `salary` int,
    `branch_id` int,
    `sup_id` int
);

create table `branch`(
	`branch_id` int primary key,
    `branch_name` varchar(20),
    `manager_id` int,
    foreign key (`manager_id`) references `employee`(`emp_id`) on delete set null
);

-- 2.添加外键
alter table `employee`
add foreign key(`branch_id`)
references `branch`(`branch_id`)
on delete set null;

alter table `employee`
add foreign key(`sup_id`)
references `employee`(`emp_id`)
on delete set null;

create table `client`(
	`client_id` int primary key,
    `client_name` varchar(20),
    `phone` varchar(20)
);

create table `work_with`(
	`emp_id` int,
    `client_id` int,
    `total_sales` int,
    primary key(`emp_id`,`client_id`),
    foreign key (`emp_id`) references `employee`(`emp_id`) on delete cascade,
    foreign key (`client_id`) references `client`(`client_id`) on delete cascade
);

-- 3.新增资料
-- （1）先给branch表增加资料
insert into `branch` values(1,'行政',null);
insert into `branch` values(2,'行政',null);
insert into `branch` values(3,'资讯',null);
-- （2）再给employee表增加
insert into `employee` values(206,'小黄','1998-10-08','F',50000,1,null);
insert into `employee` values(207,'小绿','1985-09-16','M',29000,2,206);
insert into `employee` values(208,'小黑','2000-12-19','M',35000,3,206);
insert into `employee` values(209,'小白','1997-01-22','F',39000,3,207);
insert into `employee` values(210,'小红','1925-11-10','F',84000,1,207);

update `branch`
set `manager_id` = 206
where `branch_id` = 1;

update `branch`
set `manager_id` = 207
where `branch_id` = 2;

update `branch`
set `manager_id` = 208
where `branch_id` = 3;


insert into `client` values(400,'阿狗','254354335');
insert into `client` values(401,'小猫','25633899');
insert into `client` values(402,'旺财','45354354');
insert into `client` values(403,'露西','54354365');
insert into `client` values(404,'艾瑞克','18783783');

insert into `work_with` values(206,400,'70000');
insert into `work_with` values(207,401,'24000');
insert into `work_with` values(208,402,'9800');
insert into `work_with` values(208,403,'24000');
insert into `work_with` values(210,404,'879400');

-- 练习1
-- （1）取得所有员工资料
select * from employee;

-- （2）取得所有客户资料
select * from client;

-- （4）按照薪水从低到高取得员工资料
select * from employee order by salary;

-- （5）取得薪水前3高的员工
select * from employee order by salary desc limit 3;

-- （6）取得所有员工的的名字
select name from employee;

-- 练习2 聚合函数
-- 1.取得员工人数
select count(*) from employee;

-- 2.取得所有出生于1970-01-01之后的女性员工人数
select count(*) from employee where birth_date > '1970-01-01' and sex = 'F';

-- 3.取得员工的平均薪水
select avg(salary) as avg_salary from employee;

-- 4.取得所有员工薪水总和
select sum(salary) from employee;

-- 5.取得薪水最高的员工
select max(salary) as max_salary from employee;

-- 6.取得薪水最低的员工
select min(salary) as min_salary from employee;


-- 练习3 通配符 %代表多个字符，_代表一个字符
-- 1.取得电话号码尾数为335的客户/开头是254的
select * 
from client
where `phone` like '%354%';-- 开头的写法则为'254%'， '%354%'表示中间有354就行

-- 2.取得姓艾的用户
select * 
from client
where `client_name` like '艾%';

-- 3.取得生日在12月的员工
select * 
from employee
where `birth_date` like '_____12%';-- _代表一个字符,这里有5个

-- 练习4 联集 union

-- 1.员工名字 union 客户名字
select name
from employee
union
select client_name
from client;

-- 2.员工id + 员工名字 union 客户id + 客户名字
select emp_id as total_id,name as total_name
from employee
union
select client_id,client_name
from client;

-- 3.员工薪水 union 销售金额
select salary
from employee
union
select total_sales
from work_with;

-- 练习5 join 连接
insert into branch values(4,'偷懒',null);
-- 取得所有部门经理的名字
select
emp.emp_id
,emp.name
,bra.branch_name
from employee emp
join branch bra
on emp.emp_id = bra.manager_id;

insert into branch values(4,'偷懒',null);
-- 取得所有部门经理的名字
select
emp.emp_id
,emp.name
,bra.branch_name
from employee emp
left join branch bra
on emp.emp_id = bra.manager_id;
-- left 表示，左边的表格无论如何都会回传资料，而右边的条件满足才会回传资料（若是右边没能匹配左边的，用null）
-- right 表示，右边的表格无论如何都会回传资料，而左边的条件满足才会回传资料

-- 练习6 子查询
-- 1.找出资讯部门的经理名字
select
name
from employee
where emp_id=( -- 注意使用的=，要确保子查询结果只有一条
	select manager_id
	from branch
	where branch_name='资讯'
);


-- 2.找出对单一位客户销售金额超过50000的员工名字
select
name
from employee
where emp_id in ( -- 注意使用的in，允许子查询返回多个结果
	select
	emp_id
	from work_with
	where total_sales>50000
);

select
distinct name
from employee e
join work_with w
on e.emp_id = w.emp_id
where w.total_sales > 50000;

-- 解释前面建表的时候，使用on delete set null 的原因
-- 使用on delete cascade 的原因
-- 注意：primary key 是不能为null的，所以有时候set null要慎重使用

