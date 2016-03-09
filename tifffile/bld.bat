xcopy %RECIPE_DIR%/src src /e /q /y
cd src

%PYTHON% setup.py install
