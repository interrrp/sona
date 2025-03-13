start:
    uv run -m sona

test:
    find sona tests | entr -r sh -c "clear && uv run -m pytest --benchmark-skip"

bench:
    uv run -m pytest
