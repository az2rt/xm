# Prepare before run
make sure you have docker

`docker --version`

output could be:

`Docker version 24.0.6, build ed223bc`

### For running tests locally

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest
```

### For running in docker

```
chmod a+x run.sh
./run.sh
```

### For running performance_check

```
python tests/performance_check.py -c 100 -b 5
```

-c - count of order

-b - size of bunch

## Description of project
`app/` - directory with FastApi application

`tests/` - directory with tests
