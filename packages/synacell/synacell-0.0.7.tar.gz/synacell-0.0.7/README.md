# SynaCell

Synapses and cells.

Spiking neural network (SNN) consisted of cells with processing algorithms, connected by synapses with realistic signal transmission properties. The engine that runs the SNN is written in plain C++ with interface in Python, for simplicity and platform mobility.

## Tests

We implemented test scripts as a module. You can run them by running the following commands from python console after installing the `synacell` library:

```python
import synacell.test as sctest
sctest.run_all()
```

**Warning:** The script generates temporary files in the directory from where you run the python console.

Tests that will run when running `sctest.run_all()` are the test functions from the modules:

- `test_simple`
- `test_plot`

## Examples

### example_spice

Compare results with LTSpice output. The goal is to validate the solution of the differential equation describing the synapse or cell circuit. Submodules are:

- `example_spice`
- `example_part`

#### SynaRPC

Compare the difference between the spice model of the SynaRPC circuit and the synacell model. Run the example:

```python
import synacell.examples as scex
scex.run_spice("SynaRPC")
```

Example produces files in the working directory (where you run python from).
- SynaRPC.wav - WAV file for the synacell
- SynaRPC.raw - Spice file that can be runned from python's LTSpice
- SynaRPC.asc - Spice file that can be openned from LTSpice and examine or modify the circuit.
- SynaRPC.pwl - Input file for the spice model, produced by synacell.

### example_part

Watch output from different parts.

#### CellEMA

Watch the cell output (vo) that performs Exponential Moving Average from its input (vi). Run the example:

```python
import synacell.examples as scex
scex.run_part("CellEMA")
```

#### CellMultiData

Loading of multiple files into single `CellMultiData` neuron and using the cell as validator and error computing cell:

```python
import synacell.examples as scex
scex.run_part("CellMultiData")
```

## Requirements

For now, we compiled the C++ software as a Windows shared library (.dll) for 64-bit architectures. We set the official PyPI package for:

* Windows 64bit
* Python 3.7+ 64bit

If you plan to compile the c++ by yourself, check the file: [HOWTO.md](HOWTO.md)
