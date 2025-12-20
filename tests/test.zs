print("ZedScript demo");
var counter = 0;
while counter < 3 {
    print("Counter is: {counter}")
    var counter = counter + 1
}

var score = 85
if score >= 90 {
    print("Grade: A")
} 
else {
    print("Grade: B")
}


var greeting = "Hello";
var name = input("Enter your name: ");
var message = greeting+" "+name;
print(message);

pylink(demo_python.py);
print("Value from Python: (x)");
var workingpath= os.getcwd();
print(workingpath);
print("Demo finished");
