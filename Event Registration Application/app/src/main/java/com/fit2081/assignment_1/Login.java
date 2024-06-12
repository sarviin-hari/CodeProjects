package com.fit2081.assignment_1;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class Login extends AppCompatActivity {

    EditText loginUsername, loginPassword;
    String usernameSP, passwordSP;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_login);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        loginUsername = findViewById(R.id.editTextLoginUsername);
        loginPassword = findViewById(R.id.editTextLoginPassword);

        restoreDataFromSharedPreference();
    }

//    @Override
//    public void onBackPressed() {
//        Intent intent = new Intent(this, MainActivity.class); // Replace SignUpActivity.class with your sign-up activity class
//        startActivity(intent);
////        finish();
//    }

    public void restoreDataFromSharedPreference(){
        // initialise shared preference class variable to access Android's persistent storage
        SharedPreferences sharedPreferences = getSharedPreferences(KeyStore.FILE_NAME, MODE_PRIVATE);

        // save key-value pairs to the shared preference file
        usernameSP = sharedPreferences.getString(KeyStore.KEY_USERNAME, "");
        passwordSP = sharedPreferences.getString(KeyStore.KEY_PASSWORD, "");

        // update the UI using retrieved values
        loginUsername.setText(usernameSP);
    }

    public void onRegisterClick(View view){
        Intent intent = new Intent(this, MainActivity.class);

        // finally launch the activity using startActivity method
        startActivity(intent);
    }


    public void onLoginClick(View view){

        // define strings to get username and password
        String str_username = "", str_password = "";

        // get value of user name and password
        str_username = loginUsername.getText().toString();
        str_password = loginPassword.getText().toString();

        // validate username & password and show toast if empty
        if (str_username.isEmpty() || str_password.isEmpty()) {
            Toast.makeText(getApplicationContext(), "Username and Password is required!", Toast.LENGTH_SHORT).show();
            return; // return the control and do not proceed further
        }

        Log.d("about_to_login user", str_username);
        Log.d("about_to_login pass", str_password);

        if (usernameSP.equals(str_username) && passwordSP.equals(str_password)) {
            Toast.makeText(getApplicationContext(), "Login Successfully!", Toast.LENGTH_SHORT).show();
            // successful login takes to next activity
            Intent intent_user_details = new Intent(getApplicationContext(), Dashboard.class);
            // start user activity using startActivity()
            startActivity(intent_user_details);

        } else {
            // invalid login, display toast message
            Toast.makeText(getApplicationContext(), "Authentication failure: Username or Password incorrect", Toast.LENGTH_SHORT).show();
        }

    }

    @Override
    public void onBackPressed(){
        super.onBackPressed();
        finish();
    }

//    public void

}