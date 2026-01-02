def get_non_empty_string(prompt):
    value = input(prompt).strip()
    if not value:
        raise ValueError("Input cannot be empty!")
    return value
    
def get_optional_string(prompt):
    return input(prompt).strip()

def get_int(prompt):
    value = input(prompt).strip()
    if not value.isdigit():
        raise ValueError("Please enter a valid number.")
    return int(value)