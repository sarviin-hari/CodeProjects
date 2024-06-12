package com.fit2081.assignment_1;

import androidx.annotation.NonNull;
import androidx.fragment.app.FragmentActivity;

import android.content.Intent;
import android.location.Address;
import android.location.Geocoder;
import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;
import androidx.appcompat.widget.Toolbar;


import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.fit2081.assignment_1.databinding.ActivityMapsBinding;
import com.google.android.material.snackbar.Snackbar;
import androidx.appcompat.app.AppCompatActivity;


import java.io.IOException;
import java.util.List;
import java.util.Locale;


import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebViewClient;
import android.widget.EditText;


import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;


public class MapsActivity extends AppCompatActivity implements OnMapReadyCallback {

    private GoogleMap mMap;
    private ActivityMapsBinding binding;

    private SupportMapFragment mapFragment;
    private Geocoder geocoder;
    Toolbar toolbar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        binding = ActivityMapsBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());
        geocoder = new Geocoder(getApplicationContext(), Locale.getDefault());


        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);

        toolbar = findViewById(R.id.toolbarx);
        setSupportActionBar(toolbar);
        getSupportActionBar().setTitle("Map View");


    }

    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */
    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;

        // Retrieve the latitude and longitude values from the Intent
        Intent intent = getIntent();
        String location = intent.getStringExtra("location"); // Default value 0.0 if not found
//        Toast.makeText(this, "MapTYest " + location, Toast.LENGTH_SHORT).show();

//        if (location.isEmpty()){
//            return;
//        }

        // implememtnget City
        Geocoder geocoder = new Geocoder(getApplicationContext(), Locale.getDefault());
        String country = "null";
        List<Address> addresses = null;
        List<Address> address = null;

        try {
            addresses = geocoder.getFromLocationName(location, 1);
        } catch (Exception e) {
//            Snackbar.make(mapFragment.getView(), "No such country", Snackbar.LENGTH_SHORT).show();
        }

        if (addresses == null){
            try {
                address = geocoder.getFromLocationName("Malaysia", 1);
            } catch (IOException e) {
                Log.d("No Location", "Couldn't find location");
            }

            LatLng count = new LatLng(address.get(0).getLatitude(), address.get(0).getLongitude());
            mMap.addMarker(new MarkerOptions().position(count).title("Malaysia"));
            mMap.moveCamera(CameraUpdateFactory.newLatLng(count));
            mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(count, 10), 2000, null);
            googleMap.setMapType(GoogleMap.MAP_TYPE_TERRAIN);
            Toast.makeText(this, "Category address not found", Toast.LENGTH_SHORT).show();
        }
        //if there is more than 0 addresses, then get the countryname
        else if(addresses.size() > 0){
            country = addresses.get(0).getCountryName();

            // Add a marker in Sydney and move the camera
            LatLng count = new LatLng(addresses.get(0).getLatitude(), addresses.get(0).getLongitude());
            mMap.addMarker(new MarkerOptions().position(count).title(location));
            mMap.moveCamera(CameraUpdateFactory.newLatLng(count));
//            googleMap.animateCamera(CameraUpdateFactory.zoomTo(10));
            mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(count, 10), 2000, null);

            googleMap.setMapType(GoogleMap.MAP_TYPE_TERRAIN);

            Toast.makeText(this, "The selected location is " + location, Toast.LENGTH_SHORT).show();
