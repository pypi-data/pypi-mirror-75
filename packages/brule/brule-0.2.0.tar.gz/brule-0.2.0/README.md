# Dr. Steve Brule Name Generator

Simple module that generates names that even Dr. Steve Brule could say correctly ([example of Dr. Brule on YouTube](https://www.youtube.com/watch?v=02iIN4n4y0A))

I thought it'd be fun to make my own Python package and publish it to PyPi, so this is the result

It's kinda handy for making dummy data or other random usecases when you need a list of names

## Installation

```
pip install brule
```

## Usage

```python
>>> import brule as b
>>> 
>>> # random name
>>> b.full_name()
'Franky Rangus'
>>> 
>>> # generate based on a name
>>> b.full_name('Steve', 'Brule', 'male')
'Stevie Bringus'
```

## Help

```python
>>> import brule as b
>>> 
>>> # use built-in `help` utility
>>> help(b.full_name)
>>> help(b.first_name)
>>> help(b.last_name)
```