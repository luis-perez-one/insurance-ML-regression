#!/bin/bash

# delete existent files
rm Python.gitignore Julia.gitignore .gitignore

# create new empty .ignore
touch .gitignore

# python
wget https://raw.githubusercontent.com/github/gitignore/master/Python.gitignore

# julia
wget https://raw.githubusercontent.com/github/gitignore/master/Julia.gitignore

# merge
cat Python.gitignore Julia.gitignore OSsFiles.gitignore Custom.gitignore > .gitignore

exit
