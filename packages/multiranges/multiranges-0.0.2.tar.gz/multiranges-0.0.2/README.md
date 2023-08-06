# multiranges

MultiRanges generate (lazy) tuples as a cartesian product starting from ranges, tuples, strings, sets and nested MultiRanges 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install multiranges.
```shell script
pip install multiranges
```

## Usage  
This idea was born from a proyect I had which required a large amount of data mixing objects.  

```python
from multiranges.multiranges import MultiRange
mr = MultiRange(2, 3)  # Combines range(2) and range(3)
values = list(mr)
# values = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]

list(MultiRange(10))  # Acts like normal range(10)
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

list(MultiRange('test', (1, 2, 3, 5, 8))


[('t', 1), ('t', 2), ('t', 3), ('t', 5), ('t', 8), ('e', 1), ('e', 2), ('e', 3), ('e', 5), ('e', 8), ('s', 1), 
 ('s', 2), ('s', 3), ('s', 5), ('s', 8), ('t', 1), ('t', 2), ('t', 3), ('t', 5), ('t', 8)]
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what do you suggest.

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)