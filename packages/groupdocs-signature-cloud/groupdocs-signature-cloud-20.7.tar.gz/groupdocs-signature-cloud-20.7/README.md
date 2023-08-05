# GroupDocs.Signature Cloud Python SDK
Python package for communicating with the GroupDocs.Signature Cloud API

## Requirements

Python 2.7 or 3.4+

## Installation
Install `groupdocs-signature-cloud` with [PIP](https://pypi.org/project/pip/) from [PyPI](https://pypi.org/) by:

```sh
pip install groupdocs-signature-cloud
```

Or clone repository and install it via [Setuptools](http://pypi.python.org/pypi/setuptools): 

```sh
python setup.py install
```

## Getting Started

Please follow the [installation procedure](#installation) and then run following:

```python
# Import module
import groupdocs_signature_cloud

# Get your app_sid and app_key at https://dashboard.groupdocs.cloud (free registration is required).
app_sid = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
app_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Create instance of the API
api = groupdocs_signature_cloud.InfoApi.from_keys(app_sid, app_key)

try:
    # Retrieve supported file-formats
    response = api.get_supported_file_formats()

    # Print out supported file-formats
    print("Supported file-formats:")
    for format in response.formats:
        print('{0} ({1})'.format(format.file_format, format.extension)) 
except groupdocs_signature_cloud.ApiException as e:
    print("Exception when calling get_supported_file_formats: {0}".format(e.message))
```

## Licensing
GroupDocs.Signature Cloud Python SDK licensed under [MIT License](http://github.com/groupdocs-signature-cloud/groupdocs-signature-cloud-python/LICENSE).

## Resources
+ [**Website**](https://www.groupdocs.cloud)
+ [**Product Home**](https://products.groupdocs.cloud/signature)
+ [**Documentation**](https://wiki.groupdocs.cloud/display/signaturecloud/Home)
+ [**Free Support Forum**](https://forum.groupdocs.cloud/c/signature)
+ [**Blog**](https://blog.groupdocs.cloud/category/signature)

## Contact Us
Your feedback is very important to us. Please feel free to contact us using our [Support Forums](https://forum.groupdocs.cloud/c/signature).