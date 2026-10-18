"""Teoría de números, módulo 3: congruencias, cancelación, congruencias lineales, TCR, Fermat y Wilson.

    manimgx render modulo3_congruencias.py Modulo3
"""

import math

import manimgx as m
import numpy as np

from comun import (AMBAR, AZUL, AZUL_OSC, BORDE, C_DEF, C_ESQ, C_INT, C_REGLA, C_TEOREMA, C_TRAMPA, GRIS,
                   GRIS_OSC, MORADO, NARANJA, ROJO, ROJO_CL, TEAL, VERDE, VERDE_CL, Clase, P, cubo, esfera,
                   etiqueta, lineas, losa, recta, tex, ttex, txt, up)

CLASES = [AZUL, NARANJA, VERDE, MORADO, AMBAR, TEAL, ROJO_CL]


def en_circulo(k: int, n: int, R: float, cx: float = 0.0, cz: float = 0.0, y: float = 0.0):
    """Posición k de n sobre un círculo de pie frente a la cámara, empezando arriba y en sentido horario."""
    ang = math.pi / 2 - 2 * math.pi * k / n
    return P(cx + R * math.cos(ang), cz + R * math.sin(ang), y)


class Modulo3(Clase):
    START = 9
    CHAPTERS = [
        "Congruencias: aritmética de reloj",
        "Álgebra de congruencias y cancelación",
        "Congruencias lineales ax ≡ b",
        "El Teorema Chino del Residuo",
        "El Pequeño Teorema de Fermat",
        "El Teorema de Wilson",
    ]

    def construct(self) -> None:
        self.setup_hud()
        self.intro()
        self.reloj()
        self.algebra()
        self.lineales()
        self.tcr()
        self.fermat()
        self.wilson()
        self.cierre([
            "a ≡ b (mod m)  significa  m | a − b; hay m clases, una por residuo",
            "Sumar, multiplicar y elevar respetan ≡; dividir solo con mcd(c, m) = 1 (o se divide el módulo)",
            "ax ≡ b (mod m) tiene solución si y solo si d = mcd(a, m) divide a b, y entonces hay d soluciones",
            "TCR: con módulos coprimos hay una única solución mod M, la suma de los términos a·M·y",
            "Fermat: a^(p−1) ≡ 1 (mod p), así que el exponente se reduce mod p − 1",
            "Wilson: (p − 1)! ≡ −1 (mod p), porque todos los demás se cancelan en parejas",
        ], "En el módulo 4 Fermat se generaliza a cualquier módulo con la función φ, y con eso funciona RSA")

    def intro(self):
        self.home()
        self.titulo_video("Teoría de números · Módulo 3", "congruencias, Teorema Chino, Fermat y Wilson")
        self.cap("Este es el módulo más largo y el centro del tema. Todo lo que sigue es aritmética "
                 "en la que solo importa el residuo")

    # ── 9. reloj ─────────────────────────────────────────────────────────────
    def reloj(self):
        self.chapter(9)
        self.card("Definición",
                  tex(r"a\equiv b\md{m}\iff m\mid a-b\iff a\bmod m = b\bmod m", 32), C_DEF, corner=m.UL)
        self.cap("Dos números son congruentes módulo m cuando su diferencia es múltiplo de m. Es lo mismo que "
                 "decir que dejan el mismo residuo")
        n_mod, N = 5, 20
        cx, cz = 1.3, -0.35
        balls, labs = [], []
        line_pos = [P(-5.7 + 0.6 * k, 1.4) for k in range(N)]
        for k in range(N):
            b = esfera(line_pos[k], GRIS, r=0.22)
            lab = etiqueta(str(k), line_pos[k], 20, m.WHITE, dy=-0.25)
            balls.append(b)
            labs.append(lab)
        self.play(m.LaggedStart(*(m.FadeIn(m.Group(b, l)) for b, l in zip(balls, labs)), lag_ratio=0.04),
                  run_time=1.6)
        self.cap("Pongamos los enteros en fila. Ahora vamos a enrollar la fila como un resorte, con 5 posiciones "
                 "por vuelta")
        anims = []
        for k in range(N):
            R = 0.75 + 0.48 * (k // n_mod)
            pos = en_circulo(k % n_mod, n_mod, R, cx, cz)
            anims.append(balls[k].animate.move_to(pos).set_color(CLASES[k % n_mod]))
            anims.append(labs[k].animate.move_to(pos + np.array([0, -0.25, 0])))
        self.play(*anims, run_time=2.6)
        self.cap("Cada número gira un quinto de vuelta respecto al anterior y se aleja un poco del centro. "
                 "Los que quedan en el mismo rayo son congruentes módulo 5", m.YELLOW)
        cls = [etiqueta(f"[{r}]", en_circulo(r, n_mod, 0.75 + 0.48 * 4 + 0.15, cx, cz), 30, CLASES[r])
               for r in range(n_mod)]
        self.play(*(m.FadeIn(c) for c in cls), run_time=0.8)
        self.cap("Cada rayo es una clase. Por ejemplo, la clase del 2 es {…, −3, 2, 7, 12, 17, …}. Hay exactamente "
                 "5 clases, una por cada residuo posible")
        self.move_camera(phi=60 * m.DEGREES, theta=-62 * m.DEGREES, run_time=2.0)
        spin = [b.animate.shift(-0.12 * (k // n_mod) * m.DOWN) for k, b in enumerate(balls)]
        self.play(*spin, run_time=1.0)
        self.home(run_time=1.6)
        thm = self.card("Relación de equivalencia",
                        lineas(tex(r"\text{reflexiva: } m\mid 0", 28),
                               tex(r"\text{simétrica: } m\mid a-b\Rightarrow m\mid b-a", 28),
                               tex(r"\text{transitiva: } m\mid (a-b)+(b-c) = a-c", 28)), C_TEOREMA, corner=m.DR,
                        shift=np.array([0, 1.3, 0]))
        self.cap("Es una relación de equivalencia. Las tres propiedades salen directo de la divisibilidad, y por "
                 "eso parte a los enteros en clases que no se cruzan")

    # ── 10. álgebra ──────────────────────────────────────────────────────────
    def algebra(self):
        self.chapter(10)
        self.card("Teorema",
                  lineas(tex(r"a\equiv b,\ c\equiv d \md{m}\ \Rightarrow", 30),
                         tex(r"a+c\equiv b+d,\quad ac\equiv bd,\quad a^k\equiv b^k,\quad P(a)\equiv P(b)", 30)),
                  C_TEOREMA, corner=m.UL)
        self.cap("Sumar, multiplicar y elevar a potencias respeta la congruencia. La suma es inmediata. Para el "
                 "producto hay un truco: sumar y restar lo mismo")
        self.derivar([
            r"ac - bd",
            r"= ac - bc + bc - bd",
            r"= c\,(a-b) + b\,(c-d)",
            r"m\mid a-b,\ m\mid c-d\ \Rightarrow\ m\mid ac-bd",
        ], anchor=np.array([-6.6, 1.0, 0]), size=34, notas=[
            "Queremos ver que m divide a ac − bd",
            "Se suma y se resta bc, que no cambia nada",
            "Se agrupa de a dos y se factoriza",
            "Cada pedazo tiene un factor que m divide. Por combinación lineal, m divide a todo",
        ])
        u = 0.72
        A, B, Cc, D = 5, 3, 4, 2
        org = np.array([1.9, -1.75, 0])

        def rect(x, y, w, h, col, op=0.85):
            return m.Rectangle(width=w * u, height=h * u, fill_color=col, fill_opacity=op, stroke_color=m.WHITE,
                               stroke_width=2).move_to(org + np.array([(x + w / 2) * u, (y + h / 2) * u, 0]))

        total = rect(0, 0, A, Cc, GRIS_OSC, 0.0)
        bd = rect(0, 0, B, D, GRIS, 0.6)
        der_ = rect(B, 0, A - B, Cc, NARANJA)
        arr_ = rect(0, D, B, Cc - D, AZUL_OSC)
        l_ac = tex(r"ac", 34).move_to(total)
        l_bd = tex(r"bd", 30).move_to(bd)
        l_der = tex(r"c(a-b)", 26).move_to(der_)
        l_arr = tex(r"b(c-d)", 28).move_to(arr_)
        b_a = m.BraceLabel(total, "a", brace_direction=m.DOWN, font_size=28)
        b_c = m.BraceLabel(total, "c", brace_direction=m.RIGHT, font_size=28)
        self.pin(total, l_ac, b_a, b_c)
        self.remove(total, l_ac, b_a, b_c)
        self.play(m.Create(total), m.Write(l_ac), m.FadeIn(b_a), m.FadeIn(b_c), run_time=1.0)
        self.pin(bd, l_bd)
        self.remove(bd, l_bd)
        self.play(m.FadeOut(l_ac), m.DrawBorderThenFill(bd), m.FadeIn(l_bd), run_time=0.9)
        self.cap("Como área: ac es el rectángulo grande y bd es el gris de la esquina. ac − bd es lo que queda "
                 "al quitarlo")
        b_ab = m.BraceLabel(der_, "a-b", brace_direction=m.UP, font_size=28, color=NARANJA)
        b_cd = m.BraceLabel(arr_, "c-d", brace_direction=m.LEFT, font_size=28, color=AZUL)
        self.pin(der_, arr_, l_der, l_arr, b_ab, b_cd)
        self.remove(der_, arr_, l_der, l_arr, b_ab, b_cd)
        self.play(m.FadeOut(bd), m.FadeOut(l_bd), m.DrawBorderThenFill(der_), m.DrawBorderThenFill(arr_),
                  run_time=1.2)
        self.play(m.Write(l_der), m.Write(l_arr), m.GrowFromCenter(b_ab), m.GrowFromCenter(b_cd), run_time=1.0)
        self.cap("Lo que queda se parte en dos tiras: la naranja tiene un lado a − b y la azul un lado c − d. Las "
                 "dos son múltiplos de m, así que la suma también")
        self.play(m.FadeOut(m.VGroup(total, der_, arr_, l_der, l_arr, b_a, b_c, b_ab, b_cd)), run_time=0.6)
        ej = self.card("Consecuencia práctica",
                       lineas(ttex(r"Se puede reducir en \emph{cualquier} paso:", 26),
                              tex(r"27 = 9\cdot 3\equiv 4\cdot 3 = 12\equiv 2 \md{5}", 30, VERDE_CL)),
                       C_ESQ, corner=m.UR, shift=np.array([0, -1.6, 0]))
        self.cap("Eso es lo que hace útil todo esto: en medio de una cuenta se puede cambiar cualquier número por "
                 "su residuo")
        self.clear_stage()

        self.cap("¿Y dividir? Aquí está el error más común", m.YELLOW)
        self.card("Teorema (cancelación)",
                  lineas(tex(r"ac\equiv bc\md{m}\ \Rightarrow\ a\equiv b\md{\tfrac{m}{\mcd(c,m)}}", 34),
                         ttex(r"Si $\mcd(c,m)=1$ se cancela sin cambiar el módulo.", 26)), C_TEOREMA, corner=m.UL)
        self.derivar([
            r"g=\mcd(c,m),\quad c = gc',\ m = gm',\ \mcd(c',m')=1",
            r"gm'\mid gc'(a-b)",
            r"m'\mid c'(a-b)",
            r"m'\mid a-b",
        ], anchor=np.array([-6.6, 0.9, 0]), size=32, notas=[
            "Se saca el factor común g de c y de m. Lo que queda, c' y m', es coprimo",
            "La hipótesis dice que m divide a c(a − b)",
            "Se cancela g en los dos lados, que es una división de enteros normal",
            "Y como m' y c' son coprimos, por el lema de divisibilidad coprima, m' divide a a − b",
        ])
        self.clear_stage()

        # el error, visto en el reloj de 6
        self.card("Error común",
                  lineas(tex(r"4\cdot 0\equiv 4\cdot 3 \md{6}\quad (0\equiv 12)", 30),
                         tex(r"0\not\equiv 3\md{6}\quad\text{pero}\quad 0\equiv 3\md{3}", 30, ROJO_CL)),
                  C_TRAMPA, corner=m.UL)
        cx, cz, R = 2.4, -0.2, 1.6
        dots = [esfera(en_circulo(k, 6, R, cx, cz), GRIS, r=0.25) for k in range(6)]
        labs = [etiqueta(str(k), en_circulo(k, 6, R, cx, cz), 24, m.WHITE, dy=-0.3) for k in range(6)]
        self.play(*(m.FadeIn(d) for d in dots), *(m.FadeIn(l) for l in labs), run_time=0.8)
        self.cap("Miremos el reloj de 6. Multiplicar por 4 manda el 0 al 0 y el 3 al 12, que también es 0")
        for src in (0, 3):
            self.play(m.Indicate(dots[src], color=AMBAR, scale_factor=1.5), run_time=0.6)
        self.play(dots[0].animate.set_color(ROJO_CL), dots[3].animate.set_color(ROJO_CL), run_time=0.6)
        self.cap("Dos números distintos módulo 6 terminan en el mismo lugar. Multiplicar por 4 los pegó, así que "
                 "no se puede deshacer dividiendo entre 4", ROJO_CL)
        self.cap("Lo que sí se puede decir es que 0 ≡ 3 módulo 6/mcd(4, 6) = 3. Se pierde el factor común 2 del "
                 "módulo", ROJO_CL)

    # ── 11. congruencias lineales ────────────────────────────────────────────
    def lineales(self):
        self.chapter(11)
        self.card("Teorema",
                  lineas(tex(r"d=\mcd(a,m):\quad ax\equiv b\md{m}\ \text{tiene solución}\iff d\mid b", 30),
                         ttex(r"y en ese caso hay \textbf{exactamente $d$} soluciones mod $m$.", 26)),
                  C_TEOREMA, corner=m.UL)
        self.cap("¿Cuándo tiene solución ax ≡ b? Miremos a dónde va 6x módulo 15 cuando x recorre 0, 1, …, 14")
        n = 15
        cx, cz, R = 0.8, -0.55, 1.75
        dots = [esfera(en_circulo(k, n, R, cx, cz), GRIS_OSC, r=0.17) for k in range(n)]
        labs = [etiqueta(str(k), en_circulo(k, n, R + 0.42, cx, cz), 20, m.GREY_A) for k in range(n)]
        self.play(*(m.FadeIn(d) for d in dots), *(m.FadeIn(l) for l in labs), run_time=0.9)
        stacks = {k: 0 for k in range(n)}
        chips = []
        for x in range(n):
            v = 6 * x % n
            stacks[v] += 1
            pos = en_circulo(v, n, R - 0.38 * stacks[v], cx, cz)
            c = esfera(pos, AMBAR, r=0.14)
            chips.append(c)
            self.play(m.FadeIn(c, scale=0.3), m.Indicate(dots[v], color=AMBAR), run_time=0.28)
        self.cap("Solo cae en 0, 3, 6, 9 y 12, los múltiplos de 3 = mcd(6, 15), y cae tres veces en cada uno", m.YELLOW)
        hits9 = [x for x in range(n) if 6 * x % n == 9]
        self.play(dots[9].animate.set_color(VERDE_CL), run_time=0.5)
        self.cap(f"Así que 6x ≡ 9 tiene tres soluciones, x = {hits9[0]}, {hits9[1]} y {hits9[2]}. "
                 "En cambio 6x ≡ 10 no tiene ninguna, porque 3 no divide a 10", VERDE_CL)
        self.play(dots[10].animate.set_color(ROJO_CL), run_time=0.5)
        self.move_camera(phi=62 * m.DEGREES, theta=-68 * m.DEGREES, run_time=1.8)
        self.home(run_time=1.4)
        self.clear_stage()

        self.card("Procedimiento", lineas(
            ttex(r"1. $d=\mcd(a,m)$. Si $d\nmid b$, no hay solución.", 26),
            ttex(r"2. Dividir todo entre $d$: $\tfrac ad x\equiv \tfrac bd \md{\tfrac md}$", 26),
            ttex(r"3. $x_0 = (a/d)^{-1}(b/d)\bmod \tfrac md$", 26),
            ttex(r"4. Soluciones: $x_0 + k\tfrac md$, $k=0,\dots,d-1$", 26)), C_ESQ, corner=m.UL)
        self.cap("Este es el procedimiento. Hagámoslo con 6x ≡ 9 módulo 15")
        self.derivar([
            r"d=\mcd(6,15)=3,\quad 3\mid 9\ \checkmark",
            r"2x\equiv 3\md{5}",
            r"2^{-1}\equiv 3\md 5\ \Rightarrow\ x_0\equiv 9\equiv 4\md 5",
            r"x\equiv 4,\ 9,\ 14 \md{15}",
        ], anchor=np.array([0.3, 2.0, 0]), size=32, notas=[
            "El mcd es 3 y divide a 9, así que hay tres soluciones",
            "Se divide toda la congruencia entre 3, incluido el módulo",
            "Ahora 2 sí tiene inverso módulo 5, que es 3. Multiplicando, x es 4 módulo 5",
            "Y volviendo a módulo 15 salen 4, 9 y 14, que son las mismas tres del reloj",
        ])
        nl = recta(0, 15, np.array([-3.35, -1.15, 0]), 6.2, font=18)
        sol = m.VGroup(*(m.Dot(nl.n2p(v), radius=0.12, color=VERDE_CL) for v in (4, 9, 14)))
        self.pin(nl)
        self.play(m.Create(nl), run_time=0.8)
        self.pin(sol)
        self.remove(sol)
        self.play(m.LaggedStart(*(m.GrowFromCenter(d) for d in sol), lag_ratio=0.3), run_time=0.9)
        brs = m.VGroup(*(m.BraceLabel(m.Line(nl.n2p(a_), nl.n2p(a_ + 5)), "5", brace_direction=m.UP,
                                      font_size=26, color=m.YELLOW) for a_ in (4, 9)))
        self.pin(brs)
        self.remove(brs)
        self.play(m.LaggedStart(*(m.GrowFromCenter(b) for b in brs), lag_ratio=0.4), run_time=1.0)
        self.cap("En la recta: las soluciones están separadas por m/d = 5, y antes de llegar a 15 caben "
                 "exactamente d = 3", m.YELLOW)
        self.card("Ejemplo con d = 1",
                  lineas(tex(r"55x\equiv 13\md{89},\quad 55^{-1}\equiv 34", 28),
                         tex(r"x\equiv 13\cdot 34 = 442 = 4\cdot 89+86\equiv 86", 28, VERDE_CL)),
                  C_ESQ, corner=m.DR, shift=np.array([0, 1.25, 0]))
        self.cap("Cuando d = 1 es más corto: se multiplica por el inverso. Con el 34 del módulo 2 sale x ≡ 86 "
                 "módulo 89", VERDE_CL)

    # ── 12. TCR ──────────────────────────────────────────────────────────────
    def rejilla(self, m1, m2, x0, z0, c=0.62, n_hasta=None, walk=True, caption=None):
        cells = {}
        for i in range(m1):
            for j in range(m2):
                pos = P(x0 + j * c, z0 - i * c)
                cells[(i, j)] = losa(c - 0.06, c - 0.06, pos, GRIS_OSC, depth=0.06)
        rl = [etiqueta(str(i), P(x0 - 0.55, z0 - i * c), 22, NARANJA) for i in range(m1)]
        cl = [etiqueta(str(j), P(x0 + j * c, z0 + 0.55), 22, AZUL) for j in range(m2)]
        rh = etiqueta(rf"x\bmod {m1}", P(x0 - 1.25, z0 - (m1 - 1) * c / 2), 24, NARANJA, is_tex=True)
        ch = etiqueta(rf"x\bmod {m2}", P(x0 + (m2 - 1) * c / 2, z0 + 1.0), 24, AZUL, is_tex=True)
        self.play(*(m.FadeIn(v) for v in cells.values()), *(m.FadeIn(t) for t in rl + cl), m.FadeIn(rh),
                  m.FadeIn(ch), run_time=1.0)
        nums = {}
        if walk:
            top = n_hasta if n_hasta is not None else m1 * m2
            for x in range(top):
                i, j = x % m1, x % m2
                pos = P(x0 + j * c, z0 - i * c, -0.08)
                prev = [nums[y] for y in nums if y % m1 == i and y % m2 == j]
                extra = []
                if prev:
                    pos = pos + 0.17 * m.RIGHT
                    extra = [prev[0].animate.shift(0.17 * m.LEFT)]
                t = etiqueta(str(x), pos, 22 if not prev else 20, m.WHITE if not prev else AMBAR, dy=0)
                nums[x] = t
                self.play(m.FadeIn(t, scale=0.5), cells[(i, j)].animate.set_fill(AZUL_OSC), *extra, run_time=0.3)
        return cells, nums

    def tcr(self):
        self.chapter(12)
        self.card("La pregunta",
                  ttex(r"Si sé $x\bmod 3$ y $x\bmod 5$, ¿sé $x\bmod 15$?", 30), C_INT, corner=m.UL)
        self.cap("Pongamos los números del 0 al 14 en una rejilla. La fila es el residuo módulo 3 y la columna "
                 "el residuo módulo 5")
        cells, nums = self.rejilla(3, 5, -1.2, 1.0)
        self.cap("Cada paso baja una fila y corre una columna, dando la vuelta por los bordes. Como 3 y 5 son "
                 "coprimos, la diagonal pasa por las 15 casillas sin repetir ninguna", m.YELLOW)
        self.cap("Así que cada pareja de residuos corresponde a exactamente un número módulo 15. Eso es el Teorema "
                 "Chino del Residuo")
        self.swing(theta=-62, phi=64, run_time=2.0)
        self.clear_stage()
        self.cap("Ahora con módulos que no son coprimos, 2 y 4")
        cells, nums = self.rejilla(2, 4, -1.0, 0.6, c=0.75, n_hasta=8)
        empty = [cells[(i, j)] for i in range(2) for j in range(4) if (i + j) % 2 == 1]
        self.play(*(c.animate.set_fill(ROJO) for c in empty), run_time=0.8)
        self.cap("La diagonal se cierra después de solo 4 pasos, que es mcm(2, 4): del 4 al 7 se repiten las mismas "
                 "casillas, en amarillo, y la mitad de la rejilla queda vacía. Por ejemplo, x ≡ 0 mod 2 y x ≡ 1 mod 4 no tiene solución", ROJO_CL)
        self.clear_stage()

        self.card("Teorema Chino del Residuo",
                  lineas(ttex(r"$m_1,\dots,m_n$ coprimos dos a dos $\Rightarrow$ el sistema $x\equiv a_i\md{m_i}$", 26),
                         ttex(r"tiene solución \textbf{única} mod $M=m_1\cdots m_n$:", 26),
                         tex(r"x\equiv\sum a_iM_iy_i,\quad M_i=\tfrac{M}{m_i},\quad y_i = M_i^{-1}\bmod m_i", 32,
                             m.YELLOW)), C_TEOREMA, corner=m.UL)
        self.cap("La fórmula se entiende con la idea de interruptores. Cada término M·y de la suma vale 1 módulo "
                 "su propio m y 0 módulo todos los demás")
        cells, nums = self.rejilla(3, 5, 0.6, 0.4, walk=False)
        c1 = etiqueta("10", P(0.6 + 0 * 0.62, 0.4 - 1 * 0.62, -0.08), 24, m.BLACK, dy=0)
        c2 = etiqueta("6", P(0.6 + 1 * 0.62, 0.4 - 0 * 0.62, -0.08), 24, m.BLACK, dy=0)
        self.play(cells[(1, 0)].animate.set_fill(NARANJA), m.FadeIn(c1), run_time=0.7)
        self.cap("Con 3 y 5: C₁ = 5·2 = 10. Es 1 módulo 3 y 0 módulo 5, así que cae en la fila 1 y la columna 0",
                 NARANJA)
        self.play(cells[(0, 1)].animate.set_fill(AZUL), m.FadeIn(c2), run_time=0.7)
        self.cap("C₂ = 3·2 = 6. Es 0 módulo 3 y 1 módulo 5", AZUL)
        res = etiqueta("8", P(0.6 + 3 * 0.62, 0.4 - 2 * 0.62, -0.08), 24, m.BLACK, dy=0)
        self.play(cells[(2, 3)].animate.set_fill(m.YELLOW), m.FadeIn(res), run_time=0.7)
        self.cap("Para x ≡ 2 mod 3 y x ≡ 3 mod 5 se toma 2·10 + 3·6 = 38 ≡ 8. Cada interruptor enciende solo "
                 "su coordenada", m.YELLOW)
        self.clear_stage()

        # un sistema de cuatro congruencias
        self.card("Ejemplo: cuatro congruencias",
                  lineas(tex(r"2x\equiv 1\,(5),\ \ x\equiv -1\,(7),\ \ x\equiv 4\,(9),\ \ 3x\equiv 2\,(11)", 28),
                         tex(r"\Rightarrow\ x\equiv 3\,(5),\ \ 6\,(7),\ \ 4\,(9),\ \ 8\,(11)", 28, VERDE_CL)),
                  C_ESQ, corner=m.UL)
        self.cap("Un sistema más grande. Primero se despeja x en cada ecuación: el inverso de 2 módulo 5 es 3 y "
                 "el de 3 módulo 11 es 4")
        hdr = ["m_i", "a_i", "M_i", "M_i\\bmod m_i", "y_i", "a_iM_iy_i"]
        rows = [(5, 3, 693, 3, 2, 4158), (7, 6, 495, 5, 3, 8910), (9, 4, 385, 7, 4, 6160), (11, 8, 315, 7, 8, 20160)]
        xs = [-4.6, -3.2, -1.7, 0.2, 1.9, 3.7]
        y0 = 0.9
        H = [tex(h, 28, m.YELLOW).move_to([x, y0, 0]) for h, x in zip(hdr, xs)]
        self.pin(*H)
        self.play(*(m.FadeIn(h) for h in H), run_time=0.6)
        ultimos = []
        for k, r in enumerate(rows):
            cells_ = [tex(str(v), 28).move_to([x, y0 - 0.5 * (k + 1), 0]) for v, x in zip(r, xs)]
            self.pin(*cells_)
            self.play(*(m.FadeIn(c, shift=0.2 * m.RIGHT) for c in cells_), run_time=0.5)
            ultimos.append(cells_[-1])
            if k == 0:
                self.cap("M = 5·7·9·11 = 3465. Para el primero, M₁ = 693, que es 3 módulo 5, y su inverso es 2")
        suma_lab = tex(r"x\equiv", 34, VERDE_CL)
        suma = m.Integer(0, group_with_commas=False, font_size=34, color=VERDE_CL)
        fila = m.VGroup(suma_lab, suma).arrange(m.RIGHT, buff=0.2).move_to([0, y0 - 2.9, 0])
        self.pin(fila)
        self.play(m.FadeIn(fila), run_time=0.4)
        acum = 0
        for c, r in zip(ultimos, rows):
            acum += r[-1]
            self.play(m.Circumscribe(c, color=VERDE_CL, buff=0.06), m.ChangeDecimalToValue(suma, acum),
                      run_time=0.8)
        tot = tex(r"x\equiv 4158+8910+6160+20160 = 39388\equiv 1273\md{3465}", 32, VERDE_CL)
        tot.move_to([0, y0 - 2.9, 0])
        self.pin(tot)
        self.remove(tot)
        self.play(m.TransformMatchingShapes(fila, tot), run_time=1.2)
        self.cap("Se suman los cuatro términos y se reduce. x ≡ 1273. Comprobación: 1273 deja residuos 3, 6, 4 y 8",
                 VERDE_CL)
        self.clear_stage()

        # módulos no coprimos
        self.card("Módulos no coprimos",
                  ttex(r"Se parte cada módulo en potencias de primos y se buscan choques.", 26), C_ESQ, corner=m.UL)
        ecs = [tex(r"x\equiv 7\md{10}", 32).move_to([-3.6, 0.75, 0]),
               tex(r"x\equiv 4\md{35}", 32).move_to([-3.6, -1.25, 0])]
        mods = {q_: m.VGroup(m.RoundedRectangle(width=1.7, height=0.62, corner_radius=0.1, stroke_color=BORDE,
                                                stroke_width=2, fill_color=GRIS_OSC, fill_opacity=0.6),
                             tex(rf"\bmod {q_}", 30)) for q_ in (2, 5, 7)}
        for q_, y in zip((2, 5, 7), (1.1, -0.25, -1.6)):
            mods[q_].move_to([1.6, y, 0])
        flechas = [(0, 2, "1", AZUL), (0, 5, "2", AZUL), (1, 5, "4", NARANJA), (1, 7, "4", NARANJA)]
        self.pin(*ecs, *mods.values())
        self.remove(*ecs, *mods.values())
        self.play(*(m.FadeIn(e, shift=0.2 * m.RIGHT) for e in ecs), *(m.FadeIn(b) for b in mods.values()),
                  run_time=0.8)
        valores = []
        for i, q_, v, col in flechas:
            fl = m.Arrow(ecs[i].get_right(), mods[q_].get_left(), buff=0.15, color=col, stroke_width=4)
            val = tex(rf"x\equiv {v}", 28, col).next_to(mods[q_], m.RIGHT, buff=0.2 + 1.3 * (i == 1 and q_ == 5))
            self.pin(fl, val)
            self.remove(fl, val)
            self.play(m.GrowArrow(fl), m.FadeIn(val, shift=0.15 * m.LEFT), run_time=0.6)
            valores.append(val)
        self.cap("Cada ecuación se reparte en sus primos: 10 da módulo 2 y módulo 5, y 35 da módulo 5 y módulo 7")
        choque = mods[5]
        self.play(choque[0].animate.set_stroke(ROJO_CL, width=4), m.Wiggle(choque), valores[1].animate.set_color(ROJO_CL),
                  valores[2].animate.set_color(ROJO_CL), run_time=1.0)
        self.cap("Módulo 5 llegan dos pedidos distintos, 2 y 4. Ese es el choque", ROJO_CL)
        self.clear_stage()
        self.card("Módulos no coprimos",
                  ttex(r"Se parte cada módulo en potencias de primos y se buscan choques.", 26), C_ESQ, corner=m.UL,
                  write=False)
        self.derivar([
            r"x\equiv 7\,(10)\ \Rightarrow\ x\equiv 1\,(2),\ x\equiv 2\,(5)",
            r"x\equiv 4\,(35)\ \Rightarrow\ x\equiv 4\,(5),\ x\equiv 4\,(7)",
            r"2\not\equiv 4\,(5)\ \Rightarrow\ \text{sin solución}",
        ], anchor=np.array([-6.6, 1.3, 0]), size=32, color=m.WHITE, notas=[
            "10 y 35 comparten el 5, así que el TCR no aplica directo. Se parte cada ecuación en sus primos",
            "La segunda también",
            "Módulo 5 piden 2 y 4 a la vez. Imposible, no hay solución",
        ])
        self.derivar([
            r"x\equiv 7\,(10),\ x\equiv 2\,(35)\ \Rightarrow\ x\equiv 1\,(2),\ 2\,(5),\ 2\,(7)",
            r"x\equiv 35\cdot 1 + 2\cdot 14\cdot 4 + 2\cdot 10\cdot 5 = 247\equiv 37\md{70}",
        ], anchor=np.array([-6.6, -0.6, 0]), size=30, notas=[
            "Si la segunda ecuación fuera x ≡ 2 módulo 35, módulo 5 las dos pedirían 2. No hay choque, la condición repetida se "
            "deja una sola vez",
            "Ahora los módulos 2, 5 y 7 sí son coprimos, y el TCR da 37 módulo 70",
        ])
        self.card("Regla", tex(r"\text{solución}\iff \mcd(m,n)\mid a-b,\ \text{única mod }\operatorname{mcm}(m,n)", 28),
                  C_REGLA, corner=m.UR)
        self.cap("En general, con dos ecuaciones hay solución si y solo si el mcd de los módulos divide a la "
                 "diferencia de los residuos, y es única módulo el mcm, no el producto")

    # ── 13. Fermat ───────────────────────────────────────────────────────────
    def fermat(self):
        self.chapter(13)
        self.card("Pequeño Teorema de Fermat",
                  lineas(tex(r"p\ \text{primo},\ p\nmid a\ \Rightarrow\ a^{p-1}\equiv 1\md p", 34, m.YELLOW),
                         tex(r"\text{para todo } a:\ a^p\equiv a\md p", 28)), C_TEOREMA, corner=m.UL)
        self.cap("¿Cómo se calcula 2 elevado a un millón módulo 101 sin hacer un millón de multiplicaciones? "
                 "Primero la intuición, con p = 7 y a = 3")
        p, a = 7, 3
        cx, cz, R = 1.6, -0.5, 1.7
        pos = {k: en_circulo(k - 1, p - 1, R, cx, cz) for k in range(1, p)}
        balls = {k: esfera(pos[k], CLASES[k - 1], r=0.3) for k in range(1, p)}
        labs = {k: etiqueta(str(k), pos[k], 26, m.WHITE, dy=-0.33) for k in range(1, p)}
        self.play(*(m.FadeIn(b) for b in balls.values()), *(m.FadeIn(l) for l in labs.values()), run_time=0.9)
        self.cap("Estos son los residuos 1, 2, 3, 4, 5 y 6. Multipliquemos cada uno por 3 y movámoslo a donde cae")
        dest = {k: a * k % p for k in range(1, p)}
        lab_new = {k: etiqueta(f"{k}·3", pos[dest[k]], 20, m.GREY_A, dy=-0.33).shift(0.55 * m.OUT) for k in range(1, p)}
        self.play(*(balls[k].animate.move_to(pos[dest[k]]) for k in balls),
                  *(m.FadeOut(l) for l in labs.values()), run_time=2.2)
        labs2 = {k: etiqueta(str(dest[k]), pos[dest[k]], 26, m.WHITE, dy=-0.33) for k in range(1, p)}
        self.play(*(m.FadeIn(l) for l in labs2.values()), *(m.FadeIn(l) for l in lab_new.values()), run_time=0.8)
        self.cap("Cada bolita cayó en un lugar distinto y no quedó ningún hueco. Multiplicar por 3 solo revolvió "
                 "los residuos", m.YELLOW)
        self.cap("Entonces el producto de todos es el mismo antes y después. Pero después tiene seis factores 3 "
                 "de más. Por eso 3 a la 6 tiene que ser 1")
        self.swing(theta=-60, phi=66, run_time=2.0)
        self.clear_stage()

        self.card("Pequeño Teorema de Fermat", tex(r"a^{p-1}\equiv 1\md p", 34, m.YELLOW), C_TEOREMA,
                  corner=m.UL, write=False)
        self.derivar([
            r"a,\ 2a,\ \dots,\ (p-1)a\ \ \text{son}\ \not\equiv 0\ \text{y distintos}",
            r"\{a,2a,\dots,(p-1)a\}\equiv\{1,2,\dots,p-1\}",
            r"a^{p-1}\,(p-1)!\equiv (p-1)! \md p",
            r"\mcd((p-1)!,p)=1\ \Rightarrow\ a^{p-1}\equiv 1",
        ], anchor=np.array([-6.6, 1.3, 0]), size=32, notas=[
            "Ninguno es 0, por el lema de Euclides: p no divide a k ni a a. Y son distintos porque se puede "
            "cancelar a, que es coprimo con p",
            "Son p − 1 residuos distintos y no nulos, así que son exactamente 1, 2, …, p − 1 en otro orden",
            "Se multiplican todos. A la izquierda aparece a elevado a p − 1",
            "El factorial es coprimo con p, así que se cancela",
        ])
        self.clear_stage()

        self.card("Estrategia para exponentes gigantes",
                  lineas(tex(r"E = q(p-1)+r\ \Rightarrow\ a^E = (a^{p-1})^q a^r\equiv a^r", 30),
                         ttex(r"El exponente se reduce módulo $p-1$.", 26, m.YELLOW)), C_ESQ, corner=m.UL)
        cx, cy, R = 3.4, -0.35, 1.55
        ang = {v: m.PI / 2 - 2 * m.PI * k / 6 for k, v in enumerate((1, 3, 2, 6, 4, 5))}
        sitio = {v: np.array([cx + R * math.cos(a_), cy + R * math.sin(a_), 0]) for v, a_ in ang.items()}
        nodos = {v: m.LabeledDot(tex(str(v), 30, m.BLACK), radius=0.3, color=CLASES[v - 1]).move_to(sitio[v])
                 for v in range(1, 7)}
        self.pin(*nodos.values())
        self.remove(*nodos.values())
        self.play(m.LaggedStart(*(m.GrowFromCenter(n_) for n_ in nodos.values()), lag_ratio=0.1), run_time=0.9)
        cont = tex(r"3^{0}\equiv 1", 44, m.YELLOW).move_to([-3.4, -0.4, 0])
        marca = m.Circle(radius=0.42, color=m.YELLOW, stroke_width=5).move_to(sitio[1])
        self.pin(cont, marca)
        self.remove(cont, marca)
        self.play(m.Write(cont), m.Create(marca), run_time=0.7)
        self.cap("Antes, la intuición de por qué el exponente se reduce: miremos las potencias de 3 módulo 7")
        v, flechas_ = 1, m.VGroup()
        for k in range(1, 7):
            w = 3 * v % 7
            fl = m.CurvedArrow(sitio[v], sitio[w], angle=-0.5, color=m.YELLOW, stroke_width=4)
            fl.scale(0.72)
            nuevo = tex(rf"3^{{{k}}}\equiv {w}", 44, m.YELLOW).move_to(cont)
            self.pin(fl, nuevo)
            self.remove(fl, nuevo)
            self.play(m.Create(fl), marca.animate.move_to(sitio[w]), m.Transform(cont, nuevo), run_time=0.6)
            flechas_.add(fl)
            v = w
        self.play(m.Flash(nodos[1], color=m.YELLOW, flash_radius=0.45), m.Indicate(cont, scale_factor=1.15),
                  run_time=0.8)
        self.cap("Después de 6 = p − 1 pasos se vuelve al 1, y desde ahí todo se repite. Dar 6 pasos de más es "
                 "como no darlos, así que solo importa el exponente módulo 6", m.YELLOW)
        self.play(m.FadeOut(m.VGroup(*nodos.values(), cont, marca, flechas_)), run_time=0.6)
        res = self.barra_exponente(r"2^{1000005}\bmod 101", 10000, "100", "5", r"\equiv 2^5 = 32",
                             np.array([0.2, -0.4, 0]), ancho=9.0, notas=(
            "Ejemplo: 2 a la 1000005 módulo 101. 101 es primo, así que 2 a la 100 es 1. El exponente es 10000 bloques de 100 "
            "más un resto de 5",
            "Cada bloque de 100 vale 2 a la 100, que es 1. Multiplicar por 1 no cambia nada",
            "Solo queda el resto: 2 a la 5, que es 32",
        ))
        self.play(m.FadeOut(res), run_time=0.5)
        sq = lineas(tex(r"7^2 = 49\equiv 3", 28), tex(r"7^4\equiv 9", 28), tex(r"7^8\equiv 81\equiv 12", 28),
                    tex(r"7^{16}\equiv 144\equiv 6", 28),
                    tex(r"7^{21}=7^{16}7^47\equiv 6\cdot9\cdot7=378\equiv 10", 28, VERDE_CL))
        c = self.card("Inverso de 7 mod 23 con Fermat", sq, C_ESQ, corner=m.UR, shift=np.array([0, -0.6, 0]))
        self.cap("Y Fermat también da inversos: como 7 por 7 a la 21 es 7 a la 22, que es 1, el inverso de 7 es 7 a la 21. Se calcula elevando "
                 "al cuadrado una y otra vez", VERDE_CL)
        self.cap("21 es 16 + 4 + 1, así que se multiplican esas tres potencias y sale 10. Comprobación: 7·10 = 70 = "
                 "3·23 + 1")
        self.clear_stage()
        self.card("Error común",
                  lineas(ttex(r"Fermat \textbf{solo} con módulo primo. $a^{12}\bmod 15$: NO uses exponente 14.", 28),
                         ttex(r"Usa Euler ($\varphi(15)=8$) o el TCR con 3 y 5.", 28)), C_TRAMPA, corner=m.UL)
        self.card("Contraejemplo de la recíproca",
                  lineas(tex(r"2^{340}\equiv 1\md{341},\quad 341 = 11\cdot 31", 30),
                         ttex(r"Cumplir $a^{n-1}\equiv 1$ no prueba que $n$ sea primo.", 26)),
                  C_TRAMPA, corner=m.UR, shift=np.array([0, -1.6, 0]))
        self.cap("Dos advertencias. Fermat no sirve con módulos compuestos, y la recíproca es falsa: 341 no es "
                 "primo y aun así 2 a la 340 es 1 módulo 341", ROJO_CL)

    # ── 14. Wilson ───────────────────────────────────────────────────────────
    def wilson(self):
        self.chapter(14)
        self.card("Teorema de Wilson", tex(r"n>1\ \text{es primo}\iff (n-1)!\equiv -1\md n", 34, m.YELLOW),
                  C_TEOREMA, corner=m.UL)
        self.cap("Ahora con p = 11. Pongamos los números del 1 al 10 en círculo y unamos cada uno con su inverso")
        p = 11
        cx, cz, R = 1.6, -0.55, 1.8
        pos = {k: en_circulo(k - 1, p - 1, R, cx, cz) for k in range(1, p)}
        balls = {k: esfera(pos[k], GRIS, r=0.28) for k in range(1, p)}
        labs = {k: etiqueta(str(k), pos[k], 24, m.WHITE, dy=-0.31) for k in range(1, p)}
        self.play(*(m.FadeIn(b) for b in balls.values()), *(m.FadeIn(l) for l in labs.values()), run_time=0.9)
        pairs = [(2, 6), (3, 4), (5, 9), (7, 8)]
        for (a, b), col in zip(pairs, [AZUL, NARANJA, VERDE, MORADO]):
            ln = m.Line3D(pos[a], pos[b], thickness=0.03, color=col)
            self.play(m.Create(ln), balls[a].animate.set_color(col), balls[b].animate.set_color(col), run_time=0.6)
            tag = etiqueta(rf"{a}\cdot {b} = {a * b}\equiv 1", P(-4.9, 0.9 - 0.6 * pairs.index((a, b))), 34, col,
                           is_tex=True)
            self.play(m.FadeIn(tag), run_time=0.4)
        self.cap("2 con 6, 3 con 4, 5 con 9 y 7 con 8. Cada pareja multiplica 1, así que en el producto se cancelan")
        self.play(balls[1].animate.set_color(m.YELLOW), balls[10].animate.set_color(m.YELLOW),
                  labs[1].animate.set_color(m.BLACK), labs[10].animate.set_color(m.BLACK), run_time=0.6)
        self.cap("Solo quedan sin pareja el 1 y el 10, que son su propio inverso. Entonces 10! ≡ 1·10 = 10 ≡ −1",
                 m.YELLOW)
        self.swing(theta=-58, phi=64, run_time=2.0)
        self.clear_stage()

        self.card("Teorema de Wilson", tex(r"(p-1)!\equiv -1\md p", 34, m.YELLOW), C_TEOREMA, corner=m.UL,
                  write=False)
        self.derivar([
            r"a^2\equiv 1\iff p\mid (a-1)(a+1)\iff a\equiv \pm 1",
            r"\{2,\dots,p-2\}\ \text{se parte en parejas}\ (a,a^{-1}),\ a\neq a^{-1}",
            r"(p-1)!\equiv 1\cdot \underbrace{1\cdots 1}_{\text{parejas}}\cdot (p-1)\equiv -1",
        ], anchor=np.array([-6.6, 1.3, 0]), size=32, notas=[
            "Primero: los únicos que son su propio inverso son 1 y −1, por el lema de Euclides",
            "Así que todos los demás tienen una pareja distinta de ellos mismos",
            "Las parejas dan 1 y quedan solo los extremos",
        ])
        self.cap("La vuelta: si n = ab con 1 < a < n, a aparece en (n − 1)!, así que a divide a (n − 1)! + 1 y a "
                 "(n − 1)!, y por tanto a 1. Contradicción")
        self.clear_stage()
        self.card("Ejemplo", tex(r"98!\bmod 101", 34), C_ESQ, corner=m.UL)
        self.derivar([
            r"100!\equiv -1\md{101}",
            r"100\cdot 99! \equiv -1,\quad 100\equiv -1\ \Rightarrow\ 99!\equiv 1",
            r"99\cdot 98!\equiv 1,\quad 99\equiv -2\ \Rightarrow\ -2\cdot 98!\equiv 1",
            r"2\cdot 98!\equiv -1\equiv 100\ \Rightarrow\ 98!\equiv 50",
        ], anchor=np.array([-6.6, 1.2, 0]), size=34, notas=[
            "Wilson con p = 101",
            "Se quita el factor 100 escribiéndolo como −1",
            "Ahora se quita el 99, que es −2",
            "Y 2 por algo da 100, así que ese algo es 50. Comprobación: 2·50 = 100 ≡ −1",
        ])
        self.card("Regla de 1 segundo",
                  ttex(r"¿Factorial mod primo? Wilson, y quita factores escribiéndolos como $-1,-2,\dots$", 26),
                  C_REGLA, corner=m.DL, shift=np.array([0, 1.25, 0]))
        self.wait(3)
