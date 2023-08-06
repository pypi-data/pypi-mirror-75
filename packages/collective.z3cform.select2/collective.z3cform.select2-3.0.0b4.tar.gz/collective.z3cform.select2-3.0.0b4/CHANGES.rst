Changelog
=========


3.0.0b4 (2020-07-31)
--------------------

- Fix last compilation date format for registry resource
  [mpeeters]


3.0.0b3 (2020-07-24)
--------------------

- Fix initialization of select2 widget on view mode
  [mpeeters]


3.0.0b2 (2020-02-19)
--------------------

- Use implementer instead of implements for python3 compatibility.
  [bsuttor]

- Make widget compatible with the latest versions of eea.faceted.vocabularies
  This makes it no more compatible with eea.faceted.vocabularies < 6.7
  [mpeeters]


3.0.0b1 (2019-04-16)
--------------------

- Upgrade to Plone 5
  [mpeeters]


2.0.1 (2018-08-27)
------------------

- Do not replace z3cform default widget for List/Set of Choice by
  select2 widget by default.  The widget/adapters.zcml will need to be included
  manually so this behavior is applied.
  [gbastien]

2.0.0 (2018-06-20)
------------------

- Make faceted widget compatible with eea.facetednavigation 10+.
  This makes it no more compatible with eea.facetednavigation<10.
  [gbastien]


1.4.1 (2017-12-01)
------------------

- Fixed `MultiSelect2Widget` to use a `@property` for `items` as it is the case
  for `SingleSelect2Widget.items` it is inheriting from (that was fixed in
  release 1.4.0).
  [gbastien]


1.4.0 (2017-11-22)
------------------

- Fix an issue with the width of hidden elements (e.g. in tabs)
  [mpeeters]

- Restore initialization for multi select2 widgets
  [mpeeters]

- Require `z3c.form >= 3.2.11` where the `SelectWidget.items` is a `@property`
  and no more a callable method.
  [gbastien]


1.3.4 (2017-01-10)
------------------

- Fix widget in overlays when loading a form in an existing overlay.
  This worked before 1.3, but another overlay fix in 1.3 broke this case.
  [vincentfretin]


1.3.3 (2017-01-10)
------------------

- Don't use default param feature in select2-widget.js, the previous fix
  was incomplete.
  [vincentfretin]


1.3.2 (2017-01-09)
------------------

- Don't use default param feature in select2-widget.js, this is ES6, IE 10
  doesn't support it.
  [vincentfretin]


1.3.1 (2016-12-09)
------------------

- Rename wrong class facted-select-criterion to faceted-select-criterion
  [vincentfretin]


1.3 (2016-12-01)
----------------

- Remove specific css rules that was introduced in 1.2
  [vincentfretin]

- Fix widget in overlays. If you upgrade from 1.1, you need to reinstall
  the profile to add a css in portal_css.
  [cedricmessiant]

- Wrap call to select2 initialization in JS function `initializeSelect2Widgets`
  so it is easy to call from everywhere (like in an overlay initialization).
  Parameter width can be specified when calling `initializeSelect2Widgets`
  and defaults to `resolve`.
  [gbastien]


1.2 (2016-08-25)
----------------

- Avoid an error if Faceted namespace is not defined
  [mpeeters]

- Add a select2 single and multi select widget
  [mpeeters]


1.1 (2016-07-07)
----------------

- Use faceted-select2-widget instead of faceted-select-widget to not break
  the original faceted-select-widget widget.
  [vincentfretin]

- Depends on eea.jquery >= 8.8 to fix images in select2.
  [vincentfretin]

- Replace collective.taxonomy.widget.TaxonomySelectFieldWidget by the widget
  from this package.
  [vincentfretin]

- Initialize widgets in overlays now.
  [vincentfretin]


1.0 (2016-04-20)
----------------

- Initial release.
  [vincentfretin]
