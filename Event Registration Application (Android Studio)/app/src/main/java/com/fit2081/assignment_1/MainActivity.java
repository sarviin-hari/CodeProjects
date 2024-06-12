package com.fit2081.assignment_1;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class MainActivity extends AppCompatActivity {

    EditText username, password, confirmPassword;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        username = findViewById(R.id.editTextUsername);
        password = findViewById(R.id.editTextPassword);
        confirmPassword = findViewById(R.id.editTextConfirmPassword);
    }

    public void onSignUpClick(View view){

        // define strings to get username and password
        String str_username = "", str_password = "", str_confirmPassword = "";

        // get value of user name and password
        str_username = username.getText().toString();
        str_password = password.getText().toString();
        str_confirmPassword = confirmPassword.getText().toString();

        if(str_username.trim().length() == 0 || str_password.trim().length() == 0 ){
            Toast.makeText(getApplicationContext(), "Username and Password must be alphanumeric!", Toast.LENGTH_SHORT).show();
            return; // return the control and do not proceed further
        }


            // validate username & password and show toast if empty
        if (str_username.isEmpty() || str_password.isEmpty() || str_confirmPassword.isEmpty()) {
            Toast.makeText(getApplicationContext(), "Username and Password is required!", Toast.LENGTH_SHORT).show();
            return; // return the control and do not proceed further
        }


        if (!str_password.equals(str_confirmPassword)) {
            Toast.makeText(getApplicationContext(), "Passwords do not match!", Toast.LENGTH_SHORT).show();
            return; // return the control and do not proceed further
        }

        Log.d("about_to_login user", str_username);
        Log.d("about_to_login pass", str_password);
        Log.d("about_to_login cPass", str_confirmPassword);

        // call save the new JAVA method to save data to persistent storage
        saveDataToSharedPreference(str_username, str_password);

        Intent intent = new Intent(this, Login.class);
        startActivity(intent);

        Toast.makeText(getApplicationContext(), "Signing Successfully!", Toast.LENGTH_SHORT).show();

    }

    private void saveDataToSharedPreference(String usernameValue, String passwordValue){
        // initialise shared preference class variable to access Android's persistent storage
        SharedPreferences sharedPreferences = getSharedPreferences(KeyStore.FILE_NAME, MODE_PRIVATE);

        // use .edit function to access file using Editor variable
        SharedPreferences.Editor editor = sharedPreferences.edit();

        // save key-value pairs to the shared preference file
        editor.putString(KeyStore.KEY_USERNAME, usernameValue);
        editor.putString(KeyStore.KEY_PASSWORD, passwordValue);

        // use editor.apply() to save data to the file asynchronously (in background without freezing the UI)
        // doing in background is very common practice for any File Input/Output operations
        editor.apply();
    }

    // Handle click on the "Login" button
    public void onMoveLoginClick(View view){
        // Create an intent to start the Login activity
        Intent intent = new Intent(this, Login.class);
        // Start the Login activity
        startActivity(intent);

    }


}