"""Number theory, module 2. Bézout's identity, its lemmas, the extended Euclidean algorithm and modular inverses.

    manimgx render module2_bezout.py Module2
"""

import manimgx as m
import numpy as np

from common import (AMBER, BG, BLUE, C_DEF, C_MISTAKE, C_QUESTION, C_RULE, C_THEOREM, C_WORKED, DEEP, GREEN,
                    GREEN_L, GREY, GREY_D, INK, MUTED, ORANGE, PURPLE, RED, RED_L, Lesson, P, label, number_line,
                    slab, sphere, stack, tex, tint, ttex)

PRIME_COLOR = {2: BLUE, 3: ORANGE, 5: GREEN, 7: PURPLE}


class Module2(Lesson):
    START = 5
    CHAPTERS = [
        "Bézout's identity",
        "The lemmas that follow from Bézout",
        "The extended Euclidean algorithm",
        "Modular inverses",
    ]

    def construct(self) -> None:
        self.setup_hud()
        self.intro()
        self.bezout()
        self.lemmas()
        self.extended()
        self.inverses()
        self.takeaways([
            "gcd(a, b) is the smallest positive number you can write as sa + tb",
            "gcd(a, b) = 1 exactly when some s and t give sa + tb = 1",
            "If a | bc and gcd(a, b) = 1 then a | c, by Bézout, a multiplication and a linear combination",
            "Extended Euclid works by back-substitution or with the table, which keeps r = s·a + t·b",
            "a has an inverse mod m exactly when gcd(a, m) = 1, and Bézout's s is that inverse",
        ], "In module 3 we use inverses to solve congruences and whole systems of them")

    def intro(self):
        self.home()
        self.title_card("Number Theory · Module 2", "Bézout, extended Euclid and inverses")
        self.cap("In module 1 the gcd was the largest common divisor. Here we'll see it can also be written as a "
                 "sum, and that's what lets us divide in modular arithmetic")

    # ── 5. Bézout ────────────────────────────────────────────────────────────
    def bezout(self):
        self.chapter(5)
        self.card("The question", ttex(r"Which lengths can you measure with a $6$ ruler and a $10$ ruler?", 28),
                  C_QUESTION, corner=m.UL)
        self.cap("Imagine two rulers without any markings, one 6 centimeters long and one 10. You can lay them end "
                 "to end, or line them up and measure the difference")
        u = 0.32
        y0 = 0.9

        def ruler(n, x, z, col, k=""):
            sl = slab(n * u - 0.03, 0.38, P(x + n * u / 2, z), col, depth=0.3)
            lab = label(str(n) if not k else k, P(x + n * u / 2, z), 22)
            return m.Group(sl, lab)

        x0 = -2.9
        r6a = ruler(6, x0, y0, BLUE)
        r6b = ruler(6, x0 + 6 * u, y0, BLUE)
        r10 = ruler(10, x0, y0 - 0.55, ORANGE)
        self.play(m.FadeIn(r6a, shift=0.3 * m.IN), run_time=0.6)
        self.play(m.FadeIn(r6b, shift=0.3 * m.IN), run_time=0.6)
        self.play(m.FadeIn(r10, shift=0.3 * m.IN), run_time=0.6)
        gap = slab(2 * u - 0.03, 0.38, P(x0 + 11 * u, y0 - 0.55), AMBER, depth=0.3)
        glab = label("2", P(x0 + 11 * u, y0 - 0.55), 22, BG)
        self.play(m.FadeIn(gap), m.FadeIn(glab), run_time=0.8)
        eq = label(r"2\cdot 6 - 1\cdot 10 = 2", P(x0 + 6 * u, y0 - 1.35), 36, AMBER, is_tex=True)
        self.play(m.Write(eq), run_time=0.9)
        self.cap("Two 6 rulers make 12 and the other ruler makes 10. The gap between them is 2, so you can measure "
                 "2 centimeters", AMBER)
        self.cap("Could you measure 1? No. 6 and 10 are both even, so anything you build from them is even too. "
                 "The smallest length you can get is 2, which is gcd(6, 10)")
        self.clear_stage()

        # the grid of combinations
        self.cap("Let's fill in a whole table. Cell (s, t) holds 6s + 10t, with s and t running from −3 to 3")
        cell = 0.72
        tiles = {}
        for s in range(-3, 4):
            for t in range(-3, 4):
                v = 6 * s + 10 * t
                col = DEEP if v > 0 else (GREY_D if v < 0 else GREY)
                pos = P(s * cell, t * cell * 0.82 + 0.3)
                tl = slab(cell - 0.06, cell * 0.82 - 0.06, pos, col, depth=0.1)
                lab = label(str(v), pos, 20, INK, dy=-0.08)
                tiles[(s, t)] = (v, tl, lab)
        sl = label("s", P(3.6 * cell, -3 * cell * 0.82 + 0.3 - 0.55), 26, MUTED)
        tlb = label("t", P(-3.6 * cell, 3 * cell * 0.82 + 0.3 + 0.4), 26, MUTED)
        self.play(m.LaggedStart(*(m.FadeIn(m.Group(tl, lab)) for v, tl, lab in tiles.values()), lag_ratio=0.01),
                  m.FadeIn(sl), m.FadeIn(tlb), run_time=2.2)
        self.cap("Every number in the table is even. No choice of s and t gives 1, because 2 divides both 6 and 10")
        mins = [(tl, lab) for v, tl, lab in tiles.values() if v == 2]
        self.play(*(tint(tl, AMBER) for tl, _ in mins), *(lab.animate.set_color(BG) for _, lab in mins),
                  run_time=0.8)
        self.cap("The yellow cells hold 2, the smallest positive value anywhere in the table. That smallest value "
                 "is the gcd", AMBER)
        anims = []
        for (s, t), (v, tl, lab) in tiles.items():
            if v > 0:
                h = 0.035 * v
                anims.append(tl.animate.stretch(h / 0.1, 1).shift((h / 2 - 0.05) * m.DOWN))
                anims.append(lab.animate.shift((h - 0.1) * m.DOWN))
        self.play(*anims, run_time=1.4)
        self.move_camera(phi=66 * m.DEGREES, theta=-74 * m.DEGREES, zoom=0.88, run_time=2.4)
        self.cap("Now let each positive value rise toward us in proportion to its size. The yellow columns are the "
                 "shortest, and every other column is a multiple of them")
        self.home(run_time=1.8)
        self.clear_stage()

        self.card("Bézout's theorem",
                  stack(tex(r"a,b\ \text{not both }0\ \Rightarrow\ \gcd(a,b) = sa+tb\ \text{ for some } s,t\in\mathbb{Z}",
                            32),
                        tex(r"\gcd(a,b)=\min\{sa+tb>0\}", 32, AMBER)), C_THEOREM, corner=m.UL)
        self.cap("This is the theorem. The proof shows that the smallest positive value in that table has both "
                 "properties that define the gcd")
        nl = number_line(-10, 20, np.array([0, -0.55, 0]), 12.6, font=18, only=range(-10, 21, 2))
        vals = sorted({6 * s_ + 10 * t_ for s_ in range(-3, 4) for t_ in range(-3, 4)
                       if -10 <= 6 * s_ + 10 * t_ <= 20}, key=lambda v: (abs(v), v))
        pts = m.VGroup(*(m.Dot(nl.n2p(v), radius=0.11, color=BLUE) for v in vals))
        name = tex(r"L=\{6s+10t\}", 34, BLUE).next_to(nl, m.UP, buff=0.75).align_to(nl, m.LEFT)
        self.pin(nl, name)
        self.play(m.Create(nl), m.Write(name), run_time=1.0)
        self.pin(pts)
        self.remove(pts)
        self.play(m.ShowIncreasingSubsets(pts), run_time=2.0)
        self.cap("Put every value from the table on a number line. They land on the even numbers and nowhere else",
                 BLUE)
        g_pt = pts[vals.index(2)]
        g_lab = tex(r"g = 2\cdot 6 - 1\cdot 10 = 2", 30, AMBER).next_to(nl.n2p(2), m.UP, buff=0.45)
        self.pin(g_lab)
        self.remove(g_lab)
        self.play(g_pt.animate.set_color(AMBER).scale(1.5), m.Flash(g_pt, color=AMBER), m.FadeIn(g_lab),
                  run_time=0.9)
        brs = m.VGroup(*(m.Brace(m.Line(nl.n2p(v), nl.n2p(v + 2)), m.DOWN, buff=0.45, color=AMBER)
                         for v in range(-10, 20, 2)))
        self.pin(brs)
        self.remove(brs)
        self.play(m.LaggedStart(*(m.GrowFromCenter(b) for b in brs), lag_ratio=0.06), run_time=1.6)
        self.cap("The smallest positive one is g = 2, and the rest sit exactly g apart. The proof shows this always "
                 "happens, so g divides everything in L, a and b included", AMBER)
        self.play(m.FadeOut(m.VGroup(nl, name, pts, g_lab, brs)), run_time=0.6)
        self.derive([
            r"g = s_0a + t_0b\ \ \text{the smallest positive element of } L",
            r"a = gq + r,\quad 0\le r<g",
            r"r = a - (s_0a+t_0b)q = (1-s_0q)\,a + (-t_0q)\,b \in L",
            r"r<g\ \Rightarrow\ r = 0\ \Rightarrow\ g\mid a \ (\text{and likewise } g\mid b)",
            r"d\mid a,\ d\mid b\ \Rightarrow\ d\mid s_0a+t_0b = g\ \Rightarrow\ d\le g",
        ], anchor=np.array([-6.6, 1.2, 0]), size=30, notes=[
            "Let g be the smallest positive number of the form sa + tb. Well-ordering says it exists",
            "To show g divides a, divide a by g",
            "The remainder is also a combination of a and b, so it belongs to the table",
            "But it's smaller than g, and nothing positive in the table is smaller than g. So r = 0 and g divides a",
            "Any common divisor also divides the combination g, so it can't be bigger than g. That makes g the gcd",
        ])
        self.clear_stage()
        self.card("The coprimality test",
                  tex(r"\gcd(a,b)=1 \iff sa+tb=1\ \text{ for some } s,t", 34, AMBER), C_THEOREM, corner=m.UL)
        self.cap("One direction is Bézout. For the other, a common divisor d of a and b divides sa + tb, which is 1, "
                 "so d = 1")
        self.card("Common mistake",
                  stack(tex(r"1\cdot 6 + 1\cdot 10 = 16\quad\text{but}\quad \gcd(6,10)=2", 30, RED_L),
                        ttex(r"$sa+tb=g$ only tells you $\gcd(a,b)\mid g$, unless $g=1$", 28)),
                  C_MISTAKE, corner=m.UR, shift=np.array([0, -1.8, 0]))
        self.cap("Getting sa + tb = g doesn't make g the gcd. It only tells you the gcd divides g, and the reverse "
                 "direction only works when g is 1", RED_L)

    # ── 6. lemmas ────────────────────────────────────────────────────────────
    def chips(self, factors, x, z, name, color=INK):
        """A row of spheres, one per prime factor."""
        balls = [sphere(P(x + 0.8 * i, z), PRIME_COLOR[p], r=0.32) for i, p in enumerate(factors)]
        labs = [label(str(p), P(x + 0.8 * i, z), 24, INK, dy=-0.36) for i, p in enumerate(factors)]
        tag = label(name, P(x - 1.2, z), 36, color, is_tex=True)
        return m.Group(tag, *balls, *labs)

    def lemmas(self):
        self.chapter(6)
        self.card("Lemma (coprime divisibility)",
                  tex(r"a\mid bc\ \ \wedge\ \ \gcd(a,b)=1\ \Rightarrow\ a\mid c", 34), C_THEOREM, corner=m.UL)
        self.cap("This lemma gets used more than any other in the topic, and its proof is a template you'll reuse "
                 "again and again")
        self.derive([
            r"\gcd(a,b)=1\ \Rightarrow\ sa+tb=1",
            r"sac + tbc = c",
            r"a\mid sac,\qquad bc = ak\ \Rightarrow\ tbc = a(tk)",
            r"a \mid sac + tbc = c",
        ], anchor=np.array([-6.6, 1.3, 0]), size=34, notes=[
            "Start with Bézout. Since a and b are coprime, some s and t give sa + tb = 1",
            "Multiply the whole equation by c",
            "Now a divides both terms. The first has a as a factor, and in the second bc is a multiple of a by "
            "hypothesis",
            "So a divides their sum, which is c",
        ])
        self.card("Typical exercise",
                  stack(tex(r"dx+by=1\ \Rightarrow\ adx+aby=a", 28),
                        tex(r"ab = dk\ \Rightarrow\ d(ax+ky) = a", 28)), C_WORKED, corner=m.UR,
                  shift=np.array([0, -1.3, 0]))
        self.cap("A typical exercise works exactly the same way, with d playing the role of a")
        self.clear_stage()

        # a visual counterexample with prime factors
        self.card("Canonical counterexample", tex(r"6\mid 4\cdot 3\quad\text{but}\quad 6\nmid 3", 32), C_MISTAKE,
                  corner=m.UL)
        self.cap("What goes wrong without the coprime hypothesis? Let's draw prime factors as beads, blue for 2 and "
                 "orange for 3")
        g6 = self.chips([2, 3], -1.0, 1.2, r"6")
        g12 = self.chips([2, 2, 3], -1.0, 0.2, r"4\cdot 3")
        g3 = self.chips([3], -1.0, -0.8, r"3")
        self.play(m.FadeIn(g6), run_time=0.7)
        self.play(m.FadeIn(g12), run_time=0.7)
        self.cap("6 divides 4·3 because its beads, one 2 and one 3, both show up among the beads of 12")
        self.play(m.FadeIn(g3), run_time=0.7)
        self.play(m.Indicate(g6[1], color=RED_L, scale_factor=1.4), run_time=1.0)
        self.cap("The 2 from 6 is hiding inside the 4, though, not the 3. Since gcd(6, 4) = 2, the lemma doesn't "
                 "apply, and 6 does not divide 3", RED_L)
        self.cap("Coprimality rules this out. No factor of a can hide in b, so every one of them has to be in c")
        self.swing(theta=-60, phi=66, run_time=2.0)
        self.clear_stage()

        # Euclid's lemma and coprime divisors
        self.card("Euclid's lemma", tex(r"p\ \text{prime},\ p\mid ab\ \Rightarrow\ p\mid a\ \vee\ p\mid b", 32),
                  C_THEOREM, corner=m.UL)
        self.cap("If p is prime and doesn't divide a, then gcd(p, a) = 1, because p has no divisors besides 1 and p. "
                 "The previous lemma then gives p | b")
        self.card("Counterexample", tex(r"6\mid 2\cdot 3,\quad 6\nmid 2,\quad 6\nmid 3", 30), C_MISTAKE,
                  corner=m.UR)
        self.cap("It fails for composite numbers. This is the property that makes primes special, and it comes back "
                 "in unique factorization, in Fermat, in Wilson and with self-inverse elements")
        self.card("Coprime divisors",
                  stack(tex(r"a\mid c,\ b\mid c,\ \gcd(a,b)=1\ \Rightarrow\ ab\mid c", 30),
                        tex(r"c = ak,\ b\mid ak\ \Rightarrow\ b\mid k\ \Rightarrow\ c = ab\ell", 28)),
                  C_THEOREM, corner=m.DL, shift=np.array([0, 1.3, 0]))
        self.cap("The third lemma says that if two coprime numbers divide c, so does their product. The proof applies "
                 "the first lemma to b and k")
        self.card("Counterexample", tex(r"4\mid 12,\ 6\mid 12,\ \ 24\nmid 12", 30), C_MISTAKE, corner=m.DR,
                  shift=np.array([0, 1.3, 0]))
        self.cap("Without coprimality it breaks. 4 and 6 share a factor of 2, and the product counts it twice")
        self.clear_stage()

        self.card("The gcd of a product",
                  tex(r"\gcd(a,b)=1,\ \gcd(a,c)=1\ \Rightarrow\ \gcd(a,bc)=1", 34), C_THEOREM, corner=m.UL)
        self.cap("This exercise uses a trick worth remembering, which is to multiply two Bézout identities together")
        der = self.derive([
            r"ax_1+by_1 = 1,\qquad ax_2+cy_2 = 1",
            r"(ax_1+by_1)(ax_2+cy_2) = 1",
            r"a^2x_1x_2 + ax_1cy_2 + by_1ax_2 + bcy_1y_2 = 1",
            r"a\,(ax_1x_2 + x_1cy_2 + by_1x_2) + bc\,(y_1y_2) = 1",
            r"aX + (bc)Y = 1\ \Rightarrow\ \gcd(a,bc)=1",
        ], anchor=np.array([-6.6, 1.25, 0]), size=32, notes=[
            "Write down both identities",
            "Multiply them. One times one is still one",
            "Expand the product",
            "Every term except the last contains a, so factor it out",
            "We're left with a times an integer plus bc times an integer, equal to 1. By the coprimality test, a and "
            "bc are coprime",
        ])
        self.play(m.FadeOut(der[1:4]), der[4].animate.next_to(der[0], m.DOWN, buff=0.22, aligned_edge=m.LEFT),
                  run_time=0.8)
        W, Hh = 2.0, 1.05
        cells = {}
        names = {(0, 0): r"a^2x_1x_2", (0, 1): r"a\,x_1cy_2", (1, 0): r"a\,by_1x_2", (1, 1): r"bc\,y_1y_2"}
        for (i, j), nm in names.items():
            col = ORANGE if (i, j) == (1, 1) else DEEP
            r_ = m.Rectangle(width=W, height=Hh, fill_color=col, fill_opacity=0.85, stroke_color=INK,
                             stroke_width=2).move_to([2.6 + j * W, 0.1 - i * Hh, 0])
            cells[(i, j)] = m.VGroup(r_, tex(nm, 28).move_to(r_))
        top = [tex(r"ax_2", 30, BLUE).next_to(cells[(0, 0)], m.UP, buff=0.15),
               tex(r"cy_2", 30, ORANGE).next_to(cells[(0, 1)], m.UP, buff=0.15)]
        left = [tex(t_, 30, c_).next_to(cells[(i, 0)], m.LEFT, buff=0.15)
                for i, (t_, c_) in enumerate(((r"ax_1", BLUE), (r"by_1", ORANGE)))]
        block = m.VGroup(*cells.values())
        self.pin(*top, *left, block)
        self.remove(*top, *left, block)
        self.play(*(m.FadeIn(t_, shift=0.1 * m.DOWN) for t_ in top),
                  *(m.FadeIn(t_, shift=0.1 * m.RIGHT) for t_ in left), run_time=0.7)
        self.play(m.LaggedStart(*(m.DrawBorderThenFill(c_) for c_ in cells.values()), lag_ratio=0.25),
                  run_time=1.8)
        self.cap("Picture it as an area. A rectangle with sides ax₁ + by₁ and ax₂ + cy₂ has area 1·1 = 1, and it "
                 "splits into four pieces")
        blues = m.VGroup(cells[(0, 0)], cells[(0, 1)], cells[(1, 0)])
        self.play(m.Circumscribe(blues, color=BLUE, buff=0.05), m.Indicate(cells[(1, 1)], color=AMBER),
                  run_time=1.4)
        self.cap("The three blue pieces all contain a, so together they make a·X. The orange piece is bc·y₁y₂, and "
                 "that gives aX + (bc)Y = 1")

    # ── 7. extended Euclid ───────────────────────────────────────────────────
    def extended(self):
        self.chapter(7)
        self.cap("Bézout tells us s and t exist, but not how to find them. There are two methods, and either one "
                 "gives a correct answer")
        self.card("Back-substitution",
                  ttex(r"Solve for each remainder, working from the bottom up", 26), C_WORKED, corner=m.UL)
        divs = stack(*(tex(s, 24, MUTED) for s in [
            r"89 = 1\cdot 55 + 34", r"55 = 1\cdot 34 + 21", r"34 = 1\cdot 21 + 13", r"21 = 1\cdot 13 + 8",
            r"13 = 1\cdot 8 + 5", r"8 = 1\cdot 5 + 3", r"5 = 1\cdot 3 + 2", r"3 = 1\cdot 2 + 1"]), buff=0.08)
        divs.to_edge(m.RIGHT, buff=0.5).shift(0.5 * m.UP)
        self.pin(divs)
        self.play(m.FadeIn(divs), run_time=0.8)
        self.cap("We start from the divisions of 89 and 55 we already have. The idea is to always write 1 using the "
                 "two latest remainders and climb back up")
        self.derive([
            r"1 = 3 - 1\cdot 2",
            r"= 3 - (5 - 3) = 2\cdot 3 - 5",
            r"= 2(8-5) - 5 = 2\cdot 8 - 3\cdot 5",
            r"= 2\cdot 8 - 3(13-8) = 5\cdot 8 - 3\cdot 13",
            r"= 5(21-13) - 3\cdot 13 = 5\cdot 21 - 8\cdot 13",
            r"= 5\cdot 21 - 8(34-21) = 13\cdot 21 - 8\cdot 34",
            r"= 13(55-34) - 8\cdot 34 = 13\cdot 55 - 21\cdot 34",
            r"= 13\cdot 55 - 21(89-55) = 34\cdot 55 - 21\cdot 89",
        ], anchor=np.array([-6.6, 1.45, 0]), size=28, buff=0.16, notes=[
            "The last division says 1 = 3 − 2",
            "Replace the 2 with 5 − 3, which comes from the division just above, and collect terms",
            "Then replace the 3 with 8 − 5",
            None, None, None, None,
            "At the top we end up with 1 = 34·55 − 21·89",
        ], hold=1.1, highlight=[divs[7 - i] for i in range(8)])
        self.cap("To check it, 34·55 = 1870 and 21·89 = 1869, and the difference is 1", GREEN_L)
        self.card("Note", stack(ttex(r"$1 = 34\cdot 89 - 55\cdot 55$ is another valid answer.", 24),
                                ttex(r"Bézout coefficients aren't unique, and $(s + kb,\ t - ka)$ also works.", 24)),
                  C_QUESTION, corner=m.DR, shift=np.array([0, 1.25, 0]))
        self.cap("Someone else might get 34·89 − 55·55 = 1, and that's right too. There are infinitely many pairs, "
                 "and they all give the same inverse because −55 and 34 are congruent mod 89")
        self.clear_stage()

        # the table
        self.card("The table method",
                  stack(tex(r"r_j = r_{j-2} - q_{j-1} r_{j-1}", 28),
                        tex(r"s_j = s_{j-2} - q_{j-1} s_{j-1},\quad t_j = t_{j-2} - q_{j-1} t_{j-1}", 28),
                        tex(r"\text{every row keeps } r_j = s_j\cdot 89 + t_j\cdot 55", 28, AMBER)), C_THEOREM,
                  corner=m.UL)
        rows = [(89, None, 1, 0), (55, 1, 0, 1), (34, 1, 1, -1), (21, 1, -1, 2), (13, 1, 2, -3), (8, 1, -3, 5),
                (5, 1, 5, -8), (3, 1, -8, 13), (2, 2, 13, -21), (1, None, -21, 34)]
        cols_x = [1.4, 2.6, 3.7, 4.9, 6.1]
        head = [tex(h, 28, AMBER) for h in ["r_j", "q_j", "s_j", "t_j"]]
        top = 2.1
        for h, x in zip(head, cols_x):
            h.move_to([x, top, 0])
        self.pin(*head)
        self.play(*(m.FadeIn(h) for h in head), run_time=0.6)
        pitch = 0.42
        table = []
        for j, (r, q, s, t) in enumerate(rows):
            y = top - 0.5 - j * pitch
            row = [tex(str(r), 26), tex("-" if q is None else str(q), 26, MUTED), tex(str(s), 26, BLUE),
                   tex(str(t), 26, ORANGE)]
            for c, x in zip(row, cols_x):
                c.move_to([x, y, 0])
            table.append(row)
        self.pin(*table[0], *table[1])
        self.play(*(m.FadeIn(c) for c in table[0] + table[1]), run_time=0.8)
        self.cap("The first two rows are free, since 89 = 1·89 + 0·55 and 55 = 0·89 + 1·55. The pattern already "
                 "holds there")
        for j in range(2, len(rows)):
            box = m.SurroundingRectangle(m.VGroup(*table[j - 2], *table[j - 1]), color=GREY, buff=0.06)
            self.pin(box)
            self.play(m.FadeIn(box), run_time=0.25)
            self.pin(*table[j])
            self.play(*(m.TransformFromCopy(m.VGroup(table[j - 2][k], table[j - 1][k]), table[j][k])
                        for k in (0, 2, 3)), m.FadeIn(table[j][1]), run_time=0.7)
            self.play(m.FadeOut(box), run_time=0.2)
            self.remove(box)
            if j == 2:
                self.cap("Each new row is the row two above minus q times the row just above. Everything is linear, "
                         "so if those two rows follow the pattern, the new one does too")
            elif j == 4:
                self.cap("It's the same subtraction in all three columns, with nothing to solve for")
        last = m.SurroundingRectangle(m.VGroup(*table[-1]), color=AMBER, buff=0.08)
        self.pin(last)
        self.play(m.Create(last), run_time=0.6)
        self.cap("The last row reads 1 = −21·89 + 34·55, the same answer we got by back-substitution", AMBER)

    # ── 8. inverses ──────────────────────────────────────────────────────────
    def inverses(self):
        self.chapter(8)
        self.card("Definition", tex(r"\bar a\ \text{is an inverse of } a \md{m} \iff a\,\bar a\equiv 1\md{m}", 32),
                  C_DEF, corner=m.UL)
        self.cap("With real numbers, dividing by a means multiplying by 1/a. In modular arithmetic we look for a "
                 "number that gives 1 when you multiply it by a")
        self.cap("Look at the multiplication tables mod 7 and mod 6. The cells that equal 1 will rise toward us")

        def times_table(m_, x0, title):
            tiles = []
            cs = 0.56
            for a in range(1, m_):
                for b in range(1, m_):
                    v = a * b % m_
                    pos = P(x0 + (b - 1) * cs, 1.25 - (a - 1) * cs)
                    col = GREEN if v == 1 else GREY_D
                    tl = slab(cs - 0.04, cs - 0.04, pos, col, depth=0.08)
                    lab = label(str(v), pos, 20, INK, dy=-0.05)
                    tiles.append((a, b, v, tl, lab))
            hdr = label(title, P(x0 + (m_ - 2) * cs / 2, 1.9), 32, AMBER, is_tex=True)
            rlabs = [label(str(a), P(x0 - 0.5, 1.25 - (a - 1) * cs), 22, MUTED) for a in range(1, m_)]
            return tiles, hdr, rlabs

        t7, h7, r7 = times_table(7, -5.3, r"\bmod 7")
        t6, h6, r6 = times_table(6, 1.3, r"\bmod 6")
        for tiles, hdr, rl in ((t7, h7, r7), (t6, h6, r6)):
            self.play(m.FadeIn(hdr), *(m.FadeIn(lab) for lab in rl),
                      m.LaggedStart(*(m.FadeIn(m.Group(tl, lab)) for *_, tl, lab in tiles), lag_ratio=0.01),
                      run_time=1.4)
        ones = [(tl, lab) for tiles in (t7, t6) for a, b, v, tl, lab in tiles if v == 1]
        self.play(*(tl.animate.stretch(4, 1).shift(0.12 * m.DOWN) for tl, _ in ones),
                  *(lab.animate.shift(0.3 * m.DOWN) for _, lab in ones), run_time=0.8)
        self.cap("Mod 7, every row has a 1 in it, so every number from 1 to 6 has an inverse")
        bad = [(tl, lab) for a, b, v, tl, lab in t6 if a in (2, 3, 4)]
        self.play(*(tint(tl, RED) for tl, _ in bad), run_time=0.8)
        self.cap("Mod 6, the rows for 2, 3 and 4 never reach 1. The row for 2 goes 2, 4, 0, 2, 4, only even numbers. "
                 "These are exactly the numbers that share a factor with 6", RED_L)
        self.move_camera(phi=62 * m.DEGREES, theta=-70 * m.DEGREES, run_time=2.0)
        self.home(run_time=1.6)
        self.clear_stage()

        self.card("Theorem", tex(r"a\ \text{has an inverse}\md{m}\iff \gcd(a,m)=1", 34, AMBER), C_THEOREM,
                  corner=m.UL)
        self.derive([
            r"a\bar a\equiv 1 \md{m}",
            r"\iff m\mid a\bar a - 1",
            r"\iff a\bar a - 1 = mk",
            r"\iff \bar a\cdot a + (-k)\cdot m = 1",
            r"\iff \gcd(a,m)=1",
        ], anchor=np.array([-6.6, 1.3, 0]), size=34, notes=[
            "The proof is really just translation. Saying a times a-bar is 1 mod m",
            "means m divides the difference",
            "which means the difference is a multiple of m",
            "Rearranged, that's a linear combination of a and m equal to 1",
            "And by the coprimality test, that happens exactly when gcd(a, m) = 1",
        ])
        self.card("How to compute it",
                  stack(tex(r"sa + tm = 1\ \xrightarrow{\ \bmod m\ }\ sa\equiv 1", 30),
                        tex(r"34\cdot 55 - 21\cdot 89 = 1\ \Rightarrow\ 55^{-1}\equiv 34 \md{89}", 30, GREEN_L)),
                  C_WORKED, corner=m.UR, shift=np.array([0, -2.0, 0]))
        self.cap("To compute it, run extended Euclid and reduce mod m. The m term disappears and what's left is the "
                 "inverse. From our earlier example, the inverse of 55 mod 89 is 34", GREEN_L)
        self.card("Rule of thumb",
                  ttex(r"To find $a^{-1}\bmod m$, check that $\gcd(a,m)=1$ and read off Bézout's $s$.", 26),
                  C_RULE, corner=m.DL, shift=np.array([0, 1.25, 0]))
        self.wait(3)
