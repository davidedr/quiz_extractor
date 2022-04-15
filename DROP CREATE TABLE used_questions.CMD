@ECHO off
set PGPASSWORD=postgres
@ECHO on
"c:\Program Files\PostgreSQL\11\BIN\psql.exe" -p 5433 -U postgres < "DROP CREATE TABLE used_questions.SQL"
@ECHO off
set PGPASSWORD=