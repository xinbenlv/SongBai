#!/usr/bin/env python


import sys,os,shutil,time
from xml.dom.minidom import parseString



import logging
logger = logging.getLogger("suct")
hdlr = logging.FileHandler('/tmp/suct.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)


SUCT_PATH = os.path.realpath(os.path.dirname(__file__))

ORIGIN_PATH = ""
TEMP_PATH = "/tmp/"
TARGET_PATH = os.path.join(TEMP_PATH,"suct_target")
TEST_PATH = os.path.join(TEMP_PATH,"suct_test")
PASS="dnfe3294n"
KEY_PATH = "/tmp/suct_keystore"
KEY_ALIAS = "suct_keystore"
KEY_CO = "CN=Suct User, OU=Client, O=StumbleUpon.com, L=San Francisco, S=California, C=US"
ADK_PATH = "/Users/vzhou/android-sdks"
ADK_PLATFORM_IMAGES_DIR=os.path.join(ADK_PATH,"platforms/android-10/images")

GHERKIN_SCRIPT = ""
TARGET_PACKAGE = ""
TARGET_ACTIVITY =""

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
def read_from_target_project():
    global TARGET_PACKAGE, TARGET_ACTIVITY
    shutil.copytree(ORIGIN_PATH,TARGET_PATH)
    manifest_target = os.path.join(TARGET_PATH,"AndroidManifest.xml")
    file = open(manifest_target,"r")   
     
    data = file.read()
    file.close()
    dom = parseString(data)
    
    xmlTag = dom.getElementsByTagName("manifest")[0]
    TARGET_PACKAGE = xmlTag.getAttribute("package")


    childChildOfMainActivity = None
    for xmlTag in dom.getElementsByTagName("category"):
        if xmlTag.getAttribute("android:name") == "android.intent.category.LAUNCHER":
            childChildOfMainActivity = xmlTag
            break
        # Shall always find a MAIN ACTIVITY whose "indent-filter/category" is "android.indent.category.LAUNCHER"
    activity_android_name = childChildOfMainActivity.parentNode.parentNode.getAttribute("android:name") 
    TARGET_ACTIVITY = activity_android_name.split('.')[-1]
    print "TARGET_ACTIVITY",TARGET_ACTIVITY

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


def generate_android_code():

    import gherkin
    test_code = ""
    (feature,test_obj) = gherkin.parse(open(GHERKIN_SCRIPT,"r"))
    test_code = gherkin.obj_to_java(test_obj)
    
    code = '''package net.stumble.suct;
import %s.%s;
import com.jayway.android.robotium.solo.Solo;
import android.test.ActivityInstrumentationTestCase2;
import android.test.suitebuilder.annotation.Smoke;

public class SuctTest extends ActivityInstrumentationTestCase2<%s>{
    public SuctTest() {
        super("%s", %s.class);
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
}''' % (TARGET_PACKAGE,TARGET_ACTIVITY,TARGET_ACTIVITY,TARGET_PACKAGE,TARGET_ACTIVITY,test_code)
    print "=============================================="
    print "Generated code"
    print code
    print "=============================================="


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
    package="net.stumble.suct"
    android:versionCode="1"
    android:versionName="1.0" >
    <uses-sdk android:minSdkVersion="8" />
    <instrumentation
        android:name="android.test.InstrumentationTestRunner"
        android:targetPackage="%s" />
    <application
        android:icon="@drawable/ic_launcher"
        android:label="@string/app_name" >
        <uses-library android:name="android.test.runner" />
    </application>
</manifest>
'''  % TARGET_PACKAGE
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

    <string name="app_name">SuctTesting</string>

</resources>'''
    write_file(filepath, content) 
    
    # File creation at <root>/src
    os_system("mkdir -p %s/src/net/stumble/suct" % TEST_PATH)
    filepath = "%s/src/net/stumble/suct/SuctTest.java" % TEST_PATH
    content = generate_android_code()
    write_file(filepath, content)

    # Flile creation at <root>/libs
    shutil.copytree("%s/resource/libs" % SUCT_PATH, "%s/libs" % TEST_PATH)

def create_ant_profile():
    os_system("cd %s && android update project -p %s" % (TARGET_PATH,TARGET_PATH))    
    os_system("cd %s && android update test-project -m %s -p ." % (TEST_PATH,TARGET_PATH)) 

def lauch_emulator():
    # os_system("cd %s && emulator -avd emulator-2 -no-skin -system system.img -kernel kernel-qemu -gpu off -qemu -initrd ramdisk.img &" % ADK_PLATFORM_IMAGES_DIR)
     
    os_system("cd %s/tools && emulator -no-boot-anim -ports 33917,38538 -prop persist.sys.language=en -prop persist.sys.country=US -avd e1 -no-snapshot-save -wipe-data -no-window &" % ADK_PATH)
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
    os_system("adb shell input keyevent 82") # Unlock the screen
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


    os_system("rm -rf %s" % TARGET_PATH)
    os_system("rm -rf %s" % TEST_PATH)
    os_system("rm -rf %s" % KEY_PATH)

def parse_argument():
    global ORIGIN_PATH, TEMP_PATH, GHERKIN_SCRIPT
    import argparse
    parser = argparse.ArgumentParser(description="SUCT: StumbleUpon Cross-platform Tester.")
    parser.add_argument("origin", metavar="path", type=str,
                       help="path to original project to for suct testing.")
    parser.add_argument("gherkin", metavar="script", type=str, help="suct-gherkin script file.")
    parser.add_argument("--tmp", metavar="temp", type=str, help="temporary directory for created projects.", default = TEMP_PATH)    

    args = parser.parse_args()
    ORIGIN_PATH = args.origin
    GHERKIN_SCRIPT = args.gherkin
    TEMP_PATH = args.tmp

if __name__ == "__main__":
    parse_argument()
    clean_up()

    print("Starting testing on ORIGIN %s" % ORIGIN_PATH)

    read_from_target_project()
    
    create_test_project()
    create_ant_profile()
    
    create_keystore()   
    build_and_sign()

    lauch_emulator()
    run_tests()

    # clean_up()
    print ("Finished testing!")


