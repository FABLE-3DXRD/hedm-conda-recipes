%PYTHON% -c "import time; print time.strftime('0.7.2.%%Y.%%m.%%d')" > %SRC_DIR%\__conda_version__.txt

%PYTHON% setup.py install

for %%G in (collapse.py fabian.py median.py) DO (
copy /Y %RECIPE_DIR%\temp.exe %SCRIPTS%\%%G.exe
move /Y %SCRIPTS%\%%G %SCRIPTS%\%%G-script.py)

if errorlevel 1 exit 1
