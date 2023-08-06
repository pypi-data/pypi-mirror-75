# Basic portable abstractions for Pip.Services in Python Changelog

## <a name="3.1.0"></a>3.1.0 (2020-08-04)
* Fixed issues

## <a name="3.0.0"></a>3.0.0 (2018-10-30)

### New release
* Restructuring package

### Features
* **commands** Command and Eventing patterns
* **config** Configuration framework
* **convert** Portable soft data converters
* **data** Data value objects and random value generators
* **errors** Portable application errors
* **random** Random components
* **refer** Component referencing framework
* **reflect** Portable reflection helpers
* **run** Execution framework
* **validate** Data validators

## <a name="2.4.0"></a> 2.4.0 (2017-04-20)

### Breaking changes
* Removed ReferenceQuery

## <a name="2.3.2"></a> 2.3.2 (2017-04-17)

### Bug Fixes
* Fixed validation error messages

## <a name="2.3.0"></a> 2.3.0 (2017-04-11)

### Features
* **config** Added parameters to ConfigReader.read_config()
* **validate** Added FilterParamsSchema and PagingParamsSchema

## <a name="2.0.0"></a> 2.0.0 (2016-04-05)

### Features
* **auth** Added MemoryCredentialStore
* **auth** Added DefaultCredentialStoreFactory
* **build** Added Factory
* **connect** Added MemoryDiscovery
* **connect** Added DefaultCredentialStoreFactory
* **commands** Added ICommandable
* **refer** Added ReferenceQuery
* **refer** Added DependencyResolver
* **config** Added NameResolver
* **config** Added OptionsResolver
* **config** Added IConfigReader
* **config** Added CachedConfigReader
* **config** Added FileConfigReader
* **config** Added DefaultConfigReaderFactory

### Breaking Changes
* **run** Removed IParamExecutable. Now IExecutable takes args
* **run** Removed IParamNotifable. Not INotifable takes args
* **refer** Removed IDiscoverable and ILocateable
* **refer** Changed IReferenceable interface
* **refer** ReferenceSet was renamed to References
* **log** Convertion methods moved from LogLevel to LogLevelConverter

### Bug Fixes
* Fixed datetime conversion

## <a name="1.0.0"></a> 1.0.0 (2016-09-22)

Initial public release

### Features
* **build** Component factories framework
* **commands** Command and Eventing patterns
* **config** Configuration framework
* **convert** Portable soft data converters
* **count** Performance counters components
* **data** Data value objects and random value generators
* **errors** Portable application errors
* **log** Logging components
* **refer** Component referencing framework
* **reflect** Portable reflection helpers
* **run** Execution framework
* **validate** Data validators

### Breaking Changes
No breaking changes since this is the first version

### Bug Fixes
No fixes in this version

