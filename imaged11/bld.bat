%PYTHON% -c "import time; print time.strftime('1.6.0.%%Y.%%m.%%d')" > %SRC_DIR%\__conda_version__.txt

set LDFLAGS="-static-libgfortran -static-libgcc -static -lgomp -shared -fopenmp"
%PYTHON% setup.py install

for %%G in (ImageD11Server.py ImageD11_2_shelx.py ImageD11_gui.py avg_par.py^
 bgmaker.py cutgrains.py edf2bruker.py edfheader.py filtergrain.py filterout.py^
 fit2dcake.py fitgrain.py fix_spline.py huber2bruker.py id11_summarize.py^
 index_unknown.py makemap.py mar2bruker.py merge_flt.py pars_2_sweeper.py^
 peaksearch.py plotImageD11map.py plotedf.py plotgrainhist.py plotlayer.py^
 powderimagetopeaks.py recoveromega.py refine_em.py rubber.py spatialfix.py^
 tomapper.py ubi2cellpars.py) DO (
copy /Y %RECIPE_DIR%\temp.exe %SCRIPTS%\%%G.exe
move /Y %SCRIPTS%\%%G %SCRIPTS%\%%G-script.py)

if errorlevel 1 exit 1
