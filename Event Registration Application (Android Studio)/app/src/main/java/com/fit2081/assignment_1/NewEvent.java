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

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.Random;
import java.util.StringTokenizer;
import java.util.regex.Pattern;

public class NewEvent extends AppCompatActivity {
    EditText eventId, eventCategoryID, eventName, eventTicket;
    Switch eventIsActive;
    EventBroadCastReceiver eventBroadCastReceiver;
    FragmentListCategory fragmentListCategory = new FragmentListCategory();


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_new_event);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        // Request permissions for SMS actions (In java and XML)
        ActivityCompat.requestPermissions(this, new String[]{android.Manifest.permission.SEND_SMS, android.Manifest.permission.RECEIVE_SMS, Manifest.permission.READ_SMS}, 0);

        // Register broadcast receiver to receive SMS
        eventBroadCastReceiver = new EventBroadCastReceiver();
        registerReceiver(eventBroadCastReceiver, new IntentFilter(SMSReceiver.SMS_FILTER), RECEIVER_EXPORTED);

        // Store the attributes in teh
        eventId = findViewById(R.id.editTextAutoCompleteTextView22);
        eventCategoryID = findViewById(R.id.editTextEventFormEventCategory2);
        eventName = findViewById(R.id.editTextTextEventFormEventName2);
        eventTicket = findViewById(R.id.editTextNumberEventFormTickets2);
        eventIsActive = findViewById(R.id.switchIsActiveNewEventForm2);
    }

    // Unregister the SMS Receiver when the activity is in background
    @Override
    protected void onPause() {
        super.onPause();

        // Unregister your receiver to stop it from running in the background
        unregisterReceiver(eventBroadCastReceiver);
    }

    // Register the SMS Receiver when the activity is in foreground back
    @Override
    protected void onResume() {
        super.onResume();

        // Unregister your receiver to stop it from running in the background
        registerReceiver(eventBroadCastReceiver, new IntentFilter(SMSReceiver.SMS_FILTER), RECEIVER_EXPORTED);
    }

    public boolean onClickSave(View view){

        // define strings to get username and password
        String str_eventName = "", str_eventTicket = "", str_eventCategoryID = "";
        boolean isEventActive;

        // get value of user name and password
        str_eventCategoryID = eventCategoryID.getText().toString();
        str_eventName = eventName.getText().toString();
        str_eventTicket = eventTicket.getText().toString();
        isEventActive = eventIsActive.isChecked();


        // initialise shared preference class variable to access Android's persistent storage
        SharedPreferences sharedPreferences = getSharedPreferences(KeyStore.FILE_NAME, MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();

        int numericCounter = 0;
        boolean checker = true;
        for (int i = 0; i < str_eventName.length(); i++) {
            char c = str_eventName.charAt(i);
            if (!(c == ' ' || (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')|| (c >= '0' && c <= '9'))){
                checker = false;
                break;
            }
            if ((c >= '0' && c <= '9')){
                numericCounter++;
            }
            // Process or print the character c
        }

        if(checkCatID(str_eventCategoryID)) {
            // Check if event name exists
            if (str_eventName.length() != 0 && str_eventCategoryID.length() != 0 && str_eventName.trim().length() > 0) {
                if (!(checker == true && str_eventName.trim().length() != numericCounter)){
                    Toast.makeText(this, "Event Name must be alpha-numeric!", Toast.LENGTH_SHORT).show();
                    return false;
                }
                // generate event id
                String generatedEventID = generateEventId();

                boolean check = checkEventID(generatedEventID);

                while (check == false){
                    generatedEventID = generateEventId();
                    check = checkEventID(generatedEventID);
                }

                // check if the event has values or not
                if (str_eventTicket.length() != 0) {

                    // Check if the event ticket values is an integer
                    int int_eventCount = Integer.parseInt(str_eventTicket);

                    Gson gson = new Gson();
                    String json = sharedPreferences.getString(KeyStore.EVENT_LIST, null);

                    eventId.setText(generatedEventID);
                    EventDetails eventDetails = new EventDetails(generatedEventID, str_eventCategoryID, str_eventName, int_eventCount, isEventActive);

                    if(json == null){
                        Toast.makeText(getApplicationContext(), "In 1", Toast.LENGTH_SHORT).show();

                        ArrayList<EventDetails> db = new ArrayList<>();

                        db.add(eventDetails);

                        String itemListJson = gson.toJson(db);

                        editor.putString(KeyStore.EVENT_LIST, itemListJson);
                        editor.apply();
                    }
                    else{
                        Toast.makeText(getApplicationContext(), "In 2", Toast.LENGTH_SHORT).show();

                        Type type = new TypeToken<ArrayList<EventDetails>>() {}.getType();
                        ArrayList<EventDetails> db = gson.fromJson(json,type);

                        db.add(eventDetails);

                        String itemListJson = gson.toJson(db);

                        editor.putString(KeyStore.EVENT_LIST, itemListJson);
                        editor.apply();

                    }

                    Toast.makeText(getApplicationContext(), "Event saved: " + generatedEventID + " to " + str_eventCategoryID, Toast.LENGTH_SHORT).show();
//                    fragmentListCategory.updateCategoryArray();

//                        getSupportFragmentManager().beginTransaction().replace(R.id.frag2,new FragmentListCategory()).commit();
                    return true;
                } else {
//                    eventId.setText(generatedEventID);
//                    editor.putString(KeyStore.EVENT_ID, generatedEventID);
//                    editor.putString(KeyStore.EVENT_NAME, str_eventName);
//
//                    // set category id
//                    editor.putString(KeyStore.EVENT_CATEGORY_ID, str_eventCategoryID);
//                    editor.putInt(KeyStore.EVENT_TICKETS_COUNT, 0);
//                    editor.putBoolean(KeyStore.EVENT_IS_ACTIVE, isEventActive);
//
//                    // Show toast message indicating successful save
//                    Toast.makeText(getApplicationContext(), "Event saved: " + generatedEventID + " to " + str_eventCategoryID, Toast.LENGTH_SHORT).show();
                    Gson gson = new Gson();
                    String json = sharedPreferences.getString(KeyStore.EVENT_LIST, null);

                    eventId.setText(generatedEventID);
                    EventDetails eventDetails = new EventDetails(generatedEventID, str_eventCategoryID, str_eventName, 0, isEventActive);
                    String itemListJson;
                    if(json == null){
                        Toast.makeText(getApplicationContext(), "In 3", Toast.LENGTH_SHORT).show();

                        ArrayList<EventDetails> db = new ArrayList<>();

                        db.add(eventDetails);

                        itemListJson = gson.toJson(db);

                        editor.putString(KeyStore.EVENT_LIST, itemListJson);
                        editor.apply();
                    }
                    else{
                        Toast.makeText(getApplicationContext(), "In 4" + json, Toast.LENGTH_SHORT).show();

                        Type type = new TypeToken<ArrayList<EventDetails>>() {}.getType();
                        ArrayList<EventDetails> db = gson.fromJson(json,type);

                        db.add(eventDetails);

                        itemListJson = gson.toJson(db);

                        editor.putString(KeyStore.EVENT_LIST, itemListJson);
                        editor.apply();

                    }
                    Toast.makeText(getApplicationContext(), "Event saved: " + generatedEventID + " to " + str_eventCategoryID, Toast.LENGTH_SHORT).show();
//                    fragmentListCategory.updateCategoryArray();
//                    getSupportFragmentManager().beginTransaction().replace(R.id.frag2,new FragmentListCategory()).commit();
                    return true;
                }

            } else {
                // Show toast message indicating event name and category idis required
                Toast.makeText(this, "Event Name and Category Id is Required!", Toast.LENGTH_SHORT).show();
                return false;
            }
        } else {
            // Show toast message indicating event name and category idis required
            Toast.makeText(this, "Category Id is not registered!", Toast.LENGTH_SHORT).show();
            return false;
        }
    }




    // generate Event ID
    public String generateEventId(){

        String s = "";

        Random r = new Random();
        for (int i = 0; i < 5; i++){
            s += r.nextInt(10);
        }
        // since the letters are stored as the ord values in java, we find a random number between 0 to 25 and then add with the letter 'A' which will make the letter range between 'A' to 'Z'
        return "E" + (char) (r.nextInt(26) + 'A') + (char) (r.nextInt(26) + 'A') + "-" +  s;
    }

    public boolean checkEventID(String categoryID){

        // initialise shared preference class variable to access Android's persistent storage
        SharedPreferences sharedPreferences = getSharedPreferences(KeyStore.FILE_NAME, MODE_PRIVATE);

        Gson gson = new Gson();
        String json = sharedPreferences.getString(KeyStore.EVENT_LIST, null);

        if (json == null || json.equals("null")){
            return true;
        }
        Toast.makeText(this, "INININ" + json, Toast.LENGTH_SHORT).show();

        Type type = new TypeToken<ArrayList<EventDetails>>() {}.getType();
        ArrayList<EventDetails> db = gson.fromJson(json,type);

        ArrayList<String> arrStr = new ArrayList<>();



        for (int i = 0; i < db.size() ; i++){
            arrStr.add(db.get(i).getEventCategoryID());
        }

        for (int i = 0; i < arrStr.size() ; i++){
            if (arrStr.equals(categoryID)){
                return false;
            }
        }
        return true;
    }

    public boolean checkCatID(String catID){

//        Toast.makeText(this, "IN" + catID, Toast.LENGTH_SHORT).show();

        // initialise shared preference class variable to access Android's persistent storage
        SharedPreferences sharedPreferences = getSharedPreferences(KeyStore.FILE_NAME, MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();

        Gson gson = new Gson();
        String json = sharedPreferences.getString(KeyStore.CATEGORY_LIST, null);

        if (json == null){
//            Toast.makeText(this, "No Categories!", Toast.LENGTH_SHORT).show();
            return false;
        }

        Type type = new TypeToken<ArrayList<CategoryDetails>>() {}.getType();
        ArrayList<CategoryDetails> db = gson.fromJson(json,type);


        for (int i = 0; i < db.size() ; i++){
            if(db.get(i).getCategoryId().equals(catID) ){
                db.get(i).increaseCounter();

                String itemListJson = gson.toJson(db);

                editor.putString(KeyStore.CATEGORY_LIST, itemListJson);
                editor.apply();
//                Toast.makeText(this, "Category ID exists!", Toast.LENGTH_SHORT).show();
                return true;
            }
        }
//        Toast.makeText(this, "Category ID does not exist!", Toast.LENGTH_SHORT).show();
        return false;

    }



    class EventBroadCastReceiver extends BroadcastReceiver {

        /*
         * This method 'onReceive' will get executed every time class SMSReceive sends a broadcast
         * */
        @Override
        public void onReceive(Context context, Intent intent) {
//            Toast.makeText(getApplicationContext(), "Received by event"  , Toast.LENGTH_SHORT).show();

            String msg = intent.getStringExtra(SMSReceiver.SMS_MSG_KEY);

            // Check if the message starts with "event"
            if (msg.length() >= 6 && (msg.substring(0,6)).equals("event:")){

                // split the remaining message by ';'
                String secondMessage = msg.substring(6);

                int count = 0;
                for (int i = 0; i < secondMessage.length(); i++) {
                    if (secondMessage.charAt(i) == ';') {
                        count++;
                    }
                }

                if (count >= 4){
                    Toast.makeText(getApplicationContext(), "There is more than three delimiter" , Toast.LENGTH_SHORT).show();
                    return;
                }
                else if (count < 3){
                    Toast.makeText(getApplicationContext(), "There is less than three delimiter" , Toast.LENGTH_SHORT).show();
                    return;
                }

                String[] parts = secondMessage.split(";");

                // Ensure the message format is correct (4 parameters)
                if(parts.length == 4){
                    String SMSEventName = parts[0];
                    String categoryId = parts[1];
                    String strTickets = parts[2];
                    String stringIsActive = (parts[3]).toLowerCase();


                    // Check if the event name is not empty
                    if (SMSEventName.trim().length() > 0) {
                        // check if tickets counter is integer
                        try {

                            if (strTickets.length() != 0){
                                int intTickets = Integer.parseInt(strTickets);
                                if (intTickets <= 0){
                                    Toast.makeText(getApplicationContext(), "Integer must be > 0" , Toast.LENGTH_SHORT).show();
                                    return;
                                }
                            }

                            // Set UI elements based on the received data
                            if (stringIsActive.equals("true")) {
                                eventName.setText(SMSEventName);
                                eventCategoryID.setText(categoryId);
                                eventTicket.setText(strTickets);
                                eventIsActive.setChecked(true);
                            } else if (stringIsActive.equals(("false"))) {
                                eventName.setText(SMSEventName);
                                eventCategoryID.setText(categoryId);
                                eventTicket.setText(strTickets);
                                eventIsActive.setChecked(false);
                            }
                            else {
                                Toast.makeText(getApplicationContext(), "isActive must be true / false!", Toast.LENGTH_SHORT).show();
                            }
                        }
                        catch (Exception r){
                            Toast.makeText(getApplicationContext(), "Tickets Available must be an integer!", Toast.LENGTH_SHORT).show();
                        }
                    }
                    else {
                        Toast.makeText(getApplicationContext(), "Event Name must be a valid string!", Toast.LENGTH_SHORT).show();
                    }

                }
                else if(parts.length == 3){
                    String SMSEventName = parts[0];
                    String categoryId = parts[1];
                    String strTickets = parts[2];


                        // Check if the event name is not empty
                    if (SMSEventName.trim().length() > 0) {
                        // check if tickets counter is integer
                        try {

                            if (strTickets.length() != 0){
                                int intTickets = Integer.parseInt(strTickets);
                                if (intTickets <= 0){
                                    Toast.makeText(getApplicationContext(), "Integer must be > 0" , Toast.LENGTH_SHORT).show();
//                                        return ;
                                }
                                else{
                                    eventName.setText(SMSEventName);
                                    eventCategoryID.setText(categoryId);
                                    eventTicket.setText(strTickets);
                                    eventIsActive.setChecked(false);
                                }

                            }
                            else{
                                eventName.setText(SMSEventName);
                                eventCategoryID.setText(categoryId);
                                eventTicket.setText("");
                                eventIsActive.setChecked(false);
                            }
                        }
                        catch (Exception r){
                            Toast.makeText(getApplicationContext(), "Tickets Available must be an integer!", Toast.LENGTH_SHORT).show();
                        }
                    }
                    else {
                        Toast.makeText(getApplicationContext(), "Event Name must be a valid string!", Toast.LENGTH_SHORT).show();
                    }

                }
                else if(parts.length == 2){
                    String SMSEventName = parts[0];
                    String categoryId = parts[1];

                    // Check if the event name is not empty
                    if (SMSEventName.trim().length() > 0) {
                        eventName.setText(SMSEventName);
                        eventCategoryID.setText(categoryId);
                        eventTicket.setText("");
                        eventIsActive.setChecked(false);
                    }
                    else {
                        Toast.makeText(getApplicationContext(), "Event Name must be a valid string!", Toast.LENGTH_SHORT).show();
                    }

                }
                else{
                    Toast.makeText(getApplicationContext(), "Wrong message format! Event name & Category Id are required!", Toast.LENGTH_SHORT).show();
                }
            }
            else{
                Toast.makeText(getApplicationContext(), "Wrong message format, must start with event:", Toast.LENGTH_SHORT).show();

            }

        }
    }

}