#! /bin/bash
echo "Running the script"

# check if a virtual environment exists and return if it exists or create a new one
if [ -d "env" ]; then
    echo "Virtual environment exists"
    source env/bin/activate
else
    echo "Creating a new virtual environment"
    python3 -m venv env
    pip install -r requirements.txt
    source env/bin/activate
fi

# run unit tests
python3 -m unittest discover -s test
python3 script.py
