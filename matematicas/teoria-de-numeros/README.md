# Teoría de números

Un curso corto de teoría de números en cuatro videos animados, hechos con [ManimGX](https://manimgx.academa.ai), y una guía escrita en LaTeX con todas las demostraciones completas. Va desde qué significa que un número divida a otro hasta RSA.

Cada tema sigue el mismo orden: **la pregunta → intuición visual → teorema → demostración → ejemplo con números**. Al final de cada tema hay tres ideas para recordar: el esqueleto de la prueba, el contraejemplo canónico (qué se rompe si quitas una hipótesis) y una regla rápida para saber cuándo usar el resultado.

**Requisitos previos:** álgebra básica y comodidad con demostraciones sencillas (inducción, contradicción). La referencia principal es Rosen, *Matemática discreta y sus aplicaciones*, capítulo 4.

## Dónde ver los videos

Los cuatro videos (1080p) están en el [Release v1.0](https://github.com/Carlixgonzam/manim-clases/releases/tag/v1.0) de este repositorio. La guía en PDF está en [`guia/guia_detallada.pdf`](guia/guia_detallada.pdf).

## Contenido

**Módulo 1: divisibilidad, división, MCD y factorización**
1. Qué significa dividir: bloques de cubos, las cinco propiedades y la prueba de combinación lineal con saltos en la recta numérica
2. El algoritmo de la división: cajones en la recta, −20 = 3(−7) + 1 frente al error r = −2, y la prueba de existencia y unicidad
3. El MCD y el algoritmo de Euclides: el rectángulo 21×13 cortado en cuadrados, el mcd de 89 y 55, y por qué el algoritmo termina
4. Primos y factorización única: el árbol de 360, la infinitud de los primos (30031 = 59·509) y mcd/mcm como columnas de exponentes

**Módulo 2: Bézout, Euclides extendido e inversos**

5. La identidad de Bézout: reglas de 6 y 10, la rejilla de valores 6s + 10t y la prueba del mínimo positivo
6. Los lemas que salen de Bézout: a | bc ⇒ a | c, factores primos como bolitas, lema de Euclides y mcd(a, bc) = 1 como modelo de área
7. El algoritmo extendido: sustitución hacia atrás y la tabla con s y t
8. Inversos modulares: tablas de multiplicar mod 7 y mod 6, la prueba y 55⁻¹ ≡ 34 (mod 89)

**Módulo 3: congruencias, Teorema Chino del Residuo, Fermat y Wilson**

9. Congruencias como aritmética de reloj: los enteros enrollados en espiral, una clase por rayo
10. Álgebra de congruencias (el producto como modelo de área) y el error de cancelar sin revisar el mcd
11. Congruencias lineales: a dónde va 6x mod 15 y por qué hay exactamente d soluciones
12. Teorema Chino del Residuo: la rejilla 3×5 recorrida en diagonal, la rejilla 2×4 que falla, los "interruptores" Mᵢyᵢ y los módulos no coprimos
13. Pequeño Teorema de Fermat: multiplicar por 3 revuelve los residuos mod 7, el ciclo de las potencias y 2^1000005 mod 101
14. Teorema de Wilson: parejas de inversos mod 11 y 98! mod 101

**Módulo 4: φ de Euler, Teorema de Euler y RSA**

15. La función φ: φ(12), φ(27), por qué es multiplicativa y φ(360) como un colador
16. Teorema de Euler: 2^118 mod 119 y las últimas tres cifras de 7^2407
17. Elementos autoinversos: mod p, mod 16, mod 2ⁿ, mod 100 y los 16 de mod 3600
18. RSA de principio a fin con p = 5 y q = 11: claves, cifrado, descifrado con el TCR y el error de calcular d mod n
19. Mapa de decisión (qué teorema usar según el problema) y los errores más comunes

Todos los números de los videos y de la guía se verificaron con Python (`pow`, `math.gcd` y búsqueda exhaustiva).

## Archivos

| Archivo | Qué es |
|---|---|
| `modulo1_divisibilidad.py` … `modulo4_euler_rsa.py` | Una escena por video, un método por capítulo |
| `comun.py` | Paleta, cámara, subtítulos, tarjetas de teorema, `derivar()` (cadenas de igualdades animadas), `saltar()` (saltos en la recta numérica) y `barra_exponente()` (un exponente partido en bloques que valen 1 y un resto) |
| `guia/guia_detallada.tex` | Fuente LaTeX de la guía (17 páginas) |

## Renderizar los videos

```bash
pip install manimgx
cd matematicas/teoria-de-numeros
manimgx render modulo1_divisibilidad.py Modulo1 --fps 30
manimgx render modulo2_bezout.py Modulo2 --fps 30
manimgx render modulo3_congruencias.py Modulo3 --fps 30
manimgx render modulo4_euler_rsa.py Modulo4 --fps 30
```

Cada video tarda unos 20 segundos en un portátil moderno. `manimgx render` también genera archivos `*.storyboard*.png`, que se pueden borrar.

Para compilar la guía: `cd guia && pdflatex guia_detallada.tex`, tres veces para que el índice quede bien.
