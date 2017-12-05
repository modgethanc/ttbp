"""
This module contains gopher-related stuff.
"""
import getpass
import os

from . import util

GOPHER_PROMPT = """
Would you like to publish your feels to gopher?

gopher is a pre-web technology that is text-oriented and primarily used to
share folders of your files with the world.

If you don't know what it is or don't want it that is totally ok!

You can always change this later.""".lstrip()

GOPHERMAP_HEADER = """
 welcome to {user}'s feels on gopher.

     .::                     .::
   .:                        .::
 .:.: .:   .::       .::     .:: .::::
   .::   .:   .::  .:   .::  .::.::
   .::  .::::: .::.::::: .:: .::  .:::
   .::  .:        .:         .::    .::
   .::    .::::     .::::   .:::.:: .::

 this file was created on their behalf by ttbp.

"""


def select_gopher():
    return util.input_yn(GOPHER_PROMPT)


def publish_gopher(gopher_path, entry_filenames):
    """This function (re)generates a user's list of feels posts in their gopher
    directory and their gophermap."""
    entry_filenames = entry_filenames[:]  # force a copy since this might be shared state in core.py
    entry_filenames.reverse()
    ttbp_gopher = os.path.join(
        os.path.expanduser('~/public_gopher'),
        gopher_path)

    if not os.path.isdir(ttbp_gopher):
        print('\n\tERROR: something is wrong. your gopher directory is missing. re-enable gopher publishing.')
        return

    with open(os.path.join(ttbp_gopher, 'gophermap'), 'w') as gophermap: 
        gophermap.write(GOPHERMAP_HEADER.format(
                        user=getpass.getuser()))
        for entry_filename in entry_filenames:
            filename = os.path.basename(entry_filename)

            with open(os.path.join(ttbp_gopher, filename), 'w') as gopher_entry:
                with open(entry_filename, 'r') as source_entry:
                    gopher_entry.write(source_entry.read())
            gophermap.write('0{file_label}\t{filename}'.format(
                file_label=os.path.basename(entry_filename),
                filename=filename))


def setup_gopher(gopher_path):
    """Given a path relative to ~/public_gopher, this function:

    - creates a directory under public_gopher
    - creates a landing page

    It doesn't create a gophermap as that is left to the publish_gopher
    function.
    """
    public_gopher = os.path.expanduser('~/public_gopher')
    if not os.path.isdir(public_gopher):
        print("\n\tERROR: you don't seem to have gopher set up (no public_gopher directory)")
        return

    ttbp_gopher = os.path.join(public_gopher, gopher_path)
    if os.path.isdir(ttbp_gopher):
        print("\n\tERROR: gopher path is already set up. quitting so we don't overwrite anything.")
        return

    os.makedirs(ttbp_gopher)
