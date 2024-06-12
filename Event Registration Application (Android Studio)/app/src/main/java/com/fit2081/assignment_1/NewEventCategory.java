package com.fit2081.assignment_1;

import android.Manifest;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Switch;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.lifecycle.ViewModelProvider;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Context;
import android.content.SharedPreferences;

import com.fit2081.assignment_1.provider.CategoryViewModel;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.lang.reflect.Type;
import java.util.ArrayList;
import com.google.gson.Gson;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;
import java.util.StringTokenizer;

public class NewEventCategory extends AppCompatActivity {

    EditText eventCategoryID, eventName, eventCount, categoryLocation;
    Switch eventIsActive;
//    CategoryBroadCastReceiver categoryBroadCastReceiver;

    private CategoryViewModel mCategoryViewModel;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_new_event_category);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        // Request permissions for SMS actions
        ActivityCompat.requestPermissions(this, new String[]{android.Manifest.permission.SEND_SMS, android.Manifest.permission.RECEIVE_SMS, Manifest.permission.READ_SMS}, 0);

//        // Register broadcast receiver to receive SMS
//        categoryBroadCastReceiver = new CategoryBroadCastReceiver();
//        registerReceiver(categoryBroadCastReceiver, new IntentFilter(SMSReceiver.SMS_FILTER), RECEIVER_EXPORTED);
////        registerReceiver(categoryBroadCastReceiver, new IntentFilter(SMSReceiver.SMS_FILTER2), RECEIVER_EXPORTED);

        eventCategoryID = findViewById(R.id.editTextAutoCompleteTextView);
        eventName = findViewById(R.id.editTextNameNewCategoryEventName);
        eventCount = findViewById(R.id.editTextNumberNewCategoryEventCount);
        eventIsActive = findViewById(R.id.switchIsActiveEventCategory);
        categoryLocation = findViewById(R.id.editTextNumberNewCategoryLocation);

//        ArrayList<String> db = new ArrayList<>();
//        adapter = new CategoryRecyclerAdapter();

        mCategoryViewModel = new ViewModelProvider(this).get(CategoryViewModel.class);
//        mCategoryViewModel.getmAllCategories().observe(this, newData -> {
//            adapter.setData(newData);
//            adapter.notifyDataSetChanged();
//        });

    }

