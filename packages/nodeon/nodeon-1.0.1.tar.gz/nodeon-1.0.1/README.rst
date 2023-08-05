nodeon
======

A program to create Node.js virtual environments.

Usage:

.. code:: shell

    nodeon [project-name] [--node] [--mirror] [--list] [--lts]

Example usages:

.. code:: shell

    # create virtual node with the latest stable version of Node.js
    nodeon my-project

    # create virtual node with the latest LTS version of Node.js
    nodeon my-project --lts

    # create virtual node with Node.js v14.0.0
    nodeon my-project --node=14.0.0

    # create virtual node with custom mirror
    nodeon my-project --mirror=https://nodejs.org/dist

    # show Node.js LTS versions
    nodeon --list --lts

