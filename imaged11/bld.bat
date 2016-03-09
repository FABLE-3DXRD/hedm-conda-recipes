set LDFLAGS="-static-libgfortran -static-libgcc -static -shared"
%PYTHON% setup.py install
