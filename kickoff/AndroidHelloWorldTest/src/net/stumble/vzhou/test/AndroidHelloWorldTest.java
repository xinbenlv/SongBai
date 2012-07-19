package net.stumble.vzhou.test;
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
}
