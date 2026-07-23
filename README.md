<div align="center">

# 🎤 Multi Engine
**A Universal Friday Night Funkin' Multi-Engine Mod Manager & Launcher**

![Version](https://img.shields.io/badge/version-1.3.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

[About](#-about) • [Features](#-features) • [Folder Structure](#-folder-structure)

---

</div>

## 📌 About

**ExtraLauncher** is a universal mod manager and launcher for **Friday Night Funkin'**. Designed to streamline the modding experience, it allows you to effortlessly manage, enable/disable, and launch mods across multiple game engines such as **Psych Engine**, **V-Slice**, and **Codename Engine** without the hassle of manually moving files around.

Simply pick your engine, select your mod, and press **Play**!

---

## ✨ Features

* 🎮 **Multi-Engine Support:** Built-in integration for Psych Engine, V-Slice, and Codename Engine.
* 📂 **Centralized Data Management:** All mods and executables are safely organized inside a single `data/` directory.
* ➕ **One-Click Mod Import & Deletion:** Add new mod folders or delete existing ones directly through the GUI.
* 🔄 **Smart Mod Toggle:** Enable or disable mods instantly (supports Psych Engine's `modsList.txt` synchronization).
* 🌐 **Bilingual Interface:** Real-time language switching between **English** and **Portuguese (Brazil)**.
* 🎨 **Theme Switcher:** Seamlessly toggle between Dark Mode and Light Mode.
* 🏷️ **Metadata Detection:** Automatically reads `_polymod_meta.json` to display mod versions.
* ⚠️ **Outdated Version Check:** Integrated banner alert to keep you notified of new launcher updates.

---

## 📂 Folder Structure

To ensure ExtraLauncher operates smoothly, organize your project files as follows:

```text
FNF Multi-Engine/
├── FNF Multi-Engine.exe (or launcher.py)
└── data/
    ├── mods_folder/
    │   ├── MyAwesomeMod/
    └── executables_mods/
        ├── PsychEngine.exe
        └── VSlice.exe
