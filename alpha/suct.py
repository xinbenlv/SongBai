#!/usr/bin/env python
import sys,os,shutil
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




def create_keystore():
    os.system("keytool -genkey -v -keystore %s -alias %s -keyalg RSA -keysize 2048 -validity 10000 -storepass %s -keypass %s -dname '%s' &" % (KEY_PATH,KEY_ALIAS,PASS,PASS,KEY_CO))
     
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
    

    os.system("cd %s && ant release" % TARGET_PATH) 
    os.system("cd %s && ant release" % TEST_PATH) 
# Generate target project
def create_target_project():
    shutil.copytree(ORIGINAL_PATH,TARGET_PATH)

    

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
    os.system("cp -r %s/resource/res/* %s/res/" %(SUCT_PATH,TEST_PATH)) # TODO should use a for loop to copy all
    os.mkdir("%s/res/values" % TEST_PATH)
    filepath = "%s/res/values/strings.xml" % TEST_PATH
    content = '''<?xml version="1.0" encoding="utf-8"?>
<resources>

    <string name="app_name">AndroidHelloWorldTestTest</string>

</resources>'''
    write_file(filepath, content) 
    
    # File creation at <root>/src
    os.system("mkdir -p %s/src/net/net/stumble/vzhou/test" % TEST_PATH)
    filepath = "%s/src/net/net/stumble/vzhou/test/AndroidHelloWorldTest.java" % TEST_PATH
    content = '''package net.stumble.vzhou.test;
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
    @Smoke
    public void testLaunch() throws Exception {
        solo.assertCurrentActivity("Expected MainActivit activity", "MainActivity");
        solo.assertMemoryNotLow();
    }
    @Smoke
    public void testHello() throws Exception {
        solo.clickOnButton("Button");
        boolean expected = true;
        boolean actual = solo.searchText("hello ");
        assertEquals("hello not found", expected, actual); 
    }
    @Override
    public void tearDown() throws Exception {
        //Robotium will finish all the activities that have been opened
        solo.finishOpenedActivities();
    }
}'''
    write_file(filepath, content)

    # Flile creation at <root>/libs
    shutil.copytree("%s/resource/libs" % SUCT_PATH, "%s/libs" % TEST_PATH)

def create_ant_profile():
    os.system("cd %s && android update project -p %s" % (TARGET_PATH,TARGET_PATH))    
    os.system("cd %s && android update test-project -m %s -p ." % (TEST_PATH,TARGET_PATH)) 

def lauch_emulator():
    #TODO create a avd 
    os.system("cd %s && emulator -avd emulator-2 -no-skin -system system.img -kernel kernel-qemu -gpu off -qemu -initrd ramdisk.img &" % ADK_PLATFORM_IMAGES_DIR)
    os.system("adb wait-for-device")
def run_tests():
    os.system("adb shell input keyevent 82")
    os.system("cd %s && ant test" % TEST_PATH)
if __name__ == "__main__":

    print("Starting StumbleUpon Cross-platform Tester (suct) on TARGET %s" % TARGET_PATH)

    create_target_project()
    create_test_project()
    create_ant_profile()
    
    create_keystore()   
    build_and_sign()

    lauch_emulator()
    run_tests()



