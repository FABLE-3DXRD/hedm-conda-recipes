mkdir %SCRIPTS%

for %%G in (filter_images.py ge2tiff.py stack_layers.py) DO (
copy /Y %RECIPE_DIR%\temp.exe %SCRIPTS%\%%G.exe
copy /Y %RECIPE_DIR%\%%G %SCRIPTS%\%%G-script.py)

mkdir %PREFIX%\share\3dxrd
copy %RECIPE_DIR%\*.ini %PREFIX%\share\3dxrd
