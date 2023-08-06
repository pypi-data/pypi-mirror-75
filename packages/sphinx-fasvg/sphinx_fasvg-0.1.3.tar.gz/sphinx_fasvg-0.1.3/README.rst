Fontawesome SVG for Sphinx
==========================

Install the module :

.. code:: bash

   python setup.py install

Download SVGs from fontawesome website. Configure it
in your `conf.py`:

.. code:: python

   fa_brands_path = '_static/fa/brands.svg'
   fa_regular_path = '_static/fa/brands.svg'
   fa_solid_path = '_static/fa/brands.svg'

Use inline references for brands, regular or solid:

.. code:: rst

   Display an icon, with no alt text and aria-hidden:

   :fab:`icon`
   :far:`icon`
   :fas:`icon`

   An icon with some attributes:

   .. far:: icon
      :class: myclass
      :id: myid
      :alt: alt text

   For links with fasvglink and icon name as classes.
   This can be used to create fancy social links

   :fablink:`icon: Text <url>`
   :farlink:`icon: Text <url>`
   :faslink:`icon: Text <url>`

.. warning::

   Icon is not inserted in LaTeX document for now.
   It uses alt text for all builders except HTML and
   ePub.

By kujiu, EUPL 1.2 licence.
