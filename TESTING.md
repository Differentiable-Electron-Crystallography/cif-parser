# Testing Guide

This document describes the testing infrastructure and procedures for the CIF Parser library.

## Overview

The CIF Parser project uses a multi-tier testing approach:

- ✅ **Rust Tests**: Comprehensive test suite for core parsing functionality
- ⚠️ **Python Tests**: Basic import testing (expansion needed)
- ✅ **WASM Tests**: WebAssembly functionality testing
- ✅ **CI/CD Tests**: Automated testing via GitHub Actions

## Test Structure

```
tests/
├── fixtures/
│   └── simple.cif           # Test data files
├── grammar_test.rs          # Grammar parsing tests
├── integration_tests.rs     # End-to-end integration tests
└── blockname_test.rs        # Block name parsing tests

src/
├── lib.rs                   # Unit tests embedded in source
├── python.rs               # Python binding tests (limited)
└── wasm.rs                 # WASM binding tests (limited)
```

## Running Tests

### Rust Tests (Primary Test Suite)

The Rust test suite provides comprehensive coverage of the CIF parsing functionality:

```bash
# Run all tests
cargo test

# Run with verbose output
cargo test --verbose

# Run with all features (includes Python/WASM if available)
cargo test --all-features

# Run specific test file
cargo test --test integration_tests

# Run tests with output visible
cargo test -- --nocapture

# Run tests matching a pattern
cargo test parse_simple
```

**Test Categories:**
- **Unit tests**: Embedded in `src/lib.rs` and other source files
- **Integration tests**: End-to-end parsing scenarios in `tests/*.rs`
- **Grammar tests**: CIF syntax validation
- **Block parsing**: Data block structure handling

### Python Tests (Limited Coverage)

Currently, Python testing is minimal and focuses on basic functionality:

```bash
# First, build the Python bindings
maturin develop --features python

# Test basic import (current primary test)
python -c "import cif_parser; print('✅ Python bindings work!')"

# Placeholder for future pytest tests (no .py test files yet)
python -m pytest tests/
```

**Current State:**
- ✅ Import testing works
- ⚠️ No pytest test files exist yet
- 📝 **TODO**: Expand Python test suite

**Future Python Testing Plans:**
- Add `tests/test_python.py` with comprehensive tests
- Test all Python API functionality
- Integration tests with real CIF files
- Type hint validation tests

### WASM Tests

WebAssembly tests use the wasm-pack testing framework:

```bash
# Install wasm-pack first
curl https://rustwasm.github.io/wasm-pack/installer/init.sh -sSf | sh

# Test in headless browsers
wasm-pack test --headless --firefox
wasm-pack test --headless --chrome

# Test in Node.js environment
wasm-pack test --node

# Test with specific target
wasm-pack test --node --target nodejs
```

**Coverage:**
- ✅ Basic WASM module loading
- ✅ JavaScript API functionality
- ✅ Cross-platform compatibility

### Manual Testing Examples

**Test Rust library directly:**
```bash
cargo run --example basic_usage
cargo run --example mmcif_parser
cargo run --example advanced_features
```

**Test Python bindings:**
```bash
maturin develop --features python
python python_example.py
```

**Test WASM in browser:**
```bash
wasm-pack build --target web --out-dir pkg
python -m http.server 8000
# Open http://localhost:8000/wasm-demo.html
```

**Test WASM in Node.js:**
```bash
wasm-pack build --target nodejs --out-dir pkg-node
node node-example.js
```

## CI/CD Testing

GitHub Actions automatically run tests on:
- **Push to main branch**
- **Pull requests**
- **Release creation**

### Test Matrix

**Rust Tests:**
- Platforms: Ubuntu, macOS, Windows
- Rust versions: stable, beta
- Features: all combinations

**Python Tests:**
- Platforms: Ubuntu, macOS, Windows  
- Python versions: 3.8, 3.9, 3.10, 3.11, 3.12

**WASM Tests:**
- Build verification for web, nodejs, bundler targets
- Basic functionality testing

### Workflow Files

- `.github/workflows/test.yml` - Main testing workflow
- `.github/workflows/publish-*.yml` - Release testing

## Test Coverage

### ✅ Well Covered Areas

**Core Parsing:**
- CIF 1.1 syntax validation
- Data block parsing
- Loop structure handling
- Save frame processing  
- Value type detection (text, numeric, special)
- Error handling and reporting

**File Formats:**
- Standard CIF files
- mmCIF/PDBx files
- Multi-block files
- Complex nested structures

**API Functionality:**
- Document parsing
- Block access methods
- Loop data extraction
- Value type conversion

### ⚠️ Areas Needing More Coverage

**Python Bindings:**
- Comprehensive API testing
- Error handling in Python
- Type conversion edge cases
- Iterator functionality
- Python-specific features

