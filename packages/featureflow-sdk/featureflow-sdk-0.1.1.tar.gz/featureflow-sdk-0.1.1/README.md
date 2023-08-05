# featureflow-python-sdk
[![][dependency-img]][dependency-url]

> Python SDK for the featureflow feature management platform

Get your Featureflow account at [featureflow.io](http://www.featureflow.io)

## Get Started

The easiest way to get started is to follow the [Featureflow quick start guides](http://docs.featureflow.io/docs)


## Installation
The SDK is available on ![pypi][pypi-url].

You can either add it as a dependency or install it globally.

```
python -m pip install featureflow
```

## Usage
Here is a simple example of running your feature that prints "I'm enables" on the screen.
```python
api_key = "<your-javascript-environment-sdk-key>"

def evaluate_my_feature(user):
        featureflow = Featureflow.init(api_key)

        if featureflow.evaluate(:'some-cool-feature', user).isOn():
            maybe_evaluate_my_feature()
            print("Feature evaluated")
```

[py-url]: https://pypi.org/project/featureflow/
[dependency-url]: https://www.featureflow.io
[dependency-img]: https://www.featureflow.io/wp-content/uploads/2016/12/featureflow-web.png

