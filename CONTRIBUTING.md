# Contributing

## How to Contribute

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `uv run --with pytest pytest backend/tests/unit`
5. Submit a pull request

## Code Style

- Follow PEP 8 for Python code
- Use TypeScript strict mode
- Run `ruff check` and `pyright` before committing
- Write tests for new features

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): description

feat(analytics): add streak endpoint
fix(moods): handle duplicate entry error
test(analytics): add timeline tests
```
