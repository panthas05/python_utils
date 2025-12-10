# Python Utils

This repository contains reusable code that I have written over the course of a
number of projects. It's partially a time saving measure for me so I don't have
to trawl Stack Overflow again to solve a problem I've encountered previously. It
assumes Python 3.12, and isn't guaranteed to work on other (certainly on lower)
python versions.

## Todos
Just to acknowledge that these vary in size and complexity
- Finish this readme more properly
- Set up automated testing, probably using github actions (and black
  formatting/mypy typechecking? badges would be fun too!)
- Convert into a python package at some point for ease of use in other projects
- Consider splitting out into this repo and a `django_utils` repo

## Tests

Tests can be run with `python3 -m unittest discover .`
