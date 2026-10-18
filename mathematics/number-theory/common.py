"""Shared pieces for the four number theory lessons.

A black stage with solid colored objects, book-style note cards and captions on dark rounded boxes. The
camera faces the xz plane, captions sit at the bottom, and formulas live on panels pinned to the screen.
"""

import textwrap

import manimgx as m
import numpy as np

# ── palette ───────────────────────────────────────────────────────────────────
BG = "#000000"        # the stage
PANEL_BG = "#0E1117"  # behind cards
INK = "#FFFFFF"       # main lines and text
MUTED = "#BBBBBB"     # secondary text, inactive marks
BLUE = "#3B7DD8"
DEEP = "#2D5F8A"
PURPLE = "#8E5CC4"
GREEN = "#2E8B57"
GREEN_L = "#5CC48E"
TEAL = "#1F9E89"
AMBER = "#F7D96F"     # highlights: what the eye should follow
ORANGE = "#C8734A"
RED = "#C0392B"
RED_L = "#E06C5E"
GREY = "#6E7681"
GREY_D = "#3A414A"    # inactive fills
EDGE = "#9AA4AE"

CARD_FONT = "Georgia"

# kinds of note cards
C_THEOREM = "theorem"
C_DEF = "definition"
C_MISTAKE = "mistake"
C_RULE = "rule"
C_WORKED = "worked"
C_QUESTION = "question"

TEX_PRE = r"\newcommand{\md}[1]{\ (\mathrm{mod}\ #1)}\newcommand{\lcm}{\operatorname{lcm}}"


# ── 3D helpers ────────────────────────────────────────────────────────────────
def P(x: float, z: float, y: float = 0.0) -> np.ndarray:
    return np.array([x, y, z], dtype=float)


def up(mob: m.Mobject) -> m.Mobject:
    """Stands a flat object up on the xz plane, facing the camera."""
    return mob.rotate(m.PI / 2, m.RIGHT)


def txt(text: str, size: int = 24, color=INK) -> m.Text:
    return m.Text(text, font_size=size, color=color)


def tex(s: str, size: int = 36, color=INK) -> m.MathTex:
    return m.MathTex(TEX_PRE + s, font_size=size, color=color)


def ttex(s: str, size: int = 30, color=INK) -> m.Tex:
    # manimgx's text mode doesn't know LaTeX spacing commands: swap them for plain spaces
    parts = s.split("$")
    for i in range(0, len(parts), 2):
        parts[i] = parts[i].replace(r"\quad", "   ").replace("\\ ", " ").replace("~", " ")
    return m.Tex(TEX_PRE + "$".join(parts), font_size=size, color=color)


def solid(opacity: float | None) -> float | None:
    """Solids stay opaque; only a low opacity (dimming something out) goes through."""
    return opacity if opacity is not None and opacity < 0.5 else 1.0


def tint(mob: m.Mobject, color, opacity: float | None = None):
    """Animation that repaints a solid."""
    return mob.animate.set_fill(color, opacity=solid(opacity))


def cube(label: str, pos, color: str, side: float = 0.6, size: int = 26, text_color=INK,
         is_tex: bool = False) -> m.Group:
    """Cube with a label on the face toward the camera."""
    c = m.Cube(side_length=side, fill_color=color, fill_opacity=1, stroke_width=0).move_to(pos)
    if label == "":
        return m.Group(c)
    lab = tex(label, size, text_color) if is_tex else txt(label, size, text_color)
    up(lab).move_to(np.asarray(pos) + np.array([0, -side / 2 - 0.03, 0]))
    return m.Group(c, lab)


def slab(w: float, h: float, pos, color: str, depth: float = 0.25, opacity: float = 1.0) -> m.Prism:
    """Rectangular slab standing on the xz plane (width w, height h)."""
    return m.Prism(dimensions=[w, depth, h], fill_color=color, fill_opacity=solid(opacity),
                   stroke_width=0).move_to(pos)


def label(text: str, pos, size: int = 24, color=INK, is_tex: bool = False, dy: float = -0.2):
    lab = tex(text, size, color) if is_tex else txt(text, size, color)
    return up(lab).move_to(np.asarray(pos) + np.array([0, dy, 0]))


def sphere(pos, color: str, r: float = 0.22) -> m.Sphere:
    return m.Sphere(radius=r).set_color(color).move_to(pos)


