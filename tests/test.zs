// Test ZedScript file

// Variable declaration
var x = 10;
var y = 5;

// Math operation
var sum = x + y;
var product = x * y;

// Input from user
var name = input("Enter your name: ");

// Print outputs
Print("Hello " + name + "!");
Print("x + y = " + sum);
Print("x * y = " + product);

// Python block
py:
    z = sum + product
    Print("Sum + Product from Python block = " + str(z))
endpy
