#!/usr/bin/env python3
"""
Test script to verify the Todo application functionality
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from storage import InMemoryStorage
from cli import CLI

def test_todo_app():
    print("Testing Todo Application...")
    
    # Initialize storage and CLI
    storage = InMemoryStorage()
    cli = CLI(storage)
    
    print("\n1. Testing ADD functionality:")
    cli.add("Buy groceries", "Milk, bread, eggs")
    cli.add("Write report", "Complete quarterly report")
    
    print("\n2. Testing VIEW functionality:")
    cli.view()
    
    print("\n3. Testing MARK functionality:")
    cli.mark(1)
    
    print("\n4. Testing VIEW after marking task complete:")
    cli.view()
    
    print("\n5. Testing UPDATE functionality:")
    cli.update(2, "Write quarterly report", "Complete Q4 2026 report")
    
    print("\n6. Testing VIEW after update:")
    cli.view()
    
    print("\n7. Testing DELETE functionality:")
    cli.delete(1)
    
    print("\n8. Testing VIEW after deletion:")
    cli.view()
    
    print("\n9. Testing error handling (deleting non-existent task):")
    cli.delete(999)
    
    print("\n10. Testing error handling (updating with empty title):")
    cli.add("", "This should fail")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_todo_app()