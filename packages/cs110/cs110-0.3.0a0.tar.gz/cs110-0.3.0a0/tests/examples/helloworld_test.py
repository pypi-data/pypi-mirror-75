from cs110 import autograder

# ---------------------------------------------------------------------
# Hello World Unit Test
# ---------------------------------------------------------------------


# Runs the Python script and sees if it passes the test(s)
def test_passed():

    # Runs the Script
    output, error_message = autograder.run_script("helloworld.py", [])

    # Checks to See if the Program Passed the Test
    if output.strip() == "Hello World":
        print("SUCCESS!")
        return 100.0
    else:
        print("Try Again.  Just have it print the words 'Hello World'!")
        return 0.0


# Testbench (to be run in an IDE)
if __name__ == '__main__':
    result = test_passed()
    print("Unit Test Returned:", result)
