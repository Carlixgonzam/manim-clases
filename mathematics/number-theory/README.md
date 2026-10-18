# Number theory

A short course in four videos that goes from what it means for one number to divide another all the way to RSA. It comes with a written guide that has every proof in full.

The videos are in the [latest release](https://github.com/Carlixgonzam/manim-clases/releases/latest) and the guide is in [guide/number_theory_guide.pdf](guide/number_theory_guide.pdf).

## Modules

1. **Divisibility**, the division algorithm, the gcd, Euclid's algorithm and unique factorization
2. **Bézout's identity** and its lemmas, extended Euclid and modular inverses
3. **Congruences**, linear congruences, the Chinese Remainder Theorem, Fermat and Wilson
4. **Euler and RSA**, with Euler's φ, Euler's theorem, self-inverse elements, RSA and a decision map

You'll need basic algebra and some comfort reading proofs. The main reference is Rosen's *Discrete Mathematics and Its Applications*, chapter 4.

## Rendering

```bash
pip install manimgx
manimgx render module1_divisibility.py Module1 --fps 30
manimgx render module2_bezout.py Module2 --fps 30
manimgx render module3_congruences.py Module3 --fps 30
manimgx render module4_euler_rsa.py Module4 --fps 30
```

The shared look of the videos, including colors, cards, captions and helpers, lives in `common.py`.

To build the guide, run `pdflatex number_theory_guide.tex` three times inside `guide/` so the table of contents comes out right.
