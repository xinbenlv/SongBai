#!/usr/bin/env python
import sys,os,shutil,time
SUCT_PATH = "/Users/vzhou/ws/suct/alpha"
ORIGINAL_PATH = "/Users/vzhou/ws/suct/kickoff/AndroidHelloWorld"
TARGET_PATH = "/tmp/AndroidHelloWorld"
TEST_PATH = "/tmp/AndroidHelloWorldTest"
PASS="dnfe3294n"
KEY_PATH = "/tmp/mykeystore"
KEY_ALIAS = "mykeystore"
KEY_CO = "CN=Zainan Victor Zhou, OU=Client, O=StumbleUpon.com, L=San Francisco, S=California, C=US"
ADK_PLATFORM_IMAGES_DIR="/Users/vzhou/android-sdks/platforms/android-10/images"
def write_file(filepath,content,flag="w"): # by default create, add a "b" to append
    f = open(filepath,flag)
    f.write(content)
    f.close()


def os_system(s):
    print "RUN SCRIPT  $ " ,s
    os.system(s)

def create_keystore():
    os_system("keytool -genkey -v -keystore %s -alias %s -keyalg RSA -keysize 2048 -validity 10000 -storepass %s -keypass %s -dname '%s' &" % (KEY_PATH,KEY_ALIAS,PASS,PASS,KEY_CO))
     
def build_and_sign():
    content = '''key.store=%s
key.alias=%s
key.store.password=%s
key.alias.password=%s
''' % (KEY_PATH,KEY_ALIAS,PASS,PASS)

    filepath = "%s/ant.properties" % TEST_PATH
    write_file(filepath,content,"a")
    filepath = "%s/ant.properties" % TARGET_PATH
    write_file(filepath,content,"a")
    

    os_system("cd %s && ant release" % TARGET_PATH) 
    os_system("cd %s && ant release" % TEST_PATH) 


# Generate target project
def create_target_project():
    shutil.copytree(ORIGINAL_PATH,TARGET_PATH)


# Gherkin Parser
# Object definition:
# Feature is a list of Scenario: feature  = [scenario1, scenario2,...]
# Scenario is a dictionary contains Scenario name, #TODO name format
#   Given: a list of set-up steps
#   When: a key step for state transition
#   Then: a list of assertions
# Future features: # TODO
# 1. Save state: you can define a state when then finished, and beused as a "When"
# 2. State transition verification


def gherkin_get_java_steps(s):
    ''' 
    gherkin_get_java_steps: given a string as input, find the steps of java
    '''
    predifined_steps = {
        "I see memory is sufficient": "solo.assertMemoryNotLow();",
        "I see current activity is MainActivity": 'solo.assertCurrentActivity("Expected MainActivit activity", "MainActivity");',

        "I press button":'solo.clickOnButton("Button");',
        "I see hello": '''
         boolean expected = true;
         boolean actual = solo.searchText("hello ");
         assertEquals("hello not found", expected, actual); 
         ''',
    }
    return predifined_steps[s]


def gherkin_parser():
    '''
    Generate An object from a Gherkin script
    ''' # TODO implement this
    parsed = [
        {"Scenario":"Launch",
          "Given":[],
          "When":[],
          "Then":["I see memory is sufficient","I see current activity is MainActivity"],
        },
#        {"Scenario":"Hello ",
#          "Given":[],
#          "When":["I press button"],
#          "Then":["I see hello"],
#        },
    ]
    return parsed


def gherkin_object_to_java(obj):
    
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
            code += gherkin_get_java_steps (g)
        for w in when:
            code += gherkin_get_java_steps (w)
        for t in then:
            code += gherkin_get_java_steps (t)
        code += "}"
        obj_to_java += code
    return obj_to_java
def generate_android_code():
    test_code = ""


    test_obj = gherkin_parser()
    test_code = gherkin_object_to_java(test_obj)

    code = '''package net.stumble.vzhou.test;
import net.stumble.vzhou.android.MainActivity;
import com.jayway.android.robotium.solo.Solo;
import android.test.ActivityInstrumentationTestCase2;
import android.test.suitebuilder.annotation.Smoke;

public class AndroidHelloWorldTest extends ActivityInstrumentationTestCase2<MainActivity>{
    public AndroidHelloWorldTest() {
        super("net.stumble.vzhou.android", MainActivity.class);
    }
    private Solo solo;
    public void setUp() throws Exception {
        solo = new Solo(getInstrumentation(), getActivity());
    }
    %s 
    @Override
    public void tearDown() throws Exception {
        //Robotium will finish all the activities that have been opened
        solo.finishOpenedActivities();
    }
}''' % test_code
    print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    print "Generated code"
    print code
    print "YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY"


    return code



