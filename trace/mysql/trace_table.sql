CREATE DATABASE IF NOT  EXISTS trace;

USE trace;

CREATE TABLE trace_process (
    process_id int NOT  NULL,
    process_name varchar(255),
    user_name varchar(100),
    exe_path varchar(255),
    status varchar(100),
    cpu_times double(10,2),
    count_updates int DEFAULT  1,
    create_time datetime,
    log_time datetime,
    CONS RAIN  PK_Process PRIMARY KEY(process_id, process_name)
);

CREATE TABLE system_process (
    id int NOT  NULL AUTO_INCREMENT ,
    process_name varchar(255),
    operating_system varchar(3),
    PRIMARY KEY (id)
);

SELECT  process_name FROM system_process WHERE operating_system = 'LNX';
INSERT  INTO system_process (process_name,operating_system) VALUES ('','LNX');

CREATE TABLE perfil (
    id int NOT  NULL AUTO_INCREMENT ,
    user varchar(100),
    nome varchar(255),
    time_start time,
    time_stop time,
    date_update datetime,
    PRIMARY KEY (id)
);

insert into perfil(user,nome,time_start,time_stop,date_update) values ('marcos','Marcos Cordeiro', '08:00:00','19:00:00', NOW());


CREATE TABLE perfil_process(
    id int NOT  NULL AUTO_INCREMENT ,
    user_id int,
    process_name varchar(255),
    PRIMARY KEY (id),
    FOREIGN KEY (user_id)
        REFERENCES perfil(id)
        ON DELETE CASCADE
);

insert into perfil_process(user_id,process_name) values (1,'chrome');
insert into perfil_process(user_id,process_name) values (1,'code');
insert into perfil_process(user_id,process_name) values (1,'zsh');
insert into perfil_process(user_id,process_name) values (1,'python3');
insert into perfil_process(user_id,process_name) values (1,'teams-for-linux');
insert into perfil_process(user_id,process_name) values (1,'docker');


CREATE  TEMPORARY  TABLE sum_times
select process_name, max(cpu_times) as cpu_time from trace_process_detail where process_name in(select process_name from perfil_process where user_id = 1) and cast(create_time as time) between cast('09:00:00' as time) and cast('19:00:00' as time) and status = 'running' group by process_name,process_id;



select  sum(cpu_times) as cpu_time from trace_process_detail where process_name in(select process_name from perfil_process where user_id = 1) and cast(create_time as time) between cast('09:00:00' as time) and cast('19:00:00' as time) and status = 'running';


CREATE TABLE sites(
    id int NOT  NULL AUTO_INCREMENT ,
    domain varchar(255),
    date_update datetime,
    PRIMARY KEY (id)
);

CREATE TABLE perfil_sites(
    id int NOT  NULL AUTO_INCREMENT,
    user_id int,
    domain varchar(255),
    date_update datetime,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id)
        REFERENCES perfil(id)
        ON DELETE CASCADE
);


select count(domain) as qtd_domain, sum(domain) as total_acesso from sites;

select count(domain) as qtd_domain, sum(domain) as total_acesso from sites where domain in (select domain from perfil_sites where user_id = 1);
