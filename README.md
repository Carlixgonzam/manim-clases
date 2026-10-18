# manim-clases

Clases animadas de matemáticas y ciencias de la computación, hechas con [ManimGX](https://manimgx.academa.ai). Cada serie trae los videos, el código que los genera y una guía escrita con las demostraciones completas.

La idea es que cada tema se pueda **ver** antes de demostrarlo: primero la intuición visual, después el teorema, la prueba y un ejemplo con números.

## Series

| Serie | Área | Videos | Estado |
|---|---|---|---|
| [Teoría de números](matematicas/teoria-de-numeros/) | Matemáticas | 4 módulos, 19 capítulos | Completa |

Vienen más series de ciencias de la computación, empezando por teoría de lenguajes y autómatas.

## Estructura

```
manim-clases/
├── matematicas/
│   └── teoria-de-numeros/   ← código de los videos, guía en LaTeX y README de la serie
└── computacion/             ← próximamente
```

Cada serie es independiente: tiene su propio README con el contenido y las instrucciones para renderizar.

## Requisitos para renderizar

- Python 3 y [ManimGX](https://manimgx.academa.ai): `pip install manimgx`
- Una distribución de LaTeX (TeX Live o MacTeX) para compilar las guías

## Licencia

- El **código** está bajo la licencia [MIT](LICENSE).
- Los **videos y las guías** están bajo [Creative Commons Atribución 4.0](LICENSE-CONTENIDO): puedes usarlos, compartirlos y adaptarlos, incluso en clase, siempre que des crédito a Carla González Mina.
