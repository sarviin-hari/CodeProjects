package com.fit2081.assignment_1;

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

public class WebView extends AppCompatActivity {
    Toolbar toolbar;
    android.webkit.WebView webView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
//        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_web_view);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        toolbar = findViewById(R.id.toolbar2);
        setSupportActionBar(toolbar);
        getSupportActionBar().setTitle("Google Search Results");

//        unitCodeET = findViewById(R.id.unitET);
        webView = findViewById(R.id.webView);

        // Enable loading website content using AJAX (Asynchronous JavaScript And XML) technique
        // AJAX allows web pages to be updated asynchronously by exchanging data with a web server behind the scenes.
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);

        webView.setWebViewClient(new WebViewClient());

        OnSearchBtnClick();

    }

    public void OnSearchBtnClick(){

        Intent intent = getIntent();
        String webSearch = intent.getStringExtra("websearch"); // Default value 0.0 if not found

//        String unitCode = unitCodeET.getText().toString();
//        https://www.google.com/search?q=webview%20android+studio&oq=webview+and&gs_lcrp=EgZjaHJvbWUqBwgBEAAYgAQyBwgAEAAYgAQyBwgBEAAYgAQyBggCEEUYOTIHCAMQABiABDIHCAQQABiABDIHCAUQABiABDIHCAYQABiABDIHCAcQABiABDIHCAgQABiABDIHCAkQABiABNIBCDUwOTNqMGo5qAIAsAIB&sourceid=chrome&ie=UTF-8
        String searchURL = "https://www.google.com/search?q=" + webSearch;
        webView.loadUrl(searchURL);
    }
}