//    @Override
//    protected void onPause() {
//        super.onPause();
//
//        // Unregister your receiver to stop it from running in the background
//        unregisterReceiver(categoryBroadCastReceiver);
//    }
//
//    @Override
//    protected void onResume() {
//        super.onResume();
//
//        // Unregister your receiver to stop it from running in the background
//        registerReceiver(categoryBroadCastReceiver, new IntentFilter(SMSReceiver.SMS_FILTER), RECEIVER_EXPORTED);
//    }


    public void onClickSave(View view){

        // define strings to get username and password
        String str_categoryName = "", str_eventCount = "", str_location="";
        boolean isEventActive;

        // get value of user name and password
        str_categoryName = eventName.getText().toString();
        str_eventCount = eventCount.getText().toString();
        isEventActive = eventIsActive.isChecked();
        str_location = categoryLocation.getText().toString();



        int numericCounter = 0;
        boolean checker = true;
        for (int i = 0; i < str_categoryName.length(); i++) {
            char c = str_categoryName.charAt(i);
            // to check if any values aside a-Z or 0-9 or " " exists
            if (!(c == ' ' || (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')|| (c >= '0' && c <= '9'))){
                checker = false;
                break;
            }
            // to check if all values are numeric only
            if ((c >= '0' && c <= '9')){
                numericCounter++;
            }
            // Process or print the character c
        }

        // Check if category name exists
        if(str_categoryName.length() != 0 && str_categoryName.trim().length() > 0){
            if ((checker != true || str_categoryName.trim().length() == numericCounter)){
                Toast.makeText(this, "Event Name must be alpha-numeric!", Toast.LENGTH_SHORT).show();
                return ;
            }
            // generate category Id
            String catID = generateCategoryId();


            // Set event count if provided
            if(str_eventCount.length() != 0){
                int int_eventCount = Integer.parseInt(str_eventCount);
                eventCategoryID.setText(catID);
                CategoryDetails categoryDetails = new CategoryDetails(catID, str_categoryName, int_eventCount, isEventActive, str_location);
//                CategoryDetails categoryDetails = new CategoryDetails(catID, str_categoryName, int_eventCount, isEventActive);

                mCategoryViewModel.insert(categoryDetails);
                Toast.makeText(this, "Category saved successfully: " + catID, Toast.LENGTH_SHORT).show();
                finish();

            }
            else{
                eventCategoryID.setText(catID);
                eventCount.setText("0");
                CategoryDetails categoryDetails = new CategoryDetails(catID, str_categoryName, 0, isEventActive, str_location);
//                CategoryDetails categoryDetails = new CategoryDetails(catID, str_categoryName, 0, isEventActive);

                mCategoryViewModel.insert(categoryDetails);
                Toast.makeText(getApplicationContext(), "Default Event Count set to 0", Toast.LENGTH_SHORT).show();

                // Show toast message indicating successful save
                Toast.makeText(this, "Category saved successfully: " + catID, Toast.LENGTH_SHORT).show();
                finish();

            }
        }
        else{
            // Show toast message indicating category name is required
            Toast.makeText(this, "Category Name is Required!", Toast.LENGTH_SHORT).show();
        }

    }

    // generate Category ID
    public String generateCategoryId(){

        String s = "";

        Random r = new Random();
        for (int i = 0; i < 4; i++){
            s += r.nextInt(10);
        }

        // since the letters are stored as the ord values in java, we find a random number between 0 to 25 and then add with the letter 'A' which will make the letter range between 'A' to 'Z'
        return "C" + (char) (r.nextInt(26) + 'A') + (char) (r.nextInt(26) + 'A') + "-" +  s;
    }





//    class CategoryBroadCastReceiver extends BroadcastReceiver {
//
//
//        @Override
//        public void onReceive(Context context, Intent intent) {
//
//            String msg = intent.getStringExtra(SMSReceiver.SMS_MSG_KEY);
//
//            // Check if the message starts with "category"
//            if (msg.length() >= 9 && (msg.substring(0,9)).equals("category:")){
//                // split the remaining message by ';'
//                String secondMessage = msg.substring(9);
//
//                int count = 0;
//                for (int i = 0; i < secondMessage.length(); i++) {
//                    if (secondMessage.charAt(i) == ';') {
//                        count++;
//                    }
//                }
//
//                if (count >= 3){
//                    Toast.makeText(getApplicationContext(), "There is more than two delimiter" , Toast.LENGTH_SHORT).show();
//                    return;
//                }
//                else if (count < 2){
//                    Toast.makeText(getApplicationContext(), "There is less than two delimiter" , Toast.LENGTH_SHORT).show();
//                    return;
//                }
//
////                    StringTokenizer sT = new StringTokenizer(secondMessage, ";");
//                String[] parts = secondMessage.split(";");
//
//                // Ensure the message format is correct (3 parameters)
//                if(parts.length == 3) {
//                    String SMSCategoryName = parts[0];
//                    String strEventCount = parts[1];
//                    String stringIsActive = (parts[2]).toLowerCase();
//
//                    // Check if the category name is not empty
//                    if (SMSCategoryName.trim().length() > 0) {
//                        // check if event counter is integer
//                        try {
//                            if (strEventCount.length() != 0) {
//                                int intEventCount = Integer.parseInt(strEventCount);
//                                if (intEventCount <= 0) {
//                                    Toast.makeText(getApplicationContext(), "Integer must be > 0", Toast.LENGTH_SHORT).show();
//                                    return;
//                                }
//                            }
//
//                            // Set UI elements based on the received data
//                            if (stringIsActive.equals("true")) {
//                                eventName.setText(SMSCategoryName);
//                                eventCount.setText(strEventCount);
//                                eventIsActive.setChecked(true);
//                            } else if (stringIsActive.equals(("false"))) {
//                                eventName.setText(SMSCategoryName);
//                                eventCount.setText(strEventCount);
//                                eventIsActive.setChecked(false);
//                            } else {
//                                Toast.makeText(getApplicationContext(), "isActive must be true / false!", Toast.LENGTH_SHORT).show();
//                            }
//                        } catch (Exception r) {
//                            Toast.makeText(getApplicationContext(), "Event Count must be an integer!", Toast.LENGTH_SHORT).show();
//
//                        }
//                    } else {
//                        Toast.makeText(getApplicationContext(), "Category Name must be a valid string!", Toast.LENGTH_SHORT).show();
//                    }
//                }
//                else if(parts.length == 2){
//                    String SMSCategoryName = parts[0];
//                    String strEventCount = parts[1];
//
//                    // Check if the category name is not empty
//                    if (SMSCategoryName.trim().length() > 0) {
//                        // check if event counter is integer
//                        try {
//                            if (strEventCount.length() != 0){
//                                int intEventCount = Integer.parseInt(strEventCount);
//                                if (intEventCount <= 0){
//                                    Toast.makeText(getApplicationContext(), "Integer must be > 0" , Toast.LENGTH_SHORT).show();
//                                    return;
//                                }
//                                else{
//                                    eventName.setText(SMSCategoryName);
//                                    eventCount.setText(strEventCount);
//                                    eventIsActive.setChecked(false);
//                                }
//                            }
//                            else{
//                                eventName.setText(SMSCategoryName);
//                                eventCount.setText("");
//                                eventIsActive.setChecked(false);
//                            }
//                        }
//                        catch (Exception r){
//                            Toast.makeText(getApplicationContext(), "Event Count must be an integer!", Toast.LENGTH_SHORT).show();
//                        }
//                    }
//                    else {
//                        Toast.makeText(getApplicationContext(), "Category Name must be a valid string!", Toast.LENGTH_SHORT).show();
//                    }
//                }
//                else if(parts.length == 1){
//                    String SMSCategoryName = parts[0];
//
//                    // Check if the category name is not empty
//                    if (SMSCategoryName.trim().length() > 0) {
//                        // check if event counter is integer
//                        eventName.setText(SMSCategoryName);
//                        eventCount.setText("");
//                        eventIsActive.setChecked(false);
//                    }
//                    else {
//                        Toast.makeText(getApplicationContext(), "Category Name must be a valid string!", Toast.LENGTH_SHORT).show();
//                    }
//                }
//                else{
//                    Toast.makeText(getApplicationContext(), "Wrong message format! Category Name is required!", Toast.LENGTH_SHORT).show();
//                }
//            }
//
//            else{
//                Toast.makeText(getApplicationContext(), "Wrong message format, must start with category:", Toast.LENGTH_SHORT).show();
//
//            }
//        }
//    }

}