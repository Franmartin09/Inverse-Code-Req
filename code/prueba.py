import math
# Function to calculate the area of a circle
def calculate_circle_area(radius):
    """Calculate the area of a circle given its radius."""
    return math.pi * (radius ** 2)

# Function to reverse a string
def reverse_string(input_string):
    """Reverse the given string."""
    return input_string[::-1]

# Function to check if a number is prime
def is_prime(number):
    """Check if a number is a prime number."""
    if number <= 1:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True

# Function to calculate the factorial of a number
def calculate_factorial(n):
    """Calculate the factorial of a number."""
    if n == 0:
        return 1
    return n * calculate_factorial(n - 1)

# Function to count vowels in a string
def count_vowels(input_string):
    """Count the number of vowels in a string."""
    vowels = "aeiouAEIOU"
    return sum(1 for char in input_string if char in vowels)
