sudo apt update
sudo apt install postgresql postgresql-contrib
sudo -u postgres psql

# inside psql:
CREATE DATABASE blog_db;
CREATE USER blog_user WITH PASSWORD 'strong_prod_password';
ALTER ROLE blog_user SET client_encoding TO 'utf8';
ALTER ROLE blog_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE blog_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE blog_db TO blog_user;
\q
