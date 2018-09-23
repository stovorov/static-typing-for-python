<h2> STATIC TYPING FOR PYTHON </h2>

<h4>Type annotations & mypy</h4>

<font size="5">&mdash; Pawel Stoworowicz (@stoworow)</font>

<br>

<h4> PyCode 2018, Warsaw </h4>

---

## Roadmap

1. To whom is this presentation addressed?
2. What is static typing?
3. What is Mypy?
4. Mypy in action
5. Where to start?
6. When I *may* need this?
7. Do's and don'ts aka personal experiences


---

### About me

Currently serving as a Graphics Software Engineer at Intel.

Interests: software development, ML,
RF engineering, Electronics Design Automation, analog stuff, tube amplifiers,
guitars... lot's of guitars...

ps. All statements presents only personal point of view :\)

---

#### To whom is this presentation addressed?

You are either:

1. Developer with some hands-on experience.
2. Person working mostly with python 2 and you are willing to switch to Python 3.
3. Developer who at least once got lost in his/her code...
4. Starting new Python project and considering some quality validating linters.

---

From Python's executive summary:

> Python is an interpreted, object-oriented, high-level programming
> language with dynamic semantics. Its high-level built in data
> structures, combined with **dynamic** **typing** and dynamic binding[\.\.\.]

---

### Why we love Python?

1. Fast development
2. Neat syntax
3. duck typing
4. *Batteries included*
5. Community

Lots of other...

---

### Why static typing may be cool?

1. Faster to understand code.
2. Code easier to maintain.
3. Easier to debug(?).
4. Improvement of quality.

---

### Duck typing + static types = Mypy

---

> Mypy is an **experimental** optional static type checker for Python
> that aims to combine the benefits of dynamic (or "duck")
> typing and static typing. Mypy combines the expressive power
> and convenience of Python with a powerful type system and
> compile-time type checking. 

---
## type hints (PEP 484)

```python
def foo(bar: str = 'string') -> None:
    print(bar)
    
print(foo.__annotations__)
```

\_\_annotations\_\_:

> {'bar': <str>, 'return': None}'

---

### Module typing

This module supports type hints as specified by PEP 484 and PEP 526.

---

## type hints in action

```python
from typing import List


def foo(bar: int = 10) -> List[int]:
    return [_ for _ in range(bar)]
```
---

## In a nutshell

We wish to apply static type checker for dynamically 
typed language to limit types bound to particular name (variable).
<br><br>

*Type hinting does not affect duck typing in anyway.*

---

## pip install mypy

---

### Running MYPY

```python
from typing import List


def foo(bar: int = 10) -> List[int]:
    return [_ for _ in range(bar)]

def bar() -> List[str]:
    return foo()
```
mypy test_types.py


test_typing.py:9: error: Incompatible return value type (got "List[int]", expected "List[str]")

---

### Types examples

* Dict
* Mapping
* List
* Tuple
* **Any**
* **Union**
* **Optional**
* Callable
* NamedTuple

---

### Nesting types

```python
def foo() -> Dict:

def foo() -> Dict[str, List]:

def foo() -> Dict[str, List[int]]:

```

---

### Defining names types

* Before Python 3.6:

```python
some_dict = {} # type: Dict[str, str]
```

* Since Python 3.6:

```python
some_dict: Dict[str, str] = {}
```
---

### Returning multiple types?

```python
def foo() -> Any:
    ...
```

```python
def foo() -> Union[str, int]:
    ...
```
---

## Optional

---

Simple service client code snippet:

```python
class ServiceClientBase:
    def __init__(self,
                 schema: str = 'http',
                 host: str = 'host_name',
                 port: int = 80) -> None:
        self.schema = schema
        self.host = host
        self.port = port
    
    @property
    def url(self) -> str:
        return '{}://{}:{}'.format(self.schema, self.host,
                                   self.port)
```

---

```python
class ServiceAClient(ServiceClientBase):
    pass

class ServiceBClient(ServiceClientBase):
    pass

def get_client(conn_id: int,
               cfg: Mapping) -> Optional[ServiceClientBase]:
    if conn_id == 1:
        return ServiceAClient(**cfg)
    if conn_id == 2:
        return ServiceBClient(**cfg)
    return None
```

---

```python
from typing import Optional, Mapping

class SomeClass:
    def __init__(self, cfg: Mapping) -> None:
        self.cfg = cfg
    
    @property
    def name(self) -> Optional[str]:
        return self.cfg.get('name')
```

---

## Cast function

---

Zero computing cost cast function is useful for types conversion.


```python
from typing import Mapping, Dict, cast

def foo() -> Dict:
    return {'1': 1}

data = cast(Mapping, foo())
```

---

## Custom types


```python
from typing import NewType

connection_id = NewType('connection_id', int)
```

```python
def get_client(conn_id: connection_id,
               cfg: Mapping) -> Optional[ServiceClientBase]:
    if conn_id == 1:
        return ServiceAClient(**cfg)
    if conn_id == 2:
        return ServiceBClient(**cfg)
    return None
```

---

### How to add Mypy in currently developed app/service?

1. Start checking types only for one particular module.
2. Start using type hints in newly developed modules.
3. Refactor existing code with type-hint oriented one.
4. Create stub file(?)

---

### Stub file

For already existing code we can create **stub** file which will define
types required by functions, classes, variables in our module.
Files will be named **.pyi** (C headers like files).

```python
x: int

def afunc(code: str) -> int: ...
def afunc(a: int, b: int = ...) -> int: ...
```

---

### Good practices, issues, observations

---

Type defined as a string if class method returns instance
of the same class.

```python
class SomeClass:
    ...
    def child(self, arg) -> 'SomeClass':
        return SomeClass(self, arg)
```

---

When importing from module only to denote type use TYPE_CHECKING flag.

```python
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from x_module import xyz

def some_function() -> 'xyz':
    ...

```
---

In some situations we may end up using **# type: ignore** comment.

```python
@lru_cache(1)
@property   # type: ignore
def is_passing(self) -> bool:
    ...
```

In this case mypy will identify type not as boolean but as property decorated.

---

While passing e.g. int argument to a function with Optional[int] we'll
end up with mypy's error about types mismatches...

```python
def some_function(x: Optional[int] = None) -> str:
    ...

z = 10
some_function(cast(Optional[int], z))
```

---

## Considering mypy?

---

Useful for:

1. Big services
2. Complex tools

Not necessary:

1. Ad-hoc written few liners
2. Simple scripts performing custom operations

---

## Questions?

---

## Contact

@stoworow

stoworow@gmail.com

https://github.com/stovorov/presentations

