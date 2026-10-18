"""Teoría de números, módulo 2: identidad de Bézout, lemas, Euclides extendido e inversos modulares.

    manimgx render modulo2_bezout.py Modulo2
"""

import manimgx as m
import numpy as np

from comun import (AMBAR, AZUL, AZUL_OSC, BORDE, C_DEF, C_ESQ, C_INT, C_REGLA, C_TEOREMA, C_TRAMPA, GRIS,
                   GRIS_OSC, MORADO, NARANJA, ROJO, ROJO_CL, TEAL, VERDE, VERDE_CL, Clase, P, cubo, esfera,
                   etiqueta, lineas, losa, recta, tex, ttex, txt, up)

PRIMO_COLOR = {2: AZUL, 3: NARANJA, 5: VERDE, 7: MORADO}


class Modulo2(Clase):
    START = 5
    CHAPTERS = [
        "La identidad de Bézout",
        "Los lemas que salen de Bézout",
        "El algoritmo extendido de Euclides",
        "Inversos modulares",
    ]

    def construct(self) -> None:
        self.setup_hud()
        self.intro()
        self.bezout()
        self.lemas()
        self.extendido()
        self.inversos()
        self.cierre([
            "mcd(a, b) es la combinación lineal positiva más pequeña de a y b",
            "mcd(a, b) = 1  si y solo si  existen s, t con sa + tb = 1",
            "Si a | bc y mcd(a, b) = 1, entonces a | c: Bézout, multiplicar por c y combinación lineal",
            "Euclides extendido: hacia atrás o con la tabla, con invariante r = s·a + t·b",
            "a tiene inverso mod m  si y solo si  mcd(a, m) = 1, y el inverso es el s de Bézout",
        ], "En el módulo 3 usamos los inversos para resolver congruencias y sistemas con el Teorema Chino")

    def intro(self):
        self.home()
        self.titulo_video("Teoría de números · Módulo 2", "Bézout, Euclides extendido e inversos")
        self.cap("En el módulo 1 el mcd era el mayor divisor común. Aquí vamos a ver que también se puede "
                 "escribir como una suma, y eso es lo que permite dividir en aritmética modular")

    # ── 5. Bézout ────────────────────────────────────────────────────────────
    def bezout(self):
        self.chapter(5)
        self.card("La pregunta", ttex(r"¿Qué longitudes puedo medir con una regla de $6$ y una de $10$?", 28),
                  C_INT, corner=m.UL)
        self.cap("Imagina dos reglas sin marcas, una de 6 centímetros y otra de 10. Puedes ponerlas una detrás "
                 "de la otra o medir la diferencia entre ellas")
        u = 0.32
        y0 = 0.9

        def regla(n, x, z, col, k=""):
            sl = losa(n * u - 0.03, 0.38, P(x + n * u / 2, z), col, depth=0.3)
            lab = etiqueta(str(n) if not k else k, P(x + n * u / 2, z), 22)
            return m.Group(sl, lab)

        x0 = -2.9
        r6a = regla(6, x0, y0, AZUL)
        r6b = regla(6, x0 + 6 * u, y0, AZUL)
        r10 = regla(10, x0, y0 - 0.55, NARANJA)
        self.play(m.FadeIn(r6a, shift=0.3 * m.IN), run_time=0.6)
        self.play(m.FadeIn(r6b, shift=0.3 * m.IN), run_time=0.6)
        self.play(m.FadeIn(r10, shift=0.3 * m.IN), run_time=0.6)
        gap = losa(2 * u - 0.03, 0.38, P(x0 + 11 * u, y0 - 0.55), m.YELLOW, depth=0.3)
        glab = etiqueta("2", P(x0 + 11 * u, y0 - 0.55), 22, m.BLACK)
        self.play(m.FadeIn(gap), m.FadeIn(glab), run_time=0.8)
        eq = etiqueta(r"2\cdot 6 - 1\cdot 10 = 2", P(x0 + 6 * u, y0 - 1.35), 36, m.YELLOW, is_tex=True)
        self.play(m.Write(eq), run_time=0.9)
        self.cap("Dos reglas de 6 miden 12 y una de 10 mide 10. La diferencia es 2, así que puedes medir 2 cm",
                 m.YELLOW)
        self.cap("¿Puedes medir 1? No: 6 y 10 son pares, así que cualquier suma de múltiplos de ellos también "
                 "es par. Lo más pequeño que se puede medir es 2, que es justo mcd(6, 10)")
        self.clear_stage()

        # rejilla de combinaciones
        self.cap("Hagamos la tabla completa. En la casilla (s, t) escribimos 6s + 10t, con s y t entre −3 y 3")
        cell = 0.72
        tiles = {}
        for s in range(-3, 4):
            for t in range(-3, 4):
                v = 6 * s + 10 * t
                col = AZUL_OSC if v > 0 else (GRIS_OSC if v < 0 else GRIS)
                pos = P(s * cell, t * cell * 0.82 + 0.3)
                tl = losa(cell - 0.06, cell * 0.82 - 0.06, pos, col, depth=0.1)
                lab = etiqueta(str(v), pos, 20, m.WHITE, dy=-0.08)
                tiles[(s, t)] = (v, tl, lab)
        sl = etiqueta("s", P(3.6 * cell, -3 * cell * 0.82 + 0.3 - 0.55), 26, m.GREY_A)
        tlb = etiqueta("t", P(-3.6 * cell, 3 * cell * 0.82 + 0.3 + 0.4), 26, m.GREY_A)
        self.play(m.LaggedStart(*(m.FadeIn(m.Group(tl, lab)) for v, tl, lab in tiles.values()), lag_ratio=0.01),
                  m.FadeIn(sl), m.FadeIn(tlb), run_time=2.2)
        self.cap("Todos los números que salen son pares. Ningún entero (s, t) da 1, porque 2 divide a 6 y a 10")
        mins = [(tl, lab) for v, tl, lab in tiles.values() if v == 2]
        self.play(*(tl.animate.set_fill(m.YELLOW) for tl, _ in mins), *(lab.animate.set_color(m.BLACK) for _, lab in mins),
                  run_time=0.8)
        self.cap("Las casillas amarillas valen 2, el menor valor positivo de toda la tabla. Ese mínimo es el mcd",
                 m.YELLOW)
        anims = []
        for (s, t), (v, tl, lab) in tiles.items():
            if v > 0:
                h = 0.035 * v
                anims.append(tl.animate.stretch(h / 0.1, 1).shift((h / 2 - 0.05) * m.DOWN))
                anims.append(lab.animate.shift((h - 0.1) * m.DOWN))
        self.play(*anims, run_time=1.4)
        self.move_camera(phi=66 * m.DEGREES, theta=-74 * m.DEGREES, zoom=0.88, run_time=2.4)
        self.cap("Si cada valor positivo sale hacia nosotros con una altura proporcional, las columnas amarillas son "
                 "las más bajitas. La teoría dice que todas las demás son múltiplos de ellas")
        self.home(run_time=1.8)
        self.clear_stage()

        thm = self.card("Teorema de Bézout",
                        lineas(tex(r"a,b\ \text{no ambos }0\ \Rightarrow\ \exists\, s,t\in\mathbb{Z}:\ "
                                   r"\mcd(a,b) = sa+tb", 32),
                               tex(r"\mcd(a,b)=\min\{sa+tb>0\}", 32, m.YELLOW)), C_TEOREMA, corner=m.UL)
        self.cap("Este es el teorema. La prueba muestra que el mínimo positivo de la tabla cumple las dos cosas "
                 "que definen al mcd")
        nl = recta(-10, 20, np.array([0, -0.55, 0]), 12.6, font=18, solo=range(-10, 21, 2))
        vals = sorted({6 * s_ + 10 * t_ for s_ in range(-3, 4) for t_ in range(-3, 4) if -10 <= 6 * s_ + 10 * t_ <= 20},
                      key=lambda v: (abs(v), v))
        pts = m.VGroup(*(m.Dot(nl.n2p(v), radius=0.11, color=AZUL) for v in vals))
        nom = tex(r"L=\{6s+10t\}", 34, AZUL).next_to(nl, m.UP, buff=0.75).align_to(nl, m.LEFT)
        self.pin(nl, nom)
        self.play(m.Create(nl), m.Write(nom), run_time=1.0)
        self.pin(pts)
        self.remove(pts)
        self.play(m.ShowIncreasingSubsets(pts), run_time=2.0)
        self.cap("Pongamos en la recta todos los valores de la tabla. Caen en los pares y en ningún otro lado", AZUL)
        g_pt = pts[vals.index(2)]
        g_lab = tex(r"g = 2\cdot 6 - 1\cdot 10 = 2", 30, m.YELLOW).next_to(nl.n2p(2), m.UP, buff=0.45)
        self.pin(g_lab)
        self.remove(g_lab)
        self.play(g_pt.animate.set_color(m.YELLOW).scale(1.5), m.Flash(g_pt, color=m.YELLOW), m.FadeIn(g_lab),
                  run_time=0.9)
        brs = m.VGroup(*(m.Brace(m.Line(nl.n2p(v), nl.n2p(v + 2)), m.DOWN, buff=0.45, color=m.YELLOW)
                         for v in range(-10, 20, 2)))
        self.pin(brs)
        self.remove(brs)
        self.play(m.LaggedStart(*(m.GrowFromCenter(b) for b in brs), lag_ratio=0.06), run_time=1.6)
        self.cap("El menor positivo es g = 2, y todos los demás están separados exactamente por g. Eso es lo que "
                 "dice la prueba: g divide a todo L, en particular a a y a b", m.YELLOW)
        self.play(m.FadeOut(m.VGroup(nl, nom, pts, g_lab, brs)), run_time=0.6)
        self.derivar([
            r"g = s_0a + t_0b\ \ \text{el menor positivo de } L",
            r"a = gq + r,\quad 0\le r<g",
            r"r = a - (s_0a+t_0b)q = (1-s_0q)\,a + (-t_0q)\,b \in L",
            r"r<g\ \Rightarrow\ r = 0\ \Rightarrow\ g\mid a \ (\text{igual } g\mid b)",
            r"d\mid a,\ d\mid b\ \Rightarrow\ d\mid s_0a+t_0b = g\ \Rightarrow\ d\le g",
        ], anchor=np.array([-6.6, 1.2, 0]), size=30, notas=[
            "Sea g el menor número positivo que se puede escribir como sa + tb. Existe por el buen orden",
            "Para ver que g divide a a, se divide a entre g",
            "El residuo también es una combinación de a y b, así que está en la tabla",
            "Pero es menor que g, y g era el menor positivo. Entonces r no puede ser positivo: r = 0 y g divide a a",
            "Y cualquier divisor común divide a la combinación g, así que no puede ser mayor. g es el mcd",
        ])
        self.clear_stage()
        self.card("Corolario: criterio de coprimalidad",
                  tex(r"\mcd(a,b)=1 \iff \exists\, s,t:\ sa+tb=1", 34, m.YELLOW), C_TEOREMA, corner=m.UL)
        self.cap("La flecha hacia la derecha es Bézout. Para la vuelta, si d divide a a y a b, divide a sa + tb, "
                 "que es 1. Entonces d = 1")
        self.card("Error común",
                  lineas(tex(r"1\cdot 6 + 1\cdot 10 = 16\quad\text{pero}\quad \mcd(6,10)=2", 30, ROJO_CL),
                         ttex(r"$sa+tb=g$ solo dice $\mcd(a,b)\mid g$, salvo cuando $g=1$", 28)),
                  C_TRAMPA, corner=m.UR, shift=np.array([0, -1.8, 0]))
        self.cap("Ojo: que sa + tb dé un número g no dice que g sea el mcd. Lo único que se puede concluir es que "
                 "el mcd divide a g. La implicación de vuelta solo funciona con el 1", ROJO_CL)

    # ── 6. lemas ─────────────────────────────────────────────────────────────
    def chips(self, factores, x, z, label, color=m.WHITE):
        """Fila de esferas, una por factor primo."""
        balls = [esfera(P(x + 0.8 * i, z), PRIMO_COLOR[p], r=0.32) for i, p in enumerate(factores)]
        labs = [etiqueta(str(p), P(x + 0.8 * i, z), 24, m.WHITE, dy=-0.36) for i, p in enumerate(factores)]
        name = etiqueta(label, P(x - 1.2, z), 36, color, is_tex=True)
        return m.Group(name, *balls, *labs)

    def lemas(self):
        self.chapter(6)
        self.card("Lema (divisibilidad coprima)",
                  tex(r"a\mid bc\ \ \wedge\ \ \mcd(a,b)=1\ \Rightarrow\ a\mid c", 34), C_TEOREMA, corner=m.UL)
        self.cap("Este es el lema más importante del tema, y su prueba es una plantilla que sirve una y otra vez")
        self.derivar([
            r"\mcd(a,b)=1\ \Rightarrow\ sa+tb=1",
            r"sac + tbc = c",
            r"a\mid sac,\qquad bc = ak\ \Rightarrow\ tbc = a(tk)",
            r"a \mid sac + tbc = c",
        ], anchor=np.array([-6.6, 1.3, 0]), size=34, notas=[
            "Paso uno, Bézout: como son coprimos, hay s y t con sa + tb = 1",
            "Paso dos, multiplicar toda la igualdad por c",
            "Paso tres, a divide a los dos sumandos. Al primero porque tiene a como factor, y al segundo porque "
            "bc es múltiplo de a por hipótesis",
            "Paso cuatro, combinación lineal: a divide a la suma, que es c",
        ])
        tall = self.card("Ejercicio típico",
                         lineas(tex(r"dx+by=1\ \Rightarrow\ adx+aby=a", 28),
                                tex(r"ab = dk\ \Rightarrow\ d(ax+ky) = a", 28)), C_ESQ, corner=m.UR,
                         shift=np.array([0, -1.3, 0]))
        self.cap("Un ejercicio típico se resuelve exactamente igual, con d en lugar de a")
        self.clear_stage()

        # contraejemplo visual con factores primos
        self.card("Contraejemplo canónico", tex(r"6\mid 4\cdot 3\quad\text{pero}\quad 6\nmid 3", 32), C_TRAMPA,
                  corner=m.UL)
        self.cap("¿Qué pasa si quitamos la hipótesis de coprimalidad? Miremos los factores primos como bolitas: "
                 "azul es 2 y naranja es 3")
        g6 = self.chips([2, 3], -1.0, 1.2, r"6")
        g12 = self.chips([2, 2, 3], -1.0, 0.2, r"4\cdot 3")
        g3 = self.chips([3], -1.0, -0.8, r"3")
        self.play(m.FadeIn(g6), run_time=0.7)
        self.play(m.FadeIn(g12), run_time=0.7)
        self.cap("6 divide a 4·3 porque las bolitas de 6, un 2 y un 3, están dentro de las de 12")
        self.play(m.FadeIn(g3), run_time=0.7)
        blue = g6[1]
        self.play(m.Indicate(blue, color=ROJO_CL, scale_factor=1.4), run_time=1.0)
        self.cap("Pero el 2 del 6 está escondido en el 4, no en el 3. Como mcd(6, 4) = 2 ≠ 1, el lema no aplica "
                 "y 6 no divide a 3", ROJO_CL)
        self.cap("La coprimalidad garantiza justo esto: que ningún factor de a se puede esconder en b, así que "
                 "todos tienen que estar en c")
        self.swing(theta=-60, phi=66, run_time=2.0)
        self.clear_stage()

        # Euclides y división múltiple
        self.card("Lema de Euclides", tex(r"p\ \text{primo},\ p\mid ab\ \Rightarrow\ p\mid a\ \vee\ p\mid b", 32),
                  C_TEOREMA, corner=m.UL)
        self.cap("Si p es primo y no divide a a, entonces mcd(p, a) = 1, porque los únicos divisores de p son 1 "
                 "y p. Por el lema anterior, p divide a b")
        self.card("Contraejemplo", tex(r"6\mid 2\cdot 3,\quad 6\nmid 2,\quad 6\nmid 3", 30), C_TRAMPA,
                  corner=m.UR)
        self.cap("Con un número compuesto falla. Este lema es lo que hace especiales a los primos, y lo vamos a "
                 "usar en la unicidad del TFA, en Fermat, en Wilson y en los autoinversos")
        self.card("División múltiple coprima",
                  lineas(tex(r"a\mid c,\ b\mid c,\ \mcd(a,b)=1\ \Rightarrow\ ab\mid c", 30),
                         tex(r"c = ak,\ b\mid ak\ \Rightarrow\ b\mid k\ \Rightarrow\ c = ab\ell", 28)),
                  C_TEOREMA, corner=m.DL, shift=np.array([0, 1.3, 0]))
        self.cap("Y el tercero: si dos coprimos dividen a c, su producto también. La prueba usa el primer lema "
                 "con b y k")
        self.card("Contraejemplo", tex(r"4\mid 12,\ 6\mid 12,\ \ 24\nmid 12", 30), C_TRAMPA, corner=m.DR,
                  shift=np.array([0, 1.3, 0]))
        self.cap("Sin coprimalidad, 4 y 6 comparten el factor 2, y se estaría contando dos veces")
        self.clear_stage()

        self.card("Ejercicio: el mcd con un producto",
                  tex(r"\mcd(a,b)=1,\ \mcd(a,c)=1\ \Rightarrow\ \mcd(a,bc)=1", 34), C_TEOREMA, corner=m.UL)
        self.cap("Este ejercicio usa un truco que sirve siempre: multiplicar dos identidades de Bézout")
        der = self.derivar([
            r"ax_1+by_1 = 1,\qquad ax_2+cy_2 = 1",
            r"(ax_1+by_1)(ax_2+cy_2) = 1",
            r"a^2x_1x_2 + ax_1cy_2 + by_1ax_2 + bcy_1y_2 = 1",
            r"a\,(ax_1x_2 + x_1cy_2 + by_1x_2) + bc\,(y_1y_2) = 1",
            r"aX + (bc)Y = 1\ \Rightarrow\ \mcd(a,bc)=1",
        ], anchor=np.array([-6.6, 1.25, 0]), size=32, notas=[
            "Escribimos las dos identidades",
            "Las multiplicamos. Uno por uno sigue siendo uno",
            "Se expande el producto",
            "Todos los términos menos el último tienen una a. Se saca a como factor común",
            "Queda a por un entero más bc por un entero igual a 1. Por el criterio de coprimalidad, a y bc son "
            "coprimos",
        ])
        self.play(m.FadeOut(der[1:4]), der[4].animate.next_to(der[0], m.DOWN, buff=0.22, aligned_edge=m.LEFT),
                  run_time=0.8)
        W, Hh = 2.0, 1.05
        celdas = {}
        nombres = {(0, 0): r"a^2x_1x_2", (0, 1): r"a\,x_1cy_2", (1, 0): r"a\,by_1x_2", (1, 1): r"bc\,y_1y_2"}
        for (i, j), nom_ in nombres.items():
            col = NARANJA if (i, j) == (1, 1) else AZUL_OSC
            r_ = m.Rectangle(width=W, height=Hh, fill_color=col, fill_opacity=0.85, stroke_color=m.WHITE,
                             stroke_width=2).move_to([2.6 + j * W, 0.1 - i * Hh, 0])
            celdas[(i, j)] = m.VGroup(r_, tex(nom_, 28).move_to(r_))
        top = [tex(r"ax_2", 30, AZUL).next_to(celdas[(0, j)], m.UP, buff=0.15) for j in range(2)]
        izq = [tex(t_, 30, c_).next_to(celdas[(i, 0)], m.LEFT, buff=0.15)
               for i, (t_, c_) in enumerate(((r"ax_1", AZUL), (r"by_1", NARANJA)))]
        top[1] = tex(r"cy_2", 30, NARANJA).next_to(celdas[(0, 1)], m.UP, buff=0.15)
        bloque = m.VGroup(*celdas.values())
        self.pin(*top, *izq, bloque)
        self.remove(*top, *izq, bloque)
        self.play(*(m.FadeIn(t_, shift=0.1 * m.DOWN) for t_ in top), *(m.FadeIn(t_, shift=0.1 * m.RIGHT) for t_ in izq),
                  run_time=0.7)
        self.play(m.LaggedStart(*(m.DrawBorderThenFill(c_) for c_ in celdas.values()), lag_ratio=0.25),
                  run_time=1.8)
        self.cap("Como área: un rectángulo de lados ax₁ + by₁ y ax₂ + cy₂, que vale 1·1 = 1, partido en cuatro "
                 "pedazos")
        azules = m.VGroup(celdas[(0, 0)], celdas[(0, 1)], celdas[(1, 0)])
        self.play(m.Circumscribe(azules, color=AZUL, buff=0.05), m.Indicate(celdas[(1, 1)], color=AMBAR),
                  run_time=1.4)
        self.cap("Los tres pedazos azules tienen una a, así que juntos son a·X. El naranja es bc·y₁y₂. Esa es la "
                 "combinación aX + (bc)Y = 1")

    # ── 7. Euclides extendido ────────────────────────────────────────────────
    def extendido(self):
        self.chapter(7)
        self.cap("Bézout dice que s y t existen. Ahora, ¿cómo se encuentran? Hay dos métodos y los dos dan una "
                 "respuesta correcta")
        self.card("Método 1: sustitución hacia atrás",
                  ttex(r"Se despejan los residuos de abajo hacia arriba", 26), C_ESQ, corner=m.UL)
        divs = lineas(*(tex(s, 24, m.GREY_B) for s in [
            r"89 = 1\cdot 55 + 34", r"55 = 1\cdot 34 + 21", r"34 = 1\cdot 21 + 13", r"21 = 1\cdot 13 + 8",
            r"13 = 1\cdot 8 + 5", r"8 = 1\cdot 5 + 3", r"5 = 1\cdot 3 + 2", r"3 = 1\cdot 2 + 1"]), buff=0.08)
        divs.to_edge(m.RIGHT, buff=0.5).shift(0.5 * m.UP)
        self.pin(divs)
        self.play(m.FadeIn(divs), run_time=0.8)
        self.cap("Partimos de las divisiones de 89 y 55 que ya teníamos. La idea es escribir 1 siempre usando los "
                 "dos residuos más recientes, e ir subiendo")
        self.derivar([
            r"1 = 3 - 1\cdot 2",
            r"= 3 - (5 - 3) = 2\cdot 3 - 5",
            r"= 2(8-5) - 5 = 2\cdot 8 - 3\cdot 5",
            r"= 2\cdot 8 - 3(13-8) = 5\cdot 8 - 3\cdot 13",
            r"= 5(21-13) - 3\cdot 13 = 5\cdot 21 - 8\cdot 13",
            r"= 5\cdot 21 - 8(34-21) = 13\cdot 21 - 8\cdot 34",
            r"= 13(55-34) - 8\cdot 34 = 13\cdot 55 - 21\cdot 34",
            r"= 13\cdot 55 - 21(89-55) = 34\cdot 55 - 21\cdot 89",
        ], anchor=np.array([-6.6, 1.45, 0]), size=28, buff=0.16, notas=[
            "De la última división, 1 = 3 − 2",
            "Se cambia el 2 por lo que vale según la división de arriba, 5 − 3, y se agrupa",
            "Ahora se cambia el 3 por 8 − 5",
            None, None, None, None,
            "Y al final queda 1 = 34·55 − 21·89",
        ], hold=1.1, resaltar=[divs[7 - i] for i in range(8)])
        self.cap("Comprobación: 34·55 = 1870 y 21·89 = 1869. La diferencia es 1", VERDE_CL)
        self.card("Ojo", lineas(ttex(r"Otra respuesta válida: $1 = 34\cdot 89 - 55\cdot 55$.", 24),
                                ttex(r"Los coeficientes de Bézout no son únicos: $(s + kb,\ t - ka)$ también sirve.", 24)),
                  C_INT, corner=m.DR, shift=np.array([0, 1.25, 0]))
        self.cap("Alguien más podría llegar a 34·89 − 55·55 = 1, y también estaría bien. Hay infinitas parejas, y para el "
                 "inverso dan lo mismo, porque −55 y 34 son congruentes módulo 89")
        self.clear_stage()

        # tabla
        self.card("Método 2: la tabla",
                  lineas(tex(r"r_j = r_{j-2} - q_{j-1} r_{j-1}", 28),
                         tex(r"s_j = s_{j-2} - q_{j-1} s_{j-1},\quad t_j = t_{j-2} - q_{j-1} t_{j-1}", 28),
                         tex(r"\text{invariante: } r_j = s_j\cdot 89 + t_j\cdot 55", 28, m.YELLOW)), C_TEOREMA,
                  corner=m.UL)
        rows = [(89, None, 1, 0), (55, 1, 0, 1), (34, 1, 1, -1), (21, 1, -1, 2), (13, 1, 2, -3), (8, 1, -3, 5),
                (5, 1, 5, -8), (3, 1, -8, 13), (2, 2, 13, -21), (1, None, -21, 34)]
        cols_x = [1.4, 2.6, 3.7, 4.9, 6.1]
        head = [tex(h, 28, m.YELLOW) for h in ["r_j", "q_j", "s_j", "t_j"]]
        top = 2.1
        for h, x in zip(head, cols_x):
            h.move_to([x, top, 0])
        self.pin(*head)
        self.play(*(m.FadeIn(h) for h in head), run_time=0.6)
        pitch = 0.42
        cells = []
        for j, (r, q, s, t) in enumerate(rows):
            y = top - 0.5 - j * pitch
            row = [tex(str(r), 26), tex("-" if q is None else str(q), 26, m.GREY_B), tex(str(s), 26, AZUL),
                   tex(str(t), 26, NARANJA)]
            for c, x in zip(row, cols_x):
                c.move_to([x, y, 0])
            cells.append(row)
        self.pin(*cells[0], *cells[1])
        self.play(*(m.FadeIn(c) for c in cells[0] + cells[1]), run_time=0.8)
        self.cap("Las dos primeras filas son fáciles: 89 = 1·89 + 0·55 y 55 = 0·89 + 1·55. Ahí ya se cumple el "
                 "invariante")
        for j in range(2, len(rows)):
            box = m.SurroundingRectangle(m.VGroup(*cells[j - 2], *cells[j - 1]), color=GRIS, buff=0.06)
            self.pin(box)
            self.play(m.FadeIn(box), run_time=0.25)
            self.pin(*cells[j])
            self.play(*(m.TransformFromCopy(m.VGroup(cells[j - 2][k], cells[j - 1][k]), cells[j][k])
                        for k in (0, 2, 3)), m.FadeIn(cells[j][1]), run_time=0.7)
            self.play(m.FadeOut(box), run_time=0.2)
            self.remove(box)
            if j == 2:
                self.cap("Cada fila nueva es la de hace dos menos q veces la anterior. Como todo es lineal, "
                         "si las dos filas de arriba cumplen el invariante, la nueva también")
            elif j == 4:
                self.cap("Es la misma resta en las tres columnas. No hace falta despejar nada")
        last = m.SurroundingRectangle(m.VGroup(*cells[-1]), color=m.YELLOW, buff=0.08)
        self.pin(last)
        self.play(m.Create(last), run_time=0.6)
        self.cap("En la última fila: 1 = −21·89 + 34·55. Es la misma respuesta del método 1", m.YELLOW)

    # ── 8. inversos ──────────────────────────────────────────────────────────
    def inversos(self):
        self.chapter(8)
        self.card("Definición", tex(r"\bar a\ \text{es inverso de } a \md{m} \iff a\,\bar a\equiv 1\md{m}", 32),
                  C_DEF, corner=m.UL)
        self.cap("En los reales, dividir entre a es multiplicar por 1/a. En aritmética modular lo que se busca es un "
                 "número que multiplicado por a dé 1")
        self.cap("Miremos las tablas de multiplicar módulo 7 y módulo 6. Las casillas donde da 1 van a salir "
                 "hacia nosotros")

        def tabla(m_, x0, title):
            tiles = []
            cs = 0.56
            for a in range(1, m_):
                for b in range(1, m_):
                    v = a * b % m_
                    pos = P(x0 + (b - 1) * cs, 1.25 - (a - 1) * cs)
                    col = VERDE if v == 1 else GRIS_OSC
                    tl = losa(cs - 0.04, cs - 0.04, pos, col, depth=0.08)
                    lab = etiqueta(str(v), pos, 20, m.WHITE, dy=-0.05)
                    tiles.append((a, b, v, tl, lab))
            hdr = etiqueta(title, P(x0 + (m_ - 2) * cs / 2, 1.9), 32, m.YELLOW, is_tex=True)
            rlabs = [etiqueta(str(a), P(x0 - 0.5, 1.25 - (a - 1) * cs), 22, m.GREY_A) for a in range(1, m_)]
            return tiles, hdr, rlabs

        t7, h7, r7 = tabla(7, -5.3, r"\bmod 7")
        t6, h6, r6 = tabla(6, 1.3, r"\bmod 6")
        for tiles, hdr, rl in ((t7, h7, r7), (t6, h6, r6)):
            self.play(m.FadeIn(hdr), *(m.FadeIn(l) for l in rl),
                      m.LaggedStart(*(m.FadeIn(m.Group(tl, lab)) for *_, tl, lab in tiles), lag_ratio=0.01),
                      run_time=1.4)
        ones = [(tl, lab) for tiles in (t7, t6) for a, b, v, tl, lab in tiles if v == 1]
        self.play(*(tl.animate.stretch(4, 1).shift(0.12 * m.DOWN) for tl, _ in ones), *(lab.animate.shift(0.3 * m.DOWN) for _, lab in ones),
                  run_time=0.8)
        self.cap("Módulo 7 hay un 1 en cada fila: todos los números del 1 al 6 tienen inverso")
        bad = [(tl, lab) for a, b, v, tl, lab in t6 if a in (2, 3, 4)]
        self.play(*(tl.animate.set_fill(ROJO) for tl, _ in bad), run_time=0.8)
        self.cap("Módulo 6, las filas de 2, 3 y 4 nunca llegan a 1. Por ejemplo, la del 2 es 2, 4, 0, 2, 4: "
                 "solo pares. Esos son justo los números que comparten un factor con 6", ROJO_CL)
        self.move_camera(phi=62 * m.DEGREES, theta=-70 * m.DEGREES, run_time=2.0)
        self.home(run_time=1.6)
        self.clear_stage()

        self.card("Teorema", tex(r"a\ \text{tiene inverso}\md{m}\iff \mcd(a,m)=1", 34, m.YELLOW), C_TEOREMA,
                  corner=m.UL)
        self.derivar([
            r"a\bar a\equiv 1 \md{m}",
            r"\iff m\mid a\bar a - 1",
            r"\iff a\bar a - 1 = mk",
            r"\iff \bar a\cdot a + (-k)\cdot m = 1",
            r"\iff \mcd(a,m)=1",
        ], anchor=np.array([-6.6, 1.3, 0]), size=34, notas=[
            "La prueba es solo traducir. Que a por a barra sea 1 módulo m",
            "quiere decir que m divide a la diferencia",
            "es decir, que la diferencia es un múltiplo de m",
            "Se reordena, y queda una combinación lineal de a y m que da 1",
            "Y eso, por el criterio de coprimalidad, es lo mismo que mcd(a, m) = 1",
        ])
        self.card("Cómo se calcula",
                  lineas(tex(r"sa + tm = 1\ \xrightarrow{\ \bmod m\ }\ sa\equiv 1", 30),
                         tex(r"34\cdot 55 - 21\cdot 89 = 1\ \Rightarrow\ 55^{-1}\equiv 34 \md{89}", 30, VERDE_CL)),
                  C_ESQ, corner=m.UR, shift=np.array([0, -2.0, 0]))
        self.cap("Para calcularlo se hace Euclides extendido y se reduce módulo m. El término de m desaparece y "
                 "queda el inverso. Del ejemplo anterior, el inverso de 55 módulo 89 es 34", VERDE_CL)
        self.card("Regla de 1 segundo",
                  ttex(r"¿Existe $a^{-1}\bmod m$? Mira $\mcd(a,m)$. Si es $1$, el inverso es el $s$ de Bézout.", 26),
                  C_REGLA, corner=m.DL, shift=np.array([0, 1.25, 0]))
        self.wait(3)