//
//            Snackbar.make(mapFragment.getView(), "You clicked on " + location, Snackbar.LENGTH_SHORT).show();
        }
        else{
            try {
                address = geocoder.getFromLocationName("Malaysia", 1);
            } catch (IOException e) {
                Log.d("No Location", "Couldn't find location");
            }

            LatLng count = new LatLng(address.get(0).getLatitude(), address.get(0).getLongitude());
            mMap.addMarker(new MarkerOptions().position(count).title("Malaysia"));
            mMap.moveCamera(CameraUpdateFactory.newLatLng(count));
            mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(count, 10), 2000, null);
            googleMap.setMapType(GoogleMap.MAP_TYPE_TERRAIN);
            Toast.makeText(this, "Category address not found", Toast.LENGTH_SHORT).show();
        }





        mMap.setOnMapClickListener(new GoogleMap.OnMapClickListener(){
            @Override
            public void onMapClick(@NonNull LatLng latLng) {
//                Toast.makeText(getApplicationContext(), "MapOnClick", Toast.LENGTH_SHORT).show();

                Geocoder geocoder = new Geocoder(getApplicationContext(), Locale.getDefault());
                String country = "null";
                List<Address> addresses = null;

                try {
                    //use the geocoder and return max 1 result (address) from the lat and long clicked
                    addresses = geocoder.getFromLocation(latLng.latitude, latLng.longitude, 1);
                } catch (Exception e) {
                    Log.d("No Location", "Couldn't find location");
                }
                //if there is more than 0 addresses, then get the countryname
                if(addresses.size() > 0){
                    country = addresses.get(0).getCountryName();
                    if (country == null){
                        Toast.makeText(getApplicationContext(), "No country at this location!! Sorry", Toast.LENGTH_SHORT).show();
                    }
                    else {
//                    Snackbar.make(mapFragment.getView(), "You clicked on " + country, Snackbar.LENGTH_SHORT).show();
                        Toast.makeText(getApplicationContext(), "You clicked on " + country, Toast.LENGTH_SHORT).show();
                    }
                }
                else{
//                    Snackbar.make(mapFragment.getView(), "No such country", Snackbar.LENGTH_SHORT).show();
//                    googleMap.animateCamera(CameraUpdateFactory.zoomTo(10));
                    Toast.makeText(getApplicationContext(), "No country at this location!! Sorry", Toast.LENGTH_SHORT).show();

                }



            }


            // What if I want to get a city name

        });

    }



//    @Override
//    public void onMapReady(GoogleMap googleMap) {
//        mMap = googleMap;
//
//        // Add a marker in Sydney and move the camera
//        LatLng sydney = new LatLng(-34, 151);
//        mMap.addMarker(new MarkerOptions().position(sydney).title("Marker in Sydney"));
//        mMap.moveCamera(CameraUpdateFactory.newLatLng(sydney));
//
//        //this sets the zoom level (float), min value = 2, max value = 21
//        mMap.animateCamera(CameraUpdateFactory.zoomTo(10));
//
//        // Set the map type to Hybrid. try experimenting with the other map types. :)
//        googleMap.setMapType(GoogleMap.MAP_TYPE_HYBRID);
//
//        //write your ClickListeners in onMapReady(), NOT in onCreate()
//        mMap.setOnMapClickListener(new GoogleMap.OnMapClickListener() {
//            @Override
//            public void onMapClick(@NonNull LatLng latLng) {
//
//                //setup your Geocoder
//                Geocoder geocoder = new Geocoder(getApplicationContext(), Locale.getDefault());
//                String country = "null";
//                List<Address> addresses = null;
//
//                //this commented code takes you to Malaysia when you click anywhere on the
//                //map. Comment out lines 95 - 106, then uncomment 81 - 93
//                try {
//
//                    //use the geocoder and return max 1 result (address) from the location "Malaysia"
//                    addresses = geocoder.getFromLocationName("Malaysia", 1);
//                } catch (Exception e) {
//                    Log.d("No Location", "Couldn't find location");
//                }
//
//                //if there is more than 0 addresses, then get the lat and long from the 0th
//                //address, and move the camera there
//                if (addresses.size() > 0) {
//                    mMap.moveCamera(CameraUpdateFactory.newLatLng(new LatLng(addresses.get(0).getLatitude(), addresses.get(0).getLongitude())));
//                }
//
////                try {
////
////                    //use the geocoder and return max 1 result (address) from the lat and long clicked
////                    addresses = geocoder.getFromLocation(latLng.latitude, latLng.longitude, 1);
////                } catch (Exception e) {
////                    Log.d("No Location", "Couldn't find location");
////                }
////                  //if there is more than 0 addresses, then get the countryname
////                if(addresses.size() > 0){
////                    country = addresses.get(0).getCountryName();
////                }
////                Snackbar.make(mapFragment.getView(), "you clicked on " + country, Snackbar.LENGTH_SHORT).show();
//            }
//        });
//    }



        // Create click listener in on map ready
}