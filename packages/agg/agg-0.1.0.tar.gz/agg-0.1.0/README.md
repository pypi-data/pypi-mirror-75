# Agg

![Supported Python Versions](https://img.shields.io/pypi/pyversions/agg)
![Last commit](https://img.shields.io/github/last-commit/RuedigerVoigt/agg)
![pypi version](https://img.shields.io/pypi/v/agg)

## Example

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import agg

# tuples are ordered:
my_files = ('file_01.csv', 'file_02.csv')

# Merge the CSV-files - in the specified order - into a new file called
# "merged_file". Meanwhile copy the header / first line only once from
# first file
agg.merge_csv(my_files, 'merged_file', True)

```
