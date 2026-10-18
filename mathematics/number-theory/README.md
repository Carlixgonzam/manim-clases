# Number theory

A short course in four videos, from "what does it mean to divide?" to RSA, plus a written guide with every proof.

- **Videos:** [latest release](https://github.com/Carlixgonzam/manim-clases/releases/latest)
- **Guide (PDF):** [guide/number_theory_guide.pdf](guide/number_theory_guide.pdf)

## Modules

1. **Divisibility:** the division algorithm, gcd, Euclid's algorithm, unique factorization
2. **Bézout:** Bézout's identity and its lemmas, extended Euclid, modular inverses
3. **Congruences:** linear congruences, the Chinese Remainder Theorem, Fermat, Wilson
4. **Euler and RSA:** Euler's φ, Euler's theorem, self-inverse elements, RSA, a decision map

You need basic algebra and some comfort with proofs. Reference: Rosen, *Discrete Mathematics and Its Applications*, ch. 4.

## Render

```bash
pip install manimgx
manimgx render module1_divisibility.py Module1 --fps 30
manimgx render module2_bezout.py Module2 --fps 30
manimgx render module3_congruences.py Module3 --fps 30
manimgx render module4_euler_rsa.py Module4 --fps 30
```

The shared look (colors, cards, captions and helpers) is in `common.py`.

Guide: `cd guide && pdflatex number_theory_guide.tex` (run it three times for the table of contents).
