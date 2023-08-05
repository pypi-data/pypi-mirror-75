# lung

toy^3 lung

## Documentation

### Getting started
1. Highly recommended, but optional. Use conda
```bash
conda env create -f environment.yml
```
2. Install the `lung` package
```bash
pip install -e .
```
3. Start `jupyter` from the root repository directory
```bash
jupyter notebook
```

### How to run code

Take a look at `notebooks/Delay Lung model.ipynb`.
```python
new_controller = NewController(waveform=BreathWaveform())
```

### How to add a controller

1. Suppose our name is `NewController`
2. Create file in `lung/controller/_new_controller.py`
3. Stub of the controller:

```python
from lung.controllers.core import Controller

class NewController(Controller):
    def __init__(self, **kwargs):
        pass

    def feed(self, err, t):
        pass
```

4. Add `NewController` to `lung/controllers/__init__.py`
5. Import using `from lung.controllers import NewController`

### How to add an environment

1. Same idea as above. You've got this, Cyril! (Just watch out for `self.time`...).
