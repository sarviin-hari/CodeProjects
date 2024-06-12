package com.fit2081.assignment_1;

import android.content.Intent;
import android.os.Bundle;
import android.view.GestureDetector;
import android.view.Menu;
import android.view.MenuItem;
import android.view.MotionEvent;
import android.view.View;
import android.widget.EditText;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.drawerlayout.widget.DrawerLayout;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.ViewModelProvider;

import com.fit2081.assignment_1.provider.CategoryViewModel;
import com.fit2081.assignment_1.provider.EventViewModel;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.navigation.NavigationView;
import com.google.android.material.snackbar.Snackbar;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Dashboard extends AppCompatActivity {

    DrawerLayout drawerlayout;
    Toolbar toolbar;
    NavigationView navigationView;
    FloatingActionButton fab;
    EditText eventId, eventCategoryID, eventName, eventTicket;
    Switch eventIsActive;

    private CategoryViewModel mCategoryViewModel;
    private EventViewModel mEventViewModel;

    List<CategoryDetails> categoryDetailsList;
    String undoCatID;

    private GestureDetector mDetector;
    View touchPad;

    TextView tvText;



    FragmentListCategory fragmentListCategory = new FragmentListCategory();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
//        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_dashboard);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

//        recyclerView = findViewById((R.id.))
//        // Now: all the data items are in the array list, send it to the recycler adapter to create views.
//        adapter = new CategoryRecyclerAdapter();
//        // assign the adapter to the recycler view
//        recyclerView.setAdapter(adapter);
        getSupportFragmentManager().beginTransaction().replace(R.id.frag2, fragmentListCategory).addToBackStack(null).commit();

        setContentView(R.layout.drawer_layout);

        drawerlayout = findViewById(R.id.drawer_layout);
        toolbar = findViewById(R.id.toolbar);

        fab = findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
//                boolean isMatch = onClickSave(view);

                boolean isMatch = onClickSave();
                if (isMatch) {
                    Snackbar.make(view, "Event Saved", Snackbar.LENGTH_LONG)
                            .setAction("Undo", undoOnClickListener).show();
                }


            }
        });

        navigationView = findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(new MyNavigationListener());

        setSupportActionBar(toolbar);
        getSupportActionBar().setTitle("Event Registration");

        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawerlayout, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawerlayout.addDrawerListener(toggle);
        toggle.syncState();

        // Store the attributes in teh
        eventId = findViewById(R.id.editTextAutoCompleteTextView2);
        eventCategoryID = findViewById(R.id.editTextEventFormEventCategory);
        eventName = findViewById(R.id.editTextTextEventFormEventName);
        eventTicket = findViewById(R.id.editTextNumberEventFormTickets);
        eventIsActive = findViewById(R.id.switchIsActiveNewEventForm);


        mCategoryViewModel = new ViewModelProvider(this).get(CategoryViewModel.class);
        mCategoryViewModel.getmAllCategories().observe(this, newData -> {
            categoryDetailsList = newData;

        });

        mEventViewModel = new ViewModelProvider(this).get(EventViewModel.class);
        mEventViewModel.getmLastEvent().observe(this, newData -> {
            undoCatID = newData;

        });

        MyGestureListener listener = new MyGestureListener();
        mDetector = new GestureDetector(this, listener);

        tvText = findViewById(R.id.tvText);

        touchPad = findViewById(R.id.view);
        touchPad.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
