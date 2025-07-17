![GitHub License](https://img.shields.io/github/license/EPFL-HOBEL/Airpeak) <!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)<!-- ALL-CONTRIBUTORS-BADGE:END --> [![Dev Documentation](https://img.shields.io/badge/docs-dev-blue.svg)](https://epfl-hobel.github.io/Airpeak) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15745122.svg)](https://doi.org/10.5281/zenodo.15745122)

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

## Reference
1. Du, B., & Siegel, J. A. (2023). Estimating indoor pollutant loss using mass balances and unsupervised clustering to recognize decays. Environmental Science & Technology, 57(27), 10030-10038. https://doi.org/10.1021/acs.est.3c00756

2. Du, B., Reda, I., Licina, D., Kapsis, C., Qi, D., Candanedo, J. A., & Li, T. (2024). Estimating Air Change Rate in Mechanically Ventilated Classrooms Using a Single CO2 Sensor and Automated Data Segmentation. Environmental science & technology, 58(42), 18788-18799. https://doi.org/10.1021/acs.est.4c02797

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Botato12"><img src="https://avatars.githubusercontent.com/u/46970733?v=4?s=100" width="100px;" alt="Bowen Du"/><br /><sub><b>Bowen Du</b></sub></a><br /><a href="https://github.com/EPFL-HOBEL/Airpeak/commits?author=Botato12" title="Code">💻</a> <a href="#data-Botato12" title="Data">🔣</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/QuentinEschmann"><img src="https://avatars.githubusercontent.com/u/86717822?v=4?s=100" width="100px;" alt="Quentin Eschmann"/><br /><sub><b>Quentin Eschmann</b></sub></a><br /><a href="https://github.com/EPFL-HOBEL/Airpeak/commits?author=QuentinEschmann" title="Code">💻</a> <a href="https://github.com/EPFL-HOBEL/Airpeak/commits?author=QuentinEschmann" title="Documentation">📖</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
