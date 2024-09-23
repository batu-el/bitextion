#!/bin/bash

VENV_NAME="_venv"
if ! command -v virtualenv &> /dev/null
then
    echo "virtualenv could not be found. Installing it..."
    pip install virtualenv
fi

# virtual environment
echo "Creating new virtual environment: $VENV_NAME"
virtualenv $VENV_NAME

# activate environment
source $VENV_NAME/bin/activate

# requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing packages from requirements.txt"
    pip install -r requirements.txt
else
    echo "requirements.txt not found in the current directory."
    echo "Please ensure requirements.txt is in the same directory as this script."
    deactivate
    exit 1
fi

echo "Setup complete. Your new virtual environment is ready."
echo "To activate it, run: source $VENV_NAME/bin/activate"