# Generate test project
def create_test_project():
    
    # Create folders: <root>, res, src 
    os.mkdir(TEST_PATH)
    os.mkdir("%s/res" % TEST_PATH)
    os.mkdir("%s/src" % TEST_PATH)
    
    # File creation at <root>
    # Create AndroidManifest.xml
    filepath = "%s/AndroidManifest.xml" % TEST_PATH
    content = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="net.stumble.vzhou.test"
    android:versionCode="1"
    android:versionName="1.0" >
    <uses-sdk android:minSdkVersion="8" />
    <instrumentation
        android:name="android.test.InstrumentationTestRunner"
        android:targetPackage="net.stumble.vzhou.android" />
    <application
        android:icon="@drawable/ic_launcher"
        android:label="@string/app_name" >
        <uses-library android:name="android.test.runner" />
    </application>
</manifest>
'''
    write_file(filepath,content)
   
    # Create project.properties 
    filepath = "%s/project.properties" % TEST_PATH
    content = '''target=android-10
'''
    write_file(filepath,content)    
    # File creation at <root>/res
    os_system("cp -r %s/resource/res/* %s/res/" %(SUCT_PATH,TEST_PATH)) # TODO should use a for loop to copy all
    os.mkdir("%s/res/values" % TEST_PATH)
    filepath = "%s/res/values/strings.xml" % TEST_PATH
    content = '''<?xml version="1.0" encoding="utf-8"?>
<resources>

    <string name="app_name">AndroidHelloWorldTestTest</string>

</resources>'''
    write_file(filepath, content) 
    
    # File creation at <root>/src
    os_system("mkdir -p %s/src/net/net/stumble/vzhou/test" % TEST_PATH)
    filepath = "%s/src/net/net/stumble/vzhou/test/AndroidHelloWorldTest.java" % TEST_PATH
    content = generate_android_code()
    write_file(filepath, content)

    # Flile creation at <root>/libs
    shutil.copytree("%s/resource/libs" % SUCT_PATH, "%s/libs" % TEST_PATH)

def create_ant_profile():
    os_system("cd %s && android update project -p %s" % (TARGET_PATH,TARGET_PATH))    
    os_system("cd %s && android update test-project -m %s -p ." % (TEST_PATH,TARGET_PATH)) 

def lauch_emulator():
    #TODO create a avd 
    # os_system("cd %s && emulator -avd emulator-2 -no-skin -system system.img -kernel kernel-qemu -gpu off -qemu -initrd ramdisk.img &" % ADK_PLATFORM_IMAGES_DIR)
     
    os_system("cd ~/android-sdks/tools && emulator -no-boot-anim -ports 33917,38538 -prop persist.sys.language=en -prop persist.sys.country=US -avd e1 -no-snapshot-save -wipe-data -no-window &" )
    print "START SERVER"
    os_system("adb start-server")
    print "TRY TO CONNECT"
    while True:
        f= os.popen("adb connect localhost:38538")
        s = f.readline()
        if not ("unable" in s):
            break
        print "Reconnecting ..."
        time.sleep(0.5)
     
    print ("WAIT FOR DEVICE")
    os_system("adb wait-for-device")
    
    print ("CONNECTED")
    i = 0
    while True:
        f = os.popen("adb -s localhost:38538 shell getprop dev.bootcomplete")
        s = f.readline()
        if len(s)<=2:
            continue
        if s.split()[0] == "1":
            break
        time.sleep(0.5)
        print "Still booting %s" % i
        i+=1
    print ("DEVICE FULLY BOOTED")

    
def run_tests():

    os_system("cd %s && ant release install" % TARGET_PATH) 
    os_system("cd %s && ant release install" % TEST_PATH) 
    os_system("adb shell input keyevent 82")
    
    os_system("cd %s && ant test" % TEST_PATH)



def clean_up():
    f = os.popen("lsof -i tcp:38538")
    f.readline()
    s=f.readline() # second line
    pid = s.split()[1]
    os_system("kill %s" % pid)    
    s=f.readline() # second line
    pid = s.split()[1]
    os_system("kill %s" % pid)    


    os_system("rm -rf /tmp/AndroidHelloWorld* /tmp/mykeystore")

if __name__ == "__main__":

    print("Starting StumbleUpon Cross-platform Tester (suct) on TARGET %s" % TARGET_PATH)

    create_target_project()
    create_test_project()
    create_ant_profile()
    
    create_keystore()   
    build_and_sign()

    lauch_emulator()
    run_tests()
    clean_up()

    print ("Da-la! Suct!!!")

