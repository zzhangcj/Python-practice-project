SET SQL_SAFE_UPDATES = 0;

create database `sql_tutorial`;
show databases;
use `sql_tutorial`;

create table student(
	`student_id` int,
    `name` varchar(20),
    `major` varchar(20),
    primary key(`student_id`)
);

describe `student`;
drop table `student`;

alter table `student` add gpa decimal(3,2);
alter table `student` drop column gpa;

insert into `student` values(1,'小白','历史');
insert into `student` values(2,'小黑','生物');
insert into `student` values(3,'小绿','化学');
insert into `student` values(4,'小黄','语文');
insert into `student` values(5,'小蓝','数学');
insert into `student`(`name`,`major`,`student_id`) values('小蓝','英语','4');

select * from `student`;

-- 删除，修改资料
create table `student`(
	`student_id` int,
    `name` varchar(20),
    `major` varchar(20),
    `score` int,
    primary key(`student_id`)
);
insert into `student` values(1,'小白','历史',50);
insert into `student` values(2,'小黑','生物',60);
insert into `student` values(3,'小绿','化学',70);
insert into `student` values(4,'小黄','语文',90);
insert into `student` values(5,'小蓝','数学',70);

update `student`
set `major`='英语文学'
where `major`='数学';

update `student`
set `name`='小灰',`major`='物理'
where `student_id`=1;

update `student`
set `major`='文化'
where `major`='语文' or `major`='英语文学';

delete from `student`
where `student_id`=5;

delete from `student`
where `name`='小灰' and `major`='物理';

delete from `student`;






