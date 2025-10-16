from sympy import symbols, expand

x = symbols('x')

# Each kid's generating function
g1 = 1 + x
g2 = 1 + x + x**2
g3 = 1 + x + x**2 + x**3
g4 = 1 + x + x**2 + x**3 + x**4
g5 = 1 + x + x**2 + x**3 + x**4 + x**5

# Multiply them together
product = g1 * g2 * g3 * g4 * g5

# Expand the product
expanded = expand(product)

# Get coefficient of x^10
coeff = expanded.coeff(x, 7)

print(f"Number of ways to distribute 10 dollars: {coeff}")
