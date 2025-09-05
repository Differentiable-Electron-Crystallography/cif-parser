#!/usr/bin/env python3
"""Python example using the CIF parser."""

import sys
import os

# Add the built package to the path
sys.path.insert(0, 'target/wheels')

try:
    import cif_parser
except ImportError:
    print("CIF parser not installed. Run: maturin develop --features python")
    sys.exit(1)

def main():
    print("CIF Parser Python Example")
    print("=" * 30)
    print(f"Version: {cif_parser.__version__}")
    print()

    # Example CIF content
    cif_content = """
    data_example
    _cell_length_a 10.000
    _cell_length_b 20.000
    _cell_length_c 30.000
    _cell_angle_alpha 90.0
    _cell_angle_beta 90.0
    _cell_angle_gamma 90.0
    _author_name 'John Doe'
    _title 'Example Crystal Structure'
    
    loop_
    _atom_site_label
    _atom_site_type_symbol
    _atom_site_fract_x
    _atom_site_fract_y
    _atom_site_fract_z
    C1 C 0.1234 0.5678 0.9012
    N1 N 0.2345 0.6789 0.0123
    O1 O 0.3456 0.7890 0.1234
    
    save_frame1
    _frame_item1 'Frame data 1'
    _frame_item2 42.0
    save_
    """

    try:
        print("Parsing CIF content...")
        doc = cif_parser.parse(cif_content)
        
        print(f"✅ Successfully parsed {len(doc)} blocks")
        print(f"   Block names: {doc.block_names}")
        print()
        
        # Access the first block
        block = doc.first_block()
        if block:
            print(f"📦 Block '{block.name}':")
            print(f"   - Items: {len(block.item_keys)}")
            print(f"   - Loops: {block.num_loops}")
            print(f"   - Frames: {block.num_frames}")
            print()
            
            # Show some data items
            print("📋 Data Items:")
            items_to_show = ['_cell_length_a', '_cell_length_b', '_title', '_author_name']
            for key in items_to_show:
                value = block.get_item(key)
                if value:
                    if value.is_text:
                        print(f"   {key}: '{value.text}' (text)")
                    elif value.is_numeric:
                        print(f"   {key}: {value.numeric} (numeric)")
            print()
            
            # Show loop data
            if block.num_loops > 0:
                loop = block.get_loop(0)
                print(f"🔄 First Loop:")
                print(f"   Tags: {loop.tags}")
                print(f"   Rows: {len(loop)}")
                print()
                
                print("   Sample data:")
                for i in range(min(3, len(loop))):
                    row_dict = loop.get_row_dict(i)
                    if row_dict:
                        label = row_dict.get('_atom_site_label')
                        atom_type = row_dict.get('_atom_site_type_symbol') 
                        x = row_dict.get('_atom_site_fract_x')
                        if label and atom_type and x:
                            print(f"   Row {i}: {label.text} ({atom_type.text}) at x={x.numeric}")
                print()
            
            # Show save frame
            if block.num_frames > 0:
                frame = block.get_frame(0)
                print(f"💾 Save Frame '{frame.name}':")
                print(f"   Items: {frame.item_keys}")
                
                for key in frame.item_keys:
                    value = frame.get_item(key)
                    if value:
                        if value.is_text:
                            print(f"   {key}: '{value.text}'")
                        elif value.is_numeric:
                            print(f"   {key}: {value.numeric}")
                print()
            
            # Demonstrate Python integration
            print("🐍 Python Integration:")
            
            # Dictionary-style access
            print(f"   Block by name: {doc['example'].name}")
            print(f"   Block by index: {doc[0].name}")
            
            # Iteration
            print("   All blocks:")
            for i, blk in enumerate(doc):
                print(f"     {i}: {blk.name}")
            
            # List comprehensions
            numeric_items = [
                (key, value.numeric) 
                for key in block.item_keys 
                if (value := block.get_item(key)) and value.is_numeric
            ]
            print(f"   Numeric items: {numeric_items[:3]}...")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())