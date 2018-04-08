route:
	source ./p-env/bin/activate; \
	pip3 install -r requirements.txt; \
	PYTHONPATH=../crossbar_test python3 routes/auth.py

crossbar:
	source ./p-env/bin/activate; \
	pip3 install -r requirements.txt; \
	PYTHONPATH=../crossbar_test crossbar start --loglevel=debug