set PGPASSWORD=postgres
"c:\Program Files\PostgreSQL\11\BIN\dropdb.exe" -p 5433 -U postgres quiz
"c:\Program Files\PostgreSQL\11\BIN\createdb.exe" -p 5433 -U postgres quiz
"c:\Program Files\PostgreSQL\11\BIN\psql.exe" -p 5433 -U postgres < "DROP CREATE TABLES.sql"
set PGPASSWORD=