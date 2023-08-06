ORMM
====

Operations Research Models & Methods (ORMM) implements Paul A. Jensen's Excel Add-ins in modern Python.  His Excel packages were last updated in 2011, and while I believe they do still work (for the most part), I fear that his incredible work may become outdated in a couple of ways:

- Excel is not as commonly used for OR, except in settings where security is of the utmost concern and/or modern languages like Python, R, Julia, C, C++, MATLAB, AMPL, or other modeling software are not available.
- While his website and packages are still available `here <https://www.me.utexas.edu/~jensen/ORMM/>`_, some sections are/may become unusable.  The animations rely on Flash, which is being phased out in google chrome and other web browsers.
- His work is not nearly as visible as I believe it deserves - any OR practitioner can find value in studying his examples of applications, and use his model implementations to great effect.

Developer Environment
---------------------

To use the same packages used in development (for creating additions / modifications), you may use the bash command below to install the dev requirements (recommended to do this in your virtualenv).  This includes being able to run tests and add to the documentation.

.. code:: console

   $ pip install -e .[dev]