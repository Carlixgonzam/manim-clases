# manim-clases

Animated lessons on mathematics and computer science, made with [ManimGX](https://manimgx.academa.ai).

Each series comes with the videos, the code that renders them, and a written guide.

## Series

| Area | Series | Status |
|---|---|---|
| Mathematics | [Number theory](mathematics/number-theory/) | 4 videos + guide |
| Computer science | [Languages and machines](computer-science/languages-and-machines/) | Planned |
| Computer science | [Software architecture](computer-science/software-architecture/) | Planned |

Videos are in the [Releases](https://github.com/Carlixgonzam/manim-clases/releases/latest).

## Render a video

```bash
pip install manimgx
cd mathematics/number-theory
manimgx render module1_divisibility.py Module1 --fps 30
```

## License

Code: [MIT](LICENSE). Videos and guides: [CC BY 4.0](LICENSE-CONTENT).
