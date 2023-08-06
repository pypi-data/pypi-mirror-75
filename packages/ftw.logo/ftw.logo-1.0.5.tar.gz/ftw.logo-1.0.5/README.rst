.. contents:: Table of Contents


Introduction
============

Plone extension providing smart logo handling.
Based on an svg Logo or Icon the extension is able to produce all kinds
of scales such as apple touch icons or android PWA logos.

Compatibility
-------------

Plone 4.3.x
Plone 5.1.x

Prerequisites
=============

See `wand.py dependencies <http://docs.wand-py.org/en/0.4.4/index.html#requirements>`_


OSX (High Sierra)
-----------------

Two important points for developers.

If you experience problems converting some svg's to png's, like getting a all transparent
PNG. Install imagemagick with librsvg. Also don't install imagemagick version 7. Not gonna work.

.. code-block:: sh

     brew install imagemagick@6
     brew link imagemagick@6 --force


Also make sure `/usr/local/opt/imagemagick@6/bin` is in the PATH


Installation
============

- Add the package to your buildout configuration:

.. code-block:: ini

    [instance]
    eggs +=
        ...
        ftw.logo


Development
===========

1. Fork this repo
2. Clone your fork
3. Shell: ``ln -s development.cfg buildout.cfg``
4. Shell: ``python bootstrap.py``
5. Shell: ``bin/buildout``

Run ``bin/test`` to test your changes.

Or start an instance by running ``bin/instance fg``.

Scales
======

Basically there are just logo and icon scales.
The logo scales are mostly used on the top left and can have
any dimensions. The converter creates a ``logo`` and ``mobile_logo`` from the
base logo which has to be an svg file.
The icon scales are used for ``apple_touch_icons``, ``favicons`` or ``android PWA icons``.
The base icon must be square, and the scaled icons will also if course be square.
In summary we need two different SVG source files. One with an arbitary ratio
and the other with a square ratio.

All scales are taken from https://realfavicongenerator.net/.

The available scales are:

- LOGOS
   - LOGO
   - MOBILE_LOGO
   - BASE
   - get_logo (virtual)
- ICONS
   - APPLE_TOUCH_ICON
   - FAVICON_32X32
   - FAVICON_16X16
   - MSTILE_150X150
   - ANDROID_192X192
   - ANDROID_512X512
   - FAVICON
   - BASE


"get_logo" scale
-----------------

The get_logo virtual scale returns either the BASE (svg from ZCML) or if available the overridden
BASE or LOGO scale from the Dexterity content type.


Converter
=========

The converter holds all the scale definitions and so is able to generate
the scales needed. `wand.py <http://docs.wand-py.org/en/0.4.4/>`_ is used
to convert the svg source files into the different scales.
The converter generates a modified ``wand.py``
image proxy which is able to return the actual blob of the scale behind the proxy.
Refer to the `write images <http://docs.wand-py.org/en/0.4.4/guide/write.html>`_ and
`resizing and cropping <http://docs.wand-py.org/en/0.4.4/guide/resizecrop.html>`_
section for more information about how the converter uses ``wand.py``.

ZCML
====

The extension introduces a custom icon and logo directive for zcml.
Both directives accept ``for``, ``layer`` and ``base`` attributes.
The base attribute defines the svg source files for all scales.
The multiadapter adapts context and request. So the svg source file
can be overridden by using one or both of ``for`` and ``layer``.

First include the directive:

.. code-block:: xml

   <configure
    ...
    xmlns:logo="https://namespaces.4teamwork.ch/ftw.logo"
    ...
    >

Example:

.. code-block:: xml

   <logo:logo base="logo.svg" />

The next block will override the previous config.

.. code-block:: xml

   <logo:logo base="custom_logo.svg" layer="your.product.interfaces.IYourProductLayer" />


It's also possible to define a pre scaled image for `logo`, `mobile` and `favicon`.

.. code-block:: xml

   <logo:logo base="resources/min.svg"
              logo="tests/fixtures/logo.png"
              mobile="mobile.png"
              primary_logo_scale="logo" />

   <logo:icon base="icon.svg" favicon="favicon.ico" />


Please remember a base svg is required anyway. If you can't supply one, simply put in a transparent empty svg.
If you dont't have one you can use the one from this package, which is located in the resources folder. It's called min.svg. Also set the primary_logo_scale to "logo", since ftw.logo always prefers the svg over all other scales.


Change default height for logo and mobile scale by zcml:

.. code-block:: xml

   <logo:logo base="resources/min.svg"
              height="200"
              mobile_height="30" />


Logo View
=========

All logos and icons can be accessed through the logo browser view.
The URL consists of the browser view name ``@@logo`` followed by the type of the
image and the actual scale.

Examples:

- ``@@logo/logo/BASE``  will show the svg logo source.
- ``@@logo/icon/APPLE_TOUCH_ICON``  will show the apple touch icon as a png image.

Caching
=======

Caching is provided by adding a query string parameter to every logo request.
The cachekey consist of a sha256 hash including the files binary data.
If you have plone.app.caching enabled, install the `caching` profile from ftw.logo.
This will define etag values so the viewlet is cached properly.

Links
=====

- Github: https://github.com/4teamwork/ftw.logo
- Issues: https://github.com/4teamwork/ftw.logo/issues
- Pypi: http://pypi.python.org/pypi/ftw.logo


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.logo`` is licensed under GNU General Public License, version 2.
