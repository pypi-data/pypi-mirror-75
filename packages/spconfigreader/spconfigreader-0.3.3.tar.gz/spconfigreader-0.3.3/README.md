# Spring Confing Reader

## Table of Contents

- [Spring Confing Reader](#spring-confing-reader)
  - [Table of Contents](#table-of-contents)
  - [General Information](#general-information)
  - [Configfile](#configfile)
  - [Function overview](#function-overview)
  - [Usage](#usage)
    - [object](#object)
    - [single entry](#single-entry)
  - [Override with Environment Vairables](#override-with-environment-vairables)

## General Information

There are several config readers for Python but no one matches my requirements. so, i created my own.

The focus is to read configuration from a YAML file with the option to override it with environment variables, which is needed for working with Docker.

Inspiration was the configuation in the Java framework Spring, which leads to the name.

## Configfile

As default, {root}/config.yml is the configfile. This can be changed with the following code before the first use.

```python
configreader.__configfile__ = "path/to/file.yml"

```

## Function overview

```python
get(key: str, default: str = None)
```

```python
getObject(obj: object, path: str = None)
```

## Usage

### object

first, create a class with all fields you want to read. They need either a type annotation or must be initialized. Subclasses must always be initalized.

The variable name should match the name in the YAML file.

At this point, default values can also be defined. If a value is given in the YAML, it will be overrwritten.

An additional field it the __path__ field, wich contains the root path in the YAML file. This can also be specified in the getObject() method later

As example:

config.yml

```yaml

datasource:
  server: "mssql.server"
  test:
    val1: "foo"
    val2: "bar"
```

code

```python
class Test:
    val1: str
    val2: str

class Datasource:
    __path__: str = "datasource"

    server: str
    port: int = 1433
    protocol: str = "tcp"
    test = Test()
```

To read the values, use the getObject() method in one of this ways:

```python
datasource = configreader.getObject(Datasource())
```

```python
datasource = Datasource()
configreader.getObject(datasource)
```

### single entry

To get only a single entry, use the get() function

```python
val = get("path.of.entry")
```

second parameter is a default value if no entry is found in the YAML file.

## Override with Environment Vairables

To override a entry in the YAML, set an environment variable with the same key but with upper letters and with _ instead of .

Example:

```bash
path.to.entry -> PATH_TO_ENTRY
```
