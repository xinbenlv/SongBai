suct: StumbleUpon Cross-platform Tester
is a cross-platform Behavior Driven Development (BDD) tool for iOS and Android

Created: 2012-07-17
Author: Zainan Victor Zhou, Jeff Sheldon

Dependencies:

    [Android support]
    Androdi Development Kit 
    Apache Ant: ava library and command-line tool http://ant.apache.org/
    Robotium: BDD for Android http://www.robotium.org
    JUnit: Unit Test library for Java http://www.junit.org/
    
    [iPhone/iPad support]
    Keep It Functional: BDD for iOS https://github.com/square/KIF/

Requirements
    
    P1 Gherkin Interpreter: converting Gherkin script in to Android JUnit code or iOS Ojbect-C UnitTesting code
        P1 Gherkin script to Python Gherkin object
            P1 Gherkin Given-When-Then support
            P1 Gherkin Multi-features, Multi-scenario support
            P2 Gherkin And-But support
            P2 Gherkin python style comment support
            P3 Gherkin irregular indent support
            P1 Gherkin auto parse parameters
                Example: 'Then I see text "hello world"' should be generating a method "I see text" and a parameter "hello world"
        P1 Python Gherkin object to Java converter
            P1 Gherkin user-defined step-to-code mapping
                Example: Gherkin "I see this action is true"
                    mapped to Java: "/*this is defined by suct suer:*/assertEquals("the action should be true", action, true); "
            P1 Gherkin predefined steps
            P1 Gherkin perdefined steps allowing parameters
        P1 Python Gherkin object to Object-C Converter
            P1 Gherkin user-defined step-to-code mapping
            P1 Gherkin predefined steps
            P1 Gherkin perdefined steps allowing parameters





    P1 Android support
        P1 Read Gherkin script and generate Robotium Code
        P1 Build and Sign target and test apk
        P2 Create Android Emulator profile
        P1 Launch Android Emulator and wait for its fully boot
        P1 Run the Robotium test
        P1 Turn off Android Emulator
        P2 Delete Android Emulator profile
    P1 Interpreter should handle apk (no-source-code) testing
    P1 Interpreter should handle source-code testing
        P1 Interpreter should handle the source 


    P1 iOS support
    P1 Ant Report
        P1 Log the raw console output for Android Emulator
        P1 Log the raw output from Android Emulator 
        P1 Report Ant UnitTest general result (scenario level)
        P2 Report Ant UnitTest detailed result (given-when-then support)
    
    P2 Ant code coverage report
    

