
/*show databases; /* show all the databases*/
/*use school; /* Use the school database*/
/*show tables; /* show all the tables in school database*/
/*select * from subject; /* select all the rows from subject table*/ 

use employees;
show tables;
desc employees;
Select emp_no,first_name,last_name from employees limit 10;
select emp_no,first_name, upper(last_name) from employees limit 10;
select length(first_name),first_name,length(last_name),last_name from employees
order by length(last_name),last_name,length(first_name),first_name;
select * from employees;
select *,substring(last_name,1,1) Initials from employees limit 10;
select * from employees where substring(year(birth_date),1,3) = "195" and hire_date between "1988-09-01" and "1991-02-28"
order by hire_date;

select round(avg(salary),2) from salaries;
select avg(b.salary),a.emp_no,a.first_name from employees as a, salaries as b
where a.emp_no =b.emp_no
group by a.emp_no;

select format(max(b.salary),2),a.emp_no from employees as a, salaries as b
where a.emp_no =b.emp_no
group by a.emp_no;

select format(avg(b.salary),2),a.emp_no from employees as a, salaries as b
where a.emp_no = b.emp_no
and a.emp_no in (10001, 10021, 10033,10087)
group by a.emp_no;

select format(avg(b.salary),2),a.emp_no from employees as a, salaries as b
where a.emp_no = b.emp_no
and a.emp_no in (10001, 10021, 10033,10087)
and b.salary > 80000
group by a.emp_no;


select format(avg(b.salary),2),a.emp_no from employees as a, salaries as b
where a.emp_no = b.emp_no
and a.emp_no in (10001, 10021, 10033,10087)
group by a.emp_no;

select round(avg(b.salary)),a.emp_no from employees as a, salaries as b
where a.emp_no = b.emp_no
and b.salary > 90000
group by a.emp_no;

desc employees;
desc salaries;
select emp_no, if gender ="M" then "Mr" , first_name, last_name, gender from employees;








