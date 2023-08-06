Changelog
=========

1.3.2
-----
* Fix a bug where the `get_ordered_languages` would mutate in place the list of configured languages.

1.3.1
-----
* Fix UnicodeDecodeError when installing this library on python 3 on some configurations.

1.3.0
-----

* Fix python 3 compatibility
* Declare support for python 2.7, 3.5, 3.6, 3.7, 3.8

1.2.0
-----

* Do not use deprecated AttributeExtension, use Attribute Events instead.

1.1.0
-----

* Use an OR operator for LIKE_OPS to find matches in all language columns.

1.0.1
-----

* Fix `get_text_from_dict` raising an exception when no language can be detected.

1.0.0
-----

* Initial public release
