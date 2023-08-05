# rem-calc

![GitHub](https://img.shields.io/github/license/KurzGedanke/rem-calc)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rem-calc)
![PyPI](https://img.shields.io/pypi/v/rem-calc)

rem-calc helps you to calculate rem values based on pixel values. It has an *interactive* and *calculate* mode. 
The `interactive` mode is useful if you need to convert a lot of values, the `calcualte` mode should be used for single 
values.

## Install

```bash
pip install rem-calc
```

## Usage

### Printing Help

```bash
$ rem-calc
Usage: rem-calc.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  calculate
  interactive
```
### Single Rem Calculation

```bash
$ rem-calc calculate --base 16 --target 20
1.25rem
```

### Single Pixel Calculation

```bash
$ rem-calc inverse --base 16 --rem 2.75
44px
```

### Interactive Value Calculation 

```bash
$ rem-calc interactive --base 16
Enter target pixel:
20
1.25rem
Enter target pixel:
40
2.5rem
Enter target pixel:
^C
Aborted!
```