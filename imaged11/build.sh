$PYTHON -c "import time; print time.strftime('1.6.0.%Y.%m.%d')" > $SRC_DIR/__conda_version__.txt

# work around https://github.com/numpy/numpy/issues/7427:
if [ `uname` == Darwin ]; then
    LDFLAGS="$LDFLAGS -undefined dynamic_lookup -bundle"
fi

$PYTHON setup.py install
