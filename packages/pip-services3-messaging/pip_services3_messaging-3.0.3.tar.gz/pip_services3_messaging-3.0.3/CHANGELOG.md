# Asynchronous message queues for Pip.Services in Python Changelog

## <a name="3.0.2"></a> 3.0.2 (2020-08-01)

## <a name="3.0.0"></a> 3.0.0 (2018-10-30)

### New release
* Restructuring package

### Features
- **Build** - message queues factories
- **Messaging** - asynchronous message queues

## <a name="2.0.0"></a> 2.0.0 (2017-04-13)

### Bug Fixes
* Fixed validation in RestService

## <a name="2.0.0"></a> 2.0.0 (2017-04-05)

### Features
* **rest** Added CommandableHttpService
* **rest** Added CommandableHttpClient
* **direct** Added DirectClient
* **rest** Added processing to_json method in RestClient serialization

### Breaking Changes
* Migrated to **pip-services** 2.0
* Renamed IMessageQueue.getMessageCount to IMessageQueue.readMessageCount

## <a name="1.0.0"></a> 1.0.0 (2017-01-28)

Initial public release

### Features
* **messaging** Abstract and in-memory message queues
* **rest** RESTful service and client
* **seneca** Seneca service and client

### Bug Fixes
No fixes in this version

