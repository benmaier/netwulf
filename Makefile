default: 
	make python

clean:
	-rm -f *.o
	make pyclean

clean_all:
	make clean
	make pyclean

pyclean:
	-rm -f *.so
	-rm -rf *.egg-info*
	-rm -rf ./tmp/
	-rm -rf ./build/

python:
	pip install -e ../netwulf --no-binary :all:

checkdocs:
	python setup.py checkdocs

pypi:
	rm dist/*
	python setup.py sdist
	twine upload dist/*
