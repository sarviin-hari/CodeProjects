package com.fit2081.assignment_1;

import android.content.Context;
import android.content.Intent;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.cardview.widget.CardView;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;
import java.util.List;

import androidx.core.content.ContextCompat;


public class CategoryRecyclerAdapter extends RecyclerView.Adapter<CategoryRecyclerAdapter.ViewHolder> {

    List<CategoryDetails> data = new ArrayList<CategoryDetails>();

    public void setData(List<CategoryDetails> data) {
        this.data = data;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(parent.getContext()).inflate(R.layout.category_card_layout, parent, false); //CardView inflated as RecyclerView list item
        ViewHolder viewHolder = new ViewHolder(v);
//        Log.d("week6App","onCreateViewHolder");
        return viewHolder;
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
//        if (!(data.get(position).getCategoryId() == null)) {
            holder.catId.setText(data.get(position).getCategoryId());
            holder.catName.setText(data.get(position).getCategoryName());
            holder.eventCount.setText(String.valueOf(data.get(position).getEventCount()));
            boolean isActive = data.get(position).getIsActive();
            String bool;
            if (isActive){
                bool =  "True";
            }
            else {
                bool = "False";
            }
            holder.location = data.get(position).getLocation();
            holder.isActive.setText(bool);
            holder.setCardView();
//        }
//        Log.d("week6App","onBindViewHolder");

    }

    @Override
    public int getItemCount() {
        return data.size();
    }

    public class ViewHolder extends RecyclerView.ViewHolder {
        public TextView catId, catName, eventCount, isActive;
        public CardView cardView;
        public Context context; // Declare context variable

        public String location;


        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            catId = itemView.findViewById(R.id.card_cat_event_id);
            catName = itemView.findViewById(R.id.card_cat_name);
            eventCount = itemView.findViewById(R.id.card_cat_event_count);
            isActive = itemView.findViewById(R.id.card_cat_isActive);

            cardView = itemView.findViewById(R.id.card_view);
            context = itemView.getContext();


            itemView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    // Get the text from the TextView clicked
//                    String evNameText = evName.getText().toString();
                    // Use the text as needed
                    Intent intent = new Intent(context, MapsActivity.class);

                    // Add location data as extras to the intent
                    intent.putExtra("location", location);
//                    intent.putExtra("longitude", longitudeValue);

//                    Toast.makeText(context, "Event " + catId.getText().toString()  + "' Clicked", Toast.LENGTH_SHORT).show();
                    context.startActivity(intent);
                }
            });
        }

        public void setCardView() {
            int color = ContextCompat.getColor(context, android.R.color.holo_green_dark);
            cardView.setCardBackgroundColor(color); // You can use any color resource or color value here
        }
    }
}