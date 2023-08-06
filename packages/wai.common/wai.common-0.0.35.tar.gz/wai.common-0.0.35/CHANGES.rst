Changelog
=========

0.0.35 (2020-08-05)
-------------------

- Bug fixes.

0.0.34 (2020-07-30)
-------------------

- Added function to get the standard app configuration directory on a system.

0.0.33 (2020-07-30)
-------------------

- Bug fixes.

0.0.32 (2020-07-29)
-------------------

- Fixed bug where option handlers weren't respecting redefinitions of option help text.

0.0.31 (2020-03-31)
-------------------

- Removed Rational class as a better implementation is provided by fractions.Fraction.
- Several changes to CLI classes:

  - Can query the optionality of all option types.
  - Default values are now unchecked.
  - TypedOption no longer produces lists of lists for certain combinations of nargs and action.
  - Argument parsers log by default (instead of printing to stdout/stderr).

- Can now get all registered classes from a ClassRegistry.

0.0.30 (2020-03-23)
-------------------

- Added a partial implementation of rational numbers.

0.0.29 (2020-03-18)
-------------------

- Bug fixes.
- Initial values for options on CLIInstantiable objects can be specified in internal format.

0.0.28 (2020-03-12)
-------------------

- Bug fixes.

0.0.27 (2020-03-12)
-------------------

- Additional functionality for ClassRegistry.
- New cli Option, ClassOption, selects from a predefined set of classes.
- import_code can now optionally bypass aliasing of inner classes.
- meta.code_repr package for representing values as Python code.

0.0.26 (2020-03-11)
-------------------

- Fixed bug in Option descriptors which prevented them from working with generic
  option-handlers in Python3.6.

0.0.25 (2020-03-10)
-------------------

- Added LazyDescriptor.
- Added function to get the fully-qualified name of a class.
- Added function to get the import code for a class.
- Added ClassRegistry class.
- Added meta-constants module.
- Added command-line utilities.

0.0.24 (2020-02-21)
-------------------

- Fixed typing bug in dynamic_defaults.

0.0.23 (2020-02-20)
-------------------

- Added dynamic defaults.
- Added function to get the kwargs that are supplied to a function (non-default).
- Added decorator ensure_error_type which wraps exceptions not of a particular
  type in that type.
- Removed json package, now in its own repository, wai-json.

0.0.22 (2020-02-12)
-------------------

- Added instanceoptionalmethod, a decorator for methods which can be called from
  either the class or an instance, and take whichever they are called from as their
  first argument.
- Added LoggingMixin, which adds logging support to classes.
- Added serialisation utilities.
- Added utility for a standard library logger.

0.0.21 (2020-01-24)
-------------------

- Added logging utilities package, with utility for a standard root logger.

0.0.20 (2019-12-16)
-------------------

- Added extra methods to Polygon, Point.

0.0.19 (2019-11-27)
-------------------

- Reworking of JSON configurations to unify value setting between internal and JSON values.
- Adding caching of non-varying calculated attributes to improve serialisation time.

0.0.18 (2019-11-15)
-------------------

- Added PathContextManager, which is a context manager which changes the cwd temporarily.
- Added ensure_path, which creates a directory if it doesn't exist.

0.0.17 (2019-10-31)
-------------------

- Added TypeVarProperty, for easier caching of dynamic type variables.
- Added depth argument to flatten (iterators and sequences).

0.0.16 (2019-10-22)
-------------------

- Added support for ADAMS report files.
- Added basic support for geometry.
- Added support for working with located objects in image-classification/identification
  tasks.

0.0.15 (2019-10-09)
-------------------

- Bug fixes.

0.0.14 (2019-10-09)
-------------------

- Configuration schema caching is now lazier than ever.
- JSON serialisation now validates in both directions.

0.0.13 (2019-10-09)
-------------------

- Fixed bug in Configuration where cached schema were preventing grand-inheritance.

0.0.12 (2019-10-09)
-------------------

- Added support for checking Python versions.
- get_argument_to_typevar now works with Python3.6 and Python3.7.

0.0.11 (2019-10-09)
-------------------

- Fix so that JSON schema definitions propagate through all composite schema.

0.0.10 (2019-10-08)
-------------------

- JSON schema package now has tools for working with references/definitions.
- Configurations now validate additional properties as JSON by default.

0.0.9 (2019-10-04)
-------------------

- Added StrictConfiguration, which disables additional properties by default.
- Minor fixes.

0.0.8 (2019-09-19)
-------------------

- Fixed bug in get_argument_to_typevar.
- Added new property type for configurations, MapProperty, which behaves like a dict from
  strings to some sub-property type.
- Configurations now support: validation of additional properties, initialisation by value
  or JSON, programmatically getting/setting additional properties.

0.0.7 (2019-09-18)
-------------------

- Added meta package for typing functionality.

0.0.6 (2019-09-17)
-------------------

- Fixed bug where Absent was being validated after Property.validate_value had checked
  it, and therefore failing.

0.0.5 (2019-09-17)
-------------------

- Added interfaces for serialising/deserialising JSON using custom representations.
- Added exception package to meta package for processing exceptions. Currently only
  contains ExceptionChainer, which captures exceptions as a context-manager and then
  provides methods for processing them.
- Added utility interface JSONValidatedBiserialisable.
- Refactored configurations and properties to be more understandable.
- Added AnyOfProperty.

0.0.4 (2019-09-13)
-------------------

- Two new iterable functions, all_meet_predicate and any_meets_predicate.
- Added meta-functions for determining if methods in base-classes have been overridden
  by sub-classes.
- Rejigged abc package.
- Added JSON package, with tools for working with JSON and JSONSchema. Also specifies the
  configuration class, which allows for easy manipulation of JSON files in an object-oriented
  manner.

0.0.3 (2019-08-30)
-------------------

- Added load_dir function to file package, which can load all files in a directory.
- Added is_hashable to test if an object is hashable.
- Added Interval class representing intervals on the number line.
- Added exception InvalidStateError for classes that get into an invalid setup.
- Added typing module for type-related functionality.
- Added first, which finds the first element of an iterable to match a predicate.
- Added statistics package with quartile functions.
- Added random, which returns the elements of an iterator in random order.
- Added meta package, with functions to set and retrieve arbitrary meta-data against
  objects.
- Added ConstantIterator class, which returns the same value over and over again.
- Added metadata module to iterate, for working with metadata in iterables of objects.
- Modified TwoWayDict so type-inference works with Python-3.7.

0.0.2 (2019-08-09)
-------------------

- Removed restriction that switch only work with enums. Now can switch on any type.
  Onus is on the user to handle modifications of the switched value during switching.
- Added **abc** package, with utilities for working with abstract classes/methods.
- Added **decorator** package, with custom decorators.

0.0.1 (2019-08-09)
-------------------

- Initial release
