"""Teoría de números, módulo 1: divisibilidad, algoritmo de la división, MCD, Euclides y TFA.

    manimgx render modulo1_divisibilidad.py Modulo1
"""

import manimgx as m
import numpy as np

from comun import (AMBAR, AZUL, AZUL_OSC, BORDE, C_DEF, C_ESQ, C_REGLA, C_TEOREMA, C_TRAMPA, GRIS,
                   GRIS_OSC, MORADO, NARANJA, ROJO, ROJO_CL, TEAL, VERDE, VERDE_CL, Clase, P, cubo,
                   etiqueta, lineas, losa, recta, tex, ttex, txt, up)


class Modulo1(Clase):
    START = 1
    CHAPTERS = [
        "Qué significa dividir",
        "El algoritmo de la división",
        "El MCD y el algoritmo de Euclides",
        "Primos y factorización única",
    ]

    def construct(self) -> None:
        self.setup_hud()
        self.intro()
        self.divisibilidad()
        self.division()
        self.euclides()
        self.tfa()
        self.cierre([
            "a | b  significa  b = a·k  con k entero; casi todo se prueba escribiendo eso y haciendo álgebra",
            "Si d divide a dos números, divide a cualquier combinación lineal de ellos",
            "El residuo siempre cumple 0 ≤ r < d, también cuando a es negativo",
            "mcd(a, b) = mcd(b, r): Euclides cambia el par sin cambiar los divisores comunes",
            "Factorizados: mínimo de exponentes para el mcd, máximo para el mcm",
        ], "En el módulo 2 vemos que el mcd también se puede escribir como una suma, con Bézout")

    # ── 0. introducción ──────────────────────────────────────────────────────
    def intro(self):
        self.set_camera_orientation(phi=62 * m.DEGREES, theta=-120 * m.DEGREES, zoom=0.92)
        cubes = [cubo("", P(-3.3 + 0.6 * i, 0.4), AZUL if (i // 3) % 2 == 0 else TEAL, side=0.52)
                 for i in range(12)]
        self.play(m.LaggedStart(*(m.FadeIn(c, shift=0.6 * m.OUT) for c in cubes), lag_ratio=0.06), run_time=1.6)
        self.move_camera(phi=76 * m.DEGREES, theta=-90 * m.DEGREES, run_time=1.6)
        self.cap("La teoría de números empieza con una pregunta muy simple: "
                 "¿un número cabe exacto en otro?")
        self.clear_stage()
        self.titulo_video("Teoría de números · Módulo 1", "divisibilidad, división, MCD y factorización")
        self.cap("Son cuatro capítulos y cada uno responde una pregunta. Primero la intuición, luego el "
                 "teorema, la prueba y un ejemplo con números")

    # ── 1. divisibilidad ─────────────────────────────────────────────────────
    def divisibilidad(self):
        self.chapter(1)
        d = self.card("Definición", tex(r"a \mid b \iff \exists\, k\in\mathbb{Z}:\ b = a\cdot k", 34),
                      C_DEF, corner=m.UL)
        self.cap("Decimos que a divide a b cuando b es a por algún entero. No es una fracción ni una "
                 "operación, es una afirmación que es verdadera o falsa")
        xs = [-3.3 + 0.6 * i for i in range(12)]
        cubes = [cubo("", P(x, 0.0), GRIS_OSC, side=0.52) for x in xs]
        twelve = etiqueta("b = 12", P(0, 0.9), 30)
        self.play(m.LaggedStart(*(m.FadeIn(c, shift=0.5 * m.IN) for c in cubes), lag_ratio=0.04),
                  m.FadeIn(twelve), run_time=1.4)
        self.cap("Piensa en b como una fila de doce cubos. Preguntar si 3 divide a 12 es preguntar si la fila "
                 "se puede cortar en bloques de tres sin que sobre nada")
        cols = [AZUL, TEAL]
        self.play(*(c[0].animate.set_fill(cols[(i // 3) % 2]) for i, c in enumerate(cubes)), run_time=1.0)
        self.play(*(c.animate.shift(0.18 * (i // 3) * m.RIGHT) for i, c in enumerate(cubes)), run_time=0.8)
        res = etiqueta(r"12 = 3\cdot 4", P(0.3, -0.9), 34, m.YELLOW, is_tex=True)
        self.play(m.Write(res), run_time=0.8)
        self.cap("Salen cuatro bloques exactos, así que 3 | 12 con k = 4", m.YELLOW)
        self.play(*(c.animate.shift(-0.18 * (i // 3) * m.RIGHT) for i, c in enumerate(cubes)), m.FadeOut(res),
                  run_time=0.7)
        cols5 = [NARANJA, AMBAR]
        self.play(*(c[0].animate.set_fill(cols5[(i // 5) % 2] if i < 10 else ROJO) for i, c in enumerate(cubes)),
                  run_time=1.0)
        self.play(*(c.animate.shift(0.18 * (i // 5) * m.RIGHT) for i, c in enumerate(cubes)), run_time=0.8)
        res2 = etiqueta(r"12 = 5\cdot 2 + 2 \;\Rightarrow\; 5\nmid 12", P(0.3, -0.9), 34, ROJO_CL, is_tex=True)
        self.play(m.Write(res2), *(m.Indicate(cubes[i], color=ROJO_CL) for i in (10, 11)), run_time=1.0)
        self.cap("Con bloques de cinco sobran dos cubos. Ningún entero k cumple 12 = 5k, así que 5 no divide a 12")
        self.clear_stage()

        # propiedades
        props = lineas(
            tex(r"1.\ \ 1\mid a,\quad a\mid 0,\quad a\mid a", 30),
            tex(r"2.\ \ a\mid b,\ b\mid c \;\Rightarrow\; a\mid c", 30),
            tex(r"3.\ \ a\mid b,\ a\mid c \;\Rightarrow\; a\mid bx+cy", 30),
            tex(r"4.\ \ b\neq 0,\ a\mid b \;\Rightarrow\; |a|\le |b|", 30),
            tex(r"5.\ \ a,b>0,\ a\mid b,\ b\mid a \;\Rightarrow\; a=b", 30),
            buff=0.2)
        c = self.card("Propiedades de la divisibilidad", props, C_TEOREMA, corner=m.UL)
        self.cap("Hay cinco propiedades que se usan todo el tiempo. Todas se prueban igual: escribes cada "
                 "hipótesis como un producto y haces álgebra")
        hl = m.SurroundingRectangle(props[2], color=m.YELLOW, buff=0.08)
        self.pin(hl)
        self.play(m.Create(hl), run_time=0.6)
        self.cap("La tercera es la que más se usa, la de combinación lineal. Veamos su prueba")
        self.derivar([
            r"b = a k,\qquad c = a\ell",
            r"bx + cy = akx + a\ell y",
            r"bx + cy = a\,(kx + \ell y)",
            r"kx+\ell y\in\mathbb{Z}\;\Rightarrow\; a \mid bx+cy",
        ], anchor=np.array([0.6, 1.6, 0]), size=32, notas=[
            "Las hipótesis dicen que b y c son múltiplos de a",
            "Se sustituye en la combinación lineal",
            "Y se saca a como factor común",
            "Lo que queda entre paréntesis es un entero, así que a divide a la combinación. Eso es todo",
        ])
        nl = recta(-3, 15, np.array([0, -2.0, 0]), 12.0)
        mult = m.VGroup(*(m.Dot(nl.n2p(k), radius=0.09, color=m.YELLOW) for k in range(-3, 16, 3)))
        bola = m.Dot(nl.n2p(0), radius=0.13, color=VERDE_CL)
        self.pin(nl, mult, bola)
        self.play(m.Create(nl), m.LaggedStart(*(m.GrowFromCenter(d) for d in mult), lag_ratio=0.12),
                  m.FadeIn(bola, scale=0.4), run_time=1.4)
        self.cap("En la recta, con a = 3, b = 6 y c = 9. Los puntos amarillos son los múltiplos de 3, los "
                 "únicos lugares donde 3 divide")
        saltos = self.saltar(nl, bola, 0, [6, 12], AZUL, etiquetas=["+6", "+6"], angulo=1.0)
        self.cap("Con x = 2 se dan dos saltos de tamaño b = 6. Cada salto mide un múltiplo de 3, así que siempre "
                 "se cae en amarillo", AZUL)
        saltos2 = self.saltar(nl, bola, 12, [3], NARANJA, etiquetas=["-9"], angulo=1.25)
        self.play(m.Indicate(bola, color=m.YELLOW, scale_factor=1.8), run_time=0.7)
        self.cap("Con y = −1 se salta c = 9 hacia atrás y se cae en 2·6 − 9 = 3. Por más saltos que des, nunca "
                 "sales de los amarillos", NARANJA)
        self.play(m.FadeOut(m.VGroup(nl, mult, bola, saltos, saltos2)), run_time=0.6)
        self.play(m.FadeOut(hl), run_time=0.3)
        self.remove(hl)
        contra = self.card("Contraejemplo canónico",
                           tex(r"3 \mid (1+2)\quad\text{pero}\quad 3\nmid 1,\ \ 3\nmid 2", 30), C_TRAMPA,
                           corner=None, shift=np.array([3.4, -1.5, 0]))
        self.cap("Ojo, la recíproca es falsa. Que d divida una suma no dice nada de cada sumando por separado",
                 ROJO_CL)
        regla = self.card("Regla de 1 segundo",
                          ttex(r"Para probar $a\mid X$: escribe $X = a\cdot(\text{entero})$", 28), C_REGLA,
                          corner=None, shift=np.array([3.4, -2.75, 0]), write=False)
        self.play(m.FadeOut(contra), regla.animate.shift(1.15 * m.UP), run_time=0.6)
        self.cap("O, si no sale directo, como combinación lineal de cosas que a ya divide")

    # ── 2. algoritmo de la división ──────────────────────────────────────────
    def division(self):
        self.chapter(2)
        thm = self.card("Algoritmo de la división",
                        lineas(tex(r"a\in\mathbb{Z},\ d>0\ \Rightarrow\ \exists!\, q, r:", 30),
                               tex(r"a = d\,q + r,\qquad 0\le r<d", 34, m.YELLOW)), C_TEOREMA, corner=m.UL)
        self.cap("Si d no divide a a, la pregunta es cómo describir exactamente lo que sobra, y por qué esa "
                 "descripción es única")
        lo, hi = -24, 2
        w = 0.46
        xs = {n: (n - (lo + hi) / 2) * w for n in range(lo, hi + 1)}
        z = -0.4
        cols = [AZUL_OSC, TEAL]
        cubes = {n: cubo("", P(xs[n], z), cols[(n // 3) % 2], side=0.4) for n in range(lo, hi + 1)}
        nums = {n: etiqueta(str(n), P(xs[n], z - 0.42), 15, m.GREY_B) for n in range(lo, hi + 1)}
        self.play(m.LaggedStart(*(m.FadeIn(cubes[n], shift=0.3 * m.IN) for n in cubes), lag_ratio=0.02),
                  m.FadeIn(m.Group(*nums.values())), run_time=1.8)
        self.cap("Pongamos los enteros en fila y pintemos cajones de tamaño 3. Cada cajón empieza en un "
                 "múltiplo de 3")
        mults = [n for n in range(lo, hi + 1) if n % 3 == 0]
        marks = [etiqueta(f"{n}", P(xs[n], z + 0.72), 20, m.YELLOW) for n in mults]
        self.play(*(cubes[n].animate.shift(0.18 * m.OUT) for n in mults), *(m.FadeIn(k) for k in marks),
                  run_time=1.0)
        self.cap("Todo número cae en exactamente un cajón. El cociente q dice en qué cajón cayó y el residuo r "
                 "dice cuánto avanzó adentro")
        a = -20
        self.play(cubes[a][0].animate.set_fill(m.YELLOW), m.Indicate(nums[a], color=m.YELLOW, scale_factor=1.6),
                  run_time=1.0)
        self.move_camera(zoom=1.45, frame_center=P(xs[-19] + 0.4, z - 0.4), run_time=1.4)
        good = losa(xs[-20] - xs[-21], 0.12, P((xs[-21] + xs[-20]) / 2, z - 0.75), VERDE_CL, depth=0.06)
        g_ticks = [losa(0.05, 0.3, P(xs[n], z - 0.75), VERDE_CL, depth=0.06) for n in (-21, -20)]
        r_lab = etiqueta("r = 1", P((xs[-21] + xs[-20]) / 2, z - 1.05), 24, VERDE_CL)
        self.play(m.FadeIn(good), *(m.FadeIn(t) for t in g_ticks), m.FadeIn(r_lab), run_time=0.9)
        self.cap("Para a = −20 el cajón empieza en −21, que es 3 por −7. De −21 a −20 se avanza 1. "
                 "Entonces q = −7 y r = 1", VERDE_CL)
        bad = losa(xs[-18] - xs[-20], 0.12, P((xs[-18] + xs[-20]) / 2, z - 1.4), ROJO_CL, depth=0.06)
        b_ticks = [losa(0.05, 0.3, P(xs[n], z - 1.4), ROJO_CL, depth=0.06) for n in (-20, -18)]
        bad_lab = etiqueta("r = −2", P((xs[-18] + xs[-20]) / 2, z - 1.7), 24, ROJO_CL)
        self.play(m.FadeIn(bad), *(m.FadeIn(t) for t in b_ticks), m.FadeIn(bad_lab), run_time=0.9)
        self.cap("También es cierto que −20 = 3·(−6) − 2, pero eso no es la división. Se está midiendo "
                 "hacia atrás desde −18 y sale un residuo negativo", ROJO_CL)
        self.home(run_time=1.2)
        trampa = self.card("Error común",
                           lineas(tex(r"-20 = 3(-6) - 2\quad\text{NO}\ \ (r<0)", 28, ROJO_CL),
                                  tex(r"-20 = 3(-7) + 1\quad\text{SÍ}", 28, VERDE_CL),
                                  ttex(r"Arreglo: $q\to q-1,\ r\to r+d$", 26)),
                           C_TRAMPA, corner=m.UR)
        self.cap("Si alguna vez te sale un residuo negativo, le restas uno al cociente y le sumas d al residuo")
        self.clear_stage()

        # prueba
        self.card("Algoritmo de la división", tex(r"a = d\,q + r,\qquad 0\le r<d", 34, m.YELLOW), C_TEOREMA,
                  corner=m.UL, write=False)
        self.cap("Ahora la prueba, que tiene dos partes: que q y r existen y que son únicos")
        nl = recta(-6, 19, np.array([0, 0.2, 0]), 12.4, solo=range(-5, 20, 5))
        bola = m.Dot(nl.n2p(17), radius=0.13, color=VERDE_CL)
        s_pts = m.VGroup(*(m.Dot(nl.n2p(v), radius=0.1, color=VERDE_CL) for v in (17, 12, 7, 2)))
        self.pin(nl, bola)
        self.play(m.Create(nl), m.FadeIn(bola, scale=0.4), run_time=1.0)
        self.cap("Con a = 17 y d = 5. El conjunto S son los restos que quedan al ir quitando cincos sin pasar a "
                 "negativo")
        self.pin(s_pts)
        self.remove(s_pts)
        saltos = self.saltar(nl, bola, 17, [12, 7, 2], VERDE_CL, etiquetas=["-5"] * 3, angulo=1.2,
                             run_time=0.55)
        self.play(m.LaggedStart(*(m.GrowFromCenter(d) for d in s_pts), lag_ratio=0.2), run_time=0.7)
        malo = m.DashedLine(nl.n2p(2), nl.n2p(-3), color=ROJO_CL, stroke_width=4).shift(0.35 * m.UP)
        x_malo = m.Cross(m.Dot(nl.n2p(-3), radius=0.18), stroke_width=5)
        fuera = tex(r"-3\notin S", 26, ROJO_CL).next_to(x_malo, m.UP, buff=0.35)
        self.pin(malo, x_malo, fuera)
        self.remove(malo, x_malo, fuera)
        self.play(m.Create(malo), run_time=0.5)
        self.play(m.Create(x_malo), m.FadeIn(fuera), m.Wiggle(x_malo), run_time=0.9)
        self.cap("Un salto más daría −3, que ya es negativo y no está en S. Así que S = {17, 12, 7, 2}, y su "
                 "mínimo es 2", ROJO_CL)
        caja0 = m.BraceLabel(m.Line(nl.n2p(0), nl.n2p(5)), r"0\le r<5", brace_direction=m.DOWN, font_size=26,
                             color=m.YELLOW).shift(0.35 * m.DOWN)
        self.pin(caja0)
        self.remove(caja0)
        self.play(m.FadeIn(caja0, shift=0.1 * m.UP), m.Circumscribe(bola, shape=m.Circle, color=m.YELLOW),
                  run_time=1.0)
        self.cap("El mínimo siempre cae en el primer cajón, entre 0 y d − 1: si fuera d o más, cabría otro salto "
                 "sin volverse negativo", m.YELLOW)
        self.play(m.FadeOut(m.VGroup(nl, bola, s_pts, saltos, malo, x_malo, fuera, caja0)), run_time=0.6)
        ex = lineas(
            ttex(r"\textbf{Existencia.} $S=\{a-dk\ :\ k\in\mathbb{Z},\ a-dk\ge 0\}\neq\varnothing$", 28),
            ttex(r"Buen orden: $S$ tiene un mínimo $r=a-dq\ge 0$.", 28),
            ttex(r"Si $r\ge d$: $\ r-d=a-d(q+1)\in S$ y es menor que $r$. Contradicción.", 28),
            ttex(r"Luego $0\le r<d$.", 28, m.YELLOW),
            buff=0.22).move_to(np.array([0, 0.75, 0]))
        for i, note in enumerate([
            "Se miran todos los restos no negativos que se obtienen quitándole múltiplos de d a a",
            "Por el principio del buen orden hay uno mínimo, y a ese lo llamamos r",
            "Si r fuera mayor o igual que d se podría quitar una d más y quedaría otro resto más pequeño, "
            "lo cual contradice que r era el mínimo",
            "Así que el mínimo siempre queda entre 0 y d − 1",
        ]):
            self.pin(ex[i])
            self.play(m.FadeIn(ex[i], shift=0.2 * m.RIGHT), run_time=0.7)
            self.cap(note)
        un = lineas(
            ttex(r"\textbf{Unicidad.} $dq+r=dq'+r'\ \Rightarrow\ d(q-q') = r'-r$", 28),
            ttex(r"$d\mid r'-r$ \ y \ $-d<r'-r<d\ \Rightarrow\ r'-r=0$", 28),
            buff=0.22).next_to(ex, m.DOWN, buff=0.4, aligned_edge=m.LEFT)
        self.pin(un[0])
        self.play(m.FadeIn(un[0], shift=0.2 * m.RIGHT), run_time=0.7)
        self.cap("Para la unicidad se suponen dos escrituras y se restan. La diferencia de residuos es un "
                 "múltiplo de d")
        self.pin(un[1])
        self.play(m.FadeIn(un[1], shift=0.2 * m.RIGHT), run_time=0.7)
        self.cap("Pero los dos residuos están entre 0 y d − 1, así que su diferencia está estrictamente entre −d "
                 "y d. El único múltiplo de d ahí es el cero")

    # ── 3. MCD y Euclides ────────────────────────────────────────────────────
    def euclides(self):
        self.chapter(3)
        self.card("Definición", lineas(tex(r"\mcd(a,b)=\max\{d>0:\ d\mid a\ \wedge\ d\mid b\}", 32),
                                       ttex(r"Coprimos: $\mcd(a,b)=1$", 28)), C_DEF, corner=m.UL)
        self.cap("El máximo común divisor es el mayor entero positivo que divide a los dos. Si es 1, decimos "
                 "que los números son coprimos")
        self.cap("Pero factorizar números grandes es difícil y dividir es fácil. ¿Se puede calcular el mcd "
                 "solo con divisiones?", m.YELLOW)
        lem = self.card("Lema", tex(r"a = bq + r\ \Rightarrow\ \mcd(a,b) = \mcd(b,r)", 34), C_TEOREMA,
                        corner=m.UR)
        self.cap("La clave es este lema. La idea de la prueba es más fuerte que el enunciado: los dos pares "
                 "tienen exactamente los mismos divisores comunes")
        self.derivar([
            r"d\mid a,\ d\mid b\ \Rightarrow\ d\mid a-bq = r",
            r"d\mid b,\ d\mid r\ \Rightarrow\ d\mid bq+r = a",
        ], anchor=np.array([-6.6, 1.0, 0]), size=32, notas=[
            "Si d divide a a y a b, divide a la combinación a − bq, que es r",
            "Y al revés, si d divide a b y a r, divide a bq + r, que es a",
        ])
        ejemplo = lineas(
            tex(r"84 = 2\cdot 36 + 12", 30),
            tex(r"\text{div. comunes de }(84,36)=\{1,2,3,4,6,12\}", 28),
            tex(r"\text{div. comunes de }(36,12)=\{1,2,3,4,6,12\}", 28),
        ).move_to(np.array([-2.6, -1.2, 0]), aligned_edge=m.LEFT)
        self.pin(ejemplo)
        self.play(m.FadeIn(ejemplo, shift=0.2 * m.UP), run_time=1.0)
        self.cap("Si los conjuntos de divisores comunes son iguales, sus máximos también lo son. Así que podemos "
                 "cambiar el par grande por uno más pequeño sin perder el mcd")
        self.clear_stage()

        # rectángulo
        self.cap("Ahora veamos el algoritmo de Euclides como un rompecabezas. Tenemos un rectángulo de 21 por 13")
        u = 0.27
        W, H = 21, 13
        x0, z0 = -4.6, -1.85
        frame = m.Rectangle(width=W * u, height=H * u, stroke_color=m.WHITE, stroke_width=3)
        up(frame).move_to(P(x0 + W * u / 2, z0 + H * u / 2, -0.1))
        wl = etiqueta("21", P(x0 + W * u / 2, z0 - 0.3), 26)
        hl = etiqueta("13", P(x0 - 0.35, z0 + H * u / 2), 26)
        self.play(m.Create(frame), m.FadeIn(wl), m.FadeIn(hl), run_time=1.0)
        # recorte: (x, z, lado, color)
        squares = []
        x, zb, w, h = 0, 0, W, H
        pal = [AZUL, TEAL, MORADO, AMBAR, NARANJA, VERDE, ROJO_CL]
        k = 0
        steps = []
        while w and h:
            if w >= h:
                q = w // h
                for i in range(q):
                    squares.append((x + i * h, zb, h, pal[k % len(pal)]))
                steps.append((w, h, q, w - q * h))
                x += q * h
                w -= q * h
            else:
                q = h // w
                for i in range(q):
                    squares.append((x, zb + i * w, w, pal[k % len(pal)]))
                steps.append((h, w, q, h - q * w))
                zb += q * w
                h -= q * w
            k += 1
        eqs = m.VGroup(*(tex(rf"{a} = {q}\cdot {b} + {r}", 30) for a, b, q, r in steps)).arrange(
            m.DOWN, aligned_edge=m.LEFT, buff=0.16).to_edge(m.RIGHT, buff=0.9).shift(0.4 * m.UP)
        idx = 0
        notes = [
            "Cortamos el cuadrado más grande que cabe, de lado 13. Cabe una vez y sobra un rectángulo de 13 "
            "por 8. Eso es 21 = 1·13 + 8",
            "Repetimos con lo que sobró: un cuadrado de 8 y queda uno de 8 por 5",
            "Y así seguimos, cada vez con el rectángulo que sobra",
            None, None,
            "Cuando un cuadrado llena exacto lo que queda, el residuo es cero y paramos",
        ]
        for j, (a, b, q, r) in enumerate(steps):
            blocks = []
            for _ in range(q):
                sx, sz, s, col = squares[idx]
                idx += 1
                sl = losa(s * u - 0.04, s * u - 0.04, P(x0 + (sx + s / 2) * u, z0 + (sz + s / 2) * u), col,
                          depth=0.12 + 0.05 * j)
                lab = etiqueta(str(s), P(x0 + (sx + s / 2) * u, z0 + (sz + s / 2) * u, -0.1 - 0.025 * j),
                               max(12, int(14 + s * 1.3)))
                blocks.append(m.Group(sl, lab))
            self.pin(eqs[j])
            self.play(*(m.FadeIn(b, shift=0.6 * m.IN) for b in blocks), m.Write(eqs[j]), run_time=0.9)
            if j < len(notes) and notes[j]:
                self.cap(notes[j])
            else:
                self.wait(0.4)
        last = m.SurroundingRectangle(eqs[-2], color=m.YELLOW, buff=0.08)
        self.pin(last)
        self.play(m.Create(last), run_time=0.6)
        self.cap("El lado del último cuadrado es 1, que es el último residuo distinto de cero. Ese es el mcd: "
                 "la baldosa cuadrada más grande que embaldosa todo el rectángulo", m.YELLOW)
        self.swing(theta=-60, phi=62, run_time=2.2)
        self.cap("21 y 13 son números de Fibonacci. Por eso casi todos los cocientes son 1 y el algoritmo "
                 "da la mayor cantidad de pasos posible. Es el peor caso")
        self.clear_stage()

        thm = self.card("Algoritmo de Euclides",
                        lineas(tex(r"a = bq_1 + r_1,\quad b = r_1q_2 + r_2,\ \dots", 30),
                               tex(r"\mcd(a,b) = \text{último residuo no nulo}", 30, m.YELLOW)), C_TEOREMA,
                        corner=m.UL)
        tabla = lineas(*(tex(s, 28) for s in [
            r"89 = 1\cdot 55 + 34", r"55 = 1\cdot 34 + 21", r"34 = 1\cdot 21 + 13", r"21 = 1\cdot 13 + 8",
            r"13 = 1\cdot 8 + 5", r"8 = 1\cdot 5 + 3", r"5 = 1\cdot 3 + 2", r"3 = 1\cdot 2 + 1",
            r"2 = 2\cdot 1 + 0"]), buff=0.1).to_edge(m.RIGHT, buff=1.0).shift(0.25 * m.UP)
        self.pin(tabla)
        self.play(m.LaggedStart(*(m.FadeIn(t, shift=0.2 * m.LEFT) for t in tabla), lag_ratio=0.15), run_time=2.2)
        self.cap("Otro ejemplo, el mcd de 89 y 55. Son Fibonacci otra vez, todos los cocientes son 1 y "
                 "el mcd es 1, así que son coprimos")
        res = [89, 55, 34, 21, 13, 8, 5, 3, 2, 1]
        chart = m.BarChart(res, y_range=[0, 90, 30], x_length=5.6, y_length=3.2,
                           bar_colors=[AZUL_OSC, AZUL, TEAL, VERDE], bar_fill_opacity=0.9, bar_stroke_width=0)
        chart.move_to([3.6, -0.55, 0])
        nums = chart.get_bar_labels(color=m.WHITE, font_size=22)
        self.pin(chart, nums)
        self.remove(chart, nums)
        self.play(m.FadeOut(tabla, shift=0.3 * m.RIGHT), m.Create(chart), run_time=1.6)
        self.play(m.LaggedStart(*(m.FadeIn(n, shift=0.1 * m.DOWN) for n in nums), lag_ratio=0.1), run_time=1.0)
        self.play(m.Circumscribe(m.VGroup(chart.bars[-1], nums[-1]), color=m.YELLOW), run_time=1.0)
        self.cap("Los residuos en barras: cada uno es un natural más pequeño que el anterior. Una escalera así "
                 "tiene que llegar al piso en una cantidad finita de pasos", m.YELLOW)
        esq = self.card("Esqueleto de la prueba",
                        lineas(ttex(r"1. dividir y cambiar $(a,b)\to(b,r)$", 26),
                               ttex(r"2. mismos divisores comunes $\Rightarrow$ mismo mcd", 26),
                               ttex(r"3. $b>r_1>r_2>\cdots\ge 0$, así que termina", 26),
                               ttex(r"4. $\mcd(r_k,0)=r_k$", 26)), C_ESQ, corner=m.DL,
                        shift=np.array([0, 1.25, 0]))
        self.cap("Por qué termina: los residuos son naturales que bajan estrictamente, y eso no puede seguir "
                 "para siempre")
        self.cap("Y al final, el mcd de un número y cero es el mismo número")

    # ── 4. TFA ───────────────────────────────────────────────────────────────
    def tfa(self):
        self.chapter(4)
        self.card("Teorema fundamental de la aritmética",
                  lineas(tex(r"n>1\ \Rightarrow\ n = p_1^{a_1}p_2^{a_2}\cdots p_k^{a_k}", 32),
                         ttex(r"y esa escritura es única salvo el orden", 26)), C_TEOREMA, corner=m.UL)
        self.cap("Todo entero mayor que uno se parte en primos, y de una sola manera")
        # árbol de 360
        spec = {"360": (1.8, 1.6, None), "8": (0.0, 0.4, "360"), "45": (3.6, 0.4, "360"),
                "2a": (-0.9, -0.8, "8"), "4": (0.9, -0.8, "8"), "5": (4.5, -0.8, "45"),
                "9": (2.7, -0.8, "45"), "2b": (0.25, -2.0, "4"), "2c": (1.45, -2.0, "4"),
                "3a": (2.2, -2.0, "9"), "3b": (3.3, -2.0, "9")}
        primes = {"2a", "2b", "2c", "5", "3a", "3b"}
        nodes = {}
        for k, (x, z, _) in spec.items():
            label = k.rstrip("abc")
            nodes[k] = cubo(label, P(x, z), VERDE if k in primes else AZUL_OSC, side=0.62, size=26)
        edges = [m.Line3D(nodes[k][0].get_center(), nodes[p][0].get_center(), thickness=0.02, color=BORDE)
                 for k, (_, _, p) in spec.items() if p]
        order = [["360"], ["8", "45"], ["2a", "4", "9", "5"], ["2b", "2c", "3a", "3b"]]
        for lvl in order:
            es = [e for e, (k, (_, _, p)) in zip(edges, [(k, v) for k, v in spec.items() if v[2]]) if k in lvl]
            self.play(*(m.FadeIn(nodes[k], shift=0.4 * m.IN) for k in lvl), *(m.Create(e) for e in es),
                      run_time=0.8)
        res = etiqueta(r"360 = 2^3\cdot 3^2\cdot 5", P(1.8, 2.5), 36, m.YELLOW, is_tex=True)
        self.play(m.Write(res), *(m.Indicate(nodes[k], color=VERDE_CL) for k in primes), run_time=1.2)
        self.cap("Se va partiendo hasta que solo quedan primos, que son las hojas verdes. La existencia se "
                 "prueba así, por inducción fuerte")
        self.cap("La unicidad necesita algo del módulo 2, el lema de Euclides: si un primo divide un producto, "
                 "divide a alguno de los factores")
        self.swing(theta=-62, phi=64, run_time=2.0)
        self.clear_stage()

        # infinitud
        self.card("Teorema (Euclides)", ttex(r"Hay infinitos números primos.", 30), C_TEOREMA, corner=m.UL)
        self.cap("Ahora una de las pruebas más bonitas, la de que hay infinitos primos. Es por contradicción")
        self.derivar([
            r"\text{Supón que solo existen } p_1, p_2, \dots, p_k",
            r"N = p_1 p_2\cdots p_k + 1 > 1",
            r"\text{TFA: algún primo } p_i \mid N",
            r"p_i \mid N - p_1\cdots p_k = 1",
        ], anchor=np.array([-6.6, 1.3, 0]), size=32, notas=[
            "Supongamos que la lista de primos es finita",
            "Multiplicamos todos los primos y le sumamos uno",
            "Por el teorema fundamental, N tiene algún factor primo, y tiene que estar en la lista",
            "Pero ese primo divide a N y al producto, así que divide a la resta, que es 1. Ningún primo "
            "divide a 1. Contradicción",
        ])
        ps = [2, 3, 5, 7, 11, 13]
        tabla = m.MathTable([[str(p) for p in ps], [str(30031 % p) for p in ps]],
                            row_labels=[tex("p", 34), tex(r"N\bmod p", 34)], h_buff=0.7, v_buff=0.5,
                            include_outer_lines=False, line_config={"stroke_color": GRIS})
        tabla.scale_to_fit_width(5.6).move_to([3.7, 1.35, 0])
        cab = tex(r"N = 2\cdot3\cdot5\cdot7\cdot11\cdot13+1 = 30031", 28, m.YELLOW).next_to(tabla, m.UP, buff=0.25)
        self.pin(tabla, cab)
        self.remove(tabla, cab)
        self.play(m.Write(cab), tabla.create(), run_time=1.6)
        unos = tabla.get_rows()[1][1:]
        self.play(m.LaggedStart(*(m.Flash(u, color=VERDE_CL, flash_radius=0.25) for u in unos), lag_ratio=0.15),
                  *(u.animate.set_color(VERDE_CL) for u in unos), run_time=1.4)
        self.cap("Con los seis primeros primos: N deja residuo 1 al dividir entre cada uno. Ninguno de la lista lo "
                 "divide", VERDE_CL)
        contra = self.card("Contraejemplo canónico",
                           lineas(tex(r"2\cdot3\cdot5\cdot7\cdot11\cdot13+1 = 30031 = 59\cdot 509", 30),
                                  ttex(r"$N$ no tiene por qué ser primo: sus factores primos son \emph{nuevos}", 26)),
                           C_TRAMPA, corner=m.DR, shift=np.array([0, 1.3, 0]))
        self.cap("Un error común es decir que N es primo. No lo es necesariamente: lo que la prueba dice es que "
                 "sus factores primos no están en la lista", ROJO_CL)
        self.clear_stage()

        # mcd y mcm por exponentes
        self.card("MCD y MCM con la factorización",
                  lineas(tex(r"\mcd = \prod p_i^{\min(\alpha_i,\beta_i)},\qquad"
                             r"\operatorname{mcm} = \prod p_i^{\max(\alpha_i,\beta_i)}", 30),
                         tex(r"a\cdot b = \mcd(a,b)\cdot\operatorname{mcm}(a,b)", 30)), C_TEOREMA, corner=m.UL)
        a_exp = {2: 3, 3: 2, 5: 0, 7: 1}
        b_exp = {2: 1, 3: 4, 5: 1, 7: 0}
        h = 0.42
        bars = []
        labels = []
        for i, p in enumerate([2, 3, 5, 7]):
            x = -1.8 + 1.9 * i
            for j, (e, col) in enumerate(((a_exp[p], AZUL), (b_exp[p], NARANJA))):
                xx = x + (j - 0.5) * 0.55
                if e:
                    bar = m.Prism(dimensions=[0.45, 0.45, e * h], fill_color=col, fill_opacity=1, stroke_width=0)
                    bar.move_to(P(xx, -1.6 + e * h / 2))
                else:
                    bar = m.Prism(dimensions=[0.45, 0.45, 0.04], fill_color=col, fill_opacity=0.5,
                                  stroke_width=0).move_to(P(xx, -1.58))
                bars.append((p, j, e, bar))
                labels.append(etiqueta(str(e), P(xx, -1.6 + e * h + 0.25), 20, col))
            labels.append(etiqueta(str(p), P(x, -2.0), 28, m.WHITE))
        key = lineas(tex(r"a = 504 = 2^3\cdot 3^2\cdot 7", 28, AZUL),
                     tex(r"b = 810 = 2\cdot 3^4\cdot 5", 28, NARANJA)).to_corner(m.UR, buff=0.4).shift(0.5 * m.DOWN)
        self.pin(key)
        self.play(m.FadeIn(key), *(m.GrowFromPoint(b, b.get_bottom()) for *_, b in bars),
                  *(m.FadeIn(l) for l in labels), run_time=1.6)
        self.cap("Pongamos los exponentes como columnas, una por primo: azul para a = 504 y naranja para b = 810")
        mins = [b for p, j, e, b in bars if e == min(a_exp[p], b_exp[p])]
        self.play(*(b.animate.set_fill(m.YELLOW) for b in mins), run_time=0.8)
        g = etiqueta(r"\mcd = 2^1\cdot 3^2 = 18", P(0.9, 1.45), 34, m.YELLOW, is_tex=True)
        self.play(m.Write(g), run_time=0.9)
        self.cap("Para el mcd te quedas con la columna más baja de cada primo, porque un divisor común no puede "
                 "tener más de lo que tiene cada uno", m.YELLOW)
        maxs = [b for p, j, e, b in bars if e == max(a_exp[p], b_exp[p])]
        self.play(*(b.animate.set_fill(m.YELLOW).set_opacity(0.35) for b in mins),
                  *(b.animate.set_fill(VERDE_CL).set_opacity(1) for b in maxs), run_time=0.8)
        l = etiqueta(r"\operatorname{mcm} = 2^3\cdot 3^4\cdot 5\cdot 7 = 22680", P(0.9, 0.85), 34, VERDE_CL,
                     is_tex=True)
        self.play(m.Write(l), run_time=0.9)
        self.cap("Para el mcm, con la más alta. Y como mínimo más máximo es la suma de los dos exponentes, "
                 "sale que a·b = mcd·mcm", VERDE_CL)
        self.swing(theta=-50, phi=66, run_time=2.0)
        regla = self.card("Regla de 1 segundo",
                          ttex(r"¿Números grandes? Euclides. ¿Ya factorizados? $\min$ y $\max$ de exponentes.", 26),
                          C_REGLA, corner=m.DL, shift=np.array([0, 1.25, 0]))
        self.wait(2.5)
