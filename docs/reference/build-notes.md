# Build System Architecture

## Overview

This project uses a polyglot build system with three language targets:
- **Rust**: Core library (`cargo`)
- **Python**: Python bindings via PyO3 (`maturin`)
- **JavaScript**: WASM bindings via wasm-bindgen (`wasm-pack`)

All builds are orchestrated through `just` (similar to `make`).

## Project Structure

```
cif-parser/
├── src/                           # Rust source code
│   ├── lib.rs
│   ├── python.rs                  # PyO3 bindings
│   └── ...
├── python/                        # Python package
│   ├── src/                       # Python source (src layout)
│   │   └── cif_parser/
│   │       ├── __init__.py
│   │       ├── __init__.pyi
│   │       ├── _cif_parser.pyi
│   │       └── py.typed
│   ├── tests/
│   └── pyproject.toml
├── javascript/                    # JavaScript/TypeScript source
│   ├── examples/
│   ├── tests/
│   ├── package.json
│   ├── biome.json
│   ├── pkg-node/                  # WASM build output (Node.js)
│   ├── pkg/                       # WASM build output (web)
│   └── pkg-bundler/               # WASM build output (bundler)
├── target/                        # Rust build artifacts
│   └── wheels/                    # Python wheels
└── justfile                       # Build orchestration
```

## Design Principles

### 1. Separation of Source and Build Artifacts

**Problem:** Mixed layouts place compiled extensions directly in source directories, causing:
- Git tracking issues
- CI/CD failures (duplicate file errors)
- Confusing developer experience

**Solution:**
- Python: **Src layout** (`python-source = "src"`)
- JavaScript: **Nested builds** (`--out-dir javascript/pkg-node`)

### 2. Python Src Layout

**Configuration:**
```toml
[tool.maturin]
features = ["pyo3/extension-module", "python"]
python-source = "src"
module-name = "cif_parser._cif_parser"
manifest-path = "../Cargo.toml"
```

**Why Src Layout:**
- Industry standard (used by pydantic-core, polars, ruff, cryptography)
- Clear separation: source in `src/`, builds coexist but are distinct
- Prevents "File was already added" errors on Windows CI
- Better IDE support and import resolution

**Build Process:**
1. Maturin compiles Rust to `_cif_parser.*.so/pyd/dll`
2. Extension placed in `python/src/cif_parser/`
3. Wheel packages everything from `python/src/`
4. No duplicate detection issues

**Development Workflow:**
```bash
cd python
maturin develop          # Editable install, creates .so in src/
pytest tests/            # Run tests
maturin build --release  # Create wheel in target/wheels/
```

### 3. JavaScript Nested Builds

**Configuration:**
```bash
wasm-pack build --target nodejs --out-dir javascript/pkg-node
wasm-pack build --target web --out-dir javascript/pkg
wasm-pack build --target bundler --out-dir javascript/pkg-bundler
```

**Why Nested Layout:**
- Consistent with Python's nested structure (`python/src/`)
- Clear organization in monorepo: each language has its own directory
- Scales better when adding more targets
- Isolates build artifacts from root-level project files
- Already covered by `.gitignore` patterns

**Build Process:**
1. wasm-pack compiles Rust to WebAssembly
2. Generates bindings in `javascript/pkg-node/`, `javascript/pkg/`, etc.
3. Each target has its own package structure
4. JavaScript tests import from `./pkg-node` (same directory)

**Development Workflow:**
```bash
just wasm-build          # Build for Node.js
just wasm-build-web      # Build for web
just wasm-build-all      # Build all targets
cd javascript && npm test
```

## Build System Details

### Justfile Recipes

**Python:**
```bash
just python-fmt          # Format with black
just python-lint         # Lint with ruff
just python-typecheck    # Type check with mypy
just python-develop      # Editable install
just python-test         # Run tests
just python-clean        # Clean build artifacts
just python-build        # Build wheel
just check-python        # Run all checks
```

**JavaScript:**
```bash
just wasm-build          # Build WASM (Node.js)
just wasm-build-web      # Build WASM (web)
just wasm-build-bundler  # Build WASM (bundler)
just wasm-build-all      # Build all WASM targets
just js-fmt              # Format with Biome
just js-lint             # Lint with Biome
just js-test             # Run tests
just check-js            # Run all checks
```

**Rust:**
```bash
just rust-fmt            # Format with rustfmt
just rust-clippy         # Lint with clippy
just rust-test           # Run tests
just rust-build          # Build release
just check-rust          # Run all checks
```

**Aggregate:**
```bash
just ci                  # Run all CI checks
just build-all           # Build all targets
```

### Cleanup Strategy

**Python:**
```bash
python-clean:
    # Remove compiled extensions from src layout
    rm python/src/cif_parser/*.{so,pyd,dll}
    # Remove build directories
    rm -rf target/maturin python/dist python/build
```

**JavaScript:**
- No explicit cleanup needed
- Rebuild overwrites `pkg-node/`, `pkg/`, etc.
- All are gitignored

**Rust:**
```bash
cargo clean              # Standard Rust cleanup
```

## CI/CD Considerations

### GitHub Actions Matrix

**Python:**
- Build on: `ubuntu-latest`, `macos-latest`, `windows-latest`
- Python versions: `3.8`, `3.9`, `3.10`, `3.11`, `3.12`
- Always clean before build to prevent stale artifacts
- Src layout prevents duplicate file errors on Windows

**JavaScript:**
- Single WASM build (platform-independent)
- Test on Node.js LTS versions
- Root-level pkg directories ensure consistent paths

### Common CI Issues (Solved)

**Issue 1: "File was already added" on Windows**
- **Cause:** Mixed layout with compiled extensions in source tree
- **Solution:** Src layout separates source from artifacts

**Issue 2: Build artifacts tracked by git**
- **Cause:** Incorrect `.gitignore` patterns
- **Solution:** Use proper nested patterns like `/javascript/pkg-node/`

**Issue 3: Stale artifacts between builds**
- **Cause:** Previous builds leaving files in source tree
- **Solution:** `python-clean` recipe + src layout

## Maturin Configuration

### Key Settings

```toml
[tool.maturin]
features = ["pyo3/extension-module", "python"]
python-source = "src"
module-name = "cif_parser._cif_parser"
manifest-path = "../Cargo.toml"
```

**`python-source`:**
- Points to directory containing Python package
- Relative to `pyproject.toml` location
- `"src"` means look in `python/src/`

**`module-name`:**
- Full import path for the extension
- Format: `package.submodule`
- `cif_parser._cif_parser` → importable as `from cif_parser import _cif_parser`
- Convention: prefix with `_` to indicate C extension

**`manifest-path`:**
- Location of root `Cargo.toml`
- Allows building from subdirectory (`python/`)

### Excluded Patterns

Not needed with src layout, but for reference:
```toml
exclude = ["**/*.so", "**/*.pyd", "**/*.dll"]
```

This would exclude compiled extensions, but src layout naturally handles this.

## wasm-pack Configuration

### Build Targets

**`--target nodejs`:**
- Generates Node.js-compatible module
- Uses `require()` syntax
- Output: `javascript/pkg-node/`

**`--target web`:**
- Generates ES module for web
- Includes inline base64 WASM
- Output: `javascript/pkg/`

**`--target bundler`:**
- Generates ES module for bundlers (webpack, rollup, vite)
- Separate `.wasm` file
- Output: `javascript/pkg-bundler/`

### Output Structure

Each pkg directory contains:
```
javascript/pkg-node/
├── cif_parser.js           # JS bindings
├── cif_parser.d.ts         # TypeScript types
├── cif_parser_bg.wasm      # WASM binary
├── cif_parser_bg.wasm.d.ts # WASM types
├── package.json            # npm package
└── README.md               # Package docs
```

## Git Ignore Patterns

### Root `.gitignore`

```gitignore
# Rust build artifacts
/target/

# WASM generated packages (nested builds)
/javascript/pkg/
/javascript/pkg-node/
/javascript/pkg-bundler/
/javascript/pkg-*/

# Python generated packages
/dist/
/build/
*.egg-info/

# Compiled extensions (globally)
*.so
*.pyd
*.dll
```

**Note:** Global patterns (`*.so`, `*.pyd`, `*.dll`) ensure compiled extensions are never tracked, regardless of location.

## Best Practices

### For Developers

1. **Always use `just` commands** instead of direct tool invocation
2. **Run `just python-clean` if builds fail** with duplicate errors
3. **Never commit build artifacts** (pkg/, target/, *.so, etc.)
4. **Use virtual environments** (`uv` handles this automatically)

### For CI/CD

1. **Start with clean checkout** (GitHub Actions does this)
2. **Explicitly clean before build** (`python-clean` recipe)
3. **Use matrix builds** for multi-platform testing
4. **Cache Rust build artifacts** (`target/` directory)
5. **Don't cache Python/WASM artifacts** (language-specific)

### For Contributors

1. **Follow src layout convention** for new language bindings
2. **Update justfile** when adding new build commands
3. **Document build changes** in this file
4. **Test on all platforms** before PR (use CI)

## Migration Notes

### From Mixed to Src Layout (Python)

If you have existing code using mixed layout:

```bash
# 1. Create src directory
cd python
mkdir -p src

# 2. Move package
mv cif_parser src/

# 3. Update pyproject.toml
# Change: python-source = "." → python-source = "src"

# 4. Clean old artifacts
find . -name "*.so" -delete
find . -name "*.pyd" -delete
find . -name "*.dll" -delete

# 5. Rebuild
maturin develop
pytest tests/
```

### From Root-Level to Nested (JavaScript)

If you have root-level pkg builds:

```bash
# 1. Remove root-level builds
rm -rf pkg-node pkg pkg-bundler

# 2. Update build commands to use nested --out-dir
# Change: --out-dir pkg-node → --out-dir javascript/pkg-node

# 3. Update import paths in tests/examples
# Change: require('../pkg-node') → require('./pkg-node')

# 4. Update .gitignore patterns
# Change: /pkg-node/ → /javascript/pkg-node/

# 5. Rebuild
wasm-pack build --target nodejs --out-dir javascript/pkg-node
```

## Troubleshooting

### Python: "File was already added" Error

**Symptoms:**
```
File cif_parser\_cif_parser.cp311-win_amd64.pyd was already added from
python\cif_parser\_cif_parser.cp311-win_amd64.pyd, can't added it from
target\maturin\cif_parser.dll
```

**Cause:** Mixed layout with stale artifacts

**Fix:**
1. Ensure `python-source = "src"` in `pyproject.toml`
2. Ensure package is in `python/src/cif_parser/`
3. Run `just python-clean`
4. Rebuild with `just python-build`

### Python: Import Error After Src Layout

**Symptoms:**
```python
ImportError: No module named 'cif_parser'
```

**Cause:** Stale installation from mixed layout

**Fix:**
```bash
cd python
pip uninstall cif-parser -y
maturin develop
```

### JavaScript: WASM Not Found

**Symptoms:**
```
Error: Cannot find module './pkg-node'
```

**Cause:** Build output in wrong location

**Fix:**
1. Check `wasm-pack` command uses `--out-dir javascript/pkg-node` (not root-level `pkg-node`)
2. Rebuild: `just wasm-build`
3. Verify `javascript/pkg-node/` exists in the javascript directory

### General: Build Artifacts Tracked by Git

**Symptoms:**
```bash
git status
# Shows: javascript/pkg-node/, *.so files, etc.
```

**Fix:**
```bash
# Verify .gitignore patterns
cat .gitignore

# Force remove if needed
git rm -r --cached javascript/pkg-node
git rm -r --cached "*.so"
git commit -m "Remove build artifacts"
```

## References

- [Maturin Documentation](https://www.maturin.rs/)
- [PyO3 User Guide](https://pyo3.rs/)
- [wasm-pack Documentation](https://rustwasm.github.io/docs/wasm-pack/)
- [Just Manual](https://just.systems/)
- [Python Packaging Guide](https://packaging.python.org/)
- [Rust Book](https://doc.rust-lang.org/book/)
