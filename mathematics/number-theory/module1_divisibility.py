"""Number theory, module 1: divisibility, the division algorithm, gcd, Euclid and the fundamental theorem.

    manimgx render module1_divisibility.py Module1
"""

import manimgx as m
import numpy as np

from common import (AMBER, BLUE, C_DEF, C_MISTAKE, C_RULE, C_THEOREM, C_WORKED, DEEP, EDGE, GREEN, GREEN_L,
                    GREY, GREY_D, INK, MUTED, ORANGE, PURPLE, RED, RED_L, TEAL, Lesson, P, cube, label, number_line,
                    slab, stack, tex, tint, ttex, up)


class Module1(Lesson):
    START = 1
    CHAPTERS = [
        "What it means to divide",
        "The division algorithm",
        "The gcd and Euclid's algorithm",
        "Primes and unique factorization",
    ]

    def construct(self) -> None:
        self.setup_hud()
        self.intro()
        self.divisibility()
        self.division()
        self.euclid()
        self.fta()
        self.takeaways([
            "a | b  means  b = a·k  for some integer k; almost every proof writes that down and does algebra",
            "If d divides two numbers, it divides every linear combination of them",
            "The remainder always satisfies 0 ≤ r < d, even when a is negative",
            "gcd(a, b) = gcd(b, r): Euclid swaps the pair without changing the common divisors",
            "Once factored: smallest exponents for the gcd, largest for the lcm",
        ], "In module 2 we see that the gcd can also be written as a sum, with Bézout")

    # ── 0. intro ─────────────────────────────────────────────────────────────
    def intro(self):
        self.set_camera_orientation(phi=62 * m.DEGREES, theta=-120 * m.DEGREES, zoom=0.92)
        cubes = [cube("", P(-3.3 + 0.6 * i, 0.4), BLUE if (i // 3) % 2 == 0 else TEAL, side=0.52)
                 for i in range(12)]
        self.play(m.LaggedStart(*(m.FadeIn(c, shift=0.6 * m.OUT) for c in cubes), lag_ratio=0.06), run_time=1.6)
        self.move_camera(phi=76 * m.DEGREES, theta=-90 * m.DEGREES, run_time=1.6)
        self.cap("Number theory starts with a very simple question: does one number fit exactly into another?")
        self.clear_stage()
        self.title_card("Number Theory · Module 1", "divisibility, division, gcd and factorization")
        self.cap("Four chapters, and each one answers a question. First the intuition, then the theorem, the "
                 "proof and an example with numbers")

    # ── 1. divisibility ──────────────────────────────────────────────────────
    def divisibility(self):
        self.chapter(1)
        self.card("Definition", tex(r"a \mid b \iff \exists\, k\in\mathbb{Z}:\ b = a\cdot k", 34), C_DEF,
                  corner=m.UL)
        self.cap("We say a divides b when b is a times some integer. It isn't a fraction or an operation: it's a "
                 "statement that is either true or false")
        xs = [-3.3 + 0.6 * i for i in range(12)]
        cubes = [cube("", P(x, 0.0), GREY_D, side=0.52) for x in xs]
        twelve = label("b = 12", P(0, 0.9), 30)
        self.play(m.LaggedStart(*(m.FadeIn(c, shift=0.5 * m.IN) for c in cubes), lag_ratio=0.04),
                  m.FadeIn(twelve), run_time=1.4)
        self.cap("Think of b as a row of twelve cubes. Asking whether 3 divides 12 is asking whether the row can "
                 "be cut into blocks of three with nothing left over")
        cols = [BLUE, TEAL]
        self.play(*(tint(c[0], cols[(i // 3) % 2]) for i, c in enumerate(cubes)), run_time=1.0)
        self.play(*(c.animate.shift(0.18 * (i // 3) * m.RIGHT) for i, c in enumerate(cubes)), run_time=0.8)
        res = label(r"12 = 3\cdot 4", P(0.3, -0.9), 34, AMBER, is_tex=True)
        self.play(m.Write(res), run_time=0.8)
        self.cap("Four exact blocks, so 3 | 12 with k = 4", AMBER)
        self.play(*(c.animate.shift(-0.18 * (i // 3) * m.RIGHT) for i, c in enumerate(cubes)), m.FadeOut(res),
                  run_time=0.7)
        cols5 = [ORANGE, AMBER]
        self.play(*(tint(c[0], cols5[(i // 5) % 2] if i < 10 else RED) for i, c in enumerate(cubes)), run_time=1.0)
        self.play(*(c.animate.shift(0.18 * (i // 5) * m.RIGHT) for i, c in enumerate(cubes)), run_time=0.8)
        res2 = label(r"12 = 5\cdot 2 + 2 \;\Rightarrow\; 5\nmid 12", P(0.3, -0.9), 34, RED_L, is_tex=True)
        self.play(m.Write(res2), *(m.Indicate(cubes[i], color=RED_L) for i in (10, 11)), run_time=1.0)
        self.cap("With blocks of five, two cubes are left over. No integer k gives 12 = 5k, so 5 does not divide "
                 "12")
        self.clear_stage()

        # properties
        props = stack(
            tex(r"1.\ \ 1\mid a,\quad a\mid 0,\quad a\mid a", 30),
            tex(r"2.\ \ a\mid b,\ b\mid c \;\Rightarrow\; a\mid c", 30),
            tex(r"3.\ \ a\mid b,\ a\mid c \;\Rightarrow\; a\mid bx+cy", 30),
            tex(r"4.\ \ b\neq 0,\ a\mid b \;\Rightarrow\; |a|\le |b|", 30),
            tex(r"5.\ \ a,b>0,\ a\mid b,\ b\mid a \;\Rightarrow\; a=b", 30),
            buff=0.2)
        self.card("Properties of divisibility", props, C_THEOREM, corner=m.UL)
        self.cap("Five properties get used all the time. They are all proved the same way: write each hypothesis "
                 "as a product and do algebra")
        hl = m.SurroundingRectangle(props[2], color=AMBER, buff=0.08)
        self.pin(hl)
        self.play(m.Create(hl), run_time=0.6)
        self.cap("The third one, about linear combinations, is the one you'll use most. Here's its proof")
        self.derive([
            r"b = a k,\qquad c = a\ell",
            r"bx + cy = akx + a\ell y",
            r"bx + cy = a\,(kx + \ell y)",
            r"kx+\ell y\in\mathbb{Z}\;\Rightarrow\; a \mid bx+cy",
        ], anchor=np.array([0.6, 1.6, 0]), size=32, notes=[
            "The hypotheses say that b and c are multiples of a",
            "Substitute into the linear combination",
            "And factor a out",
            "What's left in parentheses is an integer, so a divides the combination. That's all",
        ])
        nl = number_line(-3, 15, np.array([0, -2.0, 0]), 12.0)
        mult = m.VGroup(*(m.Dot(nl.n2p(k), radius=0.09, color=AMBER) for k in range(-3, 16, 3)))
        ball = m.Dot(nl.n2p(0), radius=0.13, color=GREEN_L)
        self.pin(nl, mult, ball)
        self.play(m.Create(nl), m.LaggedStart(*(m.GrowFromCenter(d) for d in mult), lag_ratio=0.12),
                  m.FadeIn(ball, scale=0.4), run_time=1.4)
        self.cap("On the number line, with a = 3, b = 6 and c = 9. The amber points are the multiples of 3, the "
                 "only places where 3 divides")
        hops = self.hop(nl, ball, 0, [6, 12], BLUE, labels=["+6", "+6"], angle=1.0)
        self.cap("With x = 2 we take two hops of size b = 6. Each hop is a multiple of 3, so we always land on "
                 "amber", BLUE)
        hops2 = self.hop(nl, ball, 12, [3], ORANGE, labels=["-9"], angle=1.25)
        self.play(m.Indicate(ball, color=AMBER, scale_factor=1.8), run_time=0.7)
        self.cap("With y = −1 we hop c = 9 backwards and land on 2·6 − 9 = 3. However many hops you take, you "
                 "never leave the amber points", ORANGE)
        self.play(m.FadeOut(m.VGroup(nl, mult, ball, hops, hops2)), run_time=0.6)
        self.play(m.FadeOut(hl), run_time=0.3)
        self.remove(hl)
        counter = self.card("Canonical counterexample",
                            tex(r"3 \mid (1+2)\quad\text{but}\quad 3\nmid 1,\ \ 3\nmid 2", 30), C_MISTAKE,
                            corner=None, shift=np.array([3.4, -1.5, 0]))
        self.cap("Careful: the converse is false. Knowing that d divides a sum says nothing about each term on "
                 "its own", RED_L)
        rule = self.card("Rule of thumb",
                         ttex(r"To prove $a\mid X$: write $X = a\cdot(\text{integer})$", 28), C_RULE,
                         corner=None, shift=np.array([3.4, -2.75, 0]), write=False)
        self.play(m.FadeOut(counter), rule.animate.shift(1.15 * m.UP), run_time=0.6)
        self.cap("Or, if that doesn't come out directly, as a linear combination of things a already divides")

    # ── 2. the division algorithm ────────────────────────────────────────────
    def division(self):
        self.chapter(2)
        self.card("Division algorithm",
                  stack(tex(r"a\in\mathbb{Z},\ d>0\ \Rightarrow\ \exists!\, q, r:", 30),
                        tex(r"a = d\,q + r,\qquad 0\le r<d", 34, AMBER)), C_THEOREM, corner=m.UL)
        self.cap("If d doesn't divide a, the question is how to describe exactly what's left over, and why that "
                 "description is unique")
        lo, hi = -24, 2
        w = 0.46
        xs = {n: (n - (lo + hi) / 2) * w for n in range(lo, hi + 1)}
        z = -0.4
        cols = [DEEP, TEAL]
        cubes = {n: cube("", P(xs[n], z), cols[(n // 3) % 2], side=0.4) for n in range(lo, hi + 1)}
        nums = {n: label(str(n), P(xs[n], z - 0.42), 15, MUTED) for n in range(lo, hi + 1)}
        self.play(m.LaggedStart(*(m.FadeIn(cubes[n], shift=0.3 * m.IN) for n in cubes), lag_ratio=0.02),
                  m.FadeIn(m.Group(*nums.values())), run_time=1.8)
        self.cap("Line the integers up and paint them in drawers of size 3. Each drawer starts at a multiple of 3")
        mults = [n for n in range(lo, hi + 1) if n % 3 == 0]
        marks = [label(f"{n}", P(xs[n], z + 0.72), 20, AMBER) for n in mults]
        self.play(*(cubes[n].animate.shift(0.18 * m.OUT) for n in mults), *(m.FadeIn(k) for k in marks),
                  run_time=1.0)
        self.cap("Every number lands in exactly one drawer. The quotient q says which drawer, and the remainder r "
                 "says how far in it went")
        a = -20
        self.play(tint(cubes[a][0], AMBER, 0.8), m.Indicate(nums[a], color=AMBER, scale_factor=1.6), run_time=1.0)
        self.move_camera(zoom=1.45, frame_center=P(xs[-19] + 0.4, z - 0.4), run_time=1.4)
        good = slab(xs[-20] - xs[-21], 0.12, P((xs[-21] + xs[-20]) / 2, z - 0.75), GREEN_L, depth=0.06,
                    opacity=0.9)
        g_ticks = [slab(0.05, 0.3, P(xs[n], z - 0.75), GREEN_L, depth=0.06, opacity=0.9) for n in (-21, -20)]
        r_lab = label("r = 1", P((xs[-21] + xs[-20]) / 2, z - 1.05), 24, GREEN_L)
        self.play(m.FadeIn(good), *(m.FadeIn(t) for t in g_ticks), m.FadeIn(r_lab), run_time=0.9)
        self.cap("For a = −20 the drawer starts at −21, which is 3 times −7. From −21 to −20 you move 1. So q = −7 "
                 "and r = 1", GREEN_L)
        bad = slab(xs[-18] - xs[-20], 0.12, P((xs[-18] + xs[-20]) / 2, z - 1.4), RED_L, depth=0.06, opacity=0.9)
        b_ticks = [slab(0.05, 0.3, P(xs[n], z - 1.4), RED_L, depth=0.06, opacity=0.9) for n in (-20, -18)]
        bad_lab = label("r = −2", P((xs[-18] + xs[-20]) / 2, z - 1.7), 24, RED_L)
        self.play(m.FadeIn(bad), *(m.FadeIn(t) for t in b_ticks), m.FadeIn(bad_lab), run_time=0.9)
        self.cap("It's also true that −20 = 3·(−6) − 2, but that is not the division. It measures backwards from "
                 "−18 and gives a negative remainder", RED_L)
        self.home(run_time=1.2)
        self.card("Common mistake",
                  stack(tex(r"-20 = 3(-6) - 2\quad\text{NO}\ \ (r<0)", 28, RED_L),
                        tex(r"-20 = 3(-7) + 1\quad\text{YES}", 28, GREEN_L),
                        ttex(r"Fix: $q\to q-1,\ r\to r+d$", 26)),
                  C_MISTAKE, corner=m.UR)
        self.cap("If you ever get a negative remainder, subtract one from the quotient and add d to the remainder")
        self.clear_stage()

        # proof
        self.card("Division algorithm", tex(r"a = d\,q + r,\qquad 0\le r<d", 34, AMBER), C_THEOREM,
                  corner=m.UL, write=False)
        self.cap("Now the proof, which has two parts: that q and r exist, and that they are unique")
        nl = number_line(-6, 19, np.array([0, 0.2, 0]), 12.4, only=range(-5, 20, 5))
        ball = m.Dot(nl.n2p(17), radius=0.13, color=GREEN_L)
        s_pts = m.VGroup(*(m.Dot(nl.n2p(v), radius=0.1, color=GREEN_L) for v in (17, 12, 7, 2)))
        self.pin(nl, ball)
        self.play(m.Create(nl), m.FadeIn(ball, scale=0.4), run_time=1.0)
        self.cap("Take a = 17 and d = 5. The set S holds the leftovers you get by removing fives without going "
                 "negative")
        self.pin(s_pts)
        self.remove(s_pts)
        hops = self.hop(nl, ball, 17, [12, 7, 2], GREEN_L, labels=["-5"] * 3, angle=1.2, run_time=0.55)
        self.play(m.LaggedStart(*(m.GrowFromCenter(d) for d in s_pts), lag_ratio=0.2), run_time=0.7)
        bad = m.DashedLine(nl.n2p(2), nl.n2p(-3), color=RED_L, stroke_width=4).shift(0.35 * m.UP)
        x_bad = m.Cross(m.Dot(nl.n2p(-3), radius=0.18), stroke_width=5, stroke_color=RED_L)
        out = tex(r"-3\notin S", 26, RED_L).next_to(x_bad, m.UP, buff=0.35)
        self.pin(bad, x_bad, out)
        self.remove(bad, x_bad, out)
        self.play(m.Create(bad), run_time=0.5)
        self.play(m.Create(x_bad), m.FadeIn(out), m.Wiggle(x_bad), run_time=0.9)
        self.cap("One more hop would give −3, which is negative and not in S. So S = {17, 12, 7, 2}, and its "
                 "minimum is 2", RED_L)
        box0 = m.BraceLabel(m.Line(nl.n2p(0), nl.n2p(5)), r"0\le r<5", brace_direction=m.DOWN, font_size=26,
                            color=AMBER).shift(0.35 * m.DOWN)
        self.pin(box0)
        self.remove(box0)
        self.play(m.FadeIn(box0, shift=0.1 * m.UP), m.Circumscribe(ball, shape=m.Circle, color=AMBER),
                  run_time=1.0)
        self.cap("The minimum always lands in the first drawer, between 0 and d − 1: if it were d or more, "
                 "another hop would fit without going negative", AMBER)
        self.play(m.FadeOut(m.VGroup(nl, ball, s_pts, hops, bad, x_bad, out, box0)), run_time=0.6)
        ex = stack(
            ttex(r"\textbf{Existence.} $S=\{a-dk\ :\ k\in\mathbb{Z},\ a-dk\ge 0\}\neq\varnothing$", 28),
            ttex(r"Well-ordering: $S$ has a minimum $r=a-dq\ge 0$.", 28),
            ttex(r"If $r\ge d$: $\ r-d=a-d(q+1)\in S$ and it is smaller than $r$. Contradiction.", 28),
            ttex(r"Hence $0\le r<d$.", 28, AMBER),
            buff=0.22).move_to(np.array([0, 0.75, 0]))
        for i, note in enumerate([
            "Look at every non-negative leftover you get by removing multiples of d from a",
            "By the well-ordering principle there is a smallest one, and we call it r",
            "If r were d or more you could remove one more d and get a smaller leftover, which contradicts r "
            "being the minimum",
            "So the minimum always sits between 0 and d − 1",
        ]):
            self.pin(ex[i])
            self.play(m.FadeIn(ex[i], shift=0.2 * m.RIGHT), run_time=0.7)
            self.cap(note)
        un = stack(
            ttex(r"\textbf{Uniqueness.} $dq+r=dq'+r'\ \Rightarrow\ d(q-q') = r'-r$", 28),
            ttex(r"$d\mid r'-r$ \ and \ $-d<r'-r<d\ \Rightarrow\ r'-r=0$", 28),
            buff=0.22).next_to(ex, m.DOWN, buff=0.4, aligned_edge=m.LEFT)
        self.pin(un[0])
        self.play(m.FadeIn(un[0], shift=0.2 * m.RIGHT), run_time=0.7)
        self.cap("For uniqueness, suppose there are two ways to write it and subtract them. The difference of the "
                 "remainders is a multiple of d")
        self.pin(un[1])
        self.play(m.FadeIn(un[1], shift=0.2 * m.RIGHT), run_time=0.7)
        self.cap("But both remainders are between 0 and d − 1, so their difference is strictly between −d and d. "
                 "The only multiple of d in there is zero")

    # ── 3. gcd and Euclid ────────────────────────────────────────────────────
    def euclid(self):
        self.chapter(3)
        self.card("Definition", stack(tex(r"\gcd(a,b)=\max\{d>0:\ d\mid a\ \wedge\ d\mid b\}", 32),
                                      ttex(r"Coprime: $\gcd(a,b)=1$", 28)), C_DEF, corner=m.UL)
        self.cap("The greatest common divisor is the largest positive integer that divides both. If it's 1, we "
                 "say the numbers are coprime")
        self.cap("But factoring large numbers is hard, and dividing is easy. Can we compute the gcd with "
                 "divisions alone?", AMBER)
        self.card("Lemma", tex(r"a = bq + r\ \Rightarrow\ \gcd(a,b) = \gcd(b,r)", 34), C_THEOREM, corner=m.UR)
        self.cap("This lemma is the key. The proof shows something stronger than the statement: both pairs have "
                 "exactly the same common divisors")
        self.derive([
            r"d\mid a,\ d\mid b\ \Rightarrow\ d\mid a-bq = r",
            r"d\mid b,\ d\mid r\ \Rightarrow\ d\mid bq+r = a",
        ], anchor=np.array([-6.6, 1.0, 0]), size=32, notes=[
            "If d divides a and b, it divides the combination a − bq, which is r",
            "And the other way: if d divides b and r, it divides bq + r, which is a",
        ])
        example = stack(
            tex(r"84 = 2\cdot 36 + 12", 30),
            tex(r"\text{common divisors of }(84,36)=\{1,2,3,4,6,12\}", 28),
            tex(r"\text{common divisors of }(36,12)=\{1,2,3,4,6,12\}", 28),
        ).move_to(np.array([-2.6, -1.2, 0]), aligned_edge=m.LEFT)
        self.pin(example)
        self.play(m.FadeIn(example, shift=0.2 * m.UP), run_time=1.0)
        self.cap("If the sets of common divisors are equal, so are their maximums. So we can swap the big pair "
                 "for a smaller one without losing the gcd")
        self.clear_stage()

        # rectangle
        self.cap("Now let's see Euclid's algorithm as a puzzle. We have a 21 by 13 rectangle")
        u = 0.27
        W, H = 21, 13
        x0, z0 = -4.6, -1.85
        frame = m.Rectangle(width=W * u, height=H * u, stroke_color=INK, stroke_width=3)
        up(frame).move_to(P(x0 + W * u / 2, z0 + H * u / 2, -0.1))
        wl = label("21", P(x0 + W * u / 2, z0 - 0.3), 26)
        hl = label("13", P(x0 - 0.35, z0 + H * u / 2), 26)
        self.play(m.Create(frame), m.FadeIn(wl), m.FadeIn(hl), run_time=1.0)
        # cuts: (x, z, side, color)
        squares = []
        x, zb, w, h = 0, 0, W, H
        pal = [BLUE, TEAL, PURPLE, AMBER, ORANGE, GREEN, RED_L]
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
            "Cut out the largest square that fits, of side 13. It fits once and leaves a 13 by 8 rectangle. "
            "That is 21 = 1·13 + 8",
            "Repeat with what's left: a square of 8, leaving an 8 by 5",
            "And so on, each time with the leftover rectangle",
            None, None,
            "When a square fills what's left exactly, the remainder is zero and we stop",
        ]
        for j, (a, b, q, r) in enumerate(steps):
            blocks = []
            for _ in range(q):
                sx, sz, s, col = squares[idx]
                idx += 1
                sl = slab(s * u - 0.04, s * u - 0.04, P(x0 + (sx + s / 2) * u, z0 + (sz + s / 2) * u), col,
                          depth=0.12 + 0.05 * j)
                lab = label(str(s), P(x0 + (sx + s / 2) * u, z0 + (sz + s / 2) * u, -0.1 - 0.025 * j),
                            max(12, int(14 + s * 1.3)))
                blocks.append(m.Group(sl, lab))
            self.pin(eqs[j])
            self.play(*(m.FadeIn(b, shift=0.6 * m.IN) for b in blocks), m.Write(eqs[j]), run_time=0.9)
            if j < len(notes) and notes[j]:
                self.cap(notes[j])
            else:
                self.wait(0.4)
        last = m.SurroundingRectangle(eqs[-2], color=AMBER, buff=0.08)
        self.pin(last)
        self.play(m.Create(last), run_time=0.6)
        self.cap("The side of the last square is 1, the last nonzero remainder. That's the gcd: the largest "
                 "square tile that tiles the whole rectangle", AMBER)
        self.swing(theta=-60, phi=62, run_time=2.2)
        self.cap("21 and 13 are Fibonacci numbers. That's why almost every quotient is 1 and the algorithm takes "
                 "as many steps as it possibly can. It's the worst case")
        self.clear_stage()

        self.card("Euclid's algorithm",
                  stack(tex(r"a = bq_1 + r_1,\quad b = r_1q_2 + r_2,\ \dots", 30),
                        tex(r"\gcd(a,b) = \text{last nonzero remainder}", 30, AMBER)), C_THEOREM, corner=m.UL)
        table = stack(*(tex(s, 28) for s in [
            r"89 = 1\cdot 55 + 34", r"55 = 1\cdot 34 + 21", r"34 = 1\cdot 21 + 13", r"21 = 1\cdot 13 + 8",
            r"13 = 1\cdot 8 + 5", r"8 = 1\cdot 5 + 3", r"5 = 1\cdot 3 + 2", r"3 = 1\cdot 2 + 1",
            r"2 = 2\cdot 1 + 0"]), buff=0.1).to_edge(m.RIGHT, buff=1.0).shift(0.25 * m.UP)
        self.pin(table)
        self.play(m.LaggedStart(*(m.FadeIn(t, shift=0.2 * m.LEFT) for t in table), lag_ratio=0.15), run_time=2.2)
        self.cap("Another example, the gcd of 89 and 55. Fibonacci again: every quotient is 1 and the gcd is 1, "
                 "so they are coprime")
        rems = [89, 55, 34, 21, 13, 8, 5, 3, 2, 1]
        chart = m.BarChart(rems, y_range=[0, 90, 30], x_length=5.6, y_length=3.2,
                           bar_colors=[DEEP, BLUE, TEAL, GREEN], bar_fill_opacity=0.9, bar_stroke_width=0)
        chart.move_to([3.6, -0.55, 0])
        nums = chart.get_bar_labels(color=INK, font_size=22)
        self.pin(chart, nums)
        self.remove(chart, nums)
        self.play(m.FadeOut(table, shift=0.3 * m.RIGHT), m.Create(chart), run_time=1.6)
        self.play(m.LaggedStart(*(m.FadeIn(n, shift=0.1 * m.DOWN) for n in nums), lag_ratio=0.1), run_time=1.0)
        self.play(m.Circumscribe(m.VGroup(chart.bars[-1], nums[-1]), color=AMBER), run_time=1.0)
        self.cap("The remainders as bars: each one is a natural number smaller than the one before. A staircase "
                 "like that has to reach the floor in finitely many steps", AMBER)
        self.card("Proof sketch",
                  stack(ttex(r"1. divide and swap $(a,b)\to(b,r)$", 26),
                        ttex(r"2. same common divisors $\Rightarrow$ same gcd", 26),
                        ttex(r"3. $b>r_1>r_2>\cdots\ge 0$, so it stops", 26),
                        ttex(r"4. $\gcd(r_k,0)=r_k$", 26)), C_WORKED, corner=m.DL,
                  shift=np.array([0, 1.25, 0]))
        self.cap("Why it stops: the remainders are natural numbers that strictly decrease, and that can't go on "
                 "forever")
        self.cap("And at the end, the gcd of a number and zero is the number itself")

    # ── 4. fundamental theorem of arithmetic ─────────────────────────────────
    def fta(self):
        self.chapter(4)
        self.card("Fundamental theorem of arithmetic",
                  stack(tex(r"n>1\ \Rightarrow\ n = p_1^{a_1}p_2^{a_2}\cdots p_k^{a_k}", 32),
                        ttex(r"and that factorization is unique up to order", 26)), C_THEOREM, corner=m.UL)
        self.cap("Every integer greater than one splits into primes, and in only one way")
        # the tree of 360
        spec = {"360": (1.8, 1.6, None), "8": (0.0, 0.4, "360"), "45": (3.6, 0.4, "360"),
                "2a": (-0.9, -0.8, "8"), "4": (0.9, -0.8, "8"), "5": (4.5, -0.8, "45"),
                "9": (2.7, -0.8, "45"), "2b": (0.25, -2.0, "4"), "2c": (1.45, -2.0, "4"),
                "3a": (2.2, -2.0, "9"), "3b": (3.3, -2.0, "9")}
        primes = {"2a", "2b", "2c", "5", "3a", "3b"}
        nodes = {}
        for k, (x, z, _) in spec.items():
            nodes[k] = cube(k.rstrip("abc"), P(x, z), GREEN if k in primes else DEEP, side=0.62, size=26)
        edges = [m.Line3D(nodes[k][0].get_center(), nodes[p][0].get_center(), thickness=0.02, color=EDGE)
                 for k, (_, _, p) in spec.items() if p]
        order = [["360"], ["8", "45"], ["2a", "4", "9", "5"], ["2b", "2c", "3a", "3b"]]
        for lvl in order:
            es = [e for e, (k, (_, _, p)) in zip(edges, [(k, v) for k, v in spec.items() if v[2]]) if k in lvl]
            self.play(*(m.FadeIn(nodes[k], shift=0.4 * m.IN) for k in lvl), *(m.Create(e) for e in es),
                      run_time=0.8)
        res = label(r"360 = 2^3\cdot 3^2\cdot 5", P(1.8, 2.5), 36, AMBER, is_tex=True)
        self.play(m.Write(res), *(m.Indicate(nodes[k], color=GREEN_L) for k in primes), run_time=1.2)
        self.cap("Keep splitting until only primes are left: the green leaves. That's how existence is proved, by "
                 "strong induction")
        self.cap("Uniqueness needs something from module 2, Euclid's lemma: if a prime divides a product, it "
                 "divides one of the factors")
        self.swing(theta=-62, phi=64, run_time=2.0)
        self.clear_stage()

        # infinitely many primes
        self.card("Theorem (Euclid)", ttex(r"There are infinitely many primes.", 30), C_THEOREM, corner=m.UL)
        self.cap("Now one of the most beautiful proofs: there are infinitely many primes. It goes by "
                 "contradiction")
        self.derive([
            r"\text{Suppose the only primes are } p_1, p_2, \dots, p_k",
            r"N = p_1 p_2\cdots p_k + 1 > 1",
            r"\text{FTA: some prime } p_i \mid N",
            r"p_i \mid N - p_1\cdots p_k = 1",
        ], anchor=np.array([-6.6, 1.3, 0]), size=32, notes=[
            "Suppose the list of primes is finite",
            "Multiply all of them together and add one",
            "By the fundamental theorem, N has some prime factor, and it has to be on the list",
            "But that prime divides both N and the product, so it divides their difference, which is 1. No prime "
            "divides 1. Contradiction",
        ])
        ps = [2, 3, 5, 7, 11, 13]
        table = m.MathTable([[str(p) for p in ps], [str(30031 % p) for p in ps]],
                            row_labels=[tex("p", 34), tex(r"N\bmod p", 34)], h_buff=0.7, v_buff=0.5,
                            include_outer_lines=False, line_config={"stroke_color": GREY})
        table.scale_to_fit_width(5.6).move_to([3.7, 1.35, 0])
        head = tex(r"N = 2\cdot3\cdot5\cdot7\cdot11\cdot13+1 = 30031", 28, AMBER).next_to(table, m.UP, buff=0.25)
        self.pin(table, head)
        self.remove(table, head)
        self.play(m.Write(head), table.create(), run_time=1.6)
        ones = table.get_rows()[1][1:]
        self.play(m.LaggedStart(*(m.Flash(u, color=GREEN_L, flash_radius=0.25) for u in ones), lag_ratio=0.15),
                  *(u.animate.set_color(GREEN_L) for u in ones), run_time=1.4)
        self.cap("With the first six primes: N leaves remainder 1 when divided by each of them. None of them "
                 "divides it", GREEN_L)
        self.card("Canonical counterexample",
                  stack(tex(r"2\cdot3\cdot5\cdot7\cdot11\cdot13+1 = 30031 = 59\cdot 509", 30),
                        ttex(r"$N$ need not be prime: its prime factors are \emph{new} ones", 26)),
                  C_MISTAKE, corner=m.DR, shift=np.array([0, 1.3, 0]))
        self.cap("A common mistake is to say that N is prime. It doesn't have to be: what the proof says is that "
                 "its prime factors are not on the list", RED_L)
        self.clear_stage()

        # gcd and lcm from exponents
        self.card("gcd and lcm from the factorization",
                  stack(tex(r"\gcd = \prod p_i^{\min(\alpha_i,\beta_i)},\qquad"
                            r"\lcm = \prod p_i^{\max(\alpha_i,\beta_i)}", 30),
                        tex(r"a\cdot b = \gcd(a,b)\cdot\lcm(a,b)", 30)), C_THEOREM, corner=m.UL)
        a_exp = {2: 3, 3: 2, 5: 0, 7: 1}
        b_exp = {2: 1, 3: 4, 5: 1, 7: 0}
        h = 0.42
        bars = []
        labels = []
        for i, p in enumerate([2, 3, 5, 7]):
            x = -1.8 + 1.9 * i
            for j, (e, col) in enumerate(((a_exp[p], BLUE), (b_exp[p], ORANGE))):
                xx = x + (j - 0.5) * 0.55
                if e:
                    bar = m.Prism(dimensions=[0.45, 0.45, e * h], fill_color=col, fill_opacity=1, stroke_width=0)
                    bar.move_to(P(xx, -1.6 + e * h / 2))
                else:
                    bar = m.Prism(dimensions=[0.45, 0.45, 0.04], fill_color=col, fill_opacity=0.5,
                                  stroke_width=0).move_to(P(xx, -1.58))
                bars.append((p, j, e, bar))
                labels.append(label(str(e), P(xx, -1.6 + e * h + 0.25), 20, col))
            labels.append(label(str(p), P(x, -2.0), 28, INK))
        key = stack(tex(r"a = 504 = 2^3\cdot 3^2\cdot 7", 28, BLUE),
                    tex(r"b = 810 = 2\cdot 3^4\cdot 5", 28, ORANGE)).to_corner(m.UR, buff=0.4).shift(0.5 * m.DOWN)
        self.pin(key)
        self.play(m.FadeIn(key), *(m.GrowFromPoint(b, b.get_bottom()) for *_, b in bars),
                  *(m.FadeIn(lab) for lab in labels), run_time=1.6)
        self.cap("Draw the exponents as columns, one per prime: blue for a = 504 and orange for b = 810")
        mins = [b for p, j, e, b in bars if e == min(a_exp[p], b_exp[p])]
        self.play(*(tint(b, AMBER, 0.75) for b in mins), run_time=0.8)
        g = label(r"\gcd = 2^1\cdot 3^2 = 18", P(0.9, 1.45), 34, AMBER, is_tex=True)
        self.play(m.Write(g), run_time=0.9)
        self.cap("For the gcd, keep the lower column for each prime: a common divisor can't have more than either "
                 "number has", AMBER)
        maxs = [b for p, j, e, b in bars if e == max(a_exp[p], b_exp[p])]
        self.play(*(tint(b, AMBER, 0.15) for b in mins), *(tint(b, GREEN_L, 0.75) for b in maxs), run_time=0.8)
        lc = label(r"\lcm = 2^3\cdot 3^4\cdot 5\cdot 7 = 22680", P(0.9, 0.85), 34, GREEN_L, is_tex=True)
        self.play(m.Write(lc), run_time=0.9)
        self.cap("For the lcm, keep the higher one. And since min plus max is the sum of both exponents, you get "
                 "a·b = gcd·lcm", GREEN_L)
        self.swing(theta=-50, phi=66, run_time=2.0)
        self.card("Rule of thumb",
                  ttex(r"Big numbers? Euclid. Already factored? $\min$ and $\max$ of the exponents.", 26),
                  C_RULE, corner=m.DL, shift=np.array([0, 1.25, 0]))
        self.wait(2.5)
