# gexecute
Generically execute any function with a unknown function, module, or set of parameters!

Specify some set of parameters in a dictionary with the only restriction being that it must have all of the parameters with non-default values.

The function and module can either be a string representation or its corresponding object.

If the function exists in another module; you must give either the module object or the package path and module name.

```
How to Install: pip install gexecute
```

<br>

```
PiPy https://pypi.org/project/gexecute/
```

<br>

<bold>How to use:</bold>
```
def test(a, b, c='test'):
    print(a, b, c)

> test(1, 2, 3)
1, 2, 3

> gexec(test, {'a': 1, 'b': 2, 'c': 3})
1, 2, 3

> gexec(test, {'a': 1, 'b': 2})
1, 2, test

# Function name can be an object or string
> gexec('test', {'a': 1, 'b': 2})
1, 2, test

# Any variables not in the function header will not be included in the function call
> gexec(test, {'a': 1, 'b': 2, 'd': 4})
1, 2, test

# If test is in the directory C:\python\test_module.py
> gexec({'a': 1, 'b': 2, 'c': 3}, 'test', module='test_module', package_path='C:\python\')
1, 2, 3

import test_module as module_
> gexec({'a': 1, 'b': 2, 'c': 3}, 'test', module=module_)
1, 2, 3
```