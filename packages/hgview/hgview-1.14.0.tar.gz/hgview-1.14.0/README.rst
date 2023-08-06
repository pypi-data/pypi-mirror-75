Description
===========

Its purpose is to easily navigate in a Mercurial repository
history. It has been written with efficiency in mind, both in terms
of computational efficiency and user experience efficiency.

It is written in Python.

There are two user interfaces:
    * a graphical interface using PyQt5 and QScintilla, the
    * a text interface: using urwid, pygments and pyinotify

Note that the Qt5 interface is much more complete than the text interface.
The Qt5 interface provides more views on the repository.

hgview intallation notes
========================

hgview can be used either as a hg extension, or as a standalone
application.

The Common library depends on: mercurial (1.0 minimum)
The Qt5 interface depends on PyQt5, QScintilla and PyQScintilla, DocUtils
The Text interfaces depend on urwid (>=0.9.1 for "raw", >=1.0.0 for "curses"),
pygments and pyinotify


Run from the hg repository
--------------------------

You can run ``hgview`` without installing it.

::

  hg clone https://foss.heptapod.net/mercurial/hgview

You may want to add the following to your main .hgrc file::

  [extensions]
  hgext.hgview=path/to/hqgv/hgext/hgview.py

  [hgview]
  # your hgview configs statements like:
  dotradius=6
  interface=qt # or curses or raw
  # type hg qv-config to list available options

Then from any Mercurial repository::

  cd <ANY_HG_REPO>
  hg qv

or::

  export PYTHONPATH=PATH_TO_HGVIEW_DIR:$PYTHONPATH
  PATH_TO_HGVIEW_DIR/bin/hgview

Installing ``hgview``
---------------------

Installing ``hgview`` is simply done using usual ``distutils`` script::

  cd $PATH_TO_HGVIEW_DIR
  python setup.py install --help # for available options
  python setup.py install


More informations
=================

See `hg help hgview` for more informations on available configuration
options.

Acknowledgements
----------------

Hgview is a free software project hosted at https://foss.heptapod.net thanks
to the support of `Clever Cloud <https://clever-cloud.com>`_,
`Octobus <https://octobus.net>`_ and the sponsors of the heptapod project.
