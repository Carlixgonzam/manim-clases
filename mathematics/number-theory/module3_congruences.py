"""Number theory, module 3. Congruences, cancellation, linear congruences, the CRT, Fermat and Wilson.

    manimgx render module3_congruences.py Module3
"""

import math

import manimgx as m
import numpy as np

from common import (AMBER, BG, BLUE, C_DEF, C_MISTAKE, C_QUESTION, C_RULE, C_THEOREM, C_WORKED, DEEP, EDGE,
                    GREEN, GREEN_L, GREY, GREY_D, INK, MUTED, ORANGE, PURPLE, RED, RED_L, TEAL, Lesson, P, label,
                    number_line, slab, sphere, stack, tex, tint, ttex)

CLASSES = [BLUE, ORANGE, GREEN, PURPLE, AMBER, TEAL, RED_L]


def on_circle(k: int, n: int, R: float, cx: float = 0.0, cz: float = 0.0, y: float = 0.0):
    """Position k of n on a circle standing in front of the camera, starting at the top, clockwise."""
    ang = math.pi / 2 - 2 * math.pi * k / n
    return P(cx + R * math.cos(ang), cz + R * math.sin(ang), y)


class Module3(Lesson):
    START = 9
    CHAPTERS = [
        "Congruences as clock arithmetic",
        "Algebra of congruences and cancellation",
        "Linear congruences ax ≡ b",
        "The Chinese Remainder Theorem",
        "Fermat's Little Theorem",
        "Wilson's Theorem",
    ]

    def construct(self) -> None:
        self.setup_hud()
        self.intro()
        self.clock_arithmetic()
        self.algebra()
        self.linear()
        self.crt()
        self.fermat()
        self.wilson()
        self.takeaways([
            "a ≡ b (mod m) means m | a − b, and there are m classes, one for each remainder",
            "Sums, products and powers respect ≡, but you can only divide when gcd(c, m) = 1",
            "ax ≡ b (mod m) is solvable exactly when d = gcd(a, m) divides b, and then it has d solutions",
            "With coprime moduli the CRT gives one solution mod M, built from the terms a·M·y",
            "Fermat says a^(p−1) ≡ 1 (mod p), so exponents can be reduced mod p − 1",
            "Wilson says (p − 1)! ≡ −1 (mod p), because everything else cancels in pairs",
        ], "In module 4 we take Fermat to any modulus with the φ function, and that's how RSA works")

    def intro(self):
        self.home()
        self.title_card("Number Theory · Module 3", "congruences, the Chinese Remainder Theorem, Fermat and Wilson")
        self.cap("This is the longest module and the one everything else builds on. From here on we do arithmetic "
                 "where only the remainder matters")

    # ── 9. clock arithmetic ──────────────────────────────────────────────────
    def clock_arithmetic(self):
        self.chapter(9)
        self.card("Definition",
                  tex(r"a\equiv b\md{m}\iff m\mid a-b\iff a\bmod m = b\bmod m", 32), C_DEF, corner=m.UL)
        self.cap("Two numbers are congruent mod m when their difference is a multiple of m. Another way to say it is "
                 "that they leave the same remainder")
        n_mod, N = 5, 20
        cx, cz = 1.3, -0.35
        balls, labs = [], []
        line_pos = [P(-5.7 + 0.6 * k, 1.4) for k in range(N)]
        for k in range(N):
            balls.append(sphere(line_pos[k], GREY, r=0.22))
            labs.append(label(str(k), line_pos[k], 20, INK, dy=-0.25))
        self.play(m.LaggedStart(*(m.FadeIn(m.Group(b, lab)) for b, lab in zip(balls, labs)), lag_ratio=0.04),
                  run_time=1.6)
        self.cap("Line the integers up in a row. Now we'll coil that row like a spring, with 5 spots per turn")
        anims = []
        for k in range(N):
            R = 0.75 + 0.48 * (k // n_mod)
            pos = on_circle(k % n_mod, n_mod, R, cx, cz)
            anims.append(balls[k].animate.move_to(pos).set_color(CLASSES[k % n_mod]))
            anims.append(labs[k].animate.move_to(pos + np.array([0, -0.25, 0])))
        self.play(*anims, run_time=2.6)
        self.cap("Each number turns a fifth of the way around from the one before and moves a bit further out. "
                 "Numbers on the same ray are congruent mod 5", AMBER)
        cls = [label(f"[{r}]", on_circle(r, n_mod, 0.75 + 0.48 * 4 + 0.15, cx, cz), 30, CLASSES[r])
               for r in range(n_mod)]
        self.play(*(m.FadeIn(c) for c in cls), run_time=0.8)
        self.cap("Each ray is a class. The class of 2, for example, is {…, −3, 2, 7, 12, 17, …}. There are exactly "
                 "5 classes, one for each possible remainder")
        self.move_camera(phi=60 * m.DEGREES, theta=-62 * m.DEGREES, run_time=2.0)
        self.play(*(b.animate.shift(-0.12 * (k // n_mod) * m.DOWN) for k, b in enumerate(balls)), run_time=1.0)
        self.home(run_time=1.6)
        self.card("Equivalence relation",
                  stack(tex(r"\text{reflexive}\quad m\mid 0", 28),
                        tex(r"\text{symmetric}\quad m\mid a-b\Rightarrow m\mid b-a", 28),
                        tex(r"\text{transitive}\quad m\mid (a-b)+(b-c) = a-c", 28)), C_THEOREM, corner=m.DR,
                  shift=np.array([0, 1.3, 0]))
        self.cap("Congruence is an equivalence relation. All three properties follow straight from divisibility, "
                 "and that's why the integers split into classes that never overlap")

    # ── 10. algebra ──────────────────────────────────────────────────────────
    def algebra(self):
        self.chapter(10)
        self.card("Theorem",
                  stack(tex(r"a\equiv b,\ c\equiv d \md{m}\ \Rightarrow", 30),
                        tex(r"a+c\equiv b+d,\quad ac\equiv bd,\quad a^k\equiv b^k,\quad P(a)\equiv P(b)", 30)),
                  C_THEOREM, corner=m.UL)
        self.cap("Adding, multiplying and taking powers all respect congruence. Addition is easy. Multiplication "
                 "needs a small trick, adding and subtracting the same term")
        self.derive([
            r"ac - bd",
            r"= ac - bc + bc - bd",
            r"= c\,(a-b) + b\,(c-d)",
            r"m\mid a-b,\ m\mid c-d\ \Rightarrow\ m\mid ac-bd",
        ], anchor=np.array([-6.6, 1.0, 0]), size=34, notes=[
            "We want to show m divides ac − bd",
            "Add and subtract bc, which doesn't change anything",
            "Group the terms in pairs and factor",
            "m divides a factor of each piece, so it divides the whole thing",
        ])
        u = 0.72
        A, B, Cc, D = 5, 3, 4, 2
        org = np.array([1.9, -1.75, 0])

        def rect(x, y, w, h, col, op=0.85):
            return m.Rectangle(width=w * u, height=h * u, fill_color=col, fill_opacity=op, stroke_color=INK,
                               stroke_width=2).move_to(org + np.array([(x + w / 2) * u, (y + h / 2) * u, 0]))

        total = rect(0, 0, A, Cc, GREY_D, 0.0)
        bd = rect(0, 0, B, D, GREY, 0.6)
        right = rect(B, 0, A - B, Cc, ORANGE)
        top = rect(0, D, B, Cc - D, DEEP)
        l_ac = tex(r"ac", 34).move_to(total)
        l_bd = tex(r"bd", 30).move_to(bd)
        l_right = tex(r"c(a-b)", 26).move_to(right)
        l_top = tex(r"b(c-d)", 28).move_to(top)
        b_a = m.BraceLabel(total, "a", brace_direction=m.DOWN, font_size=28, color=INK)
        b_c = m.BraceLabel(total, "c", brace_direction=m.RIGHT, font_size=28, color=INK)
        self.pin(total, l_ac, b_a, b_c)
        self.remove(total, l_ac, b_a, b_c)
        self.play(m.Create(total), m.Write(l_ac), m.FadeIn(b_a), m.FadeIn(b_c), run_time=1.0)
        self.pin(bd, l_bd)
        self.remove(bd, l_bd)
        self.play(m.FadeOut(l_ac), m.DrawBorderThenFill(bd), m.FadeIn(l_bd), run_time=0.9)
        self.cap("Think of it as area. ac is the big rectangle and bd is the grey one in the corner, so ac − bd is "
                 "what's left when you take it away")
        b_ab = m.BraceLabel(right, "a-b", brace_direction=m.UP, font_size=28, color=ORANGE)
        b_cd = m.BraceLabel(top, "c-d", brace_direction=m.LEFT, font_size=28, color=BLUE)
        self.pin(right, top, l_right, l_top, b_ab, b_cd)
        self.remove(right, top, l_right, l_top, b_ab, b_cd)
        self.play(m.FadeOut(bd), m.FadeOut(l_bd), m.DrawBorderThenFill(right), m.DrawBorderThenFill(top),
                  run_time=1.2)
        self.play(m.Write(l_right), m.Write(l_top), m.GrowFromCenter(b_ab), m.GrowFromCenter(b_cd), run_time=1.0)
        self.cap("What's left splits into two strips. The orange one has a side of a − b and the blue one has a side "
                 "of c − d. Both are multiples of m, and so is their sum")
        self.play(m.FadeOut(m.VGroup(total, right, top, l_right, l_top, b_a, b_c, b_ab, b_cd)), run_time=0.6)
        self.card("In practice",
                  stack(ttex(r"You can reduce at \emph{any} step", 26),
                        tex(r"27 = 9\cdot 3\equiv 4\cdot 3 = 12\equiv 2 \md{5}", 30, GREEN_L)),
                  C_WORKED, corner=m.UR, shift=np.array([0, -1.6, 0]))
        self.cap("This is what makes congruences so handy. Halfway through a calculation you can replace any number "
                 "with its remainder")
        self.clear_stage()

        self.cap("What about dividing? This is where most mistakes happen", AMBER)
        self.card("Theorem (cancellation)",
                  stack(tex(r"ac\equiv bc\md{m}\ \Rightarrow\ a\equiv b\md{\tfrac{m}{\gcd(c,m)}}", 34),
                        ttex(r"When $\gcd(c,m)=1$ you can cancel and keep the same modulus.", 26)), C_THEOREM,
                  corner=m.UL)
        self.derive([
            r"g=\gcd(c,m),\quad c = gc',\ m = gm',\ \gcd(c',m')=1",
            r"gm'\mid gc'(a-b)",
            r"m'\mid c'(a-b)",
            r"m'\mid a-b",
        ], anchor=np.array([-6.6, 0.9, 0]), size=32, notes=[
            "Pull the common factor g out of c and m. What remains, c' and m', is coprime",
            "The hypothesis says m divides c(a − b)",
            "Cancel g on both sides, which is ordinary division of integers",
            "Since m' and c' are coprime, the coprime divisibility lemma gives m' | a − b",
        ])
        self.clear_stage()

        # the mistake, seen on the clock of 6
        self.card("Common mistake",
                  stack(tex(r"4\cdot 0\equiv 4\cdot 3 \md{6}\quad (0\equiv 12)", 30),
                        tex(r"0\not\equiv 3\md{6}\quad\text{but}\quad 0\equiv 3\md{3}", 30, RED_L)),
                  C_MISTAKE, corner=m.UL)
        cx, cz, R = 2.4, -0.2, 1.6
        dots = [sphere(on_circle(k, 6, R, cx, cz), GREY, r=0.25) for k in range(6)]
        labs = [label(str(k), on_circle(k, 6, R, cx, cz), 24, INK, dy=-0.3) for k in range(6)]
        self.play(*(m.FadeIn(d) for d in dots), *(m.FadeIn(lab) for lab in labs), run_time=0.8)
        self.cap("Look at a clock with 6 hours. Multiplying by 4 sends 0 to 0, and it sends 3 to 12, which is also 0")
        for src in (0, 3):
            self.play(m.Indicate(dots[src], color=AMBER, scale_factor=1.5), run_time=0.6)
        self.play(dots[0].animate.set_color(RED_L), dots[3].animate.set_color(RED_L), run_time=0.6)
        self.cap("Two numbers that differ mod 6 land in the same place. Multiplying by 4 merged them, and dividing "
                 "by 4 can't pull them apart again", RED_L)
        self.cap("What you can say is 0 ≡ 3 mod 6/gcd(4, 6), which is mod 3. The shared factor 2 drops out of the "
                 "modulus", RED_L)

    # ── 11. linear congruences ───────────────────────────────────────────────
    def linear(self):
        self.chapter(11)
        self.card("Theorem",
                  stack(tex(r"ax\equiv b\md{m}\ \text{is solvable}\iff d\mid b,\ \text{ where } d=\gcd(a,m)", 30),
                        ttex(r"and then it has \textbf{exactly $d$} solutions mod $m$.", 26)),
                  C_THEOREM, corner=m.UL)
        self.cap("When does ax ≡ b have a solution? Let's watch where 6x lands mod 15 as x goes 0, 1, 2 and on up to "
                 "14")
        n = 15
        cx, cz, R = 0.8, -0.55, 1.75
        dots = [sphere(on_circle(k, n, R, cx, cz), GREY_D, r=0.17) for k in range(n)]
        labs = [label(str(k), on_circle(k, n, R + 0.42, cx, cz), 20, MUTED) for k in range(n)]
        self.play(*(m.FadeIn(d) for d in dots), *(m.FadeIn(lab) for lab in labs), run_time=0.9)
        stacks = {k: 0 for k in range(n)}
        for x in range(n):
            v = 6 * x % n
            stacks[v] += 1
            pos = on_circle(v, n, R - 0.38 * stacks[v], cx, cz)
            c = sphere(pos, AMBER, r=0.14)
            self.play(m.FadeIn(c, scale=0.3), m.Indicate(dots[v], color=AMBER), run_time=0.28)
        self.cap("It only ever lands on 0, 3, 6, 9 and 12, the multiples of 3 = gcd(6, 15), and it lands on each of "
                 "them three times", AMBER)
        hits9 = [x for x in range(n) if 6 * x % n == 9]
        self.play(dots[9].animate.set_color(GREEN_L), run_time=0.5)
        self.cap(f"So 6x ≡ 9 has three solutions, x = {hits9[0]}, {hits9[1]} and {hits9[2]}. And 6x ≡ 10 has none at "
                 "all, because 3 doesn't divide 10", GREEN_L)
        self.play(dots[10].animate.set_color(RED_L), run_time=0.5)
        self.move_camera(phi=62 * m.DEGREES, theta=-68 * m.DEGREES, run_time=1.8)
        self.home(run_time=1.4)
        self.clear_stage()

        self.card("Procedure", stack(
            ttex(r"1. Find $d=\gcd(a,m)$. If $d\nmid b$ there is no solution.", 26),
            ttex(r"2. Divide everything by $d$ to get $\tfrac ad x\equiv \tfrac bd \md{\tfrac md}$", 26),
            ttex(r"3. Solve it with $x_0 = (a/d)^{-1}(b/d)\bmod \tfrac md$", 26),
            ttex(r"4. The solutions are $x_0 + k\tfrac md$ for $k=0,\dots,d-1$", 26)), C_WORKED, corner=m.UL)
        self.cap("Here's the procedure in four steps. Let's run it on 6x ≡ 9 mod 15")
        self.derive([
            r"d=\gcd(6,15)=3,\quad 3\mid 9\ \checkmark",
            r"2x\equiv 3\md{5}",
            r"2^{-1}\equiv 3\md 5\ \Rightarrow\ x_0\equiv 9\equiv 4\md 5",
            r"x\equiv 4,\ 9,\ 14 \md{15}",
        ], anchor=np.array([0.3, 2.0, 0]), size=32, notes=[
            "The gcd is 3 and it divides 9, so we expect three solutions",
            "Divide the whole congruence by 3, the modulus too",
            "Now 2 has an inverse mod 5, namely 3. Multiplying through gives x ≡ 4 mod 5",
            "Going back to mod 15 gives 4, 9 and 14, the same three we saw on the clock",
        ])
        nl = number_line(0, 15, np.array([-3.35, -1.15, 0]), 6.2, font=18)
        sol = m.VGroup(*(m.Dot(nl.n2p(v), radius=0.12, color=GREEN_L) for v in (4, 9, 14)))
        self.pin(nl)
        self.play(m.Create(nl), run_time=0.8)
        self.pin(sol)
        self.remove(sol)
        self.play(m.LaggedStart(*(m.GrowFromCenter(d) for d in sol), lag_ratio=0.3), run_time=0.9)
        brs = m.VGroup(*(m.BraceLabel(m.Line(nl.n2p(a_), nl.n2p(a_ + 5)), "5", brace_direction=m.UP,
                                      font_size=26, color=AMBER) for a_ in (4, 9)))
        self.pin(brs)
        self.remove(brs)
        self.play(m.LaggedStart(*(m.GrowFromCenter(b) for b in brs), lag_ratio=0.4), run_time=1.0)
        self.cap("On the number line the solutions are m/d = 5 apart, and exactly d = 3 of them fit before you reach "
                 "15", AMBER)
        self.card("Example with d = 1",
                  stack(tex(r"55x\equiv 13\md{89},\quad 55^{-1}\equiv 34", 28),
                        tex(r"x\equiv 13\cdot 34 = 442 = 4\cdot 89+86\equiv 86", 28, GREEN_L)),
                  C_WORKED, corner=m.DR, shift=np.array([0, 1.25, 0]))
        self.cap("When d = 1 it's quicker, you just multiply by the inverse. Using the 34 from module 2 we get x ≡ 86 "
                 "mod 89", GREEN_L)

    # ── 12. CRT ──────────────────────────────────────────────────────────────
    def grid(self, m1, m2, x0, z0, c=0.62, up_to=None, walk=True):
        cells = {}
        for i in range(m1):
            for j in range(m2):
                cells[(i, j)] = slab(c - 0.06, c - 0.06, P(x0 + j * c, z0 - i * c), GREY_D, depth=0.06)
        rl = [label(str(i), P(x0 - 0.55, z0 - i * c), 22, ORANGE) for i in range(m1)]
        cl = [label(str(j), P(x0 + j * c, z0 + 0.55), 22, BLUE) for j in range(m2)]
        rh = label(rf"x\bmod {m1}", P(x0 - 1.25, z0 - (m1 - 1) * c / 2), 24, ORANGE, is_tex=True)
        ch = label(rf"x\bmod {m2}", P(x0 + (m2 - 1) * c / 2, z0 + 1.0), 24, BLUE, is_tex=True)
        self.play(*(m.FadeIn(v) for v in cells.values()), *(m.FadeIn(t) for t in rl + cl), m.FadeIn(rh),
                  m.FadeIn(ch), run_time=1.0)
        nums = {}
        if walk:
            top = up_to if up_to is not None else m1 * m2
            for x in range(top):
                i, j = x % m1, x % m2
                pos = P(x0 + j * c, z0 - i * c, -0.08)
                prev = [nums[y] for y in nums if y % m1 == i and y % m2 == j]
                extra = []
                if prev:
                    pos = pos + 0.17 * m.RIGHT
                    extra = [prev[0].animate.shift(0.17 * m.LEFT)]
                t = label(str(x), pos, 22 if not prev else 20, INK if not prev else AMBER, dy=0)
                nums[x] = t
                self.play(m.FadeIn(t, scale=0.5), tint(cells[(i, j)], DEEP), *extra, run_time=0.3)
        return cells, nums

    def crt(self):
        self.chapter(12)
        self.card("The question",
                  ttex(r"If I know $x\bmod 3$ and $x\bmod 5$, do I know $x\bmod 15$?", 30), C_QUESTION, corner=m.UL)
        self.cap("Put the numbers 0 to 14 on a grid. The row is the remainder mod 3 and the column is the remainder "
                 "mod 5")
        self.grid(3, 5, -1.2, 1.0)
        self.cap("Each step moves down one row and over one column, wrapping around at the edges. Because 3 and 5 are "
                 "coprime, the diagonal reaches all 15 cells without repeating any", AMBER)
        self.cap("So every pair of remainders matches exactly one number mod 15. That's the Chinese Remainder "
                 "Theorem")
        self.swing(theta=-62, phi=64, run_time=2.0)
        self.clear_stage()
        self.cap("Now try moduli that aren't coprime, 2 and 4")
        cells, _ = self.grid(2, 4, -1.0, 0.6, c=0.75, up_to=8)
        empty = [cells[(i, j)] for i in range(2) for j in range(4) if (i + j) % 2 == 1]
        self.play(*(tint(c, RED) for c in empty), run_time=0.8)
        self.cap("The diagonal closes up after only 4 steps, which is lcm(2, 4). From 4 to 7 it revisits the same "
                 "cells, shown in yellow, and half the grid stays empty. For example, x ≡ 0 mod 2 together with "
                 "x ≡ 1 mod 4 has no solution", RED_L)
        self.clear_stage()

        self.card("Chinese Remainder Theorem",
                  stack(ttex(r"If $m_1,\dots,m_n$ are pairwise coprime, the system $x\equiv a_i\md{m_i}$", 26),
                        ttex(r"has a \textbf{unique} solution mod $M=m_1\cdots m_n$, namely", 26),
                        tex(r"x\equiv\sum a_iM_iy_i,\quad M_i=\tfrac{M}{m_i},\quad y_i = M_i^{-1}\bmod m_i", 32,
                            AMBER)), C_THEOREM, corner=m.UL)
        self.cap("The formula makes sense once you think of each term as a switch. Each M·y in the sum is 1 mod its "
                 "own m and 0 mod all the others")
        cells, _ = self.grid(3, 5, 0.6, 0.4, walk=False)
        c1 = label("10", P(0.6 + 0 * 0.62, 0.4 - 1 * 0.62, -0.08), 24, BG, dy=0)
        c2 = label("6", P(0.6 + 1 * 0.62, 0.4 - 0 * 0.62, -0.08), 24, BG, dy=0)
        self.play(tint(cells[(1, 0)], ORANGE), m.FadeIn(c1), run_time=0.7)
        self.cap("With 3 and 5, C₁ = 5·2 = 10. It's 1 mod 3 and 0 mod 5, so it sits in row 1, column 0", ORANGE)
        self.play(tint(cells[(0, 1)], BLUE), m.FadeIn(c2), run_time=0.7)
        self.cap("C₂ = 3·2 = 6 is 0 mod 3 and 1 mod 5", BLUE)
        res = label("8", P(0.6 + 3 * 0.62, 0.4 - 2 * 0.62, -0.08), 24, BG, dy=0)
        self.play(tint(cells[(2, 3)], AMBER), m.FadeIn(res), run_time=0.7)
        self.cap("For x ≡ 2 mod 3 and x ≡ 3 mod 5, take 2·10 + 3·6 = 38, which is 8 mod 15. Each switch only "
                 "turns on its own coordinate", AMBER)
        self.clear_stage()

        # a system of four congruences
        self.card("Four congruences at once",
                  stack(tex(r"2x\equiv 1\,(5),\ \ x\equiv -1\,(7),\ \ x\equiv 4\,(9),\ \ 3x\equiv 2\,(11)", 28),
                        tex(r"\Rightarrow\ x\equiv 3\,(5),\ \ 6\,(7),\ \ 4\,(9),\ \ 8\,(11)", 28, GREEN_L)),
                  C_WORKED, corner=m.UL)
        self.cap("Here's a bigger system. First solve each equation for x. The inverse of 2 mod 5 is 3, and the "
                 "inverse of 3 mod 11 is 4")
        hdr = ["m_i", "a_i", "M_i", "M_i\\bmod m_i", "y_i", "a_iM_iy_i"]
        rows = [(5, 3, 693, 3, 2, 4158), (7, 6, 495, 5, 3, 8910), (9, 4, 385, 7, 4, 6160), (11, 8, 315, 7, 8, 20160)]
        xs = [-4.6, -3.2, -1.7, 0.2, 1.9, 3.7]
        y0 = 0.9
        H = [tex(h, 28, AMBER).move_to([x, y0, 0]) for h, x in zip(hdr, xs)]
        self.pin(*H)
        self.play(*(m.FadeIn(h) for h in H), run_time=0.6)
        lasts = []
        for k, r in enumerate(rows):
            row = [tex(str(v), 28).move_to([x, y0 - 0.5 * (k + 1), 0]) for v, x in zip(r, xs)]
            self.pin(*row)
            self.play(*(m.FadeIn(c, shift=0.2 * m.RIGHT) for c in row), run_time=0.5)
            lasts.append(row[-1])
            if k == 0:
                self.cap("M = 5·7·9·11 = 3465. In the first row M₁ = 693, which is 3 mod 5, and its inverse is 2")
        sum_lab = tex(r"x\equiv", 34, GREEN_L)
        total = m.Integer(0, group_with_commas=False, font_size=34, color=GREEN_L)
        line = m.VGroup(sum_lab, total).arrange(m.RIGHT, buff=0.2).move_to([0, y0 - 2.9, 0])
        self.pin(line)
        self.play(m.FadeIn(line), run_time=0.4)
        acc = 0
        for c, r in zip(lasts, rows):
            acc += r[-1]
            self.play(m.Circumscribe(c, color=GREEN_L, buff=0.06), m.ChangeDecimalToValue(total, acc), run_time=0.8)
        tot = tex(r"x\equiv 4158+8910+6160+20160 = 39388\equiv 1273\md{3465}", 32, GREEN_L)
        tot.move_to([0, y0 - 2.9, 0])
        self.pin(tot)
        self.remove(tot)
        self.play(m.TransformMatchingShapes(line, tot), run_time=1.2)
        self.cap("Add up the four terms and reduce, and you get x ≡ 1273. As a check, 1273 leaves remainders 3, 6, 4 "
                 "and 8", GREEN_L)
        self.clear_stage()

        # moduli that aren't coprime
        self.card("Moduli that aren't coprime",
                  ttex(r"Split each modulus into prime powers and look for clashes.", 26), C_WORKED, corner=m.UL)
        eqs = [tex(r"x\equiv 7\md{10}", 32).move_to([-3.6, 0.75, 0]),
               tex(r"x\equiv 4\md{35}", 32).move_to([-3.6, -1.25, 0])]
        mods = {q_: m.VGroup(m.RoundedRectangle(width=1.7, height=0.62, corner_radius=0.1, stroke_color=EDGE,
                                                stroke_width=2, fill_color=GREY_D, fill_opacity=0.6),
                             tex(rf"\bmod {q_}", 30)) for q_ in (2, 5, 7)}
        for q_, y in zip((2, 5, 7), (1.1, -0.25, -1.6)):
            mods[q_].move_to([1.6, y, 0])
        arrows = [(0, 2, "1", BLUE), (0, 5, "2", BLUE), (1, 5, "4", ORANGE), (1, 7, "4", ORANGE)]
        self.pin(*eqs, *mods.values())
        self.remove(*eqs, *mods.values())
        self.play(*(m.FadeIn(e, shift=0.2 * m.RIGHT) for e in eqs), *(m.FadeIn(b) for b in mods.values()),
                  run_time=0.8)
        values = []
        for i, q_, v, col in arrows:
            ar = m.Arrow(eqs[i].get_right(), mods[q_].get_left(), buff=0.15, color=col, stroke_width=4)
            val = tex(rf"x\equiv {v}", 28, col).next_to(mods[q_], m.RIGHT, buff=0.2 + 1.3 * (i == 1 and q_ == 5))
            self.pin(ar, val)
            self.remove(ar, val)
            self.play(m.GrowArrow(ar), m.FadeIn(val, shift=0.15 * m.LEFT), run_time=0.6)
            values.append(val)
        self.cap("Each equation breaks into its primes. The one mod 10 gives conditions mod 2 and mod 5, and the one "
                 "mod 35 gives conditions mod 5 and mod 7")
        clash = mods[5]
        self.play(clash[0].animate.set_stroke(RED_L, width=4), m.Wiggle(clash), values[1].animate.set_color(RED_L),
                  values[2].animate.set_color(RED_L), run_time=1.0)
        self.cap("Mod 5 gets two different demands, 2 and 4, and they can't both hold", RED_L)
        self.clear_stage()
        self.card("Moduli that aren't coprime",
                  ttex(r"Split each modulus into prime powers and look for clashes.", 26), C_WORKED, corner=m.UL,
                  write=False)
        self.derive([
            r"x\equiv 7\,(10)\ \Rightarrow\ x\equiv 1\,(2),\ x\equiv 2\,(5)",
            r"x\equiv 4\,(35)\ \Rightarrow\ x\equiv 4\,(5),\ x\equiv 4\,(7)",
            r"2\not\equiv 4\,(5)\ \Rightarrow\ \text{no solution}",
        ], anchor=np.array([-6.6, 1.3, 0]), size=32, notes=[
            "10 and 35 share the factor 5, so the CRT doesn't apply directly. Split each equation into its primes",
            "Do the same with the second one",
            "Mod 5 we'd need 2 and 4 at the same time, which is impossible, so there's no solution",
        ])
        self.derive([
            r"x\equiv 7\,(10),\ x\equiv 2\,(35)\ \Rightarrow\ x\equiv 1\,(2),\ 2\,(5),\ 2\,(7)",
            r"x\equiv 35\cdot 1 + 2\cdot 14\cdot 4 + 2\cdot 10\cdot 5 = 247\equiv 37\md{70}",
        ], anchor=np.array([-6.6, -0.6, 0]), size=30, notes=[
            "If the second equation were x ≡ 2 mod 35 instead, both would ask for 2 mod 5. There's no clash, and the "
            "repeated condition only needs to be kept once",
            "Now the moduli 2, 5 and 7 are coprime, and the CRT gives 37 mod 70",
        ])
        self.card("Rule", tex(r"\text{solvable}\iff \gcd(m,n)\mid a-b,\ \text{unique mod }\lcm(m,n)", 28),
                  C_RULE, corner=m.UR)
        self.cap("In general, two equations can be solved together exactly when the gcd of the moduli divides the "
                 "difference of the remainders, and the answer is unique mod the lcm, not the product")

    # ── 13. Fermat ───────────────────────────────────────────────────────────
    def fermat(self):
        self.chapter(13)
        self.card("Fermat's Little Theorem",
                  stack(tex(r"p\ \text{prime},\ p\nmid a\ \Rightarrow\ a^{p-1}\equiv 1\md p", 34, AMBER),
                        tex(r"\text{for every } a,\quad a^p\equiv a\md p", 28)), C_THEOREM, corner=m.UL)
        self.cap("How would you work out 2 to the millionth power mod 101 without doing a million multiplications? "
                 "Let's build the intuition first, with p = 7 and a = 3")
        p, a = 7, 3
        cx, cz, R = 1.6, -0.5, 1.7
        pos = {k: on_circle(k - 1, p - 1, R, cx, cz) for k in range(1, p)}
        balls = {k: sphere(pos[k], CLASSES[k - 1], r=0.3) for k in range(1, p)}
        labs = {k: label(str(k), pos[k], 26, INK, dy=-0.33) for k in range(1, p)}
        self.play(*(m.FadeIn(b) for b in balls.values()), *(m.FadeIn(lab) for lab in labs.values()), run_time=0.9)
        self.cap("These are the remainders 1 through 6. Multiply each one by 3 and move it to where it lands")
        dest = {k: a * k % p for k in range(1, p)}
        lab_new = {k: label(f"{k}·3", pos[dest[k]], 20, MUTED, dy=-0.33).shift(0.55 * m.OUT) for k in range(1, p)}
        self.play(*(balls[k].animate.move_to(pos[dest[k]]) for k in balls),
                  *(m.FadeOut(lab) for lab in labs.values()), run_time=2.2)
        labs2 = {k: label(str(dest[k]), pos[dest[k]], 26, INK, dy=-0.33) for k in range(1, p)}
        self.play(*(m.FadeIn(lab) for lab in labs2.values()), *(m.FadeIn(lab) for lab in lab_new.values()),
                  run_time=0.8)
        self.cap("Every bead landed in a different spot and no spot was left empty. Multiplying by 3 only shuffled "
                 "the remainders", AMBER)
        self.cap("So the product of all six is the same before and after. But afterwards there are six extra factors "
                 "of 3 in it, which means 3 to the 6th has to be 1")
        self.swing(theta=-60, phi=66, run_time=2.0)
        self.clear_stage()

        self.card("Fermat's Little Theorem", tex(r"a^{p-1}\equiv 1\md p", 34, AMBER), C_THEOREM,
                  corner=m.UL, write=False)
        self.derive([
            r"a,\ 2a,\ \dots,\ (p-1)a\ \ \text{are}\ \not\equiv 0\ \text{and distinct}",
            r"\{a,2a,\dots,(p-1)a\}\equiv\{1,2,\dots,p-1\}",
            r"a^{p-1}\,(p-1)!\equiv (p-1)! \md p",
            r"\gcd((p-1)!,p)=1\ \Rightarrow\ a^{p-1}\equiv 1",
        ], anchor=np.array([-6.6, 1.3, 0]), size=32, notes=[
            "None of them is 0, by Euclid's lemma, since p divides neither k nor a. They're all different because "
            "a is coprime to p and can be cancelled",
            "That's p − 1 different nonzero remainders, so they must be 1, 2, up to p − 1 in some order",
            "Multiply them all together, and a to the p − 1 appears on the left",
            "The factorial is coprime to p, so it cancels",
        ])
        self.clear_stage()

        self.card("Strategy for huge exponents",
                  stack(tex(r"E = q(p-1)+r\ \Rightarrow\ a^E = (a^{p-1})^q a^r\equiv a^r", 30),
                        ttex(r"Reduce the exponent mod $p-1$.", 26, AMBER)), C_WORKED, corner=m.UL)
        cx, cy, R = 3.4, -0.35, 1.55
        ang = {v: m.PI / 2 - 2 * m.PI * k / 6 for k, v in enumerate((1, 3, 2, 6, 4, 5))}
        spot = {v: np.array([cx + R * math.cos(a_), cy + R * math.sin(a_), 0]) for v, a_ in ang.items()}
        nodes = {v: m.LabeledDot(tex(str(v), 30, BG), radius=0.3, color=CLASSES[v - 1]).move_to(spot[v])
                 for v in range(1, 7)}
        self.pin(*nodes.values())
        self.remove(*nodes.values())
        self.play(m.LaggedStart(*(m.GrowFromCenter(n_) for n_ in nodes.values()), lag_ratio=0.1), run_time=0.9)
        count = tex(r"3^{0}\equiv 1", 44, AMBER).move_to([-3.4, -0.4, 0])
        ring = m.Circle(radius=0.44, color=AMBER, stroke_width=5).move_to(spot[1])
        self.pin(count, ring)
        self.remove(count, ring)
        self.play(m.Write(count), m.Create(ring), run_time=0.7)
        self.cap("First, some intuition for why the exponent can be reduced. Watch the powers of 3 mod 7")
        v, arrows = 1, m.VGroup()
        for k in range(1, 7):
            w = 3 * v % 7
            ar = m.CurvedArrow(spot[v], spot[w], angle=-0.5, color=AMBER, stroke_width=4)
            ar.scale(0.72)
            new = tex(rf"3^{{{k}}}\equiv {w}", 44, AMBER).move_to(count)
            self.pin(ar, new)
            self.remove(ar, new)
            self.play(m.Create(ar), ring.animate.move_to(spot[w]), m.Transform(count, new), run_time=0.6)
            arrows.add(ar)
            v = w
        self.play(m.Flash(nodes[1], color=AMBER, flash_radius=0.45), m.Indicate(count, scale_factor=1.15),
                  run_time=0.8)
        self.cap("After 6 = p − 1 steps we're back at 1, and the cycle repeats from there. Six extra steps change "
                 "nothing, so only the exponent mod 6 matters", AMBER)
        self.play(m.FadeOut(m.VGroup(*nodes.values(), count, ring, arrows)), run_time=0.6)
        res = self.exponent_bar(r"2^{1000005}\bmod 101", 10000, "100", "5", r"\equiv 2^5 = 32",
                                np.array([0.2, -0.4, 0]), width=9.0, notes=(
            "Now 2 to the 1000005 mod 101. Since 101 is prime, 2 to the 100 is 1, and the exponent is 10000 blocks "
            "of 100 plus 5 more",
            "Each block of 100 is worth 2 to the 100, which is 1, and multiplying by 1 changes nothing",
            "Only the remainder survives, 2 to the 5th, which is 32",
        ))
        self.play(m.FadeOut(res), run_time=0.5)
        sq = stack(tex(r"7^2 = 49\equiv 3", 28), tex(r"7^4\equiv 9", 28), tex(r"7^8\equiv 81\equiv 12", 28),
                   tex(r"7^{16}\equiv 144\equiv 6", 28),
                   tex(r"7^{21}=7^{16}7^47\equiv 6\cdot9\cdot7=378\equiv 10", 28, GREEN_L))
        self.card("Inverse of 7 mod 23 with Fermat", sq, C_WORKED, corner=m.UR, shift=np.array([0, -0.6, 0]))
        self.cap("Fermat also hands you inverses. 7 times 7 to the 21st is 7 to the 22nd, which is 1, so the inverse "
                 "of 7 is 7 to the 21st. You get it by squaring again and again", GREEN_L)
        self.cap("Since 21 = 16 + 4 + 1, multiply those three powers together to get 10. As a check, 7·10 = 70 = "
                 "3·23 + 1")
        self.clear_stage()
        self.card("Common mistake",
                  stack(ttex(r"Fermat needs a \textbf{prime} modulus, so $a^{12}\bmod 15$ can't use exponent 14.", 28),
                        ttex(r"Use Euler with $\varphi(15)=8$, or the CRT with 3 and 5.", 28)), C_MISTAKE,
                  corner=m.UL)
        self.card("The converse fails",
                  stack(tex(r"2^{340}\equiv 1\md{341},\quad 341 = 11\cdot 31", 30),
                        ttex(r"$a^{n-1}\equiv 1$ does not prove that $n$ is prime.", 26)),
                  C_MISTAKE, corner=m.UR, shift=np.array([0, -1.6, 0]))
        self.cap("Two things to watch out for. Fermat doesn't hold for composite moduli, and its converse is false, "
                 "since 341 isn't prime and yet 2 to the 340 is 1 mod 341", RED_L)

    # ── 14. Wilson ───────────────────────────────────────────────────────────
    def wilson(self):
        self.chapter(14)
        self.card("Wilson's Theorem", tex(r"n>1\ \text{is prime}\iff (n-1)!\equiv -1\md n", 34, AMBER),
                  C_THEOREM, corner=m.UL)
        self.cap("Let's try p = 11. Put the numbers 1 to 10 around a circle and connect each one to its inverse")
        p = 11
        cx, cz, R = 1.6, -0.55, 1.8
        pos = {k: on_circle(k - 1, p - 1, R, cx, cz) for k in range(1, p)}
        balls = {k: sphere(pos[k], GREY, r=0.28) for k in range(1, p)}
        labs = {k: label(str(k), pos[k], 24, INK, dy=-0.31) for k in range(1, p)}
        self.play(*(m.FadeIn(b) for b in balls.values()), *(m.FadeIn(lab) for lab in labs.values()), run_time=0.9)
        pairs = [(2, 6), (3, 4), (5, 9), (7, 8)]
        for (a, b), col in zip(pairs, [BLUE, ORANGE, GREEN, PURPLE]):
            ln = m.Line3D(pos[a], pos[b], thickness=0.03, color=col)
            self.play(m.Create(ln), balls[a].animate.set_color(col), balls[b].animate.set_color(col), run_time=0.6)
            tag = label(rf"{a}\cdot {b} = {a * b}\equiv 1", P(-4.9, 0.9 - 0.6 * pairs.index((a, b))), 34, col,
                        is_tex=True)
            self.play(m.FadeIn(tag), run_time=0.4)
        self.cap("2 goes with 6, 3 with 4, 5 with 9 and 7 with 8. Each pair multiplies to 1, so they cancel out of "
                 "the product")
        self.play(balls[1].animate.set_color(AMBER), balls[10].animate.set_color(AMBER),
                  labs[1].animate.set_color(BG), labs[10].animate.set_color(BG), run_time=0.6)
        self.cap("Only 1 and 10 have no partner, because each is its own inverse. That leaves 10! ≡ 1·10 = 10, "
                 "which is −1", AMBER)
        self.swing(theta=-58, phi=64, run_time=2.0)
        self.clear_stage()

        self.card("Wilson's Theorem", tex(r"(p-1)!\equiv -1\md p", 34, AMBER), C_THEOREM, corner=m.UL,
                  write=False)
        self.derive([
            r"a^2\equiv 1\iff p\mid (a-1)(a+1)\iff a\equiv \pm 1",
            r"\{2,\dots,p-2\}\ \text{splits into pairs}\ (a,a^{-1}),\ a\neq a^{-1}",
            r"(p-1)!\equiv 1\cdot \underbrace{1\cdots 1}_{\text{pairs}}\cdot (p-1)\equiv -1",
        ], anchor=np.array([-6.6, 1.3, 0]), size=32, notes=[
            "First, Euclid's lemma shows the only numbers that are their own inverse are 1 and −1",
            "So every other number has a partner different from itself",
            "Each pair gives 1, and only the two ends are left",
        ])
        self.cap("For the converse, suppose n = ab with 1 < a < n. Then a appears in (n − 1)!, so it divides both "
                 "(n − 1)! + 1 and (n − 1)!, and therefore it divides 1, which is impossible")
        self.clear_stage()
        self.card("Example", tex(r"98!\bmod 101", 34), C_WORKED, corner=m.UL)
        self.derive([
            r"100!\equiv -1\md{101}",
            r"100\cdot 99! \equiv -1,\quad 100\equiv -1\ \Rightarrow\ 99!\equiv 1",
            r"99\cdot 98!\equiv 1,\quad 99\equiv -2\ \Rightarrow\ -2\cdot 98!\equiv 1",
            r"2\cdot 98!\equiv -1\equiv 100\ \Rightarrow\ 98!\equiv 50",
        ], anchor=np.array([-6.6, 1.2, 0]), size=34, notes=[
            "Wilson with p = 101",
            "Take out the factor 100 by writing it as −1",
            "Then take out the 99, which is −2",
            "Two times something is 100, so that something is 50. As a check, 2·50 = 100, which is −1",
        ])
        self.card("Rule of thumb",
                  ttex(r"For a factorial mod a prime, start from Wilson and peel off factors as $-1,-2,\dots$", 26),
                  C_RULE, corner=m.DL, shift=np.array([0, 1.25, 0]))
        self.wait(3)
