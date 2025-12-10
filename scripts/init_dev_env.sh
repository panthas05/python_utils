#!/bin/bash
cd $( dirname $0 )
cd ../

# generic functions

function yes_or_no {
    while true; do
        read -p "$* [y/n]: " yn
        case $yn in
            [Yy]*) return 0;;  
            [Nn]*) return 1;;
        esac
    done
}

# installing virtual environment

SHOULD_CREATE_ENV=true

if [ -d env ]; then
    SHOULD_DELETE_ENV=1
    yes_or_no "Recreate virtual environment?" && SHOULD_DELETE_ENV=0
    if [[ $SHOULD_DELETE_ENV == 0 ]]; then 
        echo "Deleting old virtual environment"
        rm -r env
        echo "Old virtual environment deleted"
        echo ""
    else
        SHOULD_CREATE_ENV=false
    fi
fi

if $SHOULD_CREATE_ENV; then
    echo "Creating virtual environment..."
    python3 -m venv env
    source env/bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install \
        -r requirements/requirements.txt \
        -r requirements/requirements.dev.txt \
        -r requirements/requirements.types.txt
    echo "Virtual environment created"
    echo ""
fi

# setting up pre-commit hook

echo "Setting up pre-commit hook"

PRE_COMMIT_HOOK_PATH=".git/hooks/pre-commit"

cat <<EOF > $PRE_COMMIT_HOOK_PATH
#!/bin/bash
cd \$(dirname "\$0")
cd ../../

files_to_blacken=\$(git diff --name-only --cached --diff-filter=d | grep "\.py$")
if [[ "\$files_to_blacken" != "" ]]; then
	echo "Running black..."
	echo ""
	env/bin/python3 -m black \$files_to_blacken
	git add \$files_to_blacken
	echo ""
fi

echo "Running mypy..."
mypy_output=\$(python3 -m mypy ./src)

if [[ "\$mypy_output" != Success* ]]; then
	echo "mypy detected errors:"
	echo ""
	echo "\$mypy_output"
	echo ""
	exit 1
else
	echo "mypy checks passed"
	echo ""
fi
EOF
chmod 700 $PRE_COMMIT_HOOK_PATH


echo "Pre-commit hook created"
