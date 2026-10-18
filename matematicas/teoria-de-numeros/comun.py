"""Piezas comunes a las cuatro clases de teoría de números.

Andamiaje compartido: cámara de frente sobre el plano xz, subtítulos abajo,
tarjetas de capítulo con barra de progreso, y paneles fijos en pantalla para las fórmulas.
"""

import textwrap

import manimgx as m
import numpy as np

# ── paleta ────────────────────────────────────────────────────────────────────
AZUL = "#3B7DD8"
AZUL_OSC = "#2D5F8A"
MORADO = "#8E5CC4"
VERDE = "#2E8B57"
VERDE_CL = "#5CC48E"
TEAL = "#1F9E89"
AMBAR = "#D9A441"
NARANJA = "#C8734A"
ROJO = "#C0392B"
ROJO_CL = "#E06C5E"
GRIS = "#6E7681"
GRIS_OSC = "#3A414A"
BORDE = "#9AA4AE"
PANEL_BG = "#0E1117"

# colores por tipo de nota (las tarjetas ya no los usan; quedan para figuras)
C_TEOREMA = AZUL_OSC
C_DEF = TEAL
C_TRAMPA = ROJO
C_REGLA = VERDE
C_ESQ = MORADO
C_INT = AMBAR

TEX_PRE = r"\newcommand{\md}[1]{\ (\mathrm{mod}\ #1)}\newcommand{\mcd}{\operatorname{mcd}}"


# ── utilidades 3D ─────────────────────────────────────────────────────────────
def P(x: float, z: float, y: float = 0.0) -> np.ndarray:
    return np.array([x, y, z], dtype=float)


def up(mob: m.Mobject) -> m.Mobject:
    """Pone un objeto plano de pie en el plano xz mirando a la cámara."""
    return mob.rotate(m.PI / 2, m.RIGHT)


def txt(text: str, size: int = 24, color=m.WHITE) -> m.Text:
    return m.Text(text, font_size=size, color=color)


def mono(text: str, size: int = 24, color=m.GREY_A) -> m.Text:
    return m.Text(text, font="monospace", font_size=size, color=color)


def tex(s: str, size: int = 36, color=m.WHITE) -> m.MathTex:
    return m.MathTex(TEX_PRE + s, font_size=size, color=color)


def ttex(s: str, size: int = 30, color=m.WHITE) -> m.Tex:
    # el modo texto de manimgx no entiende los espacios de LaTeX: se cambian por espacios normales
    parts = s.split("$")
    for i in range(0, len(parts), 2):
        parts[i] = parts[i].replace(r"\quad", "   ").replace("\\ ", " ").replace("~", " ")
    return m.Tex(TEX_PRE + "$".join(parts), font_size=size, color=color)


def cubo(label: str, pos, color: str, side: float = 0.6, size: int = 26, text_color=m.WHITE,
         is_tex: bool = False) -> m.Group:
    """Cubo con una etiqueta en la cara que mira a la cámara."""
    c = m.Cube(side_length=side, fill_color=color, fill_opacity=1, stroke_width=0).move_to(pos)
    if label == "":
        return m.Group(c)
    lab = tex(label, size, text_color) if is_tex else txt(label, size, text_color)
    up(lab).move_to(np.asarray(pos) + np.array([0, -side / 2 - 0.03, 0]))
    return m.Group(c, lab)


def losa(w: float, h: float, pos, color: str, depth: float = 0.25, opacity: float = 1.0) -> m.Prism:
    """Losa rectangular de pie en el plano xz (ancho w, alto h)."""
    return m.Prism(dimensions=[w, depth, h], fill_color=color, fill_opacity=opacity,
                   stroke_width=0).move_to(pos)


def etiqueta(text: str, pos, size: int = 24, color=m.WHITE, is_tex: bool = False, dy: float = -0.2):
    lab = tex(text, size, color) if is_tex else txt(text, size, color)
    return up(lab).move_to(np.asarray(pos) + np.array([0, dy, 0]))


def esfera(pos, color: str, r: float = 0.22) -> m.Sphere:
    return m.Sphere(radius=r).set_color(color).move_to(pos)


