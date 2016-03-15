$PYTHON -c "import time; print time.strftime('0.0.2.%Y.%m.%d')" > $SRC_DIR/__conda_version__.txt

$PYTHON setup.py install
