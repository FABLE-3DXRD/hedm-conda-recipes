$PYTHON -c "import time; print time.strftime('1.1.0.%Y.%m.%d')" > $SRC_DIR/__conda_version__.txt

$PYTHON setup.py install
