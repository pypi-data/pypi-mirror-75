DeferredResult
---

This library provides simple deferred result.

# Usage

Create deferred result:
```python
def_result = DeferredResult[str]()
``` 

Then you can wait for the result using optional timeout:
```python
result = def_result.wait(timeout=1)
```

While waiting for result other thread can set result:
```python
def_result.resolve('Hello World')
```

After resolving result all threads waiting for result will be resumed.

It is also possible to reject deferred result:
```python
def_result.reject(RuntimeError('Well....'))
```

In that case all threads waiting for result will be resumed and exception passed to `reject` will be thrown.
