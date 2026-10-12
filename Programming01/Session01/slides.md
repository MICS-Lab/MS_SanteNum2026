---
title: |
  Session 1\
  Python Types
subtitle: "Digital Health, Mastère Spécialisé · 2026"
author: "Paul Dubois"
date: "Week 1, Lecture"
---

# 1. Variables and values

## A variable is a name for a value

![](img/names.png)

::: notes
The single most useful picture of the session. `age = 54` does not put 54 "in a box
called age": it creates the value 54 somewhere in memory, and sticks the label `age` on it.
The type belongs to the value, not to the name. That is why there is no declaration in
Python (no `int age;` as in C, seen in Session 0): you never say what a name will hold.
`type(x)` asks the value what it is. Make them type it live; it is the first debugging
tool they will reach for.
:::

## Every value has a type

![](img/type_map.png)

::: notes
This is the whole map of the session, and of the notebook: five single values on the left,
four containers on the right.
Anchor each one to a health example, they will remember the example before the name:
an age is an `int`, a temperature a `float`, "has a fever" a `bool`, a patient id a `str`,
a measurement nobody took is `None`. A series of heart rates is a `list`, a blood pressure
a `tuple`, a patient record a `dict`, the distinct medications on a ward a `set`.
:::

## Names can change type

```python
x = 42          # an int
x = "42"        # now a str
x + 1           # TypeError
int(x) + 1      # 43
```

::: notes
Dynamic typing: the label moved to a new value, of a new type. Python allowed the
reassignment, but it still refuses to mix types that make no sense together.
Read the error message out loud with them. Python errors name the types involved, and
learning to read that line is half of debugging.
:::

# 2. Single values

## Numbers: `int` and `float`

![](img/numbers.png)

::: notes
`int` is exact and has no maximum: `2 ** 100` just works, Python grows the integer as
needed. `float` is a 64 bit approximation: about 16 significant digits, and a maximum
near 1.8e308 (`2.0 ** 1024` overflows).
`0.1 + 0.2 != 0.3` surprises everyone once. It is not a Python bug: 0.1 has no exact
binary form, exactly as 1/3 has no exact decimal form. Every language does this.
The rule to take away: compare floats with `math.isclose`, never with `==`. A lab value
filter written with `==` on floats will silently drop rows.
:::

## Arithmetic operators

| Expression | Result | Type |
|---|---|---|
| `7 + 2`, `7 - 2`, `7 * 2` | `9`, `5`, `14` | `int` |
| `7 / 2` | `3.5` | `float`, always |
| `7 // 2` | `3` | `int` (floor division) |
| `7 % 2` | `1` | `int` (remainder) |
| `7 ** 2` | `49` | `int` (power) |
| `round(3.14159, 2)` | `3.14` | `float` |

::: notes
The one to underline: `/` always returns a float, even for `6 / 2` (gives `3.0`).
`//` and `%` go together: "how many full groups, and what is left over". Example:
`minutes // 60` and `minutes % 60` turn a stay duration into hours and minutes.
`int(3.9)` is 3: `int` truncates, it does not round. Use `round` when you mean round.
:::

## Booleans and comparisons

```python
temp = 38.4

36.5 <= temp <= 37.5   # False
fever = temp >= 38     # True
fever and not False    # True

type(fever)            # bool
True + True            # 2
```

::: notes
Comparisons produce booleans, and booleans are what `if` and filters consume.
The chained comparison is a Python nicety that reads like maths; most languages need
`temp >= 36.5 and temp <= 37.5`.
`True + True == 2` is a curiosity now, but it is useful later: `sum(fevers)` counts the
patients with a fever, and `mean` of a boolean column is a proportion.
Note `=` (assign) versus `==` (compare): the most common typo of the week.
:::

## Every value is true or false

![](img/truthy.png)

::: notes
Any value can stand in an `if`. Zero and empty are false, everything else is true.
This gives short, idiomatic code (`if heart_rates:` instead of `if len(heart_rates) > 0:`),
and one classic trap: the string `"0"` read from a CSV is truthy, because it is a
non-empty string. Convert before you test.
:::

## Strings: `str`

![](img/string_index.png)

::: notes
A string is a sequence of characters, and sequences share one indexing grammar that they
will reuse for lists, tuples, numpy arrays and pandas: indices start at 0, negative indices
count from the end, and a slice `[start:stop]` excludes `stop`.
`name[:3]` is "the first three", `name[-1]` "the last one": say these as sentences.
Strings are immutable: you never change a string, you build a new one. That is why every
string method returns a result instead of modifying the string in place.
:::

## Working with text

```python
raw = "  Diabetes Type 2 \n"
raw.strip()       # "Diabetes Type 2"
raw.strip().lower().replace(" ", "_")
                  # "diabetes_type_2"
"Ada Lovelace".split()
                  # ["Ada", "Lovelace"]
bmi = 22.857142
f"BMI: {bmi:.2f}" # "BMI: 22.86"
```

::: notes
This slide is data cleaning in miniature. Free text from a hospital system comes with
stray spaces, mixed case and line breaks; `strip`, `lower` and `replace` normalise it
so that "Diabetes Type 2" and "diabetes type 2 " count as the same diagnosis.
Methods chain because each returns a new string.
f-strings are the way to build text from values: `{bmi:.2f}` means "two decimals".
They replace `"BMI: " + str(bmi)`, which is longer and does not format.
:::

