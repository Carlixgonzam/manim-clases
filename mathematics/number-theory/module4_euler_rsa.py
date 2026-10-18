"""Number theory, module 4: Euler's φ function, Euler's theorem, self-inverse elements, RSA and a decision map.

    manimgx render module4_euler_rsa.py Module4
"""

import math

import manimgx as m
import numpy as np

from common import (AMBER, BG, BLUE, C_DEF, C_MISTAKE, C_QUESTION, C_RULE, C_THEOREM, C_WORKED, DEEP, EDGE,
                    GREEN, GREEN_L, GREY, GREY_D, INK, MONO_FONT, MUTED, ORANGE, PURPLE, RED, RED_L, TEXT_FONT,
                    Lesson, P, cube, label, slab, sphere, stack, tex, tint, ttex)


def on_circle(k: int, n: int, R: float, cx: float = 0.0, cz: float = 0.0, y: float = 0.0):
    ang = math.pi / 2 - 2 * math.pi * k / n
    return P(cx + R * math.cos(ang), cz + R * math.sin(ang), y)


class Module4(Lesson):
    START = 15
    CHAPTERS = [
        "Euler's φ function",
        "Euler's Theorem",
        "Self-inverse elements",
        "RSA from start to finish",
        "Decision map and common mistakes",
    ]

    def construct(self) -> None:
        self.setup_hud()
        self.intro()
        self.phi()
        self.euler()
        self.self_inverse()
        self.rsa()
        self.decision_map()
        self.takeaways([
            "φ(n) counts the invertible remainders; φ(pᵏ) = pᵏ − pᵏ⁻¹, and φ is multiplicative on coprimes",
            "Euler: if gcd(a, n) = 1, a to the φ(n) is ≡ 1, so the exponent can be reduced mod φ(n)",
            "a² ≡ 1: 2 solutions mod an odd pᵏ, 4 mod 2ⁿ for n ≥ 3, and they multiply via the CRT",
            "RSA: d = e⁻¹ mod φ(n); it works because of Euler and the CRT",
            "Before using a theorem, check its hypothesis: prime, coprime, or pairwise coprime",
        ], "That's the whole journey. The written guide has every proof in full and exercises with solutions")

    def intro(self):
        self.home()
        self.title_card("Number Theory · Module 4", "Euler's φ, Euler's Theorem and RSA")
        self.cap("Fermat only works for prime moduli. In this module we generalize it to any modulus, and with "
                 "that we build RSA, the cryptography that protects most of the internet")

    # ── 15. φ ────────────────────────────────────────────────────────────────
    def phi(self):
        self.chapter(15)
        self.card("Definition",
                  stack(tex(r"\varphi(n) = \#\{x:\ 1\le x\le n,\ \gcd(x,n)=1\}", 32),
                        ttex(r"that is, how many remainders have an inverse mod $n$", 26)), C_DEF, corner=m.UL)
        self.cap("φ of n counts how many numbers between 1 and n are coprime to n. By what we saw in module 2, "
                 "those are exactly the ones with an inverse")
        n = 12
        xs = [-3.3 + 0.6 * i for i in range(n)]
        cubes = [cube(str(k + 1), P(xs[k], 0.4), GREY_D, side=0.5, size=22) for k in range(n)]
        self.play(m.LaggedStart(*(m.FadeIn(c, shift=0.3 * m.IN) for c in cubes), lag_ratio=0.05), run_time=1.2)
        good = [k for k in range(n) if math.gcd(k + 1, n) == 1]
        self.play(*(tint(cubes[k][0], GREEN, 0.5) for k in good),
                  *(tint(cubes[k][0], RED, 0.15) for k in range(n) if k not in good),
                  *(cubes[k].animate.shift(0.25 * m.OUT) for k in good), run_time=1.0)
        res = label(r"\varphi(12) = 4", P(0, -0.7), 38, GREEN_L, is_tex=True)
        self.play(m.Write(res), run_time=0.8)
        self.cap("With 12: only 1, 5, 7 and 11 are coprime to 12, so φ(12) = 4. The red ones share a 2 or a 3 "
                 "with 12", GREEN_L)
        self.clear_stage()

        self.card("Prime power", tex(r"\varphi(p^k) = p^k - p^{k-1} = p^k\left(1-\tfrac1p\right)", 34),
                  C_THEOREM, corner=m.UL)
        self.cap("For a prime power it's easy. With 27 = 3³: a number shares a factor with 27 only if it's a "
                 "multiple of 3")
        cubes = []
        for k in range(27):
            r, c = divmod(k, 9)
            cubes.append(cube(str(k + 1), P(-2.4 + 0.6 * c, 0.9 - 0.65 * r), GREY_D, side=0.5, size=20))
        self.play(m.LaggedStart(*(m.FadeIn(c) for c in cubes), lag_ratio=0.02), run_time=1.4)
        bad = [k for k in range(27) if (k + 1) % 3 == 0]
        self.play(*(tint(cubes[k][0], RED, 0.45) for k in bad),
                  *(tint(cubes[k][0], GREEN, 0.45) for k in range(27) if k not in bad), run_time=0.9)
        res = label(r"\varphi(27) = 27 - 9 = 18", P(0, -1.3), 38, GREEN_L, is_tex=True)
        self.play(m.Write(res), run_time=0.8)
        self.cap("The multiples of 3 are one in every three, so 27/3 = 9 = 3². Subtract them and 18 are left",
                 GREEN_L)
        self.clear_stage()

        # multiplicativity on the CRT grid
        self.card("Multiplicative",
                  tex(r"\gcd(m,n)=1\ \Rightarrow\ \varphi(mn)=\varphi(m)\varphi(n)", 34), C_THEOREM, corner=m.UL)
        self.cap("Why is φ multiplicative? Back to the Chinese Remainder grid, with 15 = 3 · 5")
        c = 0.66
        x0, z0 = -0.6, 0.6
        cells, labs = {}, []
        for x in range(15):
            i, j = x % 3, x % 5
            cells[(i, j)] = slab(c - 0.06, c - 0.06, P(x0 + j * c, z0 - i * c), GREY_D, depth=0.06)
            labs.append(label(str(x), P(x0 + j * c, z0 - i * c, -0.08), 22, INK, dy=0))
        rl = [label(str(i), P(x0 - 0.55, z0 - i * c), 22, ORANGE) for i in range(3)]
        cl = [label(str(j), P(x0 + j * c, z0 + 0.55), 22, BLUE) for j in range(5)]
        self.play(*(m.FadeIn(v) for v in cells.values()), *(m.FadeIn(t) for t in labs + rl + cl), run_time=1.0)
        self.play(*(tint(cells[(i, j)], ORANGE, 0.45) for i in (1, 2) for j in range(5)), run_time=0.7)
        self.cap("x is coprime to 15 iff it's coprime to 3 and to 5. Coprime to 3 means rows 1 and 2: φ(3) = 2 "
                 "rows", ORANGE)
        self.play(*(tint(cells[(i, j)], GREEN, 0.7) for i in (1, 2) for j in (1, 2, 3, 4)),
                  *(tint(cells[(0, j)], GREY_D, 0.38) for j in range(5)),
                  *(tint(cells[(i, 0)], GREY_D, 0.38) for i in range(3)), run_time=0.8)
        self.cap("And coprime to 5 means columns 1 to 4: φ(5) = 4. The cells that satisfy both number "
                 "2 · 4 = 8 = φ(15)", GREEN_L)
        self.swing(theta=-60, phi=64, run_time=2.0)
        self.clear_stage()

        self.card("General formula",
                  tex(r"n=p_1^{a_1}\cdots p_k^{a_k}\ \Rightarrow\ \varphi(n)=n\prod_i\left(1-\tfrac{1}{p_i}\right)", 34),
                  C_THEOREM, corner=m.UL)
        self.derive([
            r"\varphi(119)=\varphi(7)\,\varphi(17)=6\cdot 16 = 96",
            r"\varphi(1000)=\varphi(2^3)\,\varphi(5^3)=4\cdot 100=400",
            r"\varphi(360)=360\cdot\tfrac12\cdot\tfrac23\cdot\tfrac45 = 96",
        ], anchor=np.array([-6.6, 1.3, 0]), size=34, notes=[
            "Three examples. 119 is 7 times 17, two different primes",
            "1000 is 2 cubed times 5 cubed, and each power uses the formula from before",
            "And with the product formula, 360 = 2³ · 3² · 5 gives 96",
        ])
        x0, y, width = -6.2, -1.55, 8.4
        bar = m.Rectangle(width=width, height=0.5, fill_color=GREEN, fill_opacity=0.55, stroke_color=GREEN_L,
                          stroke_width=2)
        bar.move_to([x0 + width / 2, y, 0])
        cnt = m.Integer(360, group_with_commas=False, font_size=44, color=GREEN_L).move_to([4.6, y, 0])
        self.pin(bar, cnt)
        self.remove(bar, cnt)
        self.play(m.GrowFromEdge(bar, m.LEFT), m.FadeIn(cnt), run_time=1.0)
        w = width
        steps = [(r"\times\tfrac12", 2, 180, "Removing the multiples of 2 leaves half: 180"),
                 (r"\times\tfrac23", 3, 120, "From what's left, removing the multiples of 3 leaves two thirds: 120"),
                 (r"\times\tfrac45", 5, 96, "And removing the multiples of 5 leaves four fifths: 96 = φ(360)")]
        for frac, p_, new, note in steps:
            w2 = w * (p_ - 1) / p_
            cut = m.Rectangle(width=w - w2, height=0.5, fill_color=RED, fill_opacity=0.6, stroke_color=RED_L,
                              stroke_width=2)
            cut.move_to([x0 + w2 + (w - w2) / 2, y, 0])
            tag = tex(frac, 34, RED_L).next_to(cut, m.UP, buff=0.2)
            self.pin(cut, tag)
            self.remove(cut, tag)
            self.play(m.FadeIn(cut), m.FadeIn(tag, shift=0.1 * m.DOWN), run_time=0.5)
            self.play(m.FadeOut(cut, shift=0.5 * m.DOWN), m.FadeOut(tag),
                      bar.animate.stretch_to_fit_width(w2, about_edge=m.LEFT),
                      m.ChangeDecimalToValue(cnt, new), run_time=0.9)
            self.cap(note, GREEN_L)
            w = w2
        self.play(m.Circumscribe(cnt, color=AMBER), m.Flash(bar.get_right(), color=GREEN_L), run_time=0.9)
        self.play(m.FadeOut(m.VGroup(bar, cnt)), run_time=0.5)
        self.card("Common mistake",
                  stack(tex(r"\varphi(4) = 2\neq \varphi(2)\,\varphi(2) = 1", 30, RED_L),
                        ttex(r"Multiplicative \textbf{only} for coprime factors.", 26)),
                  C_MISTAKE, corner=m.DR, shift=np.array([0, 1.3, 0]))
        self.cap("Careful: φ(mn) = φ(m)φ(n) only when m and n are coprime. With 4 = 2·2 it fails", RED_L)

    # ── 16. Euler ────────────────────────────────────────────────────────────
    def euler(self):
        self.chapter(16)
        self.card("Euler's Theorem", tex(r"\gcd(a,n)=1\ \Rightarrow\ a^{\varphi(n)}\equiv 1\md n", 36, AMBER),
                  C_THEOREM, corner=m.UL)
        self.cap("The proof is Fermat's, but using only the remainders that have an inverse. Let's see it with "
                 "n = 10 and a = 3")
        n, a = 10, 3
        units = [1, 3, 7, 9]
        cx, cz, R = 1.6, -0.5, 1.6
        pos = {u: on_circle(i, 4, R, cx, cz) for i, u in enumerate(units)}
        cols = {1: BLUE, 3: ORANGE, 7: GREEN, 9: PURPLE}
        balls = {u: sphere(pos[u], cols[u], r=0.34) for u in units}
        labs = {u: label(str(u), pos[u], 28, INK, dy=-0.37) for u in units}
        self.play(*(m.FadeIn(b) for b in balls.values()), *(m.FadeIn(lab) for lab in labs.values()), run_time=0.8)
        self.cap("The numbers coprime to 10 are 1, 3, 7 and 9, so φ(10) = 4. Multiply each one by 3")
        dest = {u: a * u % n for u in units}
        self.play(*(balls[u].animate.move_to(pos[dest[u]]) for u in units),
                  *(m.FadeOut(lab) for lab in labs.values()), run_time=2.0)
        new = {u: label(str(dest[u]), pos[dest[u]], 28, INK, dy=-0.37) for u in units}
        self.play(*(m.FadeIn(lab) for lab in new.values()), run_time=0.6)
        self.cap("3, 9, 21 and 27 are 3, 9, 1 and 7 mod 10: the same four in a different order. So 3⁴ times the "
                 "product equals the product, and 3⁴ ≡ 1. Indeed 81 ≡ 1 mod 10", GREEN_L)
        self.clear_stage()

        self.card("Euler's Theorem", tex(r"a^{\varphi(n)}\equiv 1\md n", 34, AMBER), C_THEOREM, corner=m.UL,
                  write=False)
        self.cap("Example: the remainder of 2 to the 118 mod 119. 119 isn't prime, so Fermat doesn't apply, but "
                 "Euler does")
        res = self.exponent_bar(r"2^{118}\bmod 119", 1, "96", "22", r"\equiv 2^{22}", np.array([0.2, -0.3, 0]),
                                width=8.0, notes=(
            "φ(119) = 96, so the exponent 118 is one block of 96 plus a remainder of 22",
            "By Euler, the block of 96 is worth 1",
            "That leaves 2 to the 22. Now let's compute it",
        ))
        self.play(m.FadeOut(res), run_time=0.5)
        self.derive([
            r"\varphi(119)=96,\quad \gcd(2,119)=1",
            r"2^{118}=2^{96}\cdot 2^{22}\equiv 2^{22}",
            r"2^7=128\equiv 9,\quad 2^{11}=2^7\cdot 2^4\equiv 9\cdot 16=144\equiv 25",
            r"2^{22}=(2^{11})^2\equiv 25^2=625=5\cdot 119+30\equiv 30",
        ], anchor=np.array([-6.6, 1.3, 0]), size=32, notes=[
            "φ(119) = 96 and 2 is coprime to 119",
            "Remove the 96 from the exponent and 2 to the 22 is left",
            "Compute 2 to the 11 in pieces",
            "And square it. The remainder is 30",
        ])
        self.clear_stage()
        self.card("Last three digits = remainder mod 1000", tex(r"7^{2407}\bmod 1000", 34), C_WORKED, corner=m.UL)
        res = self.exponent_bar(r"7^{2407}\bmod 1000", 6, "400", "7", r"\equiv 7^{7}", np.array([0.2, -0.3, 0]),
                                width=9.0, notes=(
            "The last three digits of 7 to the 2407. φ(1000) = 400, and 2407 is six blocks of 400 plus 7",
            "Each block of 400 is worth 1, by Euler",
            "7 to the 7th is what's left",
        ))
        self.play(m.FadeOut(res), run_time=0.5)
        self.derive([
            r"\varphi(1000)=400,\quad 2407 = 6\cdot 400 + 7",
            r"7^{2407}\equiv 7^7 \md{1000}",
            r"7^4=2401\equiv 401,\quad 7^3=343",
            r"7^7\equiv 401\cdot 343 = 137543\equiv 543",
        ], anchor=np.array([-6.6, 1.3, 0]), size=34, notes=[
            "The last three digits are the remainder mod 1000, and φ(1000) = 400",
            "Reduce the exponent mod 400 and 7 is left",
            "7 to the 4th is 2401, which ends in 401",
            "Multiply by 343 and the last three digits are 543",
        ])
        self.card("Rule of thumb",
                  ttex(r"Last $k$ digits $\to$ mod $10^k$, with $\varphi(10^k)=4\cdot 10^{k-1}$", 26),
                  C_RULE, corner=m.DR, shift=np.array([0, 1.3, 0]))
        self.wait(2.5)

    # ── 17. self-inverse elements ────────────────────────────────────────────
    def self_inverse(self):
        self.chapter(17)
        self.card("The question", ttex(r"How many $a$ satisfy $a^2\equiv 1$? In the reals only $\pm 1$.", 28),
                  C_QUESTION, corner=m.UL)
        self.derive([
            r"a^2\equiv 1\md p\iff p\mid (a-1)(a+1)",
            r"\iff p\mid a-1\ \vee\ p\mid a+1",
            r"\iff a\equiv \pm 1",
        ], anchor=np.array([-6.6, 1.3, 0]), size=34, notes=[
            "With an odd prime, factor the difference of squares",
            "By Euclid's lemma, p divides one of the two factors",
            "So there are exactly two solutions, 1 and −1, just like in the reals",
        ])
        self.cap("But with powers of 2 something odd happens. Look at mod 16")
        n = 16
        cx, cz, R = 2.6, -0.6, 1.65
        dots = [sphere(on_circle(k, n, R, cx, cz), GREY_D, r=0.17) for k in range(n)]
        labs = [label(str(k), on_circle(k, n, R + 0.4, cx, cz), 20, MUTED) for k in range(n)]
        self.play(*(m.FadeIn(d) for d in dots), *(m.FadeIn(lab) for lab in labs), run_time=0.8)
        sols = [k for k in range(n) if k * k % n == 1]
        self.play(*(dots[k].animate.set_color(AMBER).scale(1.5) for k in sols), run_time=0.8)
        self.cap("There are four: 1, 7, 9 and 15. For example, 7² = 49 = 3·16 + 1 and 9² = 81 = 5·16 + 1", AMBER)
        self.clear_stage()

        self.card("Mod 2ⁿ, n ≥ 3", tex(r"a^2\equiv 1\md{2^n}\iff a\equiv \pm 1,\ 2^{n-1}\pm 1", 34),
                  C_THEOREM, corner=m.UL)
        self.derive([
            r"2^n\mid (a-1)(a+1),\quad a\ \text{odd}",
            r"\gcd(a-1,a+1)=\gcd(a-1,2)=2",
            r"\text{one has a single } 2\ \Rightarrow\ 2^{n-1}\mid a-1\ \ \text{or}\ \ 2^{n-1}\mid a+1",
            r"a\equiv 1,\ 2^{n-1}+1\quad\text{or}\quad a\equiv 2^{n-1}-1,\ -1",
        ], anchor=np.array([-6.6, 1.25, 0]), size=32, notes=[
            "a has to be odd, so a − 1 and a + 1 are consecutive even numbers",
            "Since gcd(x, y) = gcd(x, y − x), their gcd is 2",
            "They share a single factor of 2, so one of them has exactly one 2 and the other carries all the "
            "rest, at least n − 1",
            "That gives two options in each case: four solutions in total",
        ])
        self.clear_stage()

        self.card("Mod 100 = 4 · 25",
                  stack(tex(r"\bmod 4:\ \{1,3\}\qquad \bmod 25:\ \{1,24\}", 30),
                        tex(r"\Rightarrow\ \{1,49,51,99\}", 32, AMBER)), C_WORKED, corner=m.UL)
        self.cap("With composite moduli, use the CRT: two solutions mod 4 and two mod 25 make four mod 100")
        table = m.MathTable([["1", "49"], ["51", "99"]],
                            row_labels=[tex("1", 36, ORANGE), tex("3", 36, ORANGE)],
                            col_labels=[tex("1", 36, BLUE), tex("24", 36, BLUE)],
                            include_outer_lines=False, h_buff=0.9, v_buff=0.55, line_config={"stroke_color": GREY})
        table.move_to([4.5, -0.45, 0])
        h25 = tex(r"\bmod 25", 30, BLUE).next_to(table, m.UP, buff=0.2).shift(0.45 * m.RIGHT)
        h4 = tex(r"\bmod 4", 30, ORANGE).next_to(table, m.LEFT, buff=0.2).shift(0.4 * m.DOWN)
        entries = table.get_entries_without_labels()
        self.pin(table, h25, h4)
        self.remove(table, h25, h4)
        self.play(m.Create(table.get_horizontal_lines()), m.Create(table.get_vertical_lines()),
                  m.FadeIn(table.get_labels()), m.FadeIn(h25), m.FadeIn(h4), run_time=0.9)
        self.play(m.LaggedStart(*(m.FadeIn(c, scale=0.5) for c in entries), lag_ratio=0.3), run_time=1.4)
        self.play(*(c.animate.set_color(AMBER) for c in entries),
                  m.LaggedStart(*(m.Flash(c, color=AMBER, flash_radius=0.3) for c in entries), lag_ratio=0.2),
                  run_time=1.2)
        self.cap("Each cell combines a solution mod 4 with one mod 25. For example, 49 is 1 mod 4 and 24 mod 25",
                 AMBER)
        self.derive([
            r"\prod_{\gcd(a,100)=1} a\ \equiv\ 1\cdot 49\cdot 51\cdot 99",
            r"\equiv 1\cdot(-51)\cdot 51\cdot(-1) = 51^2 = 2601",
            r"\equiv 1\md{100}",
        ], anchor=np.array([-6.6, 0.6, 0]), size=34, notes=[
            "For the product of the 40 remainders coprime to 100, use Wilson's idea: the ones with a partner "
            "cancel out and only the self-inverse ones are left",
            "49 is −51 and 99 is −1",
            "And 51² = 2601 ends in 01. The product is 1, not −1: Wilson's pattern fails here because there are "
            "four self-inverse elements instead of two",
        ])
        self.clear_stage()
        self.card("Mod 3600 = 2⁴ · 3² · 5²",
                  stack(tex(r"\bmod 16:\{1,7,9,15\},\quad \bmod 9:\{1,8\},\quad \bmod 25:\{1,24\}", 28),
                        tex(r"4\cdot 2\cdot 2 = 16\ \text{solutions}", 30, AMBER)), C_WORKED, corner=m.UL)
        sols = [a for a in range(3600) if a * a % 3600 == 1]
        grid = m.VGroup(*(tex(str(s), 30, GREEN_L) for s in sols)).arrange_in_grid(rows=4, cols=4, buff=(0.7, 0.3))
        grid.move_to([0.4, -0.3, 0])
        self.pin(grid)
        self.play(m.LaggedStart(*(m.FadeIn(g, scale=0.6) for g in grid), lag_ratio=0.08), run_time=2.0)
        self.cap("And with 3600: four mod 16, two mod 9 and two mod 25, so 16 solutions. The CRT with C = 225, "
                 "2800 and 576 gives all of them, and they match a computer search", GREEN_L)

    # ── 18. RSA ──────────────────────────────────────────────────────────────
    def rsa(self):
        self.chapter(18)
        self.card("The question",
                  ttex(r"How can someone encrypt a message with a \textbf{public} key that only I can decrypt?", 28),
                  C_QUESTION, corner=m.UL)

        def box3d(text, x, z, col, w=2.2, is_tex=True):
            sl = m.Prism(dimensions=[w, 0.5, 0.9], fill_color=col, fill_opacity=0.35, stroke_color=col,
                         stroke_width=2).move_to(P(x, z))
            lab = label(text, P(x, z), 34, INK, is_tex=is_tex, dy=-0.28)
            return m.Group(sl, lab)

        b1 = box3d(r"M = 7", -4.6, 0.2, BLUE)
        b2 = box3d(r"C = 13", 0.0, 0.2, RED_L)
        b3 = box3d(r"M = 7", 4.6, 0.2, GREEN)
        a1 = m.Arrow3D(P(-3.4, 0.2), P(-1.2, 0.2), color=EDGE, thickness=0.03)
        a2 = m.Arrow3D(P(1.2, 0.2), P(3.4, 0.2), color=EDGE, thickness=0.03)
        l1 = label(r"C = M^{e}\bmod n", P(-2.3, 0.85), 30, AMBER, is_tex=True)
        l2 = label(r"M = C^{d}\bmod n", P(2.3, 0.85), 30, GREEN_L, is_tex=True)
        k1 = label(r"\text{public: } (n,e) = (55, 3)", P(-2.3, -0.75), 26, AMBER, is_tex=True)
        k2 = label(r"\text{private: } d = 27", P(2.3, -0.75), 26, GREEN_L, is_tex=True)
        self.play(m.FadeIn(b1, shift=0.3 * m.IN), run_time=0.7)
        self.cap("Here's the round trip. Anyone encrypts the message M with the public key: raise it to e mod n")
        self.play(m.Create(a1), m.FadeIn(l1), m.FadeIn(k1), run_time=0.8)
        self.play(m.FadeIn(b2, shift=0.3 * m.IN), run_time=0.7)
        self.cap("Out comes C. To get M back you raise C to d, and only whoever knows d can do that")
        self.play(m.Create(a2), m.FadeIn(l2), m.FadeIn(k2), run_time=0.8)
        self.play(m.FadeIn(b3, shift=0.3 * m.IN), run_time=0.7)
        self.swing(theta=-62, phi=66, run_time=2.0)
        self.clear_stage()

        self.card("Key generation",
                  stack(ttex(r"1. Primes $p,q$; $\ n=pq$, $\ \varphi(n)=(p-1)(q-1)$", 26),
                        ttex(r"2. $e$ with $\gcd(e,\varphi(n))=1$", 26),
                        ttex(r"3. $d\equiv e^{-1}\md{\varphi(n)}$", 26),
                        ttex(r"4. Public $(n,e)$, private $d$", 26)), C_WORKED, corner=m.UL)
        self.derive([
            r"p=5,\ q=11,\quad n=55,\quad \varphi(n)=4\cdot 10=40",
            r"e=3,\quad \gcd(3,40)=1",
            r"40 = 13\cdot 3 + 1\ \Rightarrow\ 1 = 40 - 13\cdot 3",
            r"d\equiv -13\equiv 27\md{40}\quad (3\cdot 27 = 81 = 2\cdot 40+1)",
            r"C = 7^3 = 343 = 6\cdot 55 + 13\ \Rightarrow\ C = 13",
        ], anchor=np.array([-0.4, 2.05, 0]), size=30, notes=[
            "An example with small numbers. p = 5 and q = 11, so n = 55 and φ(n) = 40",
            "Pick e = 3, which is coprime to 40",
            "d is the inverse of 3 mod 40. Extended Euclid gets it in one line",
            "d = 27. Check: 3·27 = 81, which is 1 mod 40",
            "To encrypt M = 7, compute 7³ = 343, which is 13 mod 55",
        ])
        self.clear_stage()

        self.card("Decrypting 13²⁷ mod 55 with the CRT",
                  ttex(r"$55 = 5\cdot 11$: compute each part separately and combine.", 26), C_WORKED, corner=m.UL)
        self.derive([
            r"\bmod 5:\ 13\equiv 3,\quad 3^{27}=3^{4\cdot 6+3}\equiv 3^3=27\equiv 2",
            r"\bmod 11:\ 13\equiv 2,\quad 2^{27}=2^{10\cdot 2+7}\equiv 2^7=128\equiv 7",
            r"x\equiv 2\,(5),\ x\equiv 7\,(11)\ \Rightarrow\ x = 7",
        ], anchor=np.array([-6.6, 1.3, 0]), size=32, notes=[
            "Mod 5, by Fermat, the exponent reduces mod 4 and we get 2",
            "Mod 11, the exponent reduces mod 10 and we get 7",
            "Combine them with the CRT. The number that is 2 mod 5 and 7 mod 11 is 7. We got the message back",
        ])
        self.card("Why it works",
                  stack(tex(r"ed = 1 + k(p-1)(q-1)", 30),
                        tex(r"M^{ed} = M\cdot (M^{p-1})^{k(q-1)}\equiv M \md p", 30),
                        ttex(r"same mod $q$, and by the CRT $M^{ed}\equiv M \md{pq}$", 26)),
                  C_THEOREM, corner=m.DR, shift=np.array([0, 1.3, 0]))
        self.cap("And in general it works because ed is 1 plus a multiple of p − 1 and of q − 1. By Fermat you get "
                 "M mod p and mod q, and by the CRT you get M mod n")
        self.clear_stage()
        self.card("Common mistake",
                  stack(ttex(r"$d$ is the inverse of $e$ mod $\varphi(n)$, \textbf{not} mod $n$.", 30),
                        tex(r"3^{-1}\bmod 55 = 37,\qquad 13^{37}\bmod 55 = 18 \neq 7", 32, RED_L)),
                  C_MISTAKE, corner=None, shift=np.array([0, 0.6, 0]))
        self.cap("If you compute d mod n you get 37, and decrypting gives 18 instead of 7. Exponents live mod φ(n), "
                 "bases live mod n", RED_L)

    # ── 19. decision map ─────────────────────────────────────────────────────
    def decision_map(self):
        self.chapter(19)
        self.cap("To wrap up, the decision map: which tool to reach for depending on what the problem asks")
        pairs = [
            ("gcd of large numbers", "Euclid: last nonzero remainder"),
            (r"$s,t$ with $sa+tb=\gcd$", "Extended Euclid"),
            (r"$a^{-1}\bmod m$", r"$\gcd=1$ and Bézout; if $m$ is prime, $a^{m-2}$"),
            (r"$ax\equiv b\md m$", r"$d=\gcd(a,m)$; if $d\mid b$, $d$ solutions"),
            ("system, coprime moduli", r"CRT: $\sum a_iM_iy_i$"),
            ("system, moduli not coprime", "split into primes, look for clashes"),
            (r"$a^E\bmod p$, $p$ prime", r"Fermat: $E\bmod (p-1)$"),
            (r"$a^E\bmod n$, $\gcd(a,n)=1$", r"Euler: $E\bmod\varphi(n)$, or the CRT"),
            (r"$k!\bmod p$", r"Wilson, peeling off factors"),
            (r"last $k$ digits", r"mod $10^k$ with Euler"),
        ]
        y0 = 2.5
        rows = []
        for i, (q, a) in enumerate(pairs):
            y = y0 - 0.52 * i
            left = ttex(q, 29, INK)
            right = ttex(a, 29, GREEN_L)
            left.move_to([-3.6, y, 0])
            right.move_to([2.6, y, 0])
            arr = m.Arrow([-1.2, y, 0], [-0.6, y, 0], buff=0, color=AMBER, stroke_width=3,
                          max_tip_length_to_length_ratio=0.35)
            bg = m.Rectangle(width=13.6, height=0.46, fill_color=BG if i % 2 else "#123251", fill_opacity=0.9,
                             stroke_width=0).move_to([0, y, 0])
            rows.append((bg, left, arr, right))
        hdr = m.VGroup(m.Text("IF THE PROBLEM ASKS FOR", font=MONO_FONT, font_size=22, color=BLUE).move_to([-3.6, 3.05, 0]),
                       m.Text("USE", font=MONO_FONT, font_size=22, color=BLUE).move_to([2.6, 3.05, 0]))
        self.pin(hdr)
        self.play(m.FadeIn(hdr), run_time=0.5)
        for bg, left, arr, right in rows:
            self.pin(bg, left, arr, right)
            self.play(m.FadeIn(bg), m.FadeIn(left, shift=0.2 * m.RIGHT), run_time=0.35)
            self.play(m.GrowArrow(arr), m.FadeIn(right, shift=0.2 * m.RIGHT), run_time=0.45)
        self.uncap()
        self.wait(4)
        self.clear_stage()

        mistakes = [
            "A negative remainder in the division: always 0 ≤ r < d",
            "sa + tb = g does not mean g = gcd, except when g = 1",
            "Cancelling without checking the gcd: divide the modulus too",
            "Fermat with a composite modulus",
            "The CRT with non-coprime moduli, without checking for clashes",
            "φ(mn) = φ(m)φ(n) without coprimality",
            "In RSA, d mod n instead of mod φ(n)",
            "In ax ≡ b, giving one solution when there are d",
            "Claiming that p₁···pₖ + 1 is prime",
        ]
        head = m.Text("Common mistakes, all together", font=TEXT_FONT, font_size=36, color=RED_L, weight=m.BOLD)
        items = m.VGroup(*(m.VGroup(m.Text(f"{i + 1:02d}", font=MONO_FONT, font_size=24, color=RED_L),
                                    m.Text(t, font=TEXT_FONT, font_size=26, color=INK)).arrange(m.RIGHT, buff=0.35)
                           for i, t in enumerate(mistakes))).arrange(m.DOWN, aligned_edge=m.LEFT, buff=0.22)
        g = m.VGroup(head, items).arrange(m.DOWN, buff=0.4).move_to([0, 0.1, 0])
        self.pin(g)
        self.play(m.Write(head), run_time=0.8)
        self.play(m.LaggedStart(*(m.FadeIn(i, shift=0.2 * m.RIGHT) for i in items), lag_ratio=0.3), run_time=3.5)
        self.wait(6)
