if [[ "$OSTYPE" == "darwin"* ]]; then
    python3 -m venv .venv
    . .venv/bin/activate
    pip3 install -r requirements.txt
    touch .gitignore
    echo ".venv" >> .gitignore

elif [[ "$OSTYPE" == "msys" ]]; then
    python -m venv .venv
    . .venv/bin/activate
    pip install -r requirements.txt
    touch .gitignore
    echo ".venv" >> .gitignore

else 
    echo "Incompatible OS"
fi
