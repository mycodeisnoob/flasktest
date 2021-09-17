CREATE PROCEDURE `sp_create_user`(
IN p_email varchar(80),
IN p_username varchar(45),
IN p_password varchar(45)
)
BEGIN
IF ( select exists (select 1 from user where user_name = p_username) ) THEN  
  select 'Username Exists !';
ELSE
insert into user (
 email,
    user_name,
    password
) values (
 p_email,
    p_username,
    p_password
);
END IF;
END