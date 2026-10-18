# manim-clases

Animated lessons on mathematics and computer science, made with [ManimGX](https://manimgx.academa.ai).

Each series comes with the videos, the code that renders them and a written guide.

## Series

| Area | Series | Status |
|---|---|---|
| Mathematics | [Number theory](mathematics/number-theory/) | 4 videos and a guide |
| Computer science | [Languages and machines](computer-science/languages-and-machines/) | Planned |
| Computer science | [Software architecture](computer-science/software-architecture/) | Planned |

You can download the videos from the [latest release](https://github.com/Carlixgonzam/manim-clases/releases/latest).

## Rendering a video

```bash
pip install manimgx
cd mathematics/number-theory
manimgx render module1_divisibility.py Module1 --fps 30
```

## License

The code is under the [MIT license](LICENSE), and the videos and guides are under [CC BY 4.0](LICENSE-CONTENT).
