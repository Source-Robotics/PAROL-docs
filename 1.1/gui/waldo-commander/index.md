# Waldo Commander (web)

[Waldo Commander](https://github.com/Jepson2k/Waldo-Commander), by a member of the community, is a browser
interface on top of the Python API.

| It offers | |
|---|---|
| Control from any device on the network | In the browser |
| Python programs | With an editor and step-through debugging |
| A 3D simulation | To preview paths |
| Teaching by demonstration | Recorded as Python |
| A built-in MCP server | Through which an LLM can read the robot's status, write and run programs and drive the arm with your approval |
| Simulator mode | It runs without a robot |

![The web commander](https://docs.source-robotics.com/PAROL-docs/1.1/assets/Web_GUI.webp){ width="800" }

## Install and run

```
git clone https://github.com/Jepson2k/Waldo-Commander.git
cd Waldo-Commander
pip install -e ".[parol6]"
waldo-commander
```

It is built on [waldoctl](https://github.com/Jepson2k/waldoctl), the abstraction layer the Python API implements,
so what it offers tracks the API's features. Its documentation is at
[jepson2k.github.io/Waldo-Commander](https://jepson2k.github.io/Waldo-Commander/).
