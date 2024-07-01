
https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python

poetry add --group dev pytest coverage[toml] pytest-cov pytest-mock flake8 mypy ipykernel

poetry add pydantic_settings pydantic sqlalchemy pandas requests

# Linting

https://docs.astral.sh/ruff/

```bash
ruff check
```

# Testing

https://www.youtube.com/watch?v=cHYq1MRoyI0

```bash
pytest
```

# coverage

https://www.youtube.com/watch?v=6toeRpugWjI

https://stackoverflow.com/questions/36517137/how-to-properly-use-coverage-py-in-python#comment81103062_36524004

https://pytest-cov.readthedocs.io/en/latest/readme.html#usage

https://www.youtube.com/watch?v=7BJ_BKeeJyM

```bash

pytest tests/test_mercadolibrerealstatescraper.py --doctest-modules --junitxml=junit/test-results.xml --cov mercadolibrerealstatescraper --cov-report=

coverage report -m

pytest tests/test_mercadolibrerealstatescraper.py --doctest-modules --junitxml=junit/test-results.xml --cov mercadolibrerealstatescraper --cov-report=xml --cov-report=html


pytest  --doctest-modules --junitxml=junit/test-results.xml --cov mercadolibrerealstatescraper tests/test_mercadolibrerealstatescraper.py

pytest tests/ --doctest-modules --junitxml=junit/test-results.xml --cov --cov-report=xml --cov-report=html

pytest --cov mercadolibrerealstatescraper tests/test_mercadolibrerealstatescraper.py
```

# Python packaging

https://medium.com/@miqui.ferrer/python-packaging-best-practices-4d6da500da5f

https://dev.to/snyk/the-ultimate-guide-to-creating-a-secure-python-package-3pd6

https://www.bing.com/%2fsearch%3fq%3dbuild%2bpython%2bpackage%26filters%3dex1%253a%2522ez5_19390_19869%2522%26qs%3dMT%26pq%3dbuild%2bpython%26sk%3dLT2%26sc%3d10-12%26cvid%3d77326DD4E7BE4CE9B37F13B9C289A15A%26FORM%3d000017%26sp%3d3%26ghc%3d1%26lq%3d0%26qpvt%3dbuild%2bpython%2bpackage

# Security best practices

https://snyk.io/blog/python-security-best-practices-cheat-sheet/

https://snyk.io/advisor/python