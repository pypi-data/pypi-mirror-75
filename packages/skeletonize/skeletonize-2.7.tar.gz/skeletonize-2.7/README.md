
# skeletonize

Handles skeletonization and deskeletonizaiton of programs. This allows for easily distributing assignments to students
that contain skeleton code, and determining which parts of the skeleton they filled in after the fact, extracting blanks.

## skeletonization

Skeletonization works by taking in a piece of code with "skeleton markers" as so:

```python
def factorial(x):
    if <<<x == 0>>>:
        return <<<1>>>
    else:
        return <<<x>>> * <<<factorial(x - 1)>>>
```

and converting it into either a skeleton

```python
def factorial(x):
    if ______:
        return ______
    else:
        return ______ * ______
```

or a solution

```python
def factorial(x):
    if x == 0:
        return 1
    else:
        return x * factorial(x - 1)
```

## reskeletonization

Reskeletonization works by taking a skeleton:

```python
def factorial(x):
    if <<<x == 0>>>:
        return <<<1>>>
    else:
        return <<<x>>> * <<<factorial(x - 1)>>>
```

and a student solution:

```python
def factorial(x):
    if not x:
        return 1
    else:
        return x * factorial(x)
```

and produces a reskeletonized program

```python
def factorial(x):
    if <<<not x>>>:
        return <<<1>>>
    else:
        return <<<x>>> * <<<factorial(x)>>>
```