//                mDetector.setView(v);
                listener.setView(v);
                mDetector.onTouchEvent(event);
                return true;
            }
        });

    }

    private class MyGestureListener extends GestureDetector.SimpleOnGestureListener{
        View views;
        public void setView(View view){
            views = view;
        }

        @Override
        public void onLongPress(@NonNull MotionEvent e) {
//            gestureTypeTV.setText("OnLongPress!");
            // Do something
            Toast.makeText(getApplicationContext(), "Event Form Cleared", Toast.LENGTH_SHORT).show();
            eventId.setText("");
            eventCategoryID.setText("");
            eventName.setText("");
            eventTicket.setText("");
            eventIsActive.setChecked(false);
            tvText.setText("OnLongPress");
        }

        @Override
        public boolean onDoubleTap(@NonNull MotionEvent e) {
            tvText.setText("OnDoubleTap");
            boolean isMatch = onClickSave();
//            Toast.makeText(getApplicationContext(), isMatch + " ", Toast.LENGTH_SHORT).show();
            if (isMatch) {
                Snackbar.make(this.views, "Event Saved", Snackbar.LENGTH_LONG)
                        .setAction("Undo", undoOnClickListener).show();
            }
            return true;
        }

    }


    View.OnClickListener undoOnClickListener = new View.OnClickListener() {
        @Override
        public void onClick(View view) {

            // Undo Save

            // change thsi to event instead
//            mCategoryViewModel.deleteCategory(String.valueOf(categoryID));
//            Toast.makeText(getApplicationContext(), "Yet to implement" + undoCatID, Toast.LENGTH_SHORT).show();
            mCategoryViewModel.decreaseCounter(undoCatID);
            mEventViewModel.undoSave();
        }
    };

    //in order for the toolbar to work, we need to override the
    //following callback.
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        if (id == R.id.option_clear) {
            // Do something
            Toast.makeText(this, "Event Form Cleared", Toast.LENGTH_SHORT).show();
            eventId.setText("");
            eventCategoryID.setText("");
            eventName.setText("");
            eventTicket.setText("");
            eventIsActive.setChecked(false);

        } else if (id == R.id.option_del_cat) {
            mCategoryViewModel.deleteAll();
            Toast.makeText(this, "All Categories Deleted", Toast.LENGTH_SHORT).show();
        } else if (id == R.id.option_del_ev) {

            mCategoryViewModel.resetEventCount();
            mEventViewModel.deleteAll();
        }
        return true;
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.options_menu, menu);
        return true;
    }
