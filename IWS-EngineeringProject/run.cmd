REM This script automatically deploys the server to whatever computer it is on.
REM will also install the server on that computer if the argument "install" is given.
set install=%1
IF "%install%"=="install" (
pip install --editable .
)
set FLASK_APP=SM_SYS
set FLASK_DEBUG=true
flask initdb
flask run

