set LDFLAGS="-static-libgfortran -static-libgcc -static -lgomp -shared -fopenmp"
%PYTHON% setup.py install
if errorlevel 1 exit 1
