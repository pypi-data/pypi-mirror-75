#!/usr/bin/env python2

import click
import filecmp


message_change = 'Please change the {} file.'
message_not_change = 'Please do not change the {} file.'
shoud_edit = ['assignment_solution.c', 'assignment.rst']
shoud_not_edit = ['assignment_notes.rst']
fixtures_T12 = ['fixtures/stdio-numbers.yaml']
fixtures_T34 = ['fixtures/file-error-input-not-readable.yaml', 'fixtures/file-error-output-not-writable.yaml', 'fixtures/file-text.yaml']
fixtures_SOV = ['fixtures/file-error-input-not-readable.yaml', 'fixtures/file-error-output-not-writable.yaml', 'fixtures/file-text.yaml']


def get_fixtures(template):
    if template == 'T12':
        return fixtures_T12
    elif template == 'T34':
        return fixtures_T34
    elif template == 'SOV':
        return fixtures_SOV
    else:
        print('Unknown template')
        exit(1)


def is_edited(template):
    edited = True
    edit_files = shoud_edit + get_fixtures(template)
    for filepath in edit_files:
        if filecmp.cmp(filepath, '.templates/{}/{}'.format(template, filepath)):
            print(message_change.format(filepath))
            edited = False

    return edited


def is_not_edited(template):
    not_edited = True
    for filepath in shoud_not_edit:
        if not filecmp.cmp(filepath, '.templates/{}/{}'.format(template, filepath)):
            print(message_not_change.format(filepath))
            not_edited = False

    return not_edited


@click.command()
@click.argument('template')
def diff(template):
    exit_code = 0
    if not is_edited(template):
        exit_code = 1

    if not is_not_edited(template):
        exit_code = 1

    exit(exit_code)


if __name__ == '__main__':
    diff()
