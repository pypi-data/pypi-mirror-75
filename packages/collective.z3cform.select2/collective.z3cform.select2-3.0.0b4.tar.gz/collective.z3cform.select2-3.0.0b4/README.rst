.. image:: https://travis-ci.org/collective/collective.z3cform.select2.svg?branch=master
    :target: https://travis-ci.org/collective/collective.z3cform.select2
.. image:: https://coveralls.io/repos/collective/collective.z3cform.select2/badge.png?branch=master
   :target: https://coveralls.io/r/collective/collective.z3cform.select2?branch=master


.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide_addons.html
   This text does not appear on pypi or github. It is a comment.

==========================
collective.z3cform.select2
==========================

Features
--------

- select2 multivalued facetednavigation widget for 2-level vocabulary created
  with collective.taxonomy.
  Select "Select2" criteria in facetednavigation and select a taxonomy.
- select2 multivalued z3c.form widget that works nice with 2-level vocabulary
  created with collective.taxonomy

If you want to use the select2 widget instead the default z3cform widget for List/Set of Choice,
just include file widget/adapters.zcml in another package policy like this :

    <include package="collective.z3cform.select2.widget" file="adapters.zcml" />

Theming
-------

The widget was developped initially for a bootstrap 3 theme and fontawesome.
There is a search button icon left to the select that upon click open the select.
If your site doesn't have a bootstrap based theme, you may want to add this
css rule to your project to hide the tiny button::

    button[data-select2-open] { display: none; }

The z3cform widget in display mode uses the badge class, without a comma
separator so it may be confusing when you don't have style for the badge class.
You can revert to a comma separated display by including minimal.zcml instead
of configure.zcml, see Installation below.


Translations
------------

- One constant Faceted.taxonomyAllString currently in French.


Installation
------------

Install collective.z3cform.select2 by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.z3cform.select2
    zcml =
        collective.z3cform.select2
        # or collective.z3cform.select2-minimal


and then running ``bin/buildout``

You need to install the collective.z3cform.select2 addon to register the
select2 js library. In a facetednav, add a Select2 criterion.

eea.facetednavigation
---------------------

Version 2.0.0+ is only working with eea.facetednavigation 10+.
If you need to make it work with eea.facetednavigation < 10, use versions < 2.0.0


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.z3cform.select2/issues
- Source Code: https://github.com/collective/collective.z3cform.select2


Support
-------

If you are having issues, please let us know.


License
-------

The project is licensed under the GPLv2.
