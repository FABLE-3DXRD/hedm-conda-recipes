%PYTHON% setup.py install

for %%G in (filter_images.py ge2tiff.py stack_layers.py) DO (
copy /Y %RECIPE_DIR%\temp.exe %SCRIPTS%\%%G.exe
move /Y %SCRIPTS%\%%G %SCRIPTS%\%%G-script.py)

if errorlevel 1 exit 1
