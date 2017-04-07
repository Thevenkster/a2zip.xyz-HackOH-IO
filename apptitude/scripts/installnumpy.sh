
echo "====>"
echo "====> Manually installing numpy and/or scipy"
echo "====>"
# /opt/python/run/venv/bin/pip install -q --upgrade pip
#/opt/python/run/venv/bin/pip install -q --log /tmp/numpy.log --use-mirrors numpy
/opt/python/run/venv/bin/pip install -q --log /tmp/scipy.log scipy
/opt/python/run/venv/bin/pip install -q --log /tmp/sklearn.log scikit-learn
/opt/python/run/venv/bin/pip freeze
