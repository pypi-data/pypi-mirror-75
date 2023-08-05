# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parquet_tools',
 'parquet_tools.commands',
 'parquet_tools.gen_py',
 'parquet_tools.gen_py.parquet',
 'parquet_tools.parquet']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.13.25,<2.0.0',
 'colorama>=0.4.3,<0.5.0',
 'halo>=0.0.29,<0.0.30',
 'pandas>=1.0.4,<2.0.0',
 'pyarrow>=0.17.1,<0.18.0',
 'tabulate>=0.8.7,<0.9.0',
 'thrift>=0.13.0,<0.14.0']

entry_points = \
{'console_scripts': ['parquet-tools = parquet_tools.cli:main']}

setup_kwargs = {
    'name': 'parquet-tools',
    'version': '0.2.4',
    'description': 'Easy install parquet-tools',
    'long_description': '# parquet-tools\n\n![Run Unittest](https://github.com/ktrueda/parquet-tools/workflows/Run%20Unittest/badge.svg)\n![Run CLI test](https://github.com/ktrueda/parquet-tools/workflows/Run%20CLI%20test/badge.svg)\n\nThis is a pip installable [parquet-tools](https://github.com/apache/parquet-mr).\nIn other words, parquet-tools is a CLI tools of [Apache Arrow](https://github.com/apache/arrow).\nYou can show parquet file content/schema on local disk or on Amazon S3.\nIt is incompatible with original parquet-tools.\n\n## Features\n\n- Read Parquet data (local file or file on S3)\n- Read Parquet metadata/schema (local file or file on S3)\n\n## Installation\n\n```bash\n$ pip install parquet-tools\n```\n\n## Usage\n\n```bash\n$ parquet-tools --help\nusage: parquet-tools [-h] {show,csv,inspect} ...\n\nparquet CLI tools\n\npositional arguments:\n  {show,csv,inspect}\n    show              Show human readble format. see `show -h`\n    csv               Cat csv style. see `csv -h`\n    inspect           Inspect parquet file. see `inspect -h`\n\noptional arguments:\n  -h, --help          show this help message and exit\n```\n\n## Usage Examples\n\n#### Show local parquet file\n\n```bash\n$ parquet-tools show test.parquet\n+-------+-------+---------+\n|   one | two   | three   |\n|-------+-------+---------|\n|  -1   | foo   | True    |\n| nan   | bar   | False   |\n|   2.5 | baz   | True    |\n+-------+-------+---------+\n```\n\n#### Show parquet file on S3\n\n```bash\n$ parquet-tools show s3://bucket-name/prefix/*\n+-------+-------+---------+\n|   one | two   | three   |\n|-------+-------+---------|\n|  -1   | foo   | True    |\n| nan   | bar   | False   |\n|   2.5 | baz   | True    |\n+-------+-------+---------+\n```\n\n\n#### Inspect parquet file schema\n\n```bash\n$ parquet-tools inspect /path/to/parquet\n```\n\n<details>\n\n<summary>Inspect output</summary>\n\n```\nFileMetaData\n■■■■version = 1\n■■■■schema = list\n■■■■■■■■SchemaElement\n■■■■■■■■■■■■name = schema\n■■■■■■■■■■■■num_children = 3\n■■■■■■■■SchemaElement\n■■■■■■■■■■■■type = 5\n■■■■■■■■■■■■repetition_type = 1\n■■■■■■■■■■■■name = one\n■■■■■■■■SchemaElement\n■■■■■■■■■■■■type = 6\n■■■■■■■■■■■■repetition_type = 1\n■■■■■■■■■■■■name = two\n■■■■■■■■■■■■logicalType = LogicalType\n■■■■■■■■■■■■■■■■STRING = StringType\n■■■■■■■■SchemaElement\n■■■■■■■■■■■■repetition_type = 1\n■■■■■■■■■■■■name = three\n■■■■num_rows = 3\n■■■■row_groups = list\n■■■■■■■■RowGroup\n■■■■■■■■■■■■columns = list\n■■■■■■■■■■■■■■■■ColumnChunk\n■■■■■■■■■■■■■■■■■■■■file_offset = 108\n■■■■■■■■■■■■■■■■■■■■meta_data = ColumnMetaData\n■■■■■■■■■■■■■■■■■■■■■■■■type = 5\n■■■■■■■■■■■■■■■■■■■■■■■■encodings = list\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■2\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■0\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■3\n■■■■■■■■■■■■■■■■■■■■■■■■path_in_schema = list\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■one\n■■■■■■■■■■■■■■■■■■■■■■■■codec = 1\n■■■■■■■■■■■■■■■■■■■■■■■■num_values = 3\n■■■■■■■■■■■■■■■■■■■■■■■■total_uncompressed_size = 100\n■■■■■■■■■■■■■■■■■■■■■■■■total_compressed_size = 104\n■■■■■■■■■■■■■■■■■■■■■■■■data_page_offset = 36\n■■■■■■■■■■■■■■■■■■■■■■■■dictionary_page_offset = 4\n■■■■■■■■■■■■■■■■■■■■■■■■statistics = Statistics\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■max = b\'\\x00\\x00\\x00\\x00\\x00\\x00\\x04@\'\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■min = b\'\\x00\\x00\\x00\\x00\\x00\\x00\\xf0\\xbf\'\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■null_count = 1\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■max_value = b\'\\x00\\x00\\x00\\x00\\x00\\x00\\x04@\'\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■min_value = b\'\\x00\\x00\\x00\\x00\\x00\\x00\\xf0\\xbf\'\n■■■■■■■■■■■■■■■■■■■■■■■■encoding_stats = list\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■PageEncodingStats\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■page_type = 2\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■encoding = 2\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■count = 1\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■PageEncodingStats\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■encoding = 2\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■count = 1\n■■■■■■■■■■■■■■■■ColumnChunk\n■■■■■■■■■■■■■■■■■■■■file_offset = 281\n■■■■■■■■■■■■■■■■■■■■meta_data = ColumnMetaData\n■■■■■■■■■■■■■■■■■■■■■■■■type = 6\n■■■■■■■■■■■■■■■■■■■■■■■■encodings = list\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■2\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■0\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■3\n■■■■■■■■■■■■■■■■■■■■■■■■path_in_schema = list\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■two\n■■■■■■■■■■■■■■■■■■■■■■■■codec = 1\n■■■■■■■■■■■■■■■■■■■■■■■■num_values = 3\n■■■■■■■■■■■■■■■■■■■■■■■■total_uncompressed_size = 76\n■■■■■■■■■■■■■■■■■■■■■■■■total_compressed_size = 80\n■■■■■■■■■■■■■■■■■■■■■■■■data_page_offset = 238\n■■■■■■■■■■■■■■■■■■■■■■■■dictionary_page_offset = 201\n■■■■■■■■■■■■■■■■■■■■■■■■statistics = Statistics\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■max_value = b\'foo\'\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■min_value = b\'bar\'\n■■■■■■■■■■■■■■■■■■■■■■■■encoding_stats = list\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■PageEncodingStats\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■page_type = 2\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■encoding = 2\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■count = 1\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■PageEncodingStats\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■encoding = 2\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■count = 1\n■■■■■■■■■■■■■■■■ColumnChunk\n■■■■■■■■■■■■■■■■■■■■file_offset = 388\n■■■■■■■■■■■■■■■■■■■■meta_data = ColumnMetaData\n■■■■■■■■■■■■■■■■■■■■■■■■encodings = list\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■0\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■3\n■■■■■■■■■■■■■■■■■■■■■■■■path_in_schema = list\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■three\n■■■■■■■■■■■■■■■■■■■■■■■■codec = 1\n■■■■■■■■■■■■■■■■■■■■■■■■num_values = 3\n■■■■■■■■■■■■■■■■■■■■■■■■total_uncompressed_size = 40\n■■■■■■■■■■■■■■■■■■■■■■■■total_compressed_size = 42\n■■■■■■■■■■■■■■■■■■■■■■■■data_page_offset = 346\n■■■■■■■■■■■■■■■■■■■■■■■■statistics = Statistics\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■max = b\'\\x01\'\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■min = b\'\\x00\'\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■max_value = b\'\\x01\'\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■min_value = b\'\\x00\'\n■■■■■■■■■■■■■■■■■■■■■■■■encoding_stats = list\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■PageEncodingStats\n■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■count = 1\n■■■■■■■■■■■■total_byte_size = 226\n■■■■■■■■■■■■num_rows = 3\n■■■■■■■■■■■■file_offset = 108\n■■■■■■■■■■■■total_compressed_size = 226\n■■■■key_value_metadata = list\n■■■■■■■■KeyValue\n■■■■■■■■■■■■key = pandas\n■■■■■■■■■■■■value = {"index_columns": [{"kind": "range", "name": null,\n■■■■■■■■KeyValue\n■■■■■■■■■■■■key = ARROW:schema\n■■■■■■■■■■■■value = /////4gDAAAQAAAAAAAKAA4ABgAFAAgACgAAAAABAwAQAAAAAA\n■■■■created_by = parquet-cpp version 1.5.1-SNAPSHOT\n■■■■column_orders = list\n■■■■■■■■ColumnOrder\n■■■■■■■■■■■■TYPE_ORDER = TypeDefinedOrder\n■■■■■■■■ColumnOrder\n■■■■■■■■■■■■TYPE_ORDER = TypeDefinedOrder\n■■■■■■■■ColumnOrder\n■■■■■■■■■■■■TYPE_ORDER = TypeDefinedOrder\n```\n</details>\n\n#### Cat CSV parquet and transform [csvq](https://github.com/mithrandie/csvq)\n\n```bash\n$ parquet-tools csv s3://bucket-name/test.parquet |csvq "select one, three where three"\n+-------+-------+\n|  one  | three |\n+-------+-------+\n| -1.0  | True  |\n| 2.5   | True  |\n+-------+-------+\n```\n',
    'author': 'Kentaro Ueda',
    'author_email': 'kentaro.ueda.kentaro@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ktrueda/parquet-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
