#!/bin/bash
#cd docs
WORKDIR = "../src/testWork/"
rm -r build/html
uv run sphinx-apidoc -f -o ./source ${WORKDIR}
render="html"
if [ "$render" == "latex" ]; then
  make latex
  cd build/latex
  pdflatex first_program.tex
  evince first_program.pdf
elif [ "$render" == "html" ]; then
  make html
  cp -r build/html ../docs/
  qutebrowser ../docs/html/index.html
fi
