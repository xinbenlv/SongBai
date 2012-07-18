package net.stumble.vzhou;


import android.os.Bundle;
import android.app.Activity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.support.v4.app.NavUtils;
import android.text.Editable;

public class MainActivity extends Activity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.activity_main, menu);
        return true;
    }

    public void setLabel(View view)
    {
    	EditText mEditText = (EditText) findViewById(R.id.editText);
    	TextView mTextView = (TextView) findViewById(R.id.textView);
    	String name = mEditText.getText().toString();
    	mTextView.setText("hello "+name);
    }

}