# ── utilidades 2D (fijas en pantalla) ─────────────────────────────────────────
def caja(titulo: str, cuerpo: m.Mobject, color: str | None = None, width: float | None = None) -> m.VGroup:
    """Nota estilo libro: título en serif con punto, filete fino y el cuerpo; sin colores.

    `color` se ignora; se conserva para no tocar las llamadas de los módulos.
    """
    head = m.Text(titulo.rstrip(".") + ".", font="Georgia", font_size=22, color=m.WHITE, weight=m.BOLD)
    pad = 0.28
    w = max(cuerpo.width, head.width) + 2 * pad if width is None else width
    head.move_to(m.ORIGIN, aligned_edge=m.UL)
    rule = m.Line(m.ORIGIN, (w - 2 * pad) * m.RIGHT, color=GRIS, stroke_width=1)
    rule.next_to(head, m.DOWN, buff=0.12, aligned_edge=m.LEFT)
    cuerpo.next_to(rule, m.DOWN, buff=0.2, aligned_edge=m.LEFT)
    inner = m.VGroup(head, rule, cuerpo)
    bg = m.Rectangle(width=w, height=inner.height + 2 * 0.22, fill_color=PANEL_BG, fill_opacity=0.9,
                     stroke_width=0)
    bg.move_to(inner).align_to(inner, m.LEFT).shift(pad * m.LEFT)
    return m.VGroup(bg, head, rule, cuerpo)


def lineas(*items, buff: float = 0.18, aligned=m.LEFT) -> m.VGroup:
    return m.VGroup(*items).arrange(m.DOWN, aligned_edge=aligned, buff=buff)


def recta(lo: int, hi: int, centro, ancho: float, font: int = 18, solo=None) -> m.NumberLine:
    """Recta numérica plana; `solo` limita los números que se escriben (por ejemplo, solo los pares)."""
    excluir = [k for k in range(lo, hi + 1) if solo is not None and k not in solo]
    nl = m.NumberLine(x_range=[lo, hi, 1], length=ancho, include_numbers=True, font_size=font, color=BORDE,
                      numbers_to_exclude=excluir)
    return nl.move_to(centro)


def arco(nl: m.NumberLine, a: float, b: float, color, angulo: float = 1.4) -> m.CurvedArrow:
    """Flecha curva de a a b que siempre pasa por encima de la recta."""
    s = -1 if b > a else 1
    return m.CurvedArrow(nl.n2p(a), nl.n2p(b), angle=s * angulo, color=color, stroke_width=4)


