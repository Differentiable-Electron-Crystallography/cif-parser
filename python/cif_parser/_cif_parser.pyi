"""Type stubs for the native CIF parser module."""

from typing import Dict, List, Optional, Union, Iterator, Any, overload

__version__: str
__author__: str
__doc__: str

class Value:
    """A CIF value with automatic type detection."""
    
    @property
    def is_text(self) -> bool:
        """True if this is a text value."""
        ...
    
    @property
    def is_numeric(self) -> bool:
        """True if this is a numeric value."""
        ...
    
    @property
    def is_unknown(self) -> bool:
        """True if this is an unknown value (?)."""
        ...
    
    @property
    def is_not_applicable(self) -> bool:
        """True if this is a not-applicable value (.)."""
        ...
    
    @property
    def text(self) -> Optional[str]:
        """Get text content (None if not a text value)."""
        ...
    
    @property
    def numeric(self) -> Optional[float]:
        """Get numeric content (None if not numeric)."""
        ...
    
    @property
    def value_type(self) -> str:
        """Get the value type as a string."""
        ...
    
    def to_python(self) -> Union[str, float, None]:
        """Convert to native Python type."""
        ...
    
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...

class Loop:
    """A CIF loop structure (tabular data)."""
    
    @property
    def tags(self) -> List[str]:
        """Get column tags (headers)."""
        ...
    
    @property
    def num_columns(self) -> int:
        """Get the number of columns."""
        ...
    
    def __len__(self) -> int:
        """Get the number of rows."""
        ...
    
    def is_empty(self) -> bool:
        """Check if the loop has no rows."""
        ...
    
    def get(self, row: int, col: int) -> Optional[Value]:
        """Get a value by row and column index."""
        ...
    
    def get_by_tag(self, row: int, tag: str) -> Optional[Value]:
        """Get a value by row index and tag name."""
        ...
    
    def get_column(self, tag: str) -> Optional[List[Value]]:
        """Get all values for a specific tag."""
        ...
    
    def rows(self) -> List[List[Value]]:
        """Get all rows as lists of values."""
        ...
    
    def get_row_dict(self, row: int) -> Optional[Dict[str, Value]]:
        """Get a row as a dictionary mapping tags to values."""
        ...
    
    def __iter__(self) -> Iterator[List[Value]]:
        """Iterate over rows."""
        ...
    
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

class Frame:
    """A CIF save frame."""
    
    @property
    def name(self) -> str:
        """Get the frame name."""
        ...
    
    @property
    def item_keys(self) -> List[str]:
        """Get all item keys."""
        ...
    
    @property
    def num_loops(self) -> int:
        """Get the number of loops."""
        ...
    
    @property
    def loops(self) -> List[Loop]:
        """Get all loops."""
        ...
    
    def get_item(self, key: str) -> Optional[Value]:
        """Get an item by key."""
        ...
    
    def items(self) -> Dict[str, Value]:
        """Get all items as a dictionary."""
        ...
    
    def get_loop(self, index: int) -> Optional[Loop]:
        """Get a loop by index."""
        ...
    
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

class Block:
    """A CIF data block."""
    
    @property
    def name(self) -> str:
        """Get the block name."""
        ...
    
    @property
    def item_keys(self) -> List[str]:
        """Get all item keys."""
        ...
    
    @property
    def num_loops(self) -> int:
        """Get the number of loops."""
        ...
    
    @property
    def loops(self) -> List[Loop]:
        """Get all loops."""
        ...
    
    @property
    def num_frames(self) -> int:
        """Get the number of frames."""
        ...
    
    @property
    def frames(self) -> List[Frame]:
        """Get all frames."""
        ...
    
    def get_item(self, key: str) -> Optional[Value]:
        """Get an item by key."""
        ...
    
    def items(self) -> Dict[str, Value]:
        """Get all items as a dictionary."""
        ...
    
    def get_loop(self, index: int) -> Optional[Loop]:
        """Get a loop by index."""
        ...
    
    def find_loop(self, tag: str) -> Optional[Loop]:
        """Find a loop containing a specific tag."""
        ...
    
    def get_loop_tags(self) -> List[str]:
        """Get all loop tags."""
        ...
    
    def get_frame(self, index: int) -> Optional[Frame]:
        """Get a frame by index."""
        ...
    
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

class Document:
    """A CIF document containing one or more data blocks."""
    
    @staticmethod
    def parse(content: str) -> Document:
        """Parse CIF content from a string."""
        ...
    
    @staticmethod  
    def from_file(path: str) -> Document:
        """Parse CIF content from a file."""
        ...
    
    @property
    def blocks(self) -> List[Block]:
        """Get all blocks."""
        ...
    
    @property
    def block_names(self) -> List[str]:
        """Get all block names."""
        ...
    
    def __len__(self) -> int:
        """Get the number of blocks."""
        ...
    
    def get_block(self, index: int) -> Optional[Block]:
        """Get a block by index."""
        ...
    
    def get_block_by_name(self, name: str) -> Optional[Block]:
        """Get a block by name."""
        ...
    
    def first_block(self) -> Optional[Block]:
        """Get the first block."""
        ...
    
    @overload
    def __getitem__(self, key: int) -> Block: ...
    @overload
    def __getitem__(self, key: str) -> Block: ...
    def __getitem__(self, key: Union[int, str]) -> Block:
        """Get a block by index or name."""
        ...
    
    def __iter__(self) -> Iterator[Block]:
        """Iterate over blocks."""
        ...
    
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

def parse(content: str) -> Document:
    """Parse CIF content from a string."""
    ...

def parse_file(path: str) -> Document:
    """Parse CIF content from a file."""
    ...