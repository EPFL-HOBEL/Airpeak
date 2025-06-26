![GitHub License](https://img.shields.io/github/license/EPFL-HOBEL/Airpeak)
[![Dev Documentation](https://img.shields.io/badge/docs-dev-blue.svg)](https://epfl-hobel.github.io/Airpeak)

# Airpeak
A Python package for recognizing build-up and decay events from pollutant concentration data and estimating pollutant loss rates.

## Installation

1. Clone this repository on your machine :
   ```bash
   git clone git@github.com:EPFL-HOBEL/Airpeak.git
   ```


2. Go inside the root directory of this package (where pyproject.toml is) and run this command :

   ```bash
   pip install .
   ```

## Documentation
You can either read online documentation from this [link](https://epfl-hobel.github.io/Airpeak/).

Or follow these steps and build them locally :

1. Go inside the root directory of this package (where pyproject.toml is) and run this command :
   ```bash
   pip install .[docs]
   ```
2. Run from root directory
    ```bash
    make -C docs html
    ```

3. Open [docs/build/html/index.html](docs/build/html/index.html) with your favorite browser.
