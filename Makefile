.PHONY : tests

all :
	echo "Configure your own targets here."

tests :
	py.test -v --cov python_skeleton --cov-report html
