package com.fit2081.assignment_1;

import android.content.Context;
import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;
import java.util.List;



public class EventRecyclerAdapter extends RecyclerView.Adapter<EventRecyclerAdapter.ViewHolder> {

    List<EventDetails> data = new ArrayList<EventDetails>();

    public void setData(List<EventDetails> data) {
        this.data = data;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(parent.getContext()).inflate(R.layout.event_card_layout, parent, false); //CardView inflated as RecyclerView list item
        ViewHolder viewHolder = new ViewHolder(v);
//        Log.d("week6App","onCreateViewHolder");
        return viewHolder;
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        holder.evId.setText(data.get(position).getEventId());
        holder.catEvId.setText(data.get(position).getEventCategoryID());
        holder.evName.setText(data.get(position).getEventName());
        holder.tickets.setText(data.get(position).getStrEventTicket());
        boolean isActive = data.get(position).getIsActive();
        String bool;
        if (isActive){
            bool =  "True";
        }
        else {
            bool = "False";
        }
        holder.isActive.setText(bool);
        //        holder.setCardView();


    }

    @Override
    public int getItemCount() {
        return data.size();
    }

    public class ViewHolder extends RecyclerView.ViewHolder {
        public TextView evId, catEvId, evName, tickets, isActive;
//        public CardView cardView;
        public Context context; // Declare context variable


        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            evId = itemView.findViewById(R.id.card_ev_event_id_txt);
            catEvId = itemView.findViewById(R.id.card_ev_cat_id_txt);
            evName = itemView.findViewById(R.id.card_ev_name_txt);
            tickets = itemView.findViewById(R.id.card_ev_tickets_txt);
            isActive = itemView.findViewById(R.id.card_ev_isActive);
//            cardView = itemView.findViewById(R.id.card_view_event);
            context = itemView.getContext();
            itemView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {

                    Intent intent = new Intent(context, WebView.class);
//
//                    // Add location data as extras to the intent
//                    intent.putExtra("location", location);
                    intent.putExtra("websearch", evName.getText().toString());
//
////                    Toast.makeText(context, "Event " + catId.getText().toString()  + "' Clicked", Toast.LENGTH_SHORT).show();
                    context.startActivity(intent);
                }
            });

        }

//        public void setCardView() {
//            int color = ContextCompat.getColor(context, android.R.color.holo_green_light);
//            cardView.setCardBackgroundColor(color); // You can use any color resource or color value here
//        }
    }
}