**WASM Bindings:**
- Browser compatibility testing
- Memory management validation
- Performance testing
- JavaScript error handling

**Edge Cases:**
- Very large files
- Malformed CIF files
- Unicode content
- Performance benchmarks

## Adding New Tests

### Rust Tests

**Unit Tests** (in source files):
```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_new_feature() {
        // Test implementation
        assert_eq!(expected, actual);
    }
}
```

**Integration Tests** (in `tests/` directory):
```rust
// tests/new_feature_test.rs
use cif_parser::{Document, CifError};

#[test]
fn test_integration_scenario() {
    let content = "data_test\n_item value";
    let doc = Document::parse(content).unwrap();
    // Test implementation
}
```

### Python Tests (Future)

Create `tests/test_python.py`:
```python
import pytest
import cif_parser

def test_parse_simple():
    content = "data_test\n_item value"
    doc = cif_parser.parse(content)
    assert len(doc) == 1
    assert doc[0].name == "test"

def test_error_handling():
    with pytest.raises(ValueError):
        cif_parser.parse("invalid cif content")
```

### WASM Tests

Add to `src/wasm.rs`:
```rust
#[cfg(test)]
mod tests {
    use super::*;
    use wasm_bindgen_test::*;
    
    #[wasm_bindgen_test]
    fn test_wasm_feature() {
        let doc = JsCifDocument::parse("data_test\n_item value");
        assert_eq!(doc.get_block_count(), 1);
    }
}
```

## Test Data

### Fixtures

Test data files are stored in `tests/fixtures/`:
- `simple.cif` - Basic CIF structure for testing
- Add more fixtures as needed for specific test cases

### Creating Test Data

When adding new tests:
1. Use minimal, focused CIF content
2. Include edge cases (empty values, special characters)
3. Add both valid and invalid examples
4. Document the purpose of each fixture

## Troubleshooting Tests

### Common Issues

**Rust Test Failures:**
```bash
# Clean build artifacts
cargo clean

# Update dependencies
cargo update

# Check specific test with backtrace
RUST_BACKTRACE=1 cargo test failing_test_name
```

**Python Test Issues:**
```bash
# Rebuild Python bindings
maturin develop --features python --force

# Check Python can import
python -c "import cif_parser"

# Clear Python cache
find . -name "*.pyc" -delete
find . -name "__pycache__" -delete
```

**WASM Test Problems:**
```bash
# Ensure wasm target is installed
rustup target add wasm32-unknown-unknown

# Rebuild WASM
wasm-pack build --target web

# Check browser console for errors
```

### Environment Issues

**Missing Dependencies:**
- Rust: `rustup update`
- Python: `pip install maturin pytest`
- WASM: Install wasm-pack
- Node.js: Install Node.js 14+

**Platform-Specific:**
- Windows: Install Visual Studio Build Tools
- macOS: Install Xcode command line tools
- Linux: Install build-essential

## Performance Testing

### Benchmarks

Currently, performance testing is limited. Future improvements:

```bash
# Add benchmark tests (requires nightly Rust)
cargo bench

# Profile with perf (Linux)
perf record cargo test
perf report
```

### Memory Testing

```bash
# Check for memory leaks in tests
valgrind --tool=memcheck cargo test
```

## Continuous Integration

### Test Requirements

All tests must pass before merging:
- Rust tests on all platforms
- Python import tests
- WASM build verification
- Code formatting (`cargo fmt --check`)
- Linting (`cargo clippy`)

### Local Pre-commit Testing

```bash
# Run the same checks as CI
cargo fmt --check
cargo clippy --all-features -- -D warnings
cargo test --all-features
```

## Future Testing Improvements

### Short Term
1. **Expand Python test suite** - Add comprehensive pytest tests
2. **Add more CIF fixtures** - Cover edge cases and real-world files
3. **Memory leak testing** - Especially for Python/WASM bindings

### Long Term
1. **Performance benchmarks** - Track parsing speed over time
2. **Fuzz testing** - Automated discovery of edge cases
3. **Integration with real datasets** - Test with PDB/crystallography databases
4. **Property-based testing** - Generate random valid CIF structures

## Contributing Tests

When contributing:
1. Add tests for new features
2. Maintain or improve test coverage
3. Include both positive and negative test cases
4. Update this documentation for new testing procedures
5. Ensure tests pass in CI before submitting PR

## Resources

- [Rust Testing Guide](https://doc.rust-lang.org/book/ch11-00-testing.html)
- [PyO3 Testing](https://pyo3.rs/latest/testing.html)
- [wasm-bindgen Testing](https://rustwasm.github.io/wasm-bindgen/wasm-bindgen-test/index.html)
- [CIF 1.1 Specification](https://www.iucr.org/resources/cif/spec/version1.1/cifsyntax)