## Conversions, and `None`

![](img/conversions.png)

::: notes
Everything read from a file or typed by a user arrives as text. `"54"` is not 54 until
you convert it, and `"54" + 1` fails.
Conversions fail loudly when the text is not what you expected: `int("3.5")` is a
`ValueError`, not a silent 3. That is a feature: a bad row stops the script instead of
corrupting the result.
`None` is Python's "no value": the glucose that was not measured. It is not 0 (a glucose
of 0 would be a dead patient). Test it with `is None`, not `== None`.
:::

# 3. Containers

## Four containers

![](img/containers.png)

::: notes
Three questions decide which container to use.
(1) Do I find items by position, or by name? Position: list or tuple. Name: dict.
(2) Will it change? A list grows as measurements arrive; a tuple is a fixed record,
  like (systolic, diastolic).
(3) Do duplicates matter? A set keeps each value once, which is exactly "the distinct
  medications".
Literal syntax: square brackets for lists, parentheses for tuples, braces for dicts and
sets (braces with `key: value` pairs make a dict). Careful: `{}` is an empty dict; an
empty set is `set()`.
:::

## Lists: `list`

```python
heart_rates = [72, 85, 64, 90, 78]
heart_rates[0]       # 72
heart_rates[1:4]     # [85, 64, 90]

heart_rates.append(101)   # at the end
heart_rates[1] = 80       # by position
heart_rates.remove(64)    # by value

sum(heart_rates) / len(heart_rates)
[hr for hr in heart_rates if hr > 80]
```

::: notes
Same indexing and slicing as strings: they already know it. The difference is that a list
can change in place.
`min`, `max`, `sum` and `len` work on any list of numbers.
The last line is a list comprehension: "the hr, for each hr in heart_rates, if hr > 80".
Read it in that order. It is the Python way to filter and transform, and it is the shape
of what pandas will do on a whole column.
`sorted(x)` returns a new sorted list; `x.sort()` sorts in place and returns `None`.
Assigning the result of `.sort()` is a classic bug.
:::

## Two names, one list

![](img/aliasing.png)

::: notes
Back to the first picture: `b = a` sticks a second label on the same list. It does not
copy. Appending through `b` is visible through `a`, because there is only one list.
This matters as soon as they pass a list to a function, or take a "copy" of a table to
clean it. `.copy()` (or `list(a)`, or `a[:]`) makes an independent list.
Strings, numbers and tuples are immutable, so sharing them is harmless: nothing can
change them in place. The trap only exists for mutable values: lists, dicts, sets.
:::

## Tuples: `tuple`

```python
blood_pressure = (120, 80)
systolic, diastolic = blood_pressure

blood_pressure[0] = 130   # TypeError

x, y = 1, 2
x, y = y, x               # swap
```

::: notes
A tuple is a fixed group of values that belong together: a blood pressure, a (row, col)
coordinate, a (min, max) range. Fixed is the point: nobody can change one half of a blood
pressure by accident.
Unpacking gives each part a name, and it is everywhere: `for key, value in d.items()`,
functions returning several values, the swap idiom.
Being immutable, a tuple can be a dict key; a list cannot.
:::

## Dictionaries: `dict`

![](img/dict_record.png)

::: notes
A dict maps keys to values: a record where each field has a name. `patient["age"]` is
clearer than `patient[1]`, and stays correct when a field is added.
Missing keys raise a `KeyError`. Two ways to cope: test first with `in`, or use `.get` with
a default. Prefer `.get` when a missing field is normal (smoking status often is).
Lookup by key is instantaneous whatever the size of the dict; that is why dicts are
also used to count things: `counts[d] = counts.get(d, 0) + 1`.
Loop with `for key, value in patient.items():`.
:::

## Sets: `set`

![](img/sets.png)

::: notes
A set keeps each value once and has no order. Converting a list to a set is the fastest
way to deduplicate: `len(set(medications))` is the number of distinct drugs.
The operators answer the clinical questions directly: which drugs do two patients share
(`&`, interaction checks), which drugs appear at all (`|`), which are specific to one (`-`).
`x in some_set` is instantaneous, like for dict keys.
:::

## Summary

| Type | Example | Changeable | Ordered | Access |
|---|---|---|---|---|
| `int`, `float` | `54`, `38.4` | no | | |
| `bool` | `True` | no | | |
| `str` | `"P001"` | no | yes | `s[0]` |
| `None` | `None` | no | | |
| `list` | `[72, 85]` | yes | yes | `l[0]` |
| `tuple` | `(120, 80)` | no | yes | `t[0]` |
| `dict` | `{"age": 54}` | yes | by insertion | `d["age"]` |
| `set` | `{"aspirin"}` | yes | no | `x in s` |

# 4. Putting it together

## A ward is a list of dicts

![](img/nested.png)

::: notes
Real data is nested: a list of patients, each a dict, some fields themselves lists.
This is exactly the shape of a JSON export, and of what a pandas DataFrame flattens later.
Read the access path one bracket at a time, saying the type at each step: `patients` is a
list, `[2]` gives a dict, `["diagnoses"]` gives a list, `[0]` gives a str.
When an access fails, print the `type` of the intermediate value: it is almost always
"I thought this was a dict but it is a list".
:::
