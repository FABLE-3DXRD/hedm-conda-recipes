%PYTHON% setup.py install

for %%G in (findpeaks.py flt_remove_beam.py flt_split_phases.py gff_to_ubi.py^
 grainspotter_loop.py make_gve.py makemap_all.py plot_gff.py tweakdetpars.py^
 ubi_to_gff.py) DO (
copy /Y %RECIPE_DIR%\temp.exe %SCRIPTS%\%%G.exe
move /Y %SCRIPTS%\%%G %SCRIPTS%\%%G-script.py)

if errorlevel 1 exit 1
