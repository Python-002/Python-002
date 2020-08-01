CREATE TABLE IF NOT EXISTS movies (
    id          int auto_increment,
    movie_name  text,
    movie_type  text,
    movie_date  datetime,
    primary key (id)
) CHARACTER SET = utf8;
