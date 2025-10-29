// ZedScript variables
var user_name = input("Enter your name: ");

// Print basic outputs
print("Hello " + user_name + "!");

// Python generates values
py:
    base = 7
    factor = 4
    multiplied = base * factor
    bonus = 10
    total = multiplied + bonus
    average = total / 2
endpy

// Use Python-generated values in ZedScript
var multiplied_from_python = multiplied;
var total_from_python = total;
var average_from_python = average;

// Print outputs in ZedScript
print("Multiplied (from Python) = " + str(multiplied_from_python));
print("Total (from Python) = " + str(total_from_python));
print("Average (from Python) = " + str(average_from_python));

// Further math in ZedScript using Python values
var doubled_total = total_from_python * 2;
print("Doubled Total = " + str(doubled_total));
