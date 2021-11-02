use project;
show tables ;
show columns from student_information;
show columns from admin_panel;
show columns from gpa;
show columns from date_information;
select *from student_information;
DELETE FROM STUDENT_INFORMATION
WHERE ID = '9';

ALTER TABLE date_information drop column id;
ALTER TABLE date_information DROP CHECK DATE_INFORMATION_CK2;

