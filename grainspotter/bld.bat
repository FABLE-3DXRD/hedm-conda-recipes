%PYTHON% -c "import time; print time.strftime('0.90.0.%%Y.%%m.%%d')" > %SRC_DIR%\__conda_version__.txt

make

if not exist "%SCRIPTS%" mkdir %SCRIPTS%
xcopy grainspotter.exe %SCRIPTS%\
