# naive-stopwords
Stop words for Chinese.


## Installation

```bash
pip install -U naive-stopwords
```

## Usage

```python
from naive_stopwords import Stopwords

sw = Stopwords()

print(sw.size())
print(sw.contains('hello'))

sw.add('的')
print(sw.size())
print(sw.contains('的'))

sw.remove('的')
print(sw.size())
print(sw.contains('的'))

```
