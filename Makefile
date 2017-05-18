.PHONY : tests clean install

NOTEBOOKS = $(wildcard examples/*.ipynb)
NOTEBOOK_OUTPUTS = $(NOTEBOOKS:.ipynb=.html)

examples : $(NOTEBOOK_OUTPUTS)

$(NOTEBOOK_OUTPUTS) : %.html : %.ipynb
	jupyter nbconvert --execute --ExecutePreprocessor.timeout=None --allow-errors $<

clean :
	rm examples/*.html

tests :
	py.test -v html -rsx

install:
	conda env create
	. activate python_skeleton && pip install -e .
