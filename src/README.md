Utils files/directories are sometimes frowned upon or considered code smell
since they can end up being a mountain of code, whose constituents bear little
coherence/structure. To mitigate this, all files/subdirectories in the directory
must have descriptive names that indicate the purpose of the
classes/functions/values which they contain. For example there was previously a
file in here called `helpers.py` - rather undescriptive, and its contents
spanned a number of areas. That has since been split into the `functions.py` and
`parsers.py` file, and the contents of `django` directory. Please follow suit
when adding files/code to this directory.

Furthermore, for the sake of rigour and documentation, please add tests for
anything you add to this directory. Tests can be found in the `tests` directory
(testing utilities should be put in the file `testing.py`).

Note, when turning this into a package/adding a testing suite, you might need to
write a shell script to run the tests which calls `django.setup()` at some
point, see:
https://docs.djangoproject.com/en/4.2/topics/settings/#calling-django-setup-is-required-for-standalone-django-usage
Also docstring this entire dir thoroughly!
