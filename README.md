<h1>
  <a href="https://trendshift.io/repositories/19699"><img align="right" src="https://trendshift.io/api/badge/repositories/19699" alt="Final2x on Trendshift" width="200" height="44" /></a>
  Final2x
</h1>

![MacOS](https://img.shields.io/badge/Support-MacOS-blue?logo=Apple&style=flat-square)
![Windows](https://img.shields.io/badge/Support-Windows-blue?logo=Windows&style=flat-square)
![Linux](https://img.shields.io/badge/Support-Linux-blue?logo=Linux&style=flat-square)
[![CI-test](https://github.com/EutropicAI/Final2x/actions/workflows/CI-test.yml/badge.svg)](https://github.com/EutropicAI/Final2x/actions/workflows/CI-test.yml)
[![CI-test-core](https://github.com/EutropicAI/Final2x/actions/workflows/CI-test-core.yml/badge.svg)](https://github.com/EutropicAI/Final2x/actions/workflows/CI-test-core.yml)
[![CI-build](https://github.com/EutropicAI/Final2x/actions/workflows/CI-build.yml/badge.svg)](https://github.com/EutropicAI/Final2x/actions/workflows/CI-build.yml)
[![Release](https://github.com/EutropicAI/Final2x/actions/workflows/Release.yml/badge.svg)](https://github.com/EutropicAI/Final2x/actions/workflows/Release.yml)
![Download](https://img.shields.io/github/downloads/EutropicAI/Final2x/total)
![GitHub](https://img.shields.io/github/license/EutropicAI/Final2x)

A cross-platform image super-resolution tool for Windows, macOS, and Linux.

Use built-in models or load your own. See the [custom model demo](https://github.com/EutropicAI/cccv_demo_remote_model) to get started.

## 🖼️ Screenshots

<div align=center>
<img width="40%" alt="image" src="https://github.com/user-attachments/assets/37f6d444-766b-4c28-b64a-018f78ae1f35" />
<img width="40%" alt="image" src="https://github.com/user-attachments/assets/3f86e693-f667-48fd-8830-0d96fb5229d2" />
</div>

## 📦 Installation

[Download the latest release](https://github.com/EutropicAI/Final2x/releases) for your platform.

### 🪟 Windows

Install from the release page, or use a package manager such as winget or Scoop. Package manager versions may lag behind the latest release.

### 🍎 macOS

If macOS blocks the app on first launch, run the following command in Terminal after placing it in `/Applications`:

```bash
xattr -cr /Applications/Final2x.app
```

### 🐧 Linux

Install Python >= 3.9 and PyTorch >= 2.0, then install the backend and required system libraries. On Debian or Ubuntu:

```bash
pip install Final2x-core
Final2x-core -h # Verify the backend installation
sudo apt install -y libomp5 xdg-utils
```

## 🧩 References

The Python CLI and desktop backend live in [`core`](./core) and share the desktop app's version number.

This project builds on the following open-source projects:

- [cccv](https://github.com/EutropicAI/cccv) — image restoration and super-resolution backend
- [naive-ui](https://github.com/tusen-ai/naive-ui)
- [electron-vite](https://github.com/alex8088/electron-vite)

## 📄 License

This project is licensed under the BSD 3-Clause - see
the [LICENSE file](./LICENSE) for details.

## 💙 Acknowledgements

Feel free to reach out to the project maintainers with any questions or concerns~
