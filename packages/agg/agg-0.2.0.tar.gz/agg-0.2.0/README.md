# Agg

![Supported Python Versions](https://img.shields.io/pypi/pyversions/agg)
![Last commit](https://img.shields.io/github/last-commit/RuedigerVoigt/agg)
![pypi version](https://img.shields.io/pypi/v/agg)

A Python library to aggregate files and data. This release supports merging two or more csv files.

## Documentation

```python
merge_csv(files_to_merge: tuple,
          output_file: Union[str, pathlib.Path],
          first_line_is_header: Optional[bool] = None) -> dict:
```

The method `merge_csv` merges multiple CSV files in the order they are specified. It will overwrite any existing file with the same name.

Parameters:
* `files_to_merge`: A tuple containing paths to a files in the order they are to be merged.
* `output_file`: The path to the result file. The folder must already exist. An existing file with the same name will be overwritten.
* `first_line_is_header`: if True agg will remove the first line of all csv files except for the first. If not set agg will guess if the first line is a header or not.

Its return value is a dictionary containing:
* a SHA256 hash of the result file,
* its absolute path,
* a boolean indicating whether the first line is a header or not,
* its size in bytes,
* its number of lines (including the header),
* a list of the files merged (absolute path).

### Example

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import agg

# tuples are ordered:
my_files = ('file_01.csv', 'file_02.csv')

# Merge the CSV-files - in the order specified by the tuple - into a new file
# called "merged_file". Meanwhile copy the header / first line only once from
# first file.
merged_file = agg.merge_csv(my_files, 'merged_file', True)
# The return value is a dictionary!


print(merged_file)

# {'sha256hash': 'fff30942d3d042c5128062d1a29b2c50494c3d1d033749a58268d2e687fc98c6',
#  'file_path': '/home/exampleuser/merged_file',
#  'first_line_is_header': True,
#  'file_size_bytes': 76,
#  'line_count': 8,
#  'merged_files': ['/home/exampleuser/file_01.csv',
#                  '/home/exampleuser/file_02.csv']
# }

print(merged_file['file_path'])
# '/home/exampleuser/merged_file'
```
