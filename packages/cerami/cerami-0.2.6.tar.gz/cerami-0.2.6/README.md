# Cerami

Cerami is a python library that hopefully provides some sanity to boto3's DynamoDB client. Its intended use is as a library to help define table data through the creation of models and create sane, readable, and reproducable DynamoDB requests.

**Please read the [Full Documentation](https://cerami.readthedocs.io/en/latest/).**

## Quickstart
```
python3 -m pip install cerami
```

```python
import boto3
from cerami import Cerami
from cerami.datatype import String
from cerami.decorators import primary_key

dynamodb = boto3.client('dynamodb')
db = Cerami(dynamodb)

# Configure a Model
@primary_key('title')
class Book(db.Model):
    __tablename__ = "Books"
    title = String()
    author = String()

Book.scan.filter(Book.author.eq("Dav Pilkey")).execute()
```