# ── 2D helpers (pinned to the screen) ─────────────────────────────────────────
def note_box(title: str, body: m.Mobject, kind: str = C_THEOREM, width: float | None = None) -> m.VGroup:
    """Book-style note: a serif title with a period, a thin rule and the body, on a dark panel.

    `kind` doesn't change the look; it's kept so the call says what the note is.
    """
    head = m.Text(title.rstrip(".") + ".", font=CARD_FONT, font_size=22, color=INK, weight=m.BOLD)
    pad = 0.28
    w = max(body.width, head.width) + 2 * pad if width is None else width
    head.move_to(m.ORIGIN, aligned_edge=m.UL)
    rule = m.Line(m.ORIGIN, (w - 2 * pad) * m.RIGHT, color=GREY, stroke_width=1)
    rule.next_to(head, m.DOWN, buff=0.12, aligned_edge=m.LEFT)
    body.next_to(rule, m.DOWN, buff=0.2, aligned_edge=m.LEFT)
    inner = m.VGroup(head, rule, body)
    bg = m.Rectangle(width=w, height=inner.height + 2 * 0.22, fill_color=PANEL_BG, fill_opacity=0.9,
                     stroke_width=0)
    bg.move_to(inner).align_to(inner, m.LEFT).shift(pad * m.LEFT)
    return m.VGroup(bg, head, rule, body)


def stack(*items, buff: float = 0.18, aligned=m.LEFT) -> m.VGroup:
    return m.VGroup(*items).arrange(m.DOWN, aligned_edge=aligned, buff=buff)


def number_line(lo: int, hi: int, center, width: float, font: int = 18, only=None) -> m.NumberLine:
    """Flat number line; `only` limits which numbers are written (only the even ones, say)."""
    skip = [k for k in range(lo, hi + 1) if only is not None and k not in only]
    nl = m.NumberLine(x_range=[lo, hi, 1], length=width, include_numbers=True, font_size=font, color=EDGE,
                      numbers_to_exclude=skip)
    return nl.move_to(center)


def hop_arc(nl: m.NumberLine, a: float, b: float, color, angle: float = 1.4) -> m.CurvedArrow:
    """Curved arrow from a to b that always passes above the line."""
    s = -1 if b > a else 1
    return m.CurvedArrow(nl.n2p(a), nl.n2p(b), angle=s * angle, color=color, stroke_width=4)