class Clase(m.ThreeDScene):
    CHAPTERS: list[str] = []
    START: int = 1  # número del primer capítulo de este video

    # ── andamiaje común ──────────────────────────────────────────────────────
    def home(self, run_time: float | None = None, zoom: float = 0.92, center=m.ORIGIN):
        if run_time is None:
            self.set_camera_orientation(phi=76 * m.DEGREES, theta=-90 * m.DEGREES, zoom=zoom,
                                        frame_center=center)
        else:
            self.move_camera(phi=76 * m.DEGREES, theta=-90 * m.DEGREES, zoom=zoom, frame_center=center,
                             run_time=run_time)

    def pin(self, *mobs):
        self.add_fixed_in_frame_mobjects(*mobs)
        return mobs[0] if len(mobs) == 1 else mobs

    def cap(self, text: str, color=m.WHITE, hold: float | None = None, *anims, run_time: float = 0.6):
        """Subtítulo de abajo, como lo diría el profesor; espera lo que toma leerlo."""
        lines = textwrap.wrap(text, 82)
        t = m.Text("\n".join(lines), font_size=24, color=color)
        bg = m.RoundedRectangle(width=t.width + 0.5, height=t.height + 0.3, corner_radius=0.12,
                                fill_color=m.BLACK, fill_opacity=0.72, stroke_width=0).move_to(t)
        new = m.VGroup(bg, t).to_edge(m.DOWN, buff=0.22)
        self.pin(new)
        out = [m.FadeOut(self._cap)] if self._cap is not None else []
        self.play(m.FadeIn(new, shift=0.12 * m.UP), *out, *anims, run_time=run_time)
        self._cap = new
        self.wait(hold if hold is not None else max(1.8, len(text) / 17))

    def uncap(self):
        if self._cap is not None:
            self.play(m.FadeOut(self._cap), run_time=0.4)
            self._cap = None

    def card(self, titulo: str, cuerpo: m.Mobject, color: str = C_TEOREMA, corner=m.UL,
             width: float | None = None, write: bool = True, shift=None):
        """Tarjeta fija en pantalla (teorema, definición, trampa...)."""
        c = caja(titulo, cuerpo, color, width)
        if corner is not None:
            c.to_corner(corner, buff=0.3)
            if np.array_equal(corner, m.UL) or np.array_equal(corner, m.UR):
                c.shift(0.45 * m.DOWN)
        if shift is not None:
            c.shift(shift)
        self.pin(c)
        if write:
            self.play(m.LaggedStart(m.FadeIn(c[:3]), m.Write(c[3]), lag_ratio=0.3),
                      run_time=min(3.0, 1.0 + c[3].width * 0.15))
        else:
            self.play(m.FadeIn(c), run_time=0.6)
        return c

    def swing(self, theta: float = -55, phi: float = 68, run_time: float = 2.5):
        """Gira la cámara hacia un lado y vuelve, sin que los textos queden de espaldas."""
        self.move_camera(phi=phi * m.DEGREES, theta=theta * m.DEGREES, run_time=run_time)
        self.move_camera(phi=72 * m.DEGREES, theta=(-180 - theta) * m.DEGREES, run_time=run_time * 1.4)
        self.home(run_time=run_time * 0.8)

    def clear_stage(self):
        keep = set(self._hud)
        rest = [mob for mob in self.mobjects if mob not in keep]
        if rest:
            self.play(*(m.FadeOut(mob) for mob in rest), run_time=0.8)
        for mob in rest:
            self.remove(mob)
        self._cap = None

    def chapter(self, n: int):
        """n es el número global del capítulo (1..19)."""
        self.clear_stage()
        self.home()
        title = self.CHAPTERS[n - self.START]
        ring = m.Circle(radius=0.75, color=m.YELLOW, stroke_width=5)
        num = m.Text(str(n), font_size=64, color=m.YELLOW).move_to(ring)
        name = m.Text(title, font_size=44)
        card = m.VGroup(m.VGroup(ring, num), name).arrange(m.RIGHT, buff=0.5)
        if card.width > 13:
            card.scale(13 / card.width)
        line = m.Line(name.get_corner(m.DL) + 0.15 * m.DOWN, name.get_corner(m.DR) + 0.15 * m.DOWN,
                      color=m.YELLOW, stroke_width=3)
        self.pin(card, line)
        self.play(m.SpinInFromNothing(card[0]), m.Write(name), run_time=1.3)
        self.play(m.Create(line), run_time=0.6)
        self.wait(0.8)
        label = m.Text(f"{n}  {title}", font_size=20, color=m.GREY_A).to_corner(m.UL, buff=0.22)
        k = n - self.START + 1
        progress = m.Line([-7.1, 3.98, 0], [-7.1 + 14.2 * k / len(self.CHAPTERS), 3.98, 0], color=m.YELLOW,
                          stroke_width=5)
        self.pin(label, progress)
        self.remove(label, progress)
        self.play(m.ReplacementTransform(card, label), m.FadeOut(line),
                  m.Transform(self._progress, progress), *([m.FadeOut(self._label)] if self._label else []),
                  run_time=1)
        self._hud.discard(self._label)
        self._label = label
        self._hud.add(label)

    def derivar(self, pasos: list[str], anchor, size: int = 34, buff: float = 0.22, notas=None,
                hold: float = 0.6, color=m.WHITE, resaltar=None):
        """Escribe una cadena de igualdades, cada línea nace de una copia de la anterior.

        `resaltar[i]`, si se da, es un objeto en pantalla (la fila de una tabla, por ejemplo) que se marca
        mientras se escribe la línea i.
        """
        notas = notas or [None] * len(pasos)
        resaltar = resaltar or [None] * len(pasos)
        prev = None
        out = m.VGroup()
        marcado = None
        for s, nota, obj in zip(pasos, notas, resaltar):
            line = tex(s, size, color)
            if prev is None:
                line.move_to(anchor, aligned_edge=m.UL)
            else:
                line.next_to(prev, m.DOWN, buff=buff, aligned_edge=m.LEFT)
            if obj is not None:
                extra = [m.Circumscribe(obj, color=AMBAR, buff=0.06, stroke_width=3),
                         obj.animate.set_color(AMBAR)]
                if marcado is not None:
                    extra.append(marcado.animate.set_color(m.GREY_B))
                self.play(*extra, run_time=0.7)
                marcado = obj
            if prev is None:
                self.pin(line)
                self.play(m.Write(line), run_time=1.0)
            else:
                self.morph(prev, line)
            out.add(line)
            if nota:
                self.cap(nota)
            else:
                self.wait(hold)
            prev = line
        return out

    def morph(self, src, dst, run_time: float = 1.0):
        """Una copia de src se convierte en dst (fijos en pantalla): los símbolos que se repiten viajan a su
        nuevo lugar y el resto aparece o se desvanece."""
        ghost = src.copy()
        self.pin(ghost, dst)
        self.remove(dst)
        self.play(m.TransformMatchingShapes(ghost, dst), run_time=run_time)
        self.remove(ghost)
        self.pin(dst)

    # ── visuales 2D reutilizables ────────────────────────────────────────────
    def saltar(self, nl: m.NumberLine, bola: m.Mobject, desde: float, hasta: list[float], color,
               etiquetas=None, angulo: float = 1.4, run_time: float = 0.7) -> m.VGroup:
        """La bola salta por la recta numérica de `desde` a cada valor de `hasta`; cada salto deja su arco."""
        etiquetas = etiquetas or [None] * len(hasta)
        arcos = m.VGroup()
        x = desde
        for y, lab in zip(hasta, etiquetas):
            arc = arco(nl, x, y, color, angulo)
            parts = [arc]
            anims = [m.Create(arc), m.MoveAlongPath(bola, arc)]
            if lab:
                t = tex(lab, 24, color).next_to(arc, m.UP, buff=0.06)
                parts.append(t)
                anims.append(m.FadeIn(t, shift=0.1 * m.DOWN))
            self.pin(*parts)
            self.play(*anims, run_time=run_time)
            self.play(m.Flash(nl.n2p(y), color=color, flash_radius=0.16, line_length=0.12, num_lines=10),
                      run_time=0.35)
            arcos.add(*parts)
            x = y
        return arcos

    def barra_exponente(self, pot: str, q: int, k: str, r: str, final: str, centro, ancho: float = 7.0,
                        notas=(None, None, None), max_vis: int = 6) -> m.VGroup:
        """El exponente como barra: q bloques de tamaño k, que valen 1, y un resto r, que es lo único que queda.

        Las tres notas acompañan: la barra armada, los bloques volviéndose 1, y el resultado.
        """
        alto = 0.55
        comprimido = q > max_vis
        n_bloques = 4 if comprimido else q
        w_r = 1.0
        n_slots = n_bloques + (1 if comprimido else 0)
        w_b = (ancho - w_r - 0.08 * n_slots) / n_slots
        bloques, slots = m.VGroup(), []
        for i in range(n_slots):
            if comprimido and i == 3:
                slots.append(tex(r"\cdots", 30, m.GREY_B))
                continue
            rect = m.Rectangle(width=w_b, height=alto, fill_color=AZUL_OSC, fill_opacity=1, stroke_color=AZUL,
                               stroke_width=2)
            lab = tex(k, 24).move_to(rect)
            if lab.width > w_b - 0.1:
                lab.scale_to_fit_width(w_b - 0.15)
            b = m.VGroup(rect, lab)
            bloques.add(b)
            slots.append(b)
        resto = m.VGroup(m.Rectangle(width=w_r, height=alto, fill_color=AMBAR, fill_opacity=1, stroke_width=0),
                         tex(r, 26, m.BLACK))
        resto[1].move_to(resto[0])
        barra = m.VGroup(*slots, resto).arrange(m.RIGHT, buff=0.08).move_to(centro)
        titulo = tex(pot, 40, m.YELLOW).next_to(barra, m.UP, buff=0.3, aligned_edge=m.LEFT)
        cuerpo = m.VGroup(*slots)
        br_q = m.BraceLabel(cuerpo, k if q == 1 else rf"{q}\cdot {k}", font_size=28)
        br_r = m.BraceLabel(resto, r, font_size=28, color=AMBAR)
        self.pin(titulo, barra, br_q, br_r)
        self.remove(barra, br_q, br_r)
        self.play(m.Write(titulo), run_time=0.7)
        self.play(m.LaggedStart(*(m.GrowFromEdge(s, m.LEFT) for s in slots), m.GrowFromEdge(resto, m.LEFT),
                                lag_ratio=0.15), run_time=1.4)
        self.play(m.FadeIn(br_q, shift=0.1 * m.UP), m.FadeIn(br_r, shift=0.1 * m.UP), run_time=0.6)
        if notas[0]:
            self.cap(notas[0])
        unos = [tex("1", 26, m.GREY_B).move_to(b[1]) for b in bloques]
        uno_q = m.BraceLabel(cuerpo, r"\equiv 1", font_size=28, color=m.GREY_B)
        self.pin(*unos, uno_q)
        self.remove(*unos, uno_q)
        self.play(*(m.FadeToColor(b[0], GRIS_OSC) for b in bloques),
                  *(m.FadeTransform(b[1], u) for b, u in zip(bloques, unos)),
                  m.FadeTransform(br_q, uno_q), m.Indicate(resto, color=m.YELLOW, scale_factor=1.1),
                  run_time=1.0)
        if notas[1]:
            self.cap(notas[1])
        fin = tex(final, 40, m.YELLOW)
        self.play(m.ShrinkToCenter(m.VGroup(*(b[0] for b in bloques), *unos)),
                  *(m.FadeOut(s) for s in slots if s not in bloques), m.FadeOut(uno_q), m.FadeOut(br_r),
                  resto.animate.next_to(titulo, m.RIGHT, buff=0.35), run_time=1.0)
        fin.next_to(resto, m.RIGHT, buff=0.3)
        self.pin(fin)
        self.play(m.Write(fin), m.Flash(resto, color=m.YELLOW), run_time=0.8)
        if notas[2]:
            self.cap(notas[2])
        return m.VGroup(titulo, resto, fin)

    def titulo_video(self, titulo: str, sub: str):
        title = m.Text(titulo, font_size=56)
        subt = m.Text(sub, font_size=30, color=m.GREY_A)
        head = m.VGroup(title, subt).arrange(m.DOWN, buff=0.3)
        self.pin(head)
        self.play(m.Write(title), m.FadeIn(subt, shift=0.2 * m.UP), run_time=1.8)
        self.wait(1.2)
        self.play(head.animate.scale(0.6).to_edge(m.UP, buff=0.35), run_time=0.9)
        items = m.VGroup(*(m.Text(f"{self.START + i:>2}   {t}", font_size=26, color=m.GREY_A)
                           for i, t in enumerate(self.CHAPTERS))).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.16)
        items.next_to(head, m.DOWN, buff=0.45)
        self.pin(items)
        self.play(m.LaggedStart(*(m.FadeIn(i, shift=0.3 * m.RIGHT) for i in items), lag_ratio=0.12),
                  run_time=2.0)
        return head, items

    def setup_hud(self):
        self._cap = self._label = None
        track = m.Line([-7.1, 3.98, 0], [7.1, 3.98, 0], color=m.GREY_D, stroke_width=5)
        self._progress = m.Line([-7.1, 3.98, 0], [-7.08, 3.98, 0], color=m.YELLOW, stroke_width=5)
        self.pin(track, self._progress)
        self._hud = {track, self._progress}

    def cierre(self, puntos: list[str], siguiente: str | None = None):
        self.clear_stage()
        head = m.Text("Para llevarse", font_size=40, color=m.YELLOW)
        items = m.VGroup(*(m.Text("•  " + p, font_size=26) for p in puntos)).arrange(
            m.DOWN, aligned_edge=m.LEFT, buff=0.28)
        g = m.VGroup(head, items).arrange(m.DOWN, buff=0.5)
        if g.width > 13:
            g.scale(13 / g.width)
        self.pin(g)
        self.play(m.Write(head), run_time=0.8)
        self.play(m.LaggedStart(*(m.FadeIn(i, shift=0.3 * m.RIGHT) for i in items), lag_ratio=0.35),
                  run_time=0.6 * len(puntos) + 0.6)
        self.wait(2 + 0.8 * len(puntos))
        if siguiente:
            self.cap(siguiente, m.GREY_A)
        self.clear_stage()
