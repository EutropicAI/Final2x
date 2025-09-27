# Final2x

<div align="center">
<img src="./resources/icon.png" width="30%"/>
</div>

![MacOS](https://img.shields.io/badge/Support-MacOS-blue?logo=Apple&style=flat-square)
![Windows](https://img.shields.io/badge/Support-Windows-blue?logo=Windows&style=flat-square)
![Linux](https://img.shields.io/badge/Support-Linux-blue?logo=Linux&style=flat-square)
[![CI-test](https://github.com/EutropicAI/Final2x/actions/workflows/CI-test.yml/badge.svg)](https://github.com/EutropicAI/Final2x/actions/workflows/CI-test.yml)
[![CI-build](https://github.com/EutropicAI/Final2x/actions/workflows/CI-build.yml/badge.svg)](https://github.com/EutropicAI/Final2x/actions/workflows/CI-build.yml)
[![Release](https://github.com/EutropicAI/Final2x/actions/workflows/Release.yml/badge.svg)](https://github.com/EutropicAI/Final2x/actions/workflows/Release.yml)
![Download](https://img.shields.io/github/downloads/EutropicAI/Final2x/total)
![GitHub](https://img.shields.io/github/license/EutropicAI/Final2x)

A cross-platform image super-resolution tool.

- News🎉: Enhance a video? Try [VSET](https://github.com/EutropicAI/VSET)!
- News🎉: Final2x v3.0.0 is now available, support Nvidia 50 series GPUs now!

### Screenshots

<div align=center>
<img width="40%" alt="image" src="https://github.com/user-attachments/assets/37f6d444-766b-4c28-b64a-018f78ae1f35" />
<img width="40%" alt="image" src="https://github.com/user-attachments/assets/c6a278c0-bf11-46a7-9dcc-e5fe97ccc71c" />
</div>

### Installation

##### [Download the latest release from here.](https://github.com/EutropicAI/Final2x/releases)

#### Windows

You can also use a package manager like winget or scoop to install and upgrade. Please note that the versions available through package managers may not always be the latest.

#### MacOS

```bash
sudo spctl --master-disable
# Disable Gatekeeper, then allow applications downloaded from anywhere in System Preferences > Security & Privacy > General
xattr -cr /Applications/Final2x.app
```

In first time, you need to run the command above in terminal to allow the app to run.

#### Linux

For Linux User, you need to install the dependencies first.

Make sure you have Python >= 3.9 and PyTorch >= 1.13 installed

```bash
pip install Final2x-core
Final2x-core -h # check if the installation is successful
apt install -y libomp5 xdg-utils
```

### Reference

The following references were referenced in the development of this project:

- [Final2x-core](https://github.com/EutropicAI/Final2x-core)
- [naive-ui](https://github.com/tusen-ai/naive-ui)
- [electron-vite](https://github.com/alex8088/electron-vite)

### License

This project is licensed under the BSD 3-Clause - see
the [LICENSE file](./LICENSE) for details.

### Acknowledgements

Feel free to reach out to the project maintainers with any questions or concerns~

<a href="https://star-history.com/#EutropicAI/Final2x&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=EutropicAI/Final2x&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=EutropicAI/Final2x&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=EutropicAI/Final2x&type=Date" />
  </picture>
</a>