class Lesson(m.ThreeDScene):
    CHAPTERS: list[str] = []
    START: int = 1  # number of this video's first chapter

    # ── shared scaffolding ───────────────────────────────────────────────────
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

    def cap(self, text: str, color=INK, hold: float | None = None, *anims, run_time: float = 0.6):
        """Caption at the bottom, the way a teacher would say it; waits as long as it takes to read."""
        lines = textwrap.wrap(text, 84)
        t = m.VGroup(*(m.Text(line, font_size=24, color=color) for line in lines)).arrange(m.DOWN, buff=0.14)
        bg = m.RoundedRectangle(width=t.width + 0.5, height=t.height + 0.3, corner_radius=0.12,
                                fill_color=BG, fill_opacity=0.72, stroke_width=0).move_to(t)
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

    def card(self, title: str, body: m.Mobject, kind: str = C_THEOREM, corner=m.UL,
             width: float | None = None, write: bool = True, shift=None):
        """A note pinned to the screen (theorem, definition, common mistake...)."""
        c = note_box(title, body, kind, width)
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
        """Turns the camera to one side and back, without leaving any text facing away."""
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
        """n is the chapter's number across the whole series (1..19)."""
        self.clear_stage()
        self.home()
        title = self.CHAPTERS[n - self.START]
        ring = m.Circle(radius=0.75, color=AMBER, stroke_width=5)
        num = m.Text(str(n), font_size=64, color=AMBER).move_to(ring)
        name = m.Text(title, font_size=44, color=INK)
        card = m.VGroup(m.VGroup(ring, num), name).arrange(m.RIGHT, buff=0.5)
        if card.width > 13:
            card.scale(13 / card.width)
        line = m.Line(name.get_corner(m.DL) + 0.15 * m.DOWN, name.get_corner(m.DR) + 0.15 * m.DOWN,
                      color=AMBER, stroke_width=3)
        self.pin(card, line)
        self.play(m.SpinInFromNothing(card[0]), m.Write(name), run_time=1.3)
        self.play(m.Create(line), run_time=0.6)
        self.wait(0.8)
        label_ = m.Text(f"{n}  {title}", font_size=20, color=m.GREY_A).to_corner(m.UL, buff=0.22)
        k = n - self.START + 1
        progress = m.Line([-7.1, 3.98, 0], [-7.1 + 14.2 * k / len(self.CHAPTERS), 3.98, 0], color=AMBER,
                          stroke_width=5)
        self.pin(label_, progress)
        self.remove(label_, progress)
        self.play(m.ReplacementTransform(card, label_), m.FadeOut(line),
                  m.Transform(self._progress, progress), *([m.FadeOut(self._label)] if self._label else []),
                  run_time=1)
        self._hud.discard(self._label)
        self._label = label_
        self._hud.add(label_)

    def derive(self, steps: list[str], anchor, size: int = 34, buff: float = 0.22, notes=None,
               hold: float = 0.6, color=INK, highlight=None):
        """Writes a chain of equalities; each line is born from a copy of the previous one.

        `highlight[i]`, if given, is something on screen (a row of a table, say) that gets marked while line i
        is written.
        """
        notes = notes or [None] * len(steps)
        highlight = highlight or [None] * len(steps)
        prev = None
        out = m.VGroup()
        marked = None
        for s, note, obj in zip(steps, notes, highlight):
            line = tex(s, size, color)
            if prev is None:
                line.move_to(anchor, aligned_edge=m.UL)
            else:
                line.next_to(prev, m.DOWN, buff=buff, aligned_edge=m.LEFT)
            if obj is not None:
                extra = [m.Circumscribe(obj, color=AMBER, buff=0.06, stroke_width=3),
                         obj.animate.set_color(AMBER)]
                if marked is not None:
                    extra.append(marked.animate.set_color(MUTED))
                self.play(*extra, run_time=0.7)
                marked = obj
            if prev is None:
                self.pin(line)
                self.play(m.Write(line), run_time=1.0)
            else:
                self.morph(prev, line)
            out.add(line)
            if note:
                self.cap(note)
            else:
                self.wait(hold)
            prev = line
        return out

    def morph(self, src, dst, run_time: float = 1.0):
        """A copy of src turns into dst (both pinned): symbols that repeat travel to their new place, the rest
        fades in or out."""
        ghost = src.copy()
        self.pin(ghost, dst)
        self.remove(dst)
        self.play(m.TransformMatchingShapes(ghost, dst), run_time=run_time)
        self.remove(ghost)
        self.pin(dst)

    # ── reusable 2D visuals ──────────────────────────────────────────────────
    def hop(self, nl: m.NumberLine, ball: m.Mobject, start: float, stops: list[float], color,
            labels=None, angle: float = 1.4, run_time: float = 0.7) -> m.VGroup:
        """The ball hops along the number line from `start` to each value in `stops`, leaving its arcs."""
        labels = labels or [None] * len(stops)
        arcs = m.VGroup()
        x = start
        for y, lab in zip(stops, labels):
            arc = hop_arc(nl, x, y, color, angle)
            parts = [arc]
            anims = [m.Create(arc), m.MoveAlongPath(ball, arc)]
            if lab:
                t = tex(lab, 24, color).next_to(arc, m.UP, buff=0.06)
                parts.append(t)
                anims.append(m.FadeIn(t, shift=0.1 * m.DOWN))
            self.pin(*parts)
            self.play(*anims, run_time=run_time)
            self.play(m.Flash(nl.n2p(y), color=color, flash_radius=0.16, line_length=0.12, num_lines=10),
                      run_time=0.35)
            arcs.add(*parts)
            x = y
        return arcs

    def exponent_bar(self, power: str, q: int, k: str, r: str, result: str, center, width: float = 7.0,
                     notes=(None, None, None), max_shown: int = 6) -> m.VGroup:
        """The exponent as a bar: q blocks of size k, each worth 1, and a remainder r, the only part that stays.

        The three notes go with: the bar being built, the blocks turning into 1, and the result.
        """
        height = 0.55
        squeezed = q > max_shown
        n_blocks = 4 if squeezed else q
        w_r = 1.0
        n_slots = n_blocks + (1 if squeezed else 0)
        w_b = (width - w_r - 0.08 * n_slots) / n_slots
        blocks, slots = m.VGroup(), []
        for i in range(n_slots):
            if squeezed and i == 3:
                slots.append(tex(r"\cdots", 30, MUTED))
                continue
            rect = m.Rectangle(width=w_b, height=height, fill_color=DEEP, fill_opacity=1, stroke_color=BLUE,
                               stroke_width=2)
            lab = tex(k, 24).move_to(rect)
            if lab.width > w_b - 0.1:
                lab.scale_to_fit_width(w_b - 0.15)
            b = m.VGroup(rect, lab)
            blocks.add(b)
            slots.append(b)
        rest = m.VGroup(m.Rectangle(width=w_r, height=height, fill_color=AMBER, fill_opacity=1, stroke_width=0),
                        tex(r, 26, BG))
        rest[1].move_to(rest[0])
        bar = m.VGroup(*slots, rest).arrange(m.RIGHT, buff=0.08).move_to(center)
        head = tex(power, 40, AMBER).next_to(bar, m.UP, buff=0.3, aligned_edge=m.LEFT)
        body = m.VGroup(*slots)
        br_q = m.BraceLabel(body, k if q == 1 else rf"{q}\cdot {k}", font_size=28, color=INK)
        br_r = m.BraceLabel(rest, r, font_size=28, color=AMBER)
        self.pin(head, bar, br_q, br_r)
        self.remove(bar, br_q, br_r)
        self.play(m.Write(head), run_time=0.7)
        self.play(m.LaggedStart(*(m.GrowFromEdge(s, m.LEFT) for s in slots), m.GrowFromEdge(rest, m.LEFT),
                                lag_ratio=0.15), run_time=1.4)
        self.play(m.FadeIn(br_q, shift=0.1 * m.UP), m.FadeIn(br_r, shift=0.1 * m.UP), run_time=0.6)
        if notes[0]:
            self.cap(notes[0])
        ones = [tex("1", 26, MUTED).move_to(b[1]) for b in blocks]
        one_q = m.BraceLabel(body, r"\equiv 1", font_size=28, color=MUTED)
        self.pin(*ones, one_q)
        self.remove(*ones, one_q)
        self.play(*(m.FadeToColor(b[0], GREY_D) for b in blocks),
                  *(m.FadeTransform(b[1], u) for b, u in zip(blocks, ones)),
                  m.FadeTransform(br_q, one_q), m.Indicate(rest, color=AMBER, scale_factor=1.1),
                  run_time=1.0)
        if notes[1]:
            self.cap(notes[1])
        res = tex(result, 40, AMBER)
        self.play(m.ShrinkToCenter(m.VGroup(*(b[0] for b in blocks), *ones)),
                  *(m.FadeOut(s) for s in slots if s not in blocks), m.FadeOut(one_q), m.FadeOut(br_r),
                  rest.animate.next_to(head, m.RIGHT, buff=0.35), run_time=1.0)
        res.next_to(rest, m.RIGHT, buff=0.3)
        self.pin(res)
        self.play(m.Write(res), m.Flash(rest, color=AMBER), run_time=0.8)
        if notes[2]:
            self.cap(notes[2])
        return m.VGroup(head, rest, res)

    def title_card(self, title: str, sub: str):
        head_ = m.Text(title, font_size=56, color=INK)
        subt = m.Text(sub, font_size=30, color=m.GREY_A)
        head = m.VGroup(head_, subt).arrange(m.DOWN, buff=0.3)
        self.pin(head)
        self.play(m.Write(head_), m.FadeIn(subt, shift=0.2 * m.UP), run_time=1.8)
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
        self.camera.background_color = BG
        self._cap = self._label = None
        track = m.Line([-7.1, 3.98, 0], [7.1, 3.98, 0], color=m.GREY_D, stroke_width=5)
        self._progress = m.Line([-7.1, 3.98, 0], [-7.08, 3.98, 0], color=AMBER, stroke_width=5)
        self.pin(track, self._progress)
        self._hud = {track, self._progress}

    def takeaways(self, points: list[str], next_up: str | None = None):
        self.clear_stage()
        head = m.Text("Takeaways", font_size=40, color=AMBER)
        items = m.VGroup(*(m.Text("•  " + p, font_size=26, color=INK) for p in points)).arrange(
            m.DOWN, aligned_edge=m.LEFT, buff=0.28)
        g = m.VGroup(head, items).arrange(m.DOWN, buff=0.5)
        if g.width > 13:
            g.scale(13 / g.width)
        self.pin(g)
        self.play(m.Write(head), run_time=0.8)
        self.play(m.LaggedStart(*(m.FadeIn(i, shift=0.3 * m.RIGHT) for i in items), lag_ratio=0.35),
                  run_time=0.6 * len(points) + 0.6)
        self.wait(2 + 0.8 * len(points))
        if next_up:
            self.cap(next_up, m.GREY_A)
        self.clear_stage()
