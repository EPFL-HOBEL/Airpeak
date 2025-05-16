# Airpeak
//TODO add badges
A Python package for air quality data processing

## Installation

Go inside the root directory of this package (where pyproject.toml is) and run this command :

```bash
pip install .
```

## Documentation
You can either read online documentation from this [link](https://epfl-hobel.github.io/Airpeak/).

Or follow these steps and build them locally :

1. Clone this repository on your machine :
   ```bash
   git clone git@github.com:EPFL-HOBEL/Airpeak.git
   ```

2. Go inside the root directory of this package (where pyproject.toml is) and run this command :
   ```bash
   pip install .[docs]
   ```
3. Run from root directory
    ```bash
    make -C docs html
    ```

4. Open [docs/build/html/index.html](docs/build/html/index.html) with your favorite browser.
