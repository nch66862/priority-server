#!/bin/bash
# run ./renderdocs.sh

apidoc  -v --debug -i ./priorityapi/views -f .py -o docs/

cd docs

serve

# go to localhost:3000 to view the docs