"""Teoría de números, módulo 4: función φ de Euler, Teorema de Euler, autoinversos, RSA y mapa de decisión.

    manimgx render modulo4_euler_rsa.py Modulo4
"""

import math

import manimgx as m
import numpy as np

from comun import (AMBAR, AZUL, AZUL_OSC, BORDE, C_DEF, C_ESQ, C_INT, C_REGLA, C_TEOREMA, C_TRAMPA, GRIS,
                   GRIS_OSC, MORADO, NARANJA, PANEL_BG, ROJO, ROJO_CL, TEAL, VERDE, VERDE_CL, Clase, P, cubo,
                   esfera, etiqueta, lineas, losa, tex, ttex, txt, up)


def en_circulo(k: int, n: int, R: float, cx: float = 0.0, cz: float = 0.0, y: float = 0.0):
    ang = math.pi / 2 - 2 * math.pi * k / n
    return P(cx + R * math.cos(ang), cz + R * math.sin(ang), y)


class Modulo4(Clase):
    START = 15
    CHAPTERS = [
        "La función φ de Euler",
        "El Teorema de Euler",
        "Elementos autoinversos",
        "RSA de principio a fin",
        "Mapa de decisión y errores comunes",
    ]

    def construct(self) -> None:
        self.setup_hud()
        self.intro()
        self.phi()
        self.euler()
        self.autoinversos()
        self.rsa()
        self.mapa()
        self.cierre([
            "φ(n) cuenta los residuos invertibles; φ(pᵏ) = pᵏ − pᵏ⁻¹ y es multiplicativa con coprimos",
            "Euler: si mcd(a, n) = 1, a elevado a φ(n) es ≡ 1, así que el exponente se reduce mod φ(n)",
            "a² ≡ 1: 2 soluciones mod pᵏ impar, 4 mod 2ⁿ con n ≥ 3, y se multiplican con el TCR",
            "RSA: d = e⁻¹ mod φ(n); funciona por Euler y el TCR",
            "Antes de usar un teorema, revisa la hipótesis: primo, coprimo o coprimos dos a dos",
        ], "Eso es todo el recorrido. La guía escrita tiene cada prueba completa y ejercicios con solución")

    def intro(self):
        self.home()
        self.titulo_video("Teoría de números · Módulo 4", "φ de Euler, Teorema de Euler y RSA")
        self.cap("Fermat solo sirve con módulos primos. En este módulo lo generalizamos a cualquier módulo, y con "
                 "eso armamos RSA, que es la criptografía que protege casi todo internet")

    # ── 15. φ ────────────────────────────────────────────────────────────────
    def phi(self):
        self.chapter(15)
        self.card("Definición",
                  lineas(tex(r"\varphi(n) = \#\{x:\ 1\le x\le n,\ \mcd(x,n)=1\}", 32),
                         ttex(r"es decir, cuántos residuos tienen inverso mod $n$", 26)), C_DEF, corner=m.UL)
        self.cap("φ de n cuenta cuántos números entre 1 y n son coprimos con n. Por lo que vimos en el módulo 2, "
                 "son justo los que tienen inverso")
        n = 12
        xs = [-3.3 + 0.6 * i for i in range(n)]
        cubes = [cubo(str(k + 1), P(xs[k], 0.4), GRIS_OSC, side=0.5, size=22) for k in range(n)]
        self.play(m.LaggedStart(*(m.FadeIn(c, shift=0.3 * m.IN) for c in cubes), lag_ratio=0.05), run_time=1.2)
        good = [k for k in range(n) if math.gcd(k + 1, n) == 1]
        self.play(*(cubes[k][0].animate.set_fill(VERDE) for k in good),
                  *(cubes[k][0].animate.set_fill(ROJO).set_opacity(0.45) for k in range(n) if k not in good),
                  *(cubes[k].animate.shift(0.25 * m.OUT) for k in good), run_time=1.0)
        res = etiqueta(r"\varphi(12) = 4", P(0, -0.7), 38, VERDE_CL, is_tex=True)
        self.play(m.Write(res), run_time=0.8)
        self.cap("Con 12: solo 1, 5, 7 y 11 son coprimos con 12, así que φ(12) = 4. Los rojos comparten un 2 o un 3 "
                 "con 12", VERDE_CL)
        self.clear_stage()

        self.card("Potencia de primo", tex(r"\varphi(p^k) = p^k - p^{k-1} = p^k\left(1-\tfrac1p\right)", 34),
                  C_TEOREMA, corner=m.UL)
        self.cap("Para una potencia de primo es fácil. Con 27 = 3³: un número comparte factor con 27 solo si es "
                 "múltiplo de 3")
        cubes = []
        for k in range(27):
            r, c = divmod(k, 9)
            cubes.append(cubo(str(k + 1), P(-2.4 + 0.6 * c, 0.9 - 0.65 * r), GRIS_OSC, side=0.5, size=20))
        self.play(m.LaggedStart(*(m.FadeIn(c) for c in cubes), lag_ratio=0.02), run_time=1.4)
        bad = [k for k in range(27) if (k + 1) % 3 == 0]
        self.play(*(cubes[k][0].animate.set_fill(ROJO) for k in bad),
                  *(cubes[k][0].animate.set_fill(VERDE) for k in range(27) if k not in bad), run_time=0.9)
        res = etiqueta(r"\varphi(27) = 27 - 9 = 18", P(0, -1.3), 38, VERDE_CL, is_tex=True)
        self.play(m.Write(res), run_time=0.8)
        self.cap("Los múltiplos de 3 son uno de cada tres, o sea 27/3 = 9 = 3². Se restan y quedan 18", VERDE_CL)
        self.clear_stage()

        # multiplicatividad con la rejilla del TCR
        self.card("Multiplicativa",
                  tex(r"\mcd(m,n)=1\ \Rightarrow\ \varphi(mn)=\varphi(m)\varphi(n)", 34), C_TEOREMA, corner=m.UL)
        self.cap("¿Por qué φ es multiplicativa? Volvamos a la rejilla del Teorema Chino, con 15 = 3 · 5")
        c = 0.66
        x0, z0 = -0.6, 0.6
        cells, labs = {}, []
        for x in range(15):
            i, j = x % 3, x % 5
            pos = P(x0 + j * c, z0 - i * c)
            cells[(i, j)] = losa(c - 0.06, c - 0.06, pos, GRIS_OSC, depth=0.06)
            labs.append(etiqueta(str(x), P(x0 + j * c, z0 - i * c, -0.08), 22, m.WHITE, dy=0))
        rl = [etiqueta(str(i), P(x0 - 0.55, z0 - i * c), 22, NARANJA) for i in range(3)]
        cl = [etiqueta(str(j), P(x0 + j * c, z0 + 0.55), 22, AZUL) for j in range(5)]
        self.play(*(m.FadeIn(v) for v in cells.values()), *(m.FadeIn(t) for t in labs + rl + cl), run_time=1.0)
        self.play(*(cells[(i, j)].animate.set_fill(NARANJA).set_opacity(0.55) for i in (1, 2) for j in range(5)),
                  run_time=0.7)
        self.cap("x es coprimo con 15 si y solo si es coprimo con 3 y con 5. Coprimo con 3 son las filas 1 y 2. "
                 "Son φ(3) = 2 filas", NARANJA)
        self.play(*(cells[(i, j)].animate.set_fill(VERDE).set_opacity(1) for i in (1, 2) for j in (1, 2, 3, 4)),
                  *(cells[(0, j)].animate.set_fill(GRIS_OSC) for j in range(5)),
                  *(cells[(i, 0)].animate.set_fill(GRIS_OSC).set_opacity(1) for i in range(3)), run_time=0.8)
        self.cap("Y coprimo con 5 son las columnas 1 a 4, que son φ(5) = 4. Las casillas que cumplen las dos son "
                 "2 · 4 = 8 = φ(15)", VERDE_CL)
        self.swing(theta=-60, phi=64, run_time=2.0)
        self.clear_stage()

        self.card("Fórmula general",
                  tex(r"n=p_1^{a_1}\cdots p_k^{a_k}\ \Rightarrow\ \varphi(n)=n\prod_i\left(1-\tfrac{1}{p_i}\right)", 34),
                  C_TEOREMA, corner=m.UL)
        self.derivar([
            r"\varphi(119)=\varphi(7)\,\varphi(17)=6\cdot 16 = 96",
            r"\varphi(1000)=\varphi(2^3)\,\varphi(5^3)=4\cdot 100=400",
            r"\varphi(360)=360\cdot\tfrac12\cdot\tfrac23\cdot\tfrac45 = 96",
        ], anchor=np.array([-6.6, 1.3, 0]), size=34, notas=[
            "Tres ejemplos. 119 es 7 por 17, dos primos distintos",
            "1000 es 2 al cubo por 5 al cubo, y cada potencia se hace con la fórmula de antes",
            "Y con la fórmula del producto, 360 = 2³ · 3² · 5 da 96",
        ])
        x0, y, ancho = -6.2, -1.55, 8.4
        barra = m.Rectangle(width=ancho, height=0.5, fill_color=VERDE, fill_opacity=0.9, stroke_width=0)
        barra.move_to([x0 + ancho / 2, y, 0])
        cnt = m.Integer(360, group_with_commas=False, font_size=44, color=VERDE_CL).move_to([4.6, y, 0])
        self.pin(barra, cnt)
        self.remove(barra, cnt)
        self.play(m.GrowFromEdge(barra, m.LEFT), m.FadeIn(cnt), run_time=1.0)
        w = ancho
        pasos = [(r"\times\tfrac12", 2, 180, "Quitar los múltiplos de 2 deja la mitad: 180"),
                 (r"\times\tfrac23", 3, 120, "De lo que queda, quitar los múltiplos de 3 deja dos tercios: 120"),
                 (r"\times\tfrac45", 5, 96, "Y quitar los múltiplos de 5 deja cuatro quintos: 96 = φ(360)")]
        for frac, p_, nuevo, nota in pasos:
            w2 = w * (p_ - 1) / p_
            quita = m.Rectangle(width=w - w2, height=0.5, fill_color=ROJO, fill_opacity=0.9, stroke_width=0)
            quita.move_to([x0 + w2 + (w - w2) / 2, y, 0])
            tag = tex(frac, 34, ROJO_CL).next_to(quita, m.UP, buff=0.2)
            self.pin(quita, tag)
            self.remove(quita, tag)
            self.play(m.FadeIn(quita), m.FadeIn(tag, shift=0.1 * m.DOWN), run_time=0.5)
            self.play(m.FadeOut(quita, shift=0.5 * m.DOWN), m.FadeOut(tag),
                      barra.animate.stretch_to_fit_width(w2, about_edge=m.LEFT),
                      m.ChangeDecimalToValue(cnt, nuevo), run_time=0.9)
            self.cap(nota, VERDE_CL)
            w = w2
        self.play(m.Circumscribe(cnt, color=m.YELLOW), m.Flash(barra.get_right(), color=VERDE_CL), run_time=0.9)
        self.play(m.FadeOut(m.VGroup(barra, cnt)), run_time=0.5)
        self.card("Error común",
                  lineas(tex(r"\varphi(4) = 2\neq \varphi(2)\,\varphi(2) = 1", 30, ROJO_CL),
                         ttex(r"Multiplicativa \textbf{solo} con factores coprimos.", 26)),
                  C_TRAMPA, corner=m.DR, shift=np.array([0, 1.3, 0]))
        self.cap("Ojo: φ(mn) = φ(m)φ(n) solo si m y n son coprimos. Con 4 = 2·2 no funciona", ROJO_CL)

    # ── 16. Euler ────────────────────────────────────────────────────────────
    def euler(self):
        self.chapter(16)
        self.card("Teorema de Euler", tex(r"\mcd(a,n)=1\ \Rightarrow\ a^{\varphi(n)}\equiv 1\md n", 36, m.YELLOW),
                  C_TEOREMA, corner=m.UL)
        self.cap("La prueba es la misma de Fermat, pero solo con los residuos que tienen inverso. Veámoslo con "
                 "n = 10 y a = 3")
        n, a = 10, 3
        units = [1, 3, 7, 9]
        cx, cz, R = 1.6, -0.5, 1.6
        pos = {u: en_circulo(i, 4, R, cx, cz) for i, u in enumerate(units)}
        cols = {1: AZUL, 3: NARANJA, 7: VERDE, 9: MORADO}
        balls = {u: esfera(pos[u], cols[u], r=0.34) for u in units}
        labs = {u: etiqueta(str(u), pos[u], 28, m.WHITE, dy=-0.37) for u in units}
        self.play(*(m.FadeIn(b) for b in balls.values()), *(m.FadeIn(l) for l in labs.values()), run_time=0.8)
        self.cap("Los coprimos con 10 son 1, 3, 7 y 9, así que φ(10) = 4. Multipliquemos cada uno por 3")
        dest = {u: a * u % n for u in units}
        self.play(*(balls[u].animate.move_to(pos[dest[u]]) for u in units), *(m.FadeOut(l) for l in labs.values()),
                  run_time=2.0)
        new = {u: etiqueta(str(dest[u]), pos[dest[u]], 28, m.WHITE, dy=-0.37) for u in units}
        self.play(*(m.FadeIn(l) for l in new.values()), run_time=0.6)
        self.cap("3, 9, 21 y 27 son 3, 9, 1 y 7 módulo 10: los mismos cuatro en otro orden. Así que 3⁴ por el "
                 "producto es igual al producto, y 3⁴ ≡ 1. De hecho 81 ≡ 1 módulo 10", VERDE_CL)
        self.clear_stage()

        self.card("Teorema de Euler", tex(r"a^{\varphi(n)}\equiv 1\md n", 34, m.YELLOW), C_TEOREMA, corner=m.UL,
                  write=False)
        self.cap("Ejemplo: el residuo de 2 a la 118 módulo 119. 119 no es primo, así que Fermat no "
                 "aplica, pero Euler sí")
        res = self.barra_exponente(r"2^{118}\bmod 119", 1, "96", "22", r"\equiv 2^{22}", np.array([0.2, -0.3, 0]),
                                   ancho=8.0, notas=(
            "φ(119) = 96, así que el exponente 118 es un bloque de 96 más un resto de 22",
            "Por Euler, el bloque de 96 vale 1",
            "Queda 2 a la 22. Ahora a calcularlo",
        ))
        self.play(m.FadeOut(res), run_time=0.5)
        self.derivar([
            r"\varphi(119)=96,\quad \mcd(2,119)=1",
            r"2^{118}=2^{96}\cdot 2^{22}\equiv 2^{22}",
            r"2^7=128\equiv 9,\quad 2^{11}=2^7\cdot 2^4\equiv 9\cdot 16=144\equiv 25",
            r"2^{22}=(2^{11})^2\equiv 25^2=625=5\cdot 119+30\equiv 30",
        ], anchor=np.array([-6.6, 1.3, 0]), size=32, notas=[
            "φ(119) = 96 y 2 es coprimo con 119",
            "Se quita el 96 del exponente y queda 2 a la 22",
            "Se calcula 2 a la 11 por partes",
            "Y se eleva al cuadrado. El residuo es 30",
        ])
        self.clear_stage()
        self.card("Últimas tres cifras = residuo mod 1000", tex(r"7^{2407}\bmod 1000", 34), C_ESQ, corner=m.UL)
        res = self.barra_exponente(r"7^{2407}\bmod 1000", 6, "400", "7", r"\equiv 7^{7}", np.array([0.2, -0.3, 0]),
                                   ancho=9.0, notas=(
            "Las últimas tres cifras de 7 a la 2407. φ(1000) = 400, y 2407 son seis bloques de 400 más 7",
            "Cada bloque de 400 vale 1 por Euler",
            "Quedan 7 a la 7",
        ))
        self.play(m.FadeOut(res), run_time=0.5)
        self.derivar([
            r"\varphi(1000)=400,\quad 2407 = 6\cdot 400 + 7",
            r"7^{2407}\equiv 7^7 \md{1000}",
            r"7^4=2401\equiv 401,\quad 7^3=343",
            r"7^7\equiv 401\cdot 343 = 137543\equiv 543",
        ], anchor=np.array([-6.6, 1.3, 0]), size=34, notas=[
            "Las últimas tres cifras son el residuo módulo 1000, y φ(1000) = 400",
            "El exponente se reduce módulo 400 y queda 7",
            "7 a la 4 es 2401, que termina en 401",
            "Se multiplica por 343 y las últimas tres cifras son 543",
        ])
        self.card("Regla de 1 segundo",
                  ttex(r"Últimas $k$ cifras $\to$ mod $10^k$, con $\varphi(10^k)=4\cdot 10^{k-1}$", 26),
                  C_REGLA, corner=m.DR, shift=np.array([0, 1.3, 0]))
        self.wait(2.5)

    # ── 17. autoinversos ─────────────────────────────────────────────────────
    def autoinversos(self):
        self.chapter(17)
        self.card("La pregunta", ttex(r"¿Cuántos $a$ cumplen $a^2\equiv 1$? En los reales solo $\pm 1$.", 28),
                  C_INT, corner=m.UL)
        self.derivar([
            r"a^2\equiv 1\md p\iff p\mid (a-1)(a+1)",
            r"\iff p\mid a-1\ \vee\ p\mid a+1",
            r"\iff a\equiv \pm 1",
        ], anchor=np.array([-6.6, 1.3, 0]), size=34, notas=[
            "Con un primo impar, se factoriza la diferencia de cuadrados",
            "Por el lema de Euclides, p divide a uno de los dos factores",
            "Así que hay exactamente dos soluciones, 1 y −1, igual que en los reales",
        ])
        self.cap("Pero con potencias de 2 pasa algo raro. Miremos módulo 16")
        n = 16
        cx, cz, R = 2.6, -0.6, 1.65
        dots = [esfera(en_circulo(k, n, R, cx, cz), GRIS_OSC, r=0.17) for k in range(n)]
        labs = [etiqueta(str(k), en_circulo(k, n, R + 0.4, cx, cz), 20, m.GREY_A) for k in range(n)]
        self.play(*(m.FadeIn(d) for d in dots), *(m.FadeIn(l) for l in labs), run_time=0.8)
        sols = [k for k in range(n) if k * k % n == 1]
        self.play(*(dots[k].animate.set_color(m.YELLOW).scale(1.5) for k in sols), run_time=0.8)
        self.cap("Hay cuatro: 1, 7, 9 y 15. Por ejemplo, 7² = 49 = 3·16 + 1 y 9² = 81 = 5·16 + 1", m.YELLOW)
        self.clear_stage()

        self.card("Módulo 2ⁿ, n ≥ 3", tex(r"a^2\equiv 1\md{2^n}\iff a\equiv \pm 1,\ 2^{n-1}\pm 1", 34),
                  C_TEOREMA, corner=m.UL)
        self.derivar([
            r"2^n\mid (a-1)(a+1),\quad a\ \text{impar}",
            r"\mcd(a-1,a+1)=\mcd(a-1,2)=2",
            r"\text{uno tiene un solo } 2\ \Rightarrow\ 2^{n-1}\mid a-1\ \ \text{o}\ \ 2^{n-1}\mid a+1",
            r"a\equiv 1,\ 2^{n-1}+1\quad\text{o}\quad a\equiv 2^{n-1}-1,\ -1",
        ], anchor=np.array([-6.6, 1.25, 0]), size=32, notas=[
            "a tiene que ser impar, así que a − 1 y a + 1 son pares consecutivos",
            "Como mcd(x, y) = mcd(x, y − x), su mcd es 2",
            "Comparten un solo factor 2, así que uno de los dos tiene exactamente un 2 y el otro carga todos los "
            "demás, al menos n − 1",
            "Eso da dos opciones para cada caso: cuatro soluciones en total",
        ])
        self.clear_stage()

        self.card("Módulo 100 = 4 · 25",
                  lineas(tex(r"\bmod 4:\ \{1,3\}\qquad \bmod 25:\ \{1,24\}", 30),
                         tex(r"\Rightarrow\ \{1,49,51,99\}", 32, m.YELLOW)), C_ESQ, corner=m.UL)
        self.cap("Con módulos compuestos se usa el TCR: dos soluciones módulo 4 y dos módulo 25 dan cuatro módulo "
                 "100")
        tabla = m.MathTable([["1", "49"], ["51", "99"]],
                            row_labels=[tex("1", 36, NARANJA), tex("3", 36, NARANJA)],
                            col_labels=[tex("1", 36, AZUL), tex("24", 36, AZUL)],
                            include_outer_lines=False, h_buff=0.9, v_buff=0.55, line_config={"stroke_color": GRIS})
        tabla.move_to([4.5, -0.45, 0])
        h25 = tex(r"\bmod 25", 30, AZUL).next_to(tabla, m.UP, buff=0.2).shift(0.45 * m.RIGHT)
        h4 = tex(r"\bmod 4", 30, NARANJA).next_to(tabla, m.LEFT, buff=0.2).shift(0.4 * m.DOWN)
        celdas = tabla.get_entries_without_labels()
        self.pin(tabla, h25, h4)
        self.remove(tabla, h25, h4)
        self.play(m.Create(tabla.get_horizontal_lines()), m.Create(tabla.get_vertical_lines()),
                  m.FadeIn(tabla.get_labels()), m.FadeIn(h25), m.FadeIn(h4), run_time=0.9)
        self.play(m.LaggedStart(*(m.FadeIn(c, scale=0.5) for c in celdas), lag_ratio=0.3), run_time=1.4)
        self.play(*(c.animate.set_color(m.YELLOW) for c in celdas),
                  m.LaggedStart(*(m.Flash(c, color=m.YELLOW, flash_radius=0.3) for c in celdas), lag_ratio=0.2),
                  run_time=1.2)
        self.cap("Cada casilla combina una solución módulo 4 con una módulo 25. Por ejemplo, 49 es 1 módulo 4 y 24 "
                 "módulo 25", m.YELLOW)
        self.derivar([
            r"\prod_{\mcd(a,100)=1} a\ \equiv\ 1\cdot 49\cdot 51\cdot 99",
            r"\equiv 1\cdot(-51)\cdot 51\cdot(-1) = 51^2 = 2601",
            r"\equiv 1\md{100}",
        ], anchor=np.array([-6.6, 0.6, 0]), size=34, notas=[
            "Para el producto de los 40 residuos coprimos con 100 se usa la idea de Wilson: los que tienen pareja "
            "se cancelan y quedan solo los autoinversos",
            "49 es −51 y 99 es −1",
            "Y 51² = 2601 termina en 01. El producto es 1, no −1: Wilson no se cumple aquí porque hay cuatro "
            "autoinversos en vez de dos",
        ])
        self.clear_stage()
        self.card("Módulo 3600 = 2⁴ · 3² · 5²",
                  lineas(tex(r"\bmod 16:\{1,7,9,15\},\quad \bmod 9:\{1,8\},\quad \bmod 25:\{1,24\}", 28),
                         tex(r"4\cdot 2\cdot 2 = 16\ \text{soluciones}", 30, m.YELLOW)), C_ESQ, corner=m.UL)
        sols = [a for a in range(3600) if a * a % 3600 == 1]
        grid = m.VGroup(*(tex(str(s), 30, VERDE_CL) for s in sols)).arrange_in_grid(rows=4, cols=4, buff=(0.7, 0.3))
        grid.move_to([0.4, -0.3, 0])
        self.pin(grid)
        self.play(m.LaggedStart(*(m.FadeIn(g, scale=0.6) for g in grid), lag_ratio=0.08), run_time=2.0)
        self.cap("Y con 3600: cuatro módulo 16, dos módulo 9 y dos módulo 25, así que 16 soluciones. El TCR con "
                 "C = 225, 2800 y 576 da todas, y coinciden con una búsqueda por computador", VERDE_CL)

    # ── 18. RSA ──────────────────────────────────────────────────────────────
    def rsa(self):
        self.chapter(18)
        self.card("La pregunta",
                  ttex(r"¿Cómo me cifran un mensaje con una clave \textbf{pública} que solo yo puedo descifrar?", 28),
                  C_INT, corner=m.UL)

        def caja3d(text, x, z, col, w=2.2, is_tex=True):
            sl = m.Prism(dimensions=[w, 0.5, 0.9], fill_color=col, fill_opacity=1, stroke_width=0).move_to(P(x, z))
            lab = etiqueta(text, P(x, z), 34, m.WHITE, is_tex=is_tex, dy=-0.28)
            return m.Group(sl, lab)

        b1 = caja3d(r"M = 7", -4.6, 0.2, AZUL_OSC)
        b2 = caja3d(r"C = 13", 0.0, 0.2, ROJO)
        b3 = caja3d(r"M = 7", 4.6, 0.2, VERDE)
        a1 = m.Arrow3D(P(-3.4, 0.2), P(-1.2, 0.2), color=BORDE, thickness=0.03)
        a2 = m.Arrow3D(P(1.2, 0.2), P(3.4, 0.2), color=BORDE, thickness=0.03)
        l1 = etiqueta(r"C = M^{e}\bmod n", P(-2.3, 0.85), 30, AMBAR, is_tex=True)
        l2 = etiqueta(r"M = C^{d}\bmod n", P(2.3, 0.85), 30, VERDE_CL, is_tex=True)
        k1 = etiqueta(r"\text{pública: } (n,e) = (55, 3)", P(-2.3, -0.75), 26, AMBAR, is_tex=True)
        k2 = etiqueta(r"\text{privada: } d = 27", P(2.3, -0.75), 26, VERDE_CL, is_tex=True)
        self.play(m.FadeIn(b1, shift=0.3 * m.IN), run_time=0.7)
        self.cap("Este es el recorrido. Cualquiera cifra el mensaje M con la clave pública: lo eleva a e módulo n")
        self.play(m.Create(a1), m.FadeIn(l1), m.FadeIn(k1), run_time=0.8)
        self.play(m.FadeIn(b2, shift=0.3 * m.IN), run_time=0.7)
        self.cap("Sale C. Para recuperar M se eleva C a d, y solo quien conoce d puede hacerlo")
        self.play(m.Create(a2), m.FadeIn(l2), m.FadeIn(k2), run_time=0.8)
        self.play(m.FadeIn(b3, shift=0.3 * m.IN), run_time=0.7)
        self.swing(theta=-62, phi=66, run_time=2.0)
        self.clear_stage()

        self.card("Generación de claves",
                  lineas(ttex(r"1. Primos $p,q$; $\ n=pq$, $\ \varphi(n)=(p-1)(q-1)$", 26),
                         ttex(r"2. $e$ con $\mcd(e,\varphi(n))=1$", 26),
                         ttex(r"3. $d\equiv e^{-1}\md{\varphi(n)}$", 26),
                         ttex(r"4. Pública $(n,e)$, privada $d$", 26)), C_ESQ, corner=m.UL)
        self.derivar([
            r"p=5,\ q=11,\quad n=55,\quad \varphi(n)=4\cdot 10=40",
            r"e=3,\quad \mcd(3,40)=1",
            r"40 = 13\cdot 3 + 1\ \Rightarrow\ 1 = 40 - 13\cdot 3",
            r"d\equiv -13\equiv 27\md{40}\quad (3\cdot 27 = 81 = 2\cdot 40+1)",
            r"C = 7^3 = 343 = 6\cdot 55 + 13\ \Rightarrow\ C = 13",
        ], anchor=np.array([-0.4, 2.05, 0]), size=30, notas=[
            "Un ejemplo con números pequeños. p = 5 y q = 11, así que n = 55 y φ(n) = 40",
            "Se elige e = 3, que es coprimo con 40",
            "d es el inverso de 3 módulo 40. Con Euclides extendido sale en una línea",
            "d = 27. Comprobación: 3·27 = 81, que es 1 módulo 40",
            "Para cifrar M = 7 se calcula 7³ = 343, que es 13 módulo 55",
        ])
        self.clear_stage()

        self.card("Descifrar: 13²⁷ mod 55 con el TCR",
                  ttex(r"$55 = 5\cdot 11$: se calcula por separado y se junta.", 26), C_ESQ, corner=m.UL)
        self.derivar([
            r"\bmod 5:\ 13\equiv 3,\quad 3^{27}=3^{4\cdot 6+3}\equiv 3^3=27\equiv 2",
            r"\bmod 11:\ 13\equiv 2,\quad 2^{27}=2^{10\cdot 2+7}\equiv 2^7=128\equiv 7",
            r"x\equiv 2\,(5),\ x\equiv 7\,(11)\ \Rightarrow\ x = 7",
        ], anchor=np.array([-6.6, 1.3, 0]), size=32, notas=[
            "Módulo 5, por Fermat, el exponente se reduce módulo 4 y sale 2",
            "Módulo 11, el exponente se reduce módulo 10 y sale 7",
            "Se juntan con el TCR. El número que es 2 módulo 5 y 7 módulo 11 es 7. Recuperamos el mensaje",
        ])
        self.card("Por qué funciona",
                  lineas(tex(r"ed = 1 + k(p-1)(q-1)", 30),
                         tex(r"M^{ed} = M\cdot (M^{p-1})^{k(q-1)}\equiv M \md p", 30),
                         ttex(r"igual mod $q$, y por el TCR $M^{ed}\equiv M \md{pq}$", 26)),
                  C_TEOREMA, corner=m.DR, shift=np.array([0, 1.3, 0]))
        self.cap("Y en general funciona porque ed es 1 más un múltiplo de p − 1 y de q − 1. Por Fermat da M módulo "
                 "p y módulo q, y por el TCR da M módulo n")
        self.clear_stage()
        self.card("Error común",
                  lineas(ttex(r"$d$ es inverso de $e$ módulo $\varphi(n)$, \textbf{no} módulo $n$.", 30),
                         tex(r"3^{-1}\bmod 55 = 37,\qquad 13^{37}\bmod 55 = 18 \neq 7", 32, ROJO_CL)),
                  C_TRAMPA, corner=None, shift=np.array([0, 0.6, 0]))
        self.cap("Si alguien calcula d módulo n, sale 37, y al descifrar da 18 en vez de 7. Los exponentes viven "
                 "módulo φ(n) y las bases módulo n", ROJO_CL)

    # ── 19. mapa ─────────────────────────────────────────────────────────────
    def mapa(self):
        self.chapter(19)
        self.cap("Para cerrar, el mapa de decisión: qué herramienta usar según lo que pida el problema")
        filas = [
            ("mcd con números grandes", "Euclides: último residuo no nulo"),
            (r"$s,t$ con $sa+tb=\mcd$", "Euclides extendido"),
            (r"$a^{-1}\bmod m$", r"$\mcd=1$ y Bézout; si $m$ primo, $a^{m-2}$"),
            (r"$ax\equiv b\md m$", r"$d=\mcd(a,m)$; si $d\mid b$, $d$ soluciones"),
            ("sistema, módulos coprimos", r"TCR: $\sum a_iM_iy_i$"),
            ("sistema, módulos no coprimos", "partir en primos y buscar choques"),
            (r"$a^E\bmod p$, $p$ primo", r"Fermat: $E\bmod (p-1)$"),
            (r"$a^E\bmod n$, $\mcd(a,n)=1$", r"Euler: $E\bmod\varphi(n)$, o TCR"),
            (r"$k!\bmod p$", r"Wilson y quitar factores"),
            (r"últimas $k$ cifras", r"mod $10^k$ con Euler"),
        ]
        y0 = 2.5
        rows = []
        for i, (q, a) in enumerate(filas):
            y = y0 - 0.52 * i
            left = ttex(q, 29, m.WHITE)
            right = ttex(a, 29, VERDE_CL)
            left.move_to([-3.6, y, 0])
            right.move_to([2.6, y, 0])
            arr = m.Arrow([-1.2, y, 0], [-0.6, y, 0], buff=0, color=BORDE, stroke_width=3,
                          max_tip_length_to_length_ratio=0.35)
            bg = m.Rectangle(width=13.6, height=0.46, fill_color=PANEL_BG if i % 2 else "#161B22", fill_opacity=0.9,
                             stroke_width=0).move_to([0, y, 0])
            rows.append((bg, left, arr, right))
        hdr = m.VGroup(m.Text("Si el problema pide…", font_size=28, color=m.YELLOW).move_to([-3.6, 3.05, 0]),
                       m.Text("usa…", font_size=28, color=m.YELLOW).move_to([2.6, 3.05, 0]))
        self.pin(hdr)
        self.play(m.FadeIn(hdr), run_time=0.5)
        for bg, left, arr, right in rows:
            self.pin(bg, left, arr, right)
            self.play(m.FadeIn(bg), m.FadeIn(left, shift=0.2 * m.RIGHT), run_time=0.35)
            self.play(m.GrowArrow(arr), m.FadeIn(right, shift=0.2 * m.RIGHT), run_time=0.45)
        self.uncap()
        self.wait(4)
        self.clear_stage()

        trampas = [
            "Residuo negativo en la división: siempre 0 ≤ r < d",
            "sa + tb = g no implica g = mcd, salvo con g = 1",
            "Cancelar sin revisar el mcd: se divide también el módulo",
            "Fermat con módulo compuesto",
            "TCR con módulos no coprimos sin revisar choques",
            "φ(mn) = φ(m)φ(n) sin coprimalidad",
            "En RSA, d módulo n en vez de módulo φ(n)",
            "En ax ≡ b, dar una sola solución cuando hay d",
            "Decir que p₁···pₖ + 1 es primo",
        ]
        head = m.Text("Los errores comunes, todos juntos", font_size=36, color=ROJO_CL)
        items = m.VGroup(*(m.Text(f"{i + 1}.  {t}", font_size=26) for i, t in enumerate(trampas))).arrange(
            m.DOWN, aligned_edge=m.LEFT, buff=0.22)
        g = m.VGroup(head, items).arrange(m.DOWN, buff=0.4).move_to([0, 0.1, 0])
        self.pin(g)
        self.play(m.Write(head), run_time=0.8)
        self.play(m.LaggedStart(*(m.FadeIn(i, shift=0.2 * m.RIGHT) for i in items), lag_ratio=0.3), run_time=3.5)
        self.wait(6)
