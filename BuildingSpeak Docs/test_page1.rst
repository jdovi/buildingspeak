.. _examples1:


***************
Examples 1
***************


If you now point your browser to :file:`_build/html/index.html`, you
should see a basic sphinx site.

.. image:: _static/basic_screenshot.png

.. _fetching-the-data:

Fetching the data
==================

.. sourcecode:: ipython

    In [69]: lines = plot([1,2,3])

    In [70]: setp(lines)
      alpha: float
      animated: [True | False]
      antialiased or aa: [True | False]
      ...snip
	  

Sphinx cheat sheet
===================

Here is a quick and dirty cheat sheet for some common stuff you want
to do in sphinx and ReST.  You can see the literal source for this
file at.
   

.. _formatting-text:

Formatting text
===============

You use inline markup to make text *italics*, **bold**, or ``monotype``.

You can represent code blocks fairly easily::

   import numpy as np
   x = np.random.rand(12)

Or literally include code:

.. _making-a-list:

Making a list
=============

It is easy to make lists in rest

Bullet points
-------------

This is a subsection making bullet points

* point A
* point B
* point C


Enumerated points
------------------

This is a subsection making numbered points

#. point A

#. point B

#. point C


.. _making-a-table:

Making a table
==============

This shows you how to make a table -- if you only want to make a list see :ref:`making-a-list`.

==================   ============
Name                 Age
==================   ============
John D Hunter        40
Cast of Thousands    41
And Still More       42
==================   ============

.. _making-links:

Making links
============

It is easy to make a link to `yahoo <http://yahoo.com>`_ or to some
section inside this document (see :ref:`making-a-table`) or another
document.

You can also reference classes, modules, functions, etc that are
documented using the sphinx `autodoc
<http://sphinx.pocoo.org/ext/autodoc.html>`_ facilites.  For example,
see the module :mod:`models_functions` documentation, or the
class :class:`~BuildingSpeakApp.models.Account`, or the method
:meth:`~models_functions.convert_units`.

Functions Module
=================
.. automodule:: models_functions
    :members:
