Material Design HTML Theme for Sphinx
=====================================

Requirements
------------

-  python

   -  Sphinx

Quick Start
-----------

Install the latest version of sphinx_iowmd_theme with ``pip``.

.. code:: shell

   pip install sphinx_iowmd_theme

Add the following line to ``conf.py``.

.. code:: python

   html_theme = 'sphinx_iowmd_theme'

Html theme options
------------------

The following is a description of the options that can be specified in
``html_theme_options`` in your project's ``conf.py``.

.. code:: python

   html_theme_options = {
       # Specify a list of menu in Header.
       # Tuples forms:
       #  ('Name', 'external url or path of pages in the document', boolean, 'icon name')
       #
       # Third argument:
       # True indicates an external link.
       # False indicates path of pages in the document.
       #
       # Fourth argument:
       # Specify the icon name.
       # For details see link.
       # https://material.io/icons/
       'header_links' : [
           ('Home', 'index', False, 'home'),
           ("ExternalLink", "http://example.com", True, 'launch'),
           ("NoIconLink", "http://example.com", True, ''),
           ("GitHub", "https://github.com/zaniphrom/sphinx_iowmd_theme", True, 'link')
       ],

       # Customize css colors.
       # For details see link.
       # https://getmdl.io/customize/index.html
       #
       # Values: amber, blue, brown, cyan deep_orange, deep_purple, green, grey, indigo, light_blue,
       #         light_green, lime, orange, pink, purple, red, teal, yellow(Default: indigo)
       'primary_color': 'indigo',
       # Values: Same as primary_color. (Default: pink)
       'accent_color': 'pink',

       # Customize layout.
       # For details see link.
       # https://getmdl.io/components/index.html#layout-section
       'fixed_drawer': True,
       'fixed_header': True,
       'header_waterfall': True,
       'header_scroll': False,

       # Render title in header.
       # Values: True, False (Default: False)
       'show_header_title': False,
       # Render title in drawer.
       # Values: True, False (Default: True)
       'show_drawer_title': True,
       # Render footer.
       # Values: True, False (Default: True)
       'show_footer': True
   }

Developer's Tips
----------------

packaging
~~~~~~~~~

::

   python setup.py sdist

install
~~~~~~~

::

   pip install dist/sphinx_iowmd_theme-${version}.tar.gz

Resister PyPI
~~~~~~~~~~~~~

::

   python setup.py register sdist upload

Build Example's Document
~~~~~~~~~~~~~~~~~~~~~~~~

::

   sphinx-build -b html ./example ./_build -c ./example
