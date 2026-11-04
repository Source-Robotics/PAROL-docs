# Waldo Commander (web)

[Waldo Commander](https://github.com/Jepson2k/Waldo-Commander), by a member of the community, is a browser
interface on top of the Python API: control from any device on the network, Python programs with an editor and
step-through debugging, a 3D simulation to preview paths, teaching by demonstration recorded as Python, and a
built-in MCP server through which an LLM can read the robot's status, write and run programs and drive the arm
with your approval. It runs in simulator mode without a robot.

```
git clone https://github.com/Jepson2k/Waldo-Commander.git
cd Waldo-Commander
pip install -e ".[parol6]"
waldo-commander
```

![The web commander](https://docs.source-robotics.com/PAROL-docs/1.1/assets/Web_GUI.webp){ width="800" }

It is built on [waldoctl](https://github.com/Jepson2k/waldoctl), the abstraction layer the Python API implements,
so what it offers tracks the API's features. Its documentation is at [jepson2k.github.io/Waldo-Commander](https://jepson2k.github.io/Waldo-Commander/).
