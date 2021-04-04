
__version__ = '0.0.1'
__author__ = 'Jeff Maxey'
__email__ = 'jeffmaxey@comcast.net'

__doc__ = '''
datastore is a generic layer of abstraction for data store and database access.
It is a **simple** API with the aim to enable application development in a
datastore-agnostic way, allowing datastores to be swapped seamlessly without
changing application code. Thus, one can leverage different datastores with
different strengths without committing the application to one datastore
throughout its lifetime.
'''

import key
from key import Key
from key import Namespace

import base
from base import Datastore
from base import NullDatastore
from base import DictDatastore
from base import InterfaceMappingDatastore

from base import ShimDatastore
from base import CacheShimDatastore
from base import LoggingDatastore
from base import KeyTransformDatastore
from base import LowercaseKeyDatastore
from base import NamespaceDatastore
from base import NestedPathDatastore
from base import SymlinkDatastore
from base import DirectoryTreeDatastore
from base import DirectoryDatastore

from base import DatastoreCollection
from base import ShardedDatastore
from base import TieredDatastore

import query
from query import Query
from query import Cursor

import serialize
from serialize import SerializerShimDatastore


# patch datastore with core variables
import datastore
datastore.__version__ = __version__
datastore.__author__ = __author__
datastore.__email__ = __email__

for k, v in locals().items():
  if k in ['datastore']:
    continue

  if k.startswith('__'):
    continue

  if hasattr(datastore, k):
    continue

  setattr(datastore, k, v)
