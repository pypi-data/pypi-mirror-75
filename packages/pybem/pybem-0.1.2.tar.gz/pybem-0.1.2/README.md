# PyBEM

[![Build Status](https://travis-ci.com/knaydenov/pybem.svg?branch=master)](https://travis-ci.com/knaydenov/pybem)

This package provides helpers for BEM classes generation.

## Usage

Injecting into a Flask template:

```python
from pybem import Block

@app.context_processor
def inject_bem():
    return dict(b=Block)
```

Template:

```jinja2
<div class="{{ b('block').m('color', 'red') }}">
    <div class="{{ b('block').e('element').m('hidden').add_class('no-js') }}"></div>
</div>
```

Output:

```html
<div class="block block--color_red">
    <div class="block__element block__element--hidden no-js"></div>
</div>
```