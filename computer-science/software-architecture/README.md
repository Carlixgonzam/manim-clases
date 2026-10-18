# Software architecture

How software systems are structured, and how architecture connects to compilers and domain-specific languages (DSLs).

**Status:** planned.

## Planned modules

1. **Architectural styles:** layers, pipes and filters, event-driven systems, microservices
2. **The compiler as an architecture:** lexer → parser → AST → analysis → code generation, a pipeline where each stage has one job
3. **DSLs:** small languages for one domain (SQL, regex, build files, configuration); internal vs. external DSLs
4. **Building a DSL:** grammar, parser, AST and interpreter, with a language workbench such as Rascal
5. **Models and code generation:** describing a system in a DSL and generating the code from it
