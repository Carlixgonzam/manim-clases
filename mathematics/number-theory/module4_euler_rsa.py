"""Number theory, module 4. Euler's φ function, Euler's theorem, self-inverse elements, RSA and a decision map.

    manimgx render module4_euler_rsa.py Module4
"""

import math

import manimgx as m
import numpy as np

from common import (AMBER, BG, BLUE, C_DEF, C_MISTAKE, C_QUESTION, C_RULE, C_THEOREM, C_WORKED, DEEP, EDGE,
                    GREEN, GREEN_L, GREY, GREY_D, INK, MUTED, ORANGE, PANEL_BG, PURPLE, RED, RED_L,
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
            "φ(n) counts the invertible remainders, φ(pᵏ) = pᵏ − pᵏ⁻¹, and φ multiplies over coprime factors",
            "Euler says a to the φ(n) is 1 when gcd(a, n) = 1, so exponents can be reduced mod φ(n)",
            "a² ≡ 1 has 2 solutions mod an odd pᵏ and 4 mod 2ⁿ for n ≥ 3, and the CRT multiplies the counts",
            "In RSA, d is the inverse of e mod φ(n), and it works because of Euler and the CRT",
            "Before using a theorem, check its hypothesis, whether that's prime, coprime or pairwise coprime",
        ], "The written guide has every proof in full, plus exercises with solutions")

    def intro(self):
        self.home()
        self.title_card("Number Theory · Module 4", "Euler's φ, Euler's Theorem and RSA")
        self.cap("Fermat only works when the modulus is prime. In this module we extend it to any modulus, and then "
                 "use it to build RSA, the encryption behind much of the internet")

    # ── 15. φ ────────────────────────────────────────────────────────────────
    def phi(self):
        self.chapter(15)
        self.card("Definition",
                  stack(tex(r"\varphi(n) = \#\{x\ :\ 1\le x\le n,\ \gcd(x,n)=1\}", 32),
                        ttex(r"which is the number of remainders with an inverse mod $n$", 26)), C_DEF, corner=m.UL)
        self.cap("φ of n counts how many numbers from 1 to n are coprime to n. From module 2, those are exactly the "
                 "ones that have an inverse")
        n = 12
        xs = [-3.3 + 0.6 * i for i in range(n)]
        cubes = [cube(str(k + 1), P(xs[k], 0.4), GREY_D, side=0.5, size=22) for k in range(n)]
        self.play(m.LaggedStart(*(m.FadeIn(c, shift=0.3 * m.IN) for c in cubes), lag_ratio=0.05), run_time=1.2)
        good = [k for k in range(n) if math.gcd(k + 1, n) == 1]
        self.play(*(tint(cubes[k][0], GREEN) for k in good),
                  *(tint(cubes[k][0], RED, 0.45) for k in range(n) if k not in good),
                  *(cubes[k].animate.shift(0.25 * m.OUT) for k in good), run_time=1.0)
        res = label(r"\varphi(12) = 4", P(0, -0.7), 38, GREEN_L, is_tex=True)
        self.play(m.Write(res), run_time=0.8)
        self.cap("For 12, only 1, 5, 7 and 11 are coprime to it, so φ(12) = 4. The red ones share a 2 or a 3 with 12",
                 GREEN_L)
        self.clear_stage()

        self.card("Prime power", tex(r"\varphi(p^k) = p^k - p^{k-1} = p^k\left(1-\tfrac1p\right)", 34),
                  C_THEOREM, corner=m.UL)
        self.cap("Prime powers are easy. Take 27 = 3³. A number shares a factor with 27 only if it's a multiple of 3")
        cubes = []
        for k in range(27):
            r, c = divmod(k, 9)
            cubes.append(cube(str(k + 1), P(-2.4 + 0.6 * c, 0.9 - 0.65 * r), GREY_D, side=0.5, size=20))
        self.play(m.LaggedStart(*(m.FadeIn(c) for c in cubes), lag_ratio=0.02), run_time=1.4)
        bad = [k for k in range(27) if (k + 1) % 3 == 0]
        self.play(*(tint(cubes[k][0], RED) for k in bad),
                  *(tint(cubes[k][0], GREEN) for k in range(27) if k not in bad), run_time=0.9)
        res = label(r"\varphi(27) = 27 - 9 = 18", P(0, -1.3), 38, GREEN_L, is_tex=True)
        self.play(m.Write(res), run_time=0.8)
        self.cap("One number in every three is a multiple of 3, which makes 27/3 = 9 = 3² of them. Take those away "
                 "and 18 remain", GREEN_L)
        self.clear_stage()

        # multiplicativity on the CRT grid
        self.card("Multiplicative",
                  tex(r"\gcd(m,n)=1\ \Rightarrow\ \varphi(mn)=\varphi(m)\varphi(n)", 34), C_THEOREM, corner=m.UL)
        self.cap("Why does φ multiply like this? Let's go back to the Chinese Remainder grid, with 15 = 3 · 5")
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
        self.cap("x is coprime to 15 exactly when it's coprime to both 3 and 5. Being coprime to 3 means rows 1 and "
                 "2, which is φ(3) = 2 rows", ORANGE)
        self.play(*(tint(cells[(i, j)], GREEN) for i in (1, 2) for j in (1, 2, 3, 4)),
                  *(tint(cells[(0, j)], GREY_D) for j in range(5)),
                  *(tint(cells[(i, 0)], GREY_D) for i in range(3)), run_time=0.8)
        self.cap("Being coprime to 5 means columns 1 to 4, which is φ(5) = 4 columns. The cells that pass both tests "
                 "number 2 · 4 = 8, and that's φ(15)", GREEN_L)
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
            "A few examples. 119 is 7 times 17, two different primes",
            "1000 is 2 cubed times 5 cubed, and each prime power follows the earlier formula",
            "With the product formula, 360 = 2³ · 3² · 5 gives 96",
        ])
        x0, y, width = -6.2, -1.55, 8.4
        bar = m.Rectangle(width=width, height=0.5, fill_color=GREEN, fill_opacity=0.9, stroke_width=0)
        bar.move_to([x0 + width / 2, y, 0])
        cnt = m.Integer(360, group_with_commas=False, font_size=44, color=GREEN_L).move_to([4.6, y, 0])
        self.pin(bar, cnt)
        self.remove(bar, cnt)
        self.play(m.GrowFromEdge(bar, m.LEFT), m.FadeIn(cnt), run_time=1.0)
        w = width
        steps = [(r"\times\tfrac12", 2, 180, "Throwing out the multiples of 2 leaves half, which is 180"),
                 (r"\times\tfrac23", 3, 120, "Throwing out the multiples of 3 keeps two thirds of that, which is 120"),
                 (r"\times\tfrac45", 5, 96, "Throwing out the multiples of 5 keeps four fifths, which is 96 = φ(360)")]
        for frac, p_, new, note in steps:
            w2 = w * (p_ - 1) / p_
            cut = m.Rectangle(width=w - w2, height=0.5, fill_color=RED, fill_opacity=0.9, stroke_width=0)
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
                        ttex(r"It only multiplies over \textbf{coprime} factors.", 26)),
                  C_MISTAKE, corner=m.DR, shift=np.array([0, 1.3, 0]))
        self.cap("The rule φ(mn) = φ(m)φ(n) only holds when m and n are coprime. It already fails for 4 = 2·2", RED_L)

    # ── 16. Euler ────────────────────────────────────────────────────────────
    def euler(self):
        self.chapter(16)
        self.card("Euler's Theorem", tex(r"\gcd(a,n)=1\ \Rightarrow\ a^{\varphi(n)}\equiv 1\md n", 36, AMBER),
                  C_THEOREM, corner=m.UL)
        self.cap("The proof is the same as Fermat's, except we only use the remainders that have an inverse. Let's "
                 "watch it with n = 10 and a = 3")
        n, a = 10, 3
        units = [1, 3, 7, 9]
        cx, cz, R = 1.6, -0.5, 1.6
        pos = {u: on_circle(i, 4, R, cx, cz) for i, u in enumerate(units)}
        cols = {1: BLUE, 3: ORANGE, 7: GREEN, 9: PURPLE}
        balls = {u: sphere(pos[u], cols[u], r=0.34) for u in units}
        labs = {u: label(str(u), pos[u], 28, INK, dy=-0.37) for u in units}
        self.play(*(m.FadeIn(b) for b in balls.values()), *(m.FadeIn(lab) for lab in labs.values()), run_time=0.8)
        self.cap("The numbers coprime to 10 are 1, 3, 7 and 9, so φ(10) = 4. Now multiply each of them by 3")
        dest = {u: a * u % n for u in units}
        self.play(*(balls[u].animate.move_to(pos[dest[u]]) for u in units),
                  *(m.FadeOut(lab) for lab in labs.values()), run_time=2.0)
        new = {u: label(str(dest[u]), pos[dest[u]], 28, INK, dy=-0.37) for u in units}
        self.play(*(m.FadeIn(lab) for lab in new.values()), run_time=0.6)
        self.cap("3, 9, 21 and 27 reduce to 3, 9, 1 and 7 mod 10, the same four numbers in a new order. So 3⁴ times "
                 "their product equals their product, and 3⁴ ≡ 1. Sure enough, 81 ≡ 1 mod 10", GREEN_L)
        self.clear_stage()

        self.card("Euler's Theorem", tex(r"a^{\varphi(n)}\equiv 1\md n", 34, AMBER), C_THEOREM, corner=m.UL,
                  write=False)
        self.cap("Let's find the remainder of 2 to the 118 mod 119. 119 isn't prime, so Fermat can't help, but Euler "
                 "can")
        res = self.exponent_bar(r"2^{118}\bmod 119", 1, "96", "22", r"\equiv 2^{22}", np.array([0.2, -0.3, 0]),
                                width=8.0, notes=(
            "φ(119) = 96, so the exponent 118 is one block of 96 plus 22 more",
            "Euler says that block of 96 is worth 1",
            "That leaves 2 to the 22, which we still have to compute",
        ))
        self.play(m.FadeOut(res), run_time=0.5)
        self.derive([
            r"\varphi(119)=96,\quad \gcd(2,119)=1",
            r"2^{118}=2^{96}\cdot 2^{22}\equiv 2^{22}",
            r"2^7=128\equiv 9,\quad 2^{11}=2^7\cdot 2^4\equiv 9\cdot 16=144\equiv 25",
            r"2^{22}=(2^{11})^2\equiv 25^2=625=5\cdot 119+30\equiv 30",
        ], anchor=np.array([-6.6, 1.3, 0]), size=32, notes=[
            "φ(119) = 96 and 2 is coprime to 119",
            "Drop the 96 from the exponent and 2 to the 22 is left",
            "Build 2 to the 11 in pieces",
            "Then square it, and the remainder comes out to 30",
        ])
        self.clear_stage()
        self.card("Last three digits", tex(r"7^{2407}\bmod 1000", 34), C_WORKED, corner=m.UL)
        res = self.exponent_bar(r"7^{2407}\bmod 1000", 6, "400", "7", r"\equiv 7^{7}", np.array([0.2, -0.3, 0]),
                                width=9.0, notes=(
            "The last three digits of 7 to the 2407 are its remainder mod 1000. φ(1000) = 400, and 2407 is six "
            "blocks of 400 plus 7",
            "Each block of 400 is worth 1, by Euler",
            "So all that's left is 7 to the 7th",
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
            "Multiplying by 343 gives a number ending in 543",
        ])
        self.card("Rule of thumb",
                  ttex(r"The last $k$ digits are a remainder mod $10^k$, and $\varphi(10^k)=4\cdot 10^{k-1}$", 26),
                  C_RULE, corner=m.DR, shift=np.array([0, 1.3, 0]))
        self.wait(2.5)

    # ── 17. self-inverse elements ────────────────────────────────────────────
    def self_inverse(self):
        self.chapter(17)
        self.card("The question", ttex(r"How many $a$ have $a^2\equiv 1$? With real numbers only $\pm 1$ do.", 28),
                  C_QUESTION, corner=m.UL)
        self.derive([
            r"a^2\equiv 1\md p\iff p\mid (a-1)(a+1)",
            r"\iff p\mid a-1\ \vee\ p\mid a+1",
            r"\iff a\equiv \pm 1",
        ], anchor=np.array([-6.6, 1.3, 0]), size=34, notes=[
            "For an odd prime, factor the difference of squares",
            "Euclid's lemma says p divides one of the two factors",
            "So there are exactly two solutions, 1 and −1, the same as with real numbers",
        ])
        self.cap("Powers of 2 behave strangely, though. Look at mod 16")
        n = 16
        cx, cz, R = 2.6, -0.6, 1.65
        dots = [sphere(on_circle(k, n, R, cx, cz), GREY_D, r=0.17) for k in range(n)]
        labs = [label(str(k), on_circle(k, n, R + 0.4, cx, cz), 20, MUTED) for k in range(n)]
        self.play(*(m.FadeIn(d) for d in dots), *(m.FadeIn(lab) for lab in labs), run_time=0.8)
        sols = [k for k in range(n) if k * k % n == 1]
        self.play(*(dots[k].animate.set_color(AMBER).scale(1.5) for k in sols), run_time=0.8)
        self.cap("There are four of them, 1, 7, 9 and 15. For instance 7² = 49 = 3·16 + 1 and 9² = 81 = 5·16 + 1",
                 AMBER)
        self.clear_stage()

        self.card("Mod 2ⁿ with n ≥ 3", tex(r"a^2\equiv 1\md{2^n}\iff a\equiv \pm 1,\ 2^{n-1}\pm 1", 34),
                  C_THEOREM, corner=m.UL)
        self.derive([
            r"2^n\mid (a-1)(a+1),\quad a\ \text{odd}",
            r"\gcd(a-1,a+1)=\gcd(a-1,2)=2",
            r"\text{one has a single } 2\ \Rightarrow\ 2^{n-1}\mid a-1\ \ \text{or}\ \ 2^{n-1}\mid a+1",
            r"a\equiv 1,\ 2^{n-1}+1\quad\text{or}\quad a\equiv 2^{n-1}-1,\ -1",
        ], anchor=np.array([-6.6, 1.25, 0]), size=32, notes=[
            "a has to be odd, so a − 1 and a + 1 are consecutive even numbers",
            "Since gcd(x, y) = gcd(x, y − x), their gcd is 2",
            "They share just one factor of 2, so one of them has a single 2 and the other carries the rest, at "
            "least n − 1 of them",
            "Each case gives two options, which makes four solutions in total",
        ])
        self.clear_stage()

        self.card("Mod 100 = 4 · 25",
                  stack(tex(r"\{1,3\}\bmod 4\qquad \{1,24\}\bmod 25", 30),
                        tex(r"\Rightarrow\ \{1,49,51,99\}", 32, AMBER)), C_WORKED, corner=m.UL)
        self.cap("For a composite modulus, use the CRT. Two solutions mod 4 and two mod 25 combine into four mod 100")
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
        self.cap("Each cell pairs a solution mod 4 with a solution mod 25. For example, 49 is 1 mod 4 and 24 mod 25",
                 AMBER)
        self.derive([
            r"\prod_{\gcd(a,100)=1} a\ \equiv\ 1\cdot 49\cdot 51\cdot 99",
            r"\equiv 1\cdot(-51)\cdot 51\cdot(-1) = 51^2 = 2601",
            r"\equiv 1\md{100}",
        ], anchor=np.array([-6.6, 0.6, 0]), size=34, notes=[
            "To multiply all 40 remainders coprime to 100, borrow Wilson's idea. Everything with a partner cancels, "
            "and only the self-inverse ones remain",
            "49 is −51 and 99 is −1",
            "And 51² = 2601 ends in 01. The product is 1, not −1, because there are four self-inverse elements here "
            "instead of two",
        ])
        self.clear_stage()
        self.card("Mod 3600 = 2⁴ · 3² · 5²",
                  stack(tex(r"\{1,7,9,15\}\bmod 16,\quad \{1,8\}\bmod 9,\quad \{1,24\}\bmod 25", 28),
                        tex(r"4\cdot 2\cdot 2 = 16\ \text{solutions}", 30, AMBER)), C_WORKED, corner=m.UL)
        sols = [a for a in range(3600) if a * a % 3600 == 1]
        grid = m.VGroup(*(tex(str(s), 30, GREEN_L) for s in sols)).arrange_in_grid(rows=4, cols=4, buff=(0.7, 0.3))
        grid.move_to([0.4, -0.3, 0])
        self.pin(grid)
        self.play(m.LaggedStart(*(m.FadeIn(g, scale=0.6) for g in grid), lag_ratio=0.08), run_time=2.0)
        self.cap("With 3600 there are four solutions mod 16, two mod 9 and two mod 25, so 16 in all. The CRT with "
                 "C = 225, 2800 and 576 produces every one, and a computer search finds the same list", GREEN_L)

    # ── 18. RSA ──────────────────────────────────────────────────────────────
    def rsa(self):
        self.chapter(18)
        self.card("The question",
                  ttex(r"How can anyone encrypt a message with a \textbf{public} key that only I can decrypt?", 28),
                  C_QUESTION, corner=m.UL)

        def box3d(text, x, z, col, w=2.2, is_tex=True):
            sl = m.Prism(dimensions=[w, 0.5, 0.9], fill_color=col, fill_opacity=1, stroke_width=0).move_to(P(x, z))
            lab = label(text, P(x, z), 34, INK, is_tex=is_tex, dy=-0.28)
            return m.Group(sl, lab)

        b1 = box3d(r"M = 7", -4.6, 0.2, DEEP)
        b2 = box3d(r"C = 13", 0.0, 0.2, RED)
        b3 = box3d(r"M = 7", 4.6, 0.2, GREEN)
        a1 = m.Arrow3D(P(-3.4, 0.2), P(-1.2, 0.2), color=EDGE, thickness=0.03)
        a2 = m.Arrow3D(P(1.2, 0.2), P(3.4, 0.2), color=EDGE, thickness=0.03)
        l1 = label(r"C = M^{e}\bmod n", P(-2.3, 0.85), 30, AMBER, is_tex=True)
        l2 = label(r"M = C^{d}\bmod n", P(2.3, 0.85), 30, GREEN_L, is_tex=True)
        k1 = label(r"\text{public key } (n,e) = (55, 3)", P(-2.3, -0.75), 26, AMBER, is_tex=True)
        k2 = label(r"\text{private key } d = 27", P(2.3, -0.75), 26, GREEN_L, is_tex=True)
        self.play(m.FadeIn(b1, shift=0.3 * m.IN), run_time=0.7)
        self.cap("Here's the round trip. Anyone can encrypt a message M with the public key by raising it to the e "
                 "mod n")
        self.play(m.Create(a1), m.FadeIn(l1), m.FadeIn(k1), run_time=0.8)
        self.play(m.FadeIn(b2, shift=0.3 * m.IN), run_time=0.7)
        self.cap("Out comes C. Getting M back means raising C to the d, and only the person who knows d can do that")
        self.play(m.Create(a2), m.FadeIn(l2), m.FadeIn(k2), run_time=0.8)
        self.play(m.FadeIn(b3, shift=0.3 * m.IN), run_time=0.7)
        self.swing(theta=-62, phi=66, run_time=2.0)
        self.clear_stage()

        self.card("Key generation",
                  stack(ttex(r"1. Pick primes $p,q$, set $n=pq$ and $\varphi(n)=(p-1)(q-1)$", 26),
                        ttex(r"2. Pick $e$ with $\gcd(e,\varphi(n))=1$", 26),
                        ttex(r"3. Compute $d\equiv e^{-1}\md{\varphi(n)}$", 26),
                        ttex(r"4. Publish $(n,e)$ and keep $d$ private", 26)), C_WORKED, corner=m.UL)
        self.derive([
            r"p=5,\ q=11,\quad n=55,\quad \varphi(n)=4\cdot 10=40",
            r"e=3,\quad \gcd(3,40)=1",
            r"40 = 13\cdot 3 + 1\ \Rightarrow\ 1 = 40 - 13\cdot 3",
            r"d\equiv -13\equiv 27\md{40}\quad (3\cdot 27 = 81 = 2\cdot 40+1)",
            r"C = 7^3 = 343 = 6\cdot 55 + 13\ \Rightarrow\ C = 13",
        ], anchor=np.array([-0.4, 2.05, 0]), size=30, notes=[
            "Let's use small numbers. With p = 5 and q = 11 we get n = 55 and φ(n) = 40",
            "Choose e = 3, which is coprime to 40",
            "d is the inverse of 3 mod 40, and extended Euclid finds it in one line",
            "That gives d = 27. As a check, 3·27 = 81, which is 1 mod 40",
            "To encrypt M = 7, compute 7³ = 343, which is 13 mod 55",
        ])
        self.clear_stage()

        self.card("Decrypting 13²⁷ mod 55 with the CRT",
                  ttex(r"Since $55 = 5\cdot 11$, work mod 5 and mod 11 separately and combine.", 26), C_WORKED,
                  corner=m.UL)
        self.derive([
            r"13\equiv 3\md 5,\quad 3^{27}=3^{4\cdot 6+3}\equiv 3^3=27\equiv 2",
            r"13\equiv 2\md{11},\quad 2^{27}=2^{10\cdot 2+7}\equiv 2^7=128\equiv 7",
            r"x\equiv 2\,(5),\ x\equiv 7\,(11)\ \Rightarrow\ x = 7",
        ], anchor=np.array([-6.6, 1.3, 0]), size=32, notes=[
            "Mod 5, Fermat lets us reduce the exponent mod 4, and we get 2",
            "Mod 11, we reduce the exponent mod 10 and get 7",
            "The CRT puts them together. The number that's 2 mod 5 and 7 mod 11 is 7, which is our message",
        ])
        self.card("Why it works",
                  stack(tex(r"ed = 1 + k(p-1)(q-1)", 30),
                        tex(r"M^{ed} = M\cdot (M^{p-1})^{k(q-1)}\equiv M \md p", 30),
                        ttex(r"The same holds mod $q$, so the CRT gives $M^{ed}\equiv M \md{pq}$", 26)),
                  C_THEOREM, corner=m.DR, shift=np.array([0, 1.3, 0]))
        self.cap("In general it works because ed is 1 plus a multiple of both p − 1 and q − 1. Fermat gives back M "
                 "mod p and mod q, and the CRT turns that into M mod n")
        self.clear_stage()
        self.card("Common mistake",
                  stack(ttex(r"$d$ is the inverse of $e$ mod $\varphi(n)$, \textbf{not} mod $n$.", 30),
                        tex(r"3^{-1}\bmod 55 = 37,\qquad 13^{37}\bmod 55 = 18 \neq 7", 32, RED_L)),
                  C_MISTAKE, corner=None, shift=np.array([0, 0.6, 0]))
        self.cap("If you compute d mod n you get 37, and decrypting gives 18 instead of 7. Exponents live mod φ(n), "
                 "while the bases live mod n", RED_L)

    # ── 19. decision map ─────────────────────────────────────────────────────
    def decision_map(self):
        self.chapter(19)
        self.cap("To finish, here's a map of which tool to reach for, depending on what the problem asks")
        pairs = [
            ("gcd of large numbers", "Euclid, last nonzero remainder"),
            (r"$s,t$ with $sa+tb=\gcd$", "extended Euclid"),
            (r"$a^{-1}\bmod m$", r"Bézout when $\gcd=1$, or $a^{m-2}$ for prime $m$"),
            (r"$ax\equiv b\md m$", r"$d=\gcd(a,m)$, and $d$ solutions when $d\mid b$"),
            ("a system with coprime moduli", r"the CRT, $\sum a_iM_iy_i$"),
            ("a system with shared factors", "split into primes and look for clashes"),
            (r"$a^E\bmod p$ with $p$ prime", r"Fermat, reduce $E$ mod $p-1$"),
            (r"$a^E\bmod n$ with $\gcd(a,n)=1$", r"Euler, reduce $E$ mod $\varphi(n)$"),
            (r"$k!\bmod p$", r"Wilson, then peel off factors"),
            (r"the last $k$ digits", r"work mod $10^k$ with Euler"),
        ]
        y0 = 2.5
        rows = []
        for i, (q, a) in enumerate(pairs):
            y = y0 - 0.52 * i
            left = ttex(q, 29, INK)
            right = ttex(a, 29, GREEN_L)
            for t_, w_ in ((left, 4.6), (right, 6.0)):
                if t_.width > w_:
                    t_.scale_to_fit_width(w_)
            left.move_to([-3.6, y, 0])
            right.move_to([2.6, y, 0])
            arr = m.Arrow([-1.2, y, 0], [-0.6, y, 0], buff=0, color=EDGE, stroke_width=3,
                          max_tip_length_to_length_ratio=0.35)
            bg = m.Rectangle(width=13.6, height=0.46, fill_color=PANEL_BG if i % 2 else "#161B22", fill_opacity=0.9,
                             stroke_width=0).move_to([0, y, 0])
            rows.append((bg, left, arr, right))
        hdr = m.VGroup(m.Text("If the problem asks for…", font_size=28, color=AMBER).move_to([-3.6, 3.05, 0]),
                       m.Text("use…", font_size=28, color=AMBER).move_to([2.6, 3.05, 0]))
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
            "A negative remainder in the division, when 0 ≤ r < d always",
            "Reading sa + tb = g as g = gcd, which only works for g = 1",
            "Cancelling without checking the gcd, when the modulus must be divided too",
            "Using Fermat with a composite modulus",
            "Applying the CRT to moduli that share factors without checking for clashes",
            "Writing φ(mn) = φ(m)φ(n) when m and n aren't coprime",
            "Computing the RSA key d mod n instead of mod φ(n)",
            "Giving one solution to ax ≡ b when there are d of them",
            "Claiming that p₁···pₖ + 1 must be prime",
        ]
        head = m.Text("Common mistakes, all together", font_size=36, color=RED_L)
        items = m.VGroup(*(m.Text(f"{i + 1}.  {t}", font_size=26, color=INK) for i, t in enumerate(mistakes))).arrange(
            m.DOWN, aligned_edge=m.LEFT, buff=0.22)
        g = m.VGroup(head, items).arrange(m.DOWN, buff=0.4).move_to([0, 0.1, 0])
        self.pin(g)
        self.play(m.Write(head), run_time=0.8)
        self.play(m.LaggedStart(*(m.FadeIn(i, shift=0.2 * m.RIGHT) for i in items), lag_ratio=0.3), run_time=3.5)
        self.wait(6)
