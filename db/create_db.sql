CREATE TABLE category
(
    id int(10) primary key,
    pid int(10),
    name varchar(200),
    parent_path varchar(200),
    level int(10),
    exps_order int(10),
    parents json,
    child_list json,
    leaf bool,
    deleted bool,
    svc_use bool,
    sblog_use bool,
    full_path varchar(200)
);

CREATE TABLE keyword_rank
(
    id int(10) PRIMARY KEY AUTO_INCREMENT,
    `rank` int(10),
    keyword varchar(200),
    link_id varchar(200),
    etl_date date
);

CREATE TABLE age_rate_info
(
    id int(10) PRIMARY KEY AUTO_INCREMENT,
    cid int(10),
    code varchar(200),
    title varchar(200),
    full_title varchar(200),
    date_range varchar(200),
    etl_date date,
    CONSTRAINT age_rate_cid_fk FOREIGN KEY (cid) REFERENCES category (id)
);

CREATE TABLE age_rate
(
    id int(10) PRIMARY KEY AUTO_INCREMENT,
    info_id int(10),
    code varchar(200),
    label varchar(200),
    ratio float,
    CONSTRAINT age_rate_info_fk FOREIGN KEY (info_id) REFERENCES age_rate_info (id)
);

CREATE TABLE click_trend_info
(
    id int(10) PRIMARY KEY AUTO_INCREMENT,
    cid int(10),
    code varchar(200),
    title varchar(200),
    full_title varchar(200),
    date_range varchar(200),
    etl_date date,
    CONSTRAINT click_trend_cid_fk FOREIGN KEY (cid) REFERENCES category (id)
);

CREATE TABLE click_trend
(
    id int(10) PRIMARY KEY AUTO_INCREMENT,
    info_id int(10),
    period varchar(200),
    value float,
    CONSTRAINT click_trend_info_fk FOREIGN KEY (info_id) REFERENCES click_trend_info (id)
);


CREATE TABLE device_rate_info
(
    id int(10) PRIMARY KEY AUTO_INCREMENT,
    cid int(10),
    code varchar(200),
    title varchar(200),
    full_title varchar(200),
    date_range varchar(200),
    etl_date date,
    CONSTRAINT device_rate_cid_fk FOREIGN KEY (cid) REFERENCES category (id)
);

CREATE TABLE device_rate
(
    id int(10) PRIMARY KEY AUTO_INCREMENT,
    info_id int(10),
    code varchar(200),
    label varchar(200),
    ratio float,
    CONSTRAINT device_rate_fk FOREIGN KEY (info_id) REFERENCES device_rate_info (id)
);



CREATE TABLE gender_rate_info
(
    id int(10) PRIMARY KEY AUTO_INCREMENT,
    cid int(10),
    code varchar(200),
    title varchar(200),
    full_title varchar(200),
    date_range varchar(200),
    etl_date date,
    CONSTRAINT gender_rate_cid_fk FOREIGN KEY (cid) REFERENCES category (id)
);

CREATE TABLE gender_rate
(
    id int(10) PRIMARY KEY AUTO_INCREMENT,
    info_id int(10),
    code varchar(200),
    label varchar(200),
    ratio float,
    CONSTRAINT gender_rate_fk FOREIGN KEY (info_id) REFERENCES gender_rate_info (id)
);
