-- Dropping tables (if exist) to avoid conflicts
drop table if exists ratings;
drop table if exists users;
drop table if exists movies;

create table movies (
    movie_id serial primary key,
    title varchar(255) not null,
    genre varchar(255) not null
);

create table users (
    user_id serial primary key,
    age int,
    gender varchar(10),
    occupation varchar(50),
    zip_code varchar(10)
);

create table ratings(
    rating_id serial primary key,
    user_id int references users(user_id) on delete cascade,
    movie_id int references movies(movie_id) on delete cascade,
    rating int check (rating between 1 and 5),
    timestamp timestamp
)