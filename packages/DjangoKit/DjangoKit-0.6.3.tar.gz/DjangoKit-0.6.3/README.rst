=========
DjangoKit
=========

DjangoKit is a set of extensions for Django. They have been assembled into 
this Django app from many complex and similar projects. The reason for building
this application is as follows:

    "I don't find it necessary to push most of these things into the 
    framework code, but a dedicated library for them over all these years of 
    different development has just become an urgent necessity. We need to take
    the common code out, not move it from project to project every time."

    -- Grigoriy Kramarenko.

Maybe you will find for yourself here the things you need. Just look at the
`source code`_ or documentation (when it's ready).

.. _source code: https://gitlab.com/djbaldey/djangokit/

Installation
------------

.. code-block:: shell

    pip3 install djangokit
    # or
    pip3 install git+https://gitlab.com/djbaldey/djangokit.git@master#egg=DjangoKit


Quick start
-----------

1. If you want to use templatetags and locales from this library,
   then add "djangokit" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'djangokit',
    ]


