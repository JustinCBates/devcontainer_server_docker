#!/usr/bin/env python3
"""
Simple Debug Test Script
Tests that VS Code debugging is working correctly
"""

def main():
    """Simple main function for testing debugging"""
    print("🧪 Debug Test Started")
    
    # Test variables for inspection
    test_string = "Hello VS Code!"
    test_number = 42
    test_list = [1, 2, 3, 4, 5]
    test_dict = {"name": "VPS Environment", "type": "Testing"}
    
    print(f"String: {test_string}")
    print(f"Number: {test_number}")
    print(f"List: {test_list}")
    print(f"Dict: {test_dict}")
    
    # Loop for step debugging
    print("\n🔄 Loop test:")
    for i in range(3):
        result = i * 2
        print(f"  {i} * 2 = {result}")
    
    # Function call test
    message = create_message("Debug", "Test")
    print(f"\n📝 Function result: {message}")
    
    print("\n✅ Debug Test Completed!")
    print("   Set breakpoints on any line and run with F5")

def create_message(prefix, suffix):
    """Simple function for testing step-into debugging"""
    return f"{prefix} - {suffix}"

if __name__ == "__main__":
    main()