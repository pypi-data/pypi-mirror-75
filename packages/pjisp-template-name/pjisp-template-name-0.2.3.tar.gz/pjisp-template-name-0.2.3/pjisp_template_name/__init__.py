#!/usr/bin/env python2

import os
import logging
from distutils.dir_util import copy_tree
from sys import stderr

import click

ERROR_MESSAGE = 'Repository name not valid. Error on {}'
LENGTH_MESSAGE = 'Repository name length not valid'
PROGRAMS = ('E214', 'E111')
TEMPLATES = ('T12', 'T34', 'SOV')

def check_text(text, value):
    if text != value:
        logging.error(ERROR_MESSAGE.format(value))
        exit(1)

def check_year(year):
    try:
        int(year)
    except ValueError:
        logging.error(ERROR_MESSAGE.format(year))
        exit(1)

def check_program(program):
    if program not in PROGRAMS:
        logging.error(ERROR_MESSAGE.format(program))
        exit(1)

def check_template(template):
    if template not in TEMPLATES:
        logging.error(ERROR_MESSAGE.format(template))
        exit(1)

def check_group(group):
    if not group.startswith('G'):
        logging.error(ERROR_MESSAGE.format(group))
        exit(1)
    try:
        int(group[1:])
    except ValueError:
        logging.error(ERROR_MESSAGE.format(group))
        exit(1)

def check_repo_name(repo_name):
    splits = repo_name.split("-")
    if len(splits) not in (5, 7):
        logging.error(LENGTH_MESSAGE)
        exit(1)

    pjisp, year, program, template, group = splits[0:5]
    check_text("pjisp", pjisp)
    check_year(year)
    check_program(program)
    check_template(template)
    check_group(group)

    try:
        sample, test = splits[5:7]
        check_text("sample", sample)
        check_text("test", test)
    except ValueError:
        pass

    return template

@click.command()
@click.argument('repo_name')
def get_name(repo_name):
    template = check_repo_name(repo_name)
    print(template)

if __name__ == '__main__':
    get_name()
