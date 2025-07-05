[![Actively Maintained](https://img.shields.io/badge/Maintenance%20Level-Actively%20Maintained-green.svg)](https://gist.github.com/cheerfulstoic/d107229326a01ff0f333a1d3476e068d)

# unicode-writer

**unicode-writer** is a lightweight background program that enables you to easily type Unicode characters using a standard ASCII keyboard.  
It works by intercepting key combinations and translating them into Unicode codepoints, symbols, or letters, depending on your selected input mode.

## Features

- **Type any Unicode character** from a basic keyboard layout
-  **Customizable modifier keys** (e.g. `CtrlR+Insert`, `Alt+Ctrl+K`)
- Multiple input modes (`numpad`, `letter`, `hex`, `base64`)
- Designed with support for non-US keyboard layouts
- Smart key handling to avoid clashes with OS-level shortcuts
- Easily editable config files (JSON)

## Compatibility
🟩 (Works perfectly); 🟨 (Untested); 🟧 (Some Issues); 🟥 (Unusable)

| OS                       | UX & README instructions | Tests | More Complex Functionalities |
|--------------------------|--------------------------|-------|------------------------------|
| Windows                  | 🟩                       | 🟩    | 🟩                           |
| MacOS                    | 🟨                       | 🟩    | 🟨                           |
| Linux (Ubuntu 22.04 LTS) | 🟩                       | 🟩    | 🟨                           |

## Contributing

We welcome contributions! Please see our [contributing guidelines](https://github.com/adalfarus/unicode-writer/blob/main/CONTRIBUTING.md) for more details on how you can contribute to unicode-writer.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## License

unicode-writer is licensed under the GPL-3.0 License - see the [LICENSE](https://github.com/adalfarus/unicode-writer/blob/main/LICENSE) file for details.
