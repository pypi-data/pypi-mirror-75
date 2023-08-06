# Data processing and persistence components for Pip.Services in Python Changelog

## <a name="3.0.2"></a> 3.0.2 (2020-08-01)

## <a name="3.0.0"></a> 3.0.0 (2018-10-30)

### New release
* Restructuring package

### Features
- **Persistence** - in-memory and file persistence
- **Data** - data interfaces

## <a name="2.2.0"></a> 2.2.0 (2017-04-11)

### Features
* Added getListByIds(), deleteByFilter() and deleteByIds() methods to all Identifiable persistence classes

## <a name="2.0.0"></a> 2.0.0 (2017-02-27)

### Features
* Added methods for explicit data convertion from and to public representation
* Added update_partially Method to all persistences
* Added IPartialUpdater interface

### Breaking Changes
* Migrated to **pip-services** 2.0
* Separated code persistence from IdentifiablePersistence classes

## <a name="1.0.0"></a> 1.0.0 (2017-01-28)

Initial public release

### Features
* **memory** Memory persistence
* **file** Abstract file and JSON persistence
* **mongodb** MongoDB persistence

### Bug Fixes
No fixes in this version

