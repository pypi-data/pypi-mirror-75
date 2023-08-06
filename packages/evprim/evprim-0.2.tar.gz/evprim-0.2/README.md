<span id = "subir"></span>

# Evprim

This library has the object of identify even, odd and compound numbers as individually or in tuple/lists.

### Pre requirements 📋

To install the library, it is recommended have PYTHON installed in its latest version, but if you have an earlier version install the PIP tool.

A way to check if you have PIP installed is write in the terminal: 

`pip --version`

For more information read the documentation [here](https://pip.pypa.io/en/stable/installing/)

### Installation 🔧  

To the installation the library write in your terminal:

`pip install evprim`

In case of actualization the library write:

`pip install -U evprim`

---
## Archives 

It contains 3 archives:

* <a href = "#composite">composite</a>

* <a href = "#even">even</a>

* <a href = "#prime">prime</a>

To Access an archive, we do write 

```python
import evprim.prime 
```

Other example:

```python
import evprim.composite as compt #Rename
```

We can use the “from” so we don’t have to write the exact library from the beginning, accessing the function directly.

```python
from evprim.even import * #All
```
---
<span id = "composite">

## Running composite ⚙️


List of functions:

* <a href = "#isacomposite">isacomposite</a>

* <a href = "#complitu">lituComposite</a>

* <a href = "#compnumber">compositeNumber</a>

<span id = "isacomposite"></span>

#### isacomposite 🔩

Emits a **True** if the entered value is a composite number.

```python
import evprim.composite as compt

print(compt.isacomposite(4))
```
Output:

```python 
True
```

Otherwise will emits a **False**

```python
import evprim.composite as compt

print(compt.isacomposite(2))
```
Output:

```python 
False
```

In case of write a *negative* number, *number 0* or *number 1*, will return it a **False** value.  If you write more than 2 numbers or a number of type float it will show an error.

```python
import evprim.composite as compt

print(compt.isacomposite(2,10))
```
Output:

```python
TypeError: isacomposite() takes 1 positional argument but 2 were given
```

This is because the object of the function **isacomposite** is the analyze a single value. If you wish to analyze a “group” of numbers use the functions <a href = "#complitu">***lituComposite***</a> <a href = "#compnumber">***compositeNumber***</a>.

<span id = "complitu"></span>

#### lituComposite 🔩

From a list or tuple, it does a "route" and "ejects" the numbers that aren't composed

```python
import evprim.composite as compt

print(compt.lituComposite([10,-10,100,3,2,4,1,0,12,4.5]))
```

Output:

```python
[10, 100, 4, 12]
```

In case no number is composed, it only throws a *list/tuple* empty

***lituComposite*** will not accept data other than *list/tuple*, even if it is only a single integer, that is work of the <a href = "#isacomposite">***isacomposite***</a> function

Note: As I said can be entered *tuples*, however it causes problems, when I update the project I will fix it

<span id = "compnumber"></span>

#### compositeNumber 🔩

It allows to receive multiple *int* values, if any value is not a composite number then do not will returns it:

```python 
print(compt.compositeNumber(1,0,-1,1.5,10,4))
```

Output:

```python
[10, 4]
```
As you can see show a value of type *list*, homewer, if only there were only exclusive a single composed numbers, then it will show the primitive *int* value.

```python
print(compt.compositeNumber(12,3,17,23))
 ```

Output:

```python
12
 ```
In case of that all the value do not a composed number, then will returns **False**.

```python
import evprim.composite as compt

print(compt.compositeNumber(101,89,23,17))
 ```

Output:

```python
False
 ```
<span id = "even"></span>

## Running even ⚙️

List of functions:

* <a href = "#isaeve">isaeven</a>

* <a href = "#odd">isaodd</a>

<span id = "isaeve"></span>

#### isaeven🔩

Emits a **True** if the entered value is an even number.

```python 
import evprim.even as eve

print(eve.isaeven(10))
```
Output:

```python 
True
```
Otherwise will emits a **False**.

```python
import evprim.even as eve

print(eve.isaeven(3))
```
Output:

```python 
False
```
The number *0* is considered an *even* number, the *negative* numbers will show a **False** and *decimals* will show an *error*.

This function is similar to the <a href = "#isacomposite">isacomposite</a> function in that they only accept one value and do not allow *multiples*, nor *lists* and *tuples*.

<span id = "odd"></span>

#### isaodd🔩

Emits a **True** if the entered value is an even number.

```python
import evprim.even as eve

print(eve.isaodd(3))
```
Output:

```python 
True
```

Otherwise will emits a **False**.

```python
import evprim.even as eve

print(eve.isaodd(3))
```
Output:

```python 
False
```
In a few words, is the counterpart of the <a href = "#isaeve">isaeven</a> function.

<span id = "prime"></span>

## Running prime ⚙️

List of functions:

* <a href = "#isaprime">isaprime</a>

* <a href = "#lituprime">lituPrime</a>

* <a href = "#groupPrime">groupPrime</a>

<span id = "isaprime"></span>

#### isaprime🔩

Emits a **True** if the entered value is an odd number.

```python
import evprim.prime as pri

print(pri.isaprime(3))
```
Output:

```python 
True
```

Otherwise will emits a **False**.

```python
import evprim.prime as pri

print(pri.isaprime(1))
```
Output:

```python 
False
```
The numbers *0*, *1* and negative will emit a **False** and decimals numbers will show an error. This function only supports an only value.

Is the counterpart of the <a href = "#isacomposite">isacomposite</a> function.

<span id = "lituprime"></span>

### lituPrime 🔩

From a list or *tuple*, it "loops" and "ejects" numbers that are not composite.

```python
import evprim.prime as pri

print(pri.lituPrime([0,1,3,11,-1,3.5]))
```

Output:

```python
[3, 11]
```

In case no number is composed, it will just throw an empty *list/tuple*. 

***lituComposite*** will not accept data other than *list/tuple*, even if it's just a lone integer number. 

This function Is the counterpart of <a href = "#complitu">lituComposite</a>

<span id = "groupPrime"></span>

### groupPrime 🔩

It allows to receive multiple *int* values, if some value is not a prime number then it will not return them.

```python 
import evprim.prime as pri

print(pri.groupPrime(1,0,-1,3,3.5,11))
```

Output:

```python
[3, 11]
```

As you can see it show a value of type *list*, however, if there were only a prime only number, then will show it the value *int* primitive.

```python
import evprim.prime as pri

print(pri.groupPrime(11))
```
Output:

```python 
11
```
In case all values are not a prime number then it will return **False**.

```python 
import evprim.prime as pri

print(pri.groupPrime(4,1,6))
```

Output:

```python
False
```

This function is the counterpart of the <a href = "#compnumber">compositeNumber</a> function.

Note: the tuples have faults.

## Licence 📄

Copyright (c) 2020 Moisés Marín

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Comments 🎁

Well this is the end of the documentation, it is a small project I wanted to do as pure hobby, so it is too simple, I hope you like it.

I have less than a year learning to use python, I am very beginner in this, if you can give me advice or recommendation I would appreciate it. :)

<a href = "#subir">Go back up</a># evprim
