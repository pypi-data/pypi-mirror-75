# Qutie

Yet another pythonic UI library for rapid prototyping using PyQt5.

## Quick start

```python
import qutie as ui

app = ui.Application()
window = ui.Widget(
    title="Example",
    icon='orange',
    width=320,
    height=240,
    layout=ui.Column(
        ui.Label("Hello world!", color='blue'),
        ui.Row(
            ui.Button("Go!", clicked=lambda: ui.show_info(text="Hello world!")),
            ui.Button("Quit", clicked=app.quit)
        )
    )
)
window.show()
app.run()
```

## Documentation

Qutie (pronounced as _cutie_) provides a simple and easy to use pythonic
interface to PyQt5.

### Install

```bash
pip install qutie
```

### Application

A single `Application` object must be created before other widgets. To make use
of the event system the application event loop must be executed.

```python
import qutie as ui

# Create an application object.
app = ui.Application(name='app', version='1.0')

# Create a window.
window = ui.MainWindow()
window.resize(800, 600)
window.show()

# Run the event loop.
app.run()
```

### Widgets

Any widget can be a top level window or part of another widget using the
`layout` property. All properties can be assigned using the constructor.

```python
window = ui.Widget(title="Example", width=320, height=240)
```

To make a top level window visible use property `visible` or call method
`show()`.

```python
window.show()
window.visible = True # equivalent to show
```

### Layouts

The simplified layout system provides a horizontal `Row` and a vertical `Column`
box. Items can be added while constructing the layout or using list like methods
`append` and `insert`. The consumed space of every child widget can be adjusted
using the `stretch` attribute.

```python
window.layout = ui.Row(
    ui.Column(
        ...
    ),
    ui.Column(
        ui.Row(...),
        ui.Row(...),
        ui.Row(...),
        stretch=(1, 0, 0)
    ),
    stretch=(2, 3)
)
```

### Inputs

```python
# Single line text input
text = ui.Text(value="spam")
# Numeric input
number = ui.Number(value=4, minimum=0, maximum=10, step=1.0, decimals=1)
# A multi line text area
textarea = ui.TextArea(value="Lorem ipsum et dolor.")
```

### Events

Events provide a simplified interface to Qt's signal and slot system. Events can
be emitted from any class inheriting from `Object` by calling method `emit()`.

```python
# Use any callable class attribute as event callback.
window.issue_call = lambda: print("Call to action!")
# Emit an event executing attribute `issue_call` (if callable).
window.emit('issue_call')
```

Events can also propagate positional and keyword arguments.

```python
# Use any callable class attribute as event callback.
window.update_progress = lambda a, b: print(f"Progress: {a} of {b}")
# Emit an event executing attribute `update_progress` (if callable).
window.emit('update_progress', 42, 100)
```

Many widgets provide predefined events.

```python
# Assigning callback functions
ui.Number(value=4, changed=on_change, editing_finished=on_edited)
```

### Timers

Call repeating or delayed events using timers.

```python
timer = ui.Timer(interval=1.0, timeout=lambda: print("Done!"))
timer.start()
```

Function `single_shot` exposes a convenient single shot timer.

```python
ui.single_shot(interval=1.0, timeout=lambda: print("Done!"))
```

Note that timer events are only processed when running the application event
loop.

### Settings

Persistent settings can be stored/restored using a `Settings` object as context
manager. It provides application wide settings as a JSON dictionary.

```python
with ui.Settings() as settings:
    value = settings.get('key', 'default')
    settings['key'] = value
```

Use attribute `filename` to inspect the persistent JSON data.

```python
>>> ui.Settings().filename
'/home/user/.config/app.qutie'
```

### Workers

The `Worker` class provides a convenient way to work with background threads.
Use attribute `target` to assign the function to be executed in the background.

```python
def calculate(worker):
    for i in range(100):
        ...

worker = ui.Worker(target=calculate)
worker.start()
```

**Important:** use only the event system to propagate information from inside
the worker. Do not access widgets from within the worker function.

```python
def calculate(worker):
    for i in range(100):
        # Emit custom events.
        worker.emit('progress', i, 100)
        worker.emit('message', "All ok...")

worker = ui.Worker(target=calculate)
# Assign custom event callbacks.
worker.progress = lambda step, max: print(f"progress: {step}/{max}")
worker.message = lambda msg: print(f"message: {msg}")
worker.start()
```

To control worker lifetime use method `stop()` and attribute `stopping`.

```python
def calculate(worker):
    while not worker.stopping:
        ...

worker = ui.Worker(target=calculate)
worker.start()
...
worker.stop()
```

To wait for a worker to actually stop use method `join()`.

```python
worker.stop()
worker.join()
```

#### Example

A simple dialog with progress bar running a calculation in the background.

```python
import random
import time

import qutie as ui

class Dialog(ui.Dialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Create worker
        self.worker = ui.Worker(target=self.calculate)
        self.worker.finished = self.close
        self.worker.update_progress = self.update_progress
        # Create layout
        self.progress_bar = ui.ProgressBar()
        self.layout = self.progress_bar

    def run(self):
        # Start, stop and join worker
        self.worker.start()
        super().run()
        self.worker.stop()
        self.worker.join()

    def update_progress(self, value, maximum):
        self.progress_bar.maximum = maximum
        self.progress_bar.value = value

    def calculate(self, worker):
        n = 32
        for i in range(n):
            if worker.stopping:
                break
            # Emit custom event
            worker.emit('update_progress', i, n)
            time.sleep(random.random())

app = ui.Application()

dialog = Dialog(title="Worker")
dialog.run()
```
