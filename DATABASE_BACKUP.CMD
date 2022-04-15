@ECHO off

set CUR_YYYY=%date:~6,4%
set CUR_MM=%date:~3,2%
set CUR_DD=%date:~0,2%
set CUR_HH=%time:~0,2%
if %CUR_HH% lss 10 (set CUR_HH=0%time:~1,1%)

set CUR_NN=%time:~3,2%
set CUR_SS=%time:~6,2%
set CUR_MS=%time:~9,2%

set TIMESTAMP=%CUR_YYYY%%CUR_MM%%CUR_DD%-%CUR_HH%%CUR_NN%%CUR_SS%

set BACKUP_FILE=.\backup\%TIMESTAMP%_backup_quiz_schema_data.sql
@ECHO on
ECHO Database backup filename: %BACKUP_FILE%
@ECHO off

set PGPASSWORD=postgres
@ECHO on
"c:\Program Files\PostgreSQL\11\bin\pg_dump.exe" -U postgres --serializable-deferrable -C -f %BACKUP_FILE% -h localhost -p 5433 --column-inserts --inserts --disable-triggers quiz
@ECHO off
set PGPASSWORD=