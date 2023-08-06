# xu

Collection of handy random generators.

| classes | objects | functions |
|---------|---------|-----------|
| integer | boolean | pick      |
| number  | char    |           |
| string  | random  |           |

## Examples

```python
from xu import string

for it in string(10).list(2):
	print(it)
print(string(10).lower)
print(string(10).upper)
print(string(10).digit)
print(string(10).alpha)
print(string(10).lower_d)
print(string(10).upper_d)
```

	8lfMoAUnZz  # default (lower + upper + digit)
	47Vw8Tai5Z  # default (lower + upper + digit)
	qkjnhsadha  # lower
	SEAHSVHGOZ  # upper
	9933557070  # digit
	TxIUNiaiPD  # alpha   (lower + upper)
	h33jxxnfo9  # lower_d (lower + digit)
	8ZOJKNP5RK  # upper_d (upper + digit)

----

```python
from xu import boolean

for it in boolean.matrix(2, 4):
	print(it)
```

	[False, True]
	[True, False]
	[True, True]
	[False, False]

----

```python
from xu import pick

data = [1, 2, 3, 4]
print(pick(data))

data = '1234'
print(pick(data, 2))
```

	3
	['2', '3']

----

```python
from xu import integer

print(integer(9) * 5)
print()
for row in integer(9) ** 5:
	print(row)
print()
for row in integer(9) ** (5, 3):
	print(row)
```

	[4, 9, 1, 3, 5]

	[4, 2, 0, 8, 8]
	[0, 3, 9, 4, 2]
	[5, 1, 1, 8, 2]
	[1, 5, 3, 5, 6]
	[6, 1, 1, 0, 2]

	[1, 1, 6, 1, 8]
	[4, 0, 2, 3, 9]
	[1, 5, 7, 2, 4]
