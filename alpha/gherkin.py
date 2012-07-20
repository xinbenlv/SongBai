#!/usr/bin/env python
# This is only a simple simple parser to convert a Gherkin script into Robotium/KIF  testing snippet


def gherkin_get_java_steps(s,arg):
    ''' 
    gherkin_get_java_steps: given a string as input, find the steps of java
    '''
    t1 = arg[0] if len(arg)>0 else ""
    predefined_steps = {
        "I press on the button":'solo.clickOnButton("%s");' % t1,
        "I should see the text": '''
         boolean expected = true;
         boolean actual = solo.searchText("%s");
         assertEquals("%s not found", expected, actual); 
         ''' % (t1,t1),
        "I should see memory is sufficient": "solo.assertMemoryNotLow();",
        "I should see current activity is": 'solo.assertCurrentActivity("Expected current activity to be %s ", "%s");'% (t1,t1),
    }
    # predefined steps:
    # Given and When:
    # * I enter some text
    # * I press button
    # Then
    # * I should see "some text"
    # * I should see memorry is sufficient
    

    return predefined_steps[s]


def get_indent_level(s):
    # note here we assume the su-gherkin is strictly intented with 4 spaces
    import re
    indent = re.match(r"\s*", s).group()
    return len(indent)


def parse(s):
    '''
    Generate An object from a Gherkin script
    ''' # TODO implement this
    parsed = [
        {"Scenario":"Launch",
          "Given":[],
          "When":[],
          "Then":[
              ["I should see memory is sufficient",[]],
              ["I should see current activity is",["MainActivity"]]
          ],
        },
        {"Scenario":"Hello",
          "Given":[],
          "When":[
            ["I press on the button",["Button"]]
            
          ],
          "Then":[
              ["I should see the text",["hello "]]
          ],
        },
    ]

    return parsed



def obj_to_java(obj):
    
    obj_to_java = ""
    for scenario in obj:
        scenario_name = scenario['Scenario']
        given = scenario['Given']
        when = scenario['When']
        then = scenario['Then']
        code = '''
    @Smoke
    public void test%s() throws Exception {
''' % scenario_name
        for g in given:
            code += gherkin_get_java_steps (g[0],g[1]) + "\n"
        for w in when:
            code += gherkin_get_java_steps (w[0],w[1]) + "\n"
        for t in then:
            code += gherkin_get_java_steps (t[0],t[1]) + "\n"
        code += "}\n"
        obj_to_java += code
    return obj_to_java


if __name__ == "__main__":
    obj = parse("")
    print obj_to_java(obj)