//    public boolean onClickSave(View view) {

    public boolean onClickSave() {
        List<CategoryDetails> categoryDetails = categoryDetailsList;

        String str_eventName = "", str_eventTicket = "", str_eventCategoryID = "";
        boolean isEventActive;

        // get value of user name and password
        str_eventCategoryID = eventCategoryID.getText().toString();
        str_eventName = eventName.getText().toString();
        str_eventTicket = eventTicket.getText().toString();
        isEventActive = eventIsActive.isChecked();

        int numericCounter = 0;
        boolean checker = true;
        for (int i = 0; i < str_eventName.length(); i++) {
            char c = str_eventName.charAt(i);
            if (!(c == ' ' || (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9'))) {
                checker = false;
                break;
            }
            if ((c >= '0' && c <= '9')) {
                numericCounter++;
            }
        }

        boolean isMatch = false;
//        Toast.makeText(getApplicationContext(),  " Am i good? " + categoryDetailsList, Toast.LENGTH_SHORT).show();

        for (int i = 0; i < categoryDetails.size(); i++) {

            if (categoryDetails.get(i).getCategoryId().equalsIgnoreCase(str_eventCategoryID)) {
                isMatch = true; // Exit the loop and observer
                break;
            }
        }

        if (isMatch)  {
            // Check if event name exists
            if (str_eventName.length() != 0 && str_eventCategoryID.length() != 0 && str_eventName.trim().length() > 0) {
                if (!(checker == true && str_eventName.trim().length() != numericCounter)) {
                    Toast.makeText(this, "Event Name must be alpha-numeric!", Toast.LENGTH_SHORT).show();
                    return false;
                }
                // generate event id
                String generatedEventID = generateEventId();

                // increase the counter of category for the respective one
                for (int i = 0; i < categoryDetails.size(); i++) {
                    if (categoryDetails.get(i).getCategoryId().equalsIgnoreCase(str_eventCategoryID)) {
//                            Toast.makeText(this, str_eventCategoryID + " increased "  + db.get(i).getCategoryId(), Toast.LENGTH_SHORT).show();
                        mCategoryViewModel.increaseCounter(str_eventCategoryID);
                        break;
                    }
                }

                // check if the event has values or not
                if (str_eventTicket.length() != 0) {

                    // Check if the event ticket values is an integer
                    int int_eventCount = Integer.parseInt(str_eventTicket);
                    eventId.setText(generatedEventID);
                    EventDetails eventDetails = new EventDetails(generatedEventID, str_eventCategoryID.toUpperCase(), str_eventName, int_eventCount, isEventActive);
                    mEventViewModel.insert(eventDetails);
                    Toast.makeText(getApplicationContext(), "Event saved: " + generatedEventID + " to " + str_eventCategoryID, Toast.LENGTH_SHORT).show();
//                    fragmentListCategory.updateCategoryArray();

//                        getSupportFragmentManager().beginTransaction().replace(R.id.frag2,new FragmentListCategory()).commit();
                    return true;

                } else {

                    eventId.setText(generatedEventID);
                    eventTicket.setText("0");
                    EventDetails eventDetails = new EventDetails(generatedEventID, str_eventCategoryID.toUpperCase(), str_eventName, 0, isEventActive);
                    mEventViewModel.insert(eventDetails);

                    Toast.makeText(getApplicationContext(), "Default Tickets set to 0", Toast.LENGTH_SHORT).show();
                    Toast.makeText(getApplicationContext(), "Event saved: " + generatedEventID + " to " + str_eventCategoryID, Toast.LENGTH_SHORT).show();
                    return true;
                }

            } else {
                // Show toast message indicating event name and category idis required
                Toast.makeText(this, "Event Name and Category Id is Required!", Toast.LENGTH_SHORT).show();
                return false;
            }
        } else {
            // Show toast message indicating event name and category idis required

            if(str_eventCategoryID.length() == 0 && str_eventName.length() == 0){
                Toast.makeText(this, "Event Name and Category Id is Required!", Toast.LENGTH_SHORT).show();
            }
            else if(str_eventCategoryID.length() == 0){
                Toast.makeText(this, "Category Id is required! ", Toast.LENGTH_SHORT).show();

                if ((str_eventName.length() != 0 && str_eventName.trim().length() > 0)) {

                    if (!(checker == true && str_eventName.trim().length() != numericCounter)) {

                        Toast.makeText(this, "Event Name must be alpha-numeric!", Toast.LENGTH_SHORT).show();
                        return false;
                    }
                }
            }
            else if(str_eventName.length() == 0){
                Toast.makeText(this, "Category Id is not registered! ", Toast.LENGTH_SHORT).show();
                Toast.makeText(this, "Event Name is required! ", Toast.LENGTH_SHORT).show();

            }
            else {
                Toast.makeText(this, "Category Id is not registered! ", Toast.LENGTH_SHORT).show();
                if ((str_eventName.length() != 0 && str_eventCategoryID.length() != 0 && str_eventName.trim().length() > 0)) {
                    if (!(checker == true && str_eventName.trim().length() != numericCounter)) {
                        Toast.makeText(this, "Event Name must be alpha-numeric!", Toast.LENGTH_SHORT).show();
                        return false;
                    }
                }
                else{
                    Toast.makeText(this, "Event Name is Required!", Toast.LENGTH_SHORT).show();
                    return false;

                }
            }

            return false;
        }



    }

    // generate Event ID
    public String generateEventId() {

        String s = "";

        Random r = new Random();
        for (int i = 0; i < 5; i++) {
            s += r.nextInt(10);
        }
        // since the letters are stored as the ord values in java, we find a random number between 0 to 25 and then add with the letter 'A' which will make the letter range between 'A' to 'Z'
        return "E" + (char) (r.nextInt(26) + 'A') + (char) (r.nextInt(26) + 'A') + "-" + s;
    }


    @Override
    public void onBackPressed() {
//        super.onBackPressed();
        finish();
    }

    class MyNavigationListener implements NavigationView.OnNavigationItemSelectedListener {
        @Override
        public boolean onNavigationItemSelected(@NonNull MenuItem item) {
            // get the id of the selected item
            int id = item.getItemId();

            if (id == R.id.nav_view_cat) {
                Intent intent = new Intent(getApplicationContext(), ListCategoryActivity.class);
                startActivity(intent);
                Toast.makeText(getApplicationContext(), "Move to View Category", Toast.LENGTH_SHORT).show();
            } else if (id == R.id.nav_add_cat) {
                // Create an intent to start the NewEventCategory activity
                Intent intent = new Intent(getApplicationContext(), NewEventCategory.class);
                startActivity(intent);
                Toast.makeText(getApplicationContext(), "Move to Add New Category", Toast.LENGTH_SHORT).show();
            } else if (id == R.id.nav_view_ev) {
                Intent intent = new Intent(getApplicationContext(), ListEventActivity.class);
                startActivity(intent);
                Toast.makeText(getApplicationContext(), "Move to View Event", Toast.LENGTH_SHORT).show();
            } else if (id == R.id.nav_logout) {
//                Intent intent = new Intent(getApplicationContext(), Login.class);
//                startActivity(intent);
                Toast.makeText(getApplicationContext(), "Successfully Logged Out!", Toast.LENGTH_SHORT).show();
                finish();

            }
            // close the drawer
            drawerlayout.closeDrawers();
            // tell the OS
            return true;
        }
    }
}

