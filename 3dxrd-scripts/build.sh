$PYTHON -c "import time; print time.strftime('0.1.0.dev.%Y.%m.%d')" > $SRC_DIR/__conda_version__.txt

$PYTHON setup.py install
