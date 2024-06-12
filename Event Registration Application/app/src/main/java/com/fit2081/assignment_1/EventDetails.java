package com.fit2081.assignment_1;

import androidx.annotation.NonNull;
import androidx.room.ColumnInfo;
import androidx.room.Entity;
import androidx.room.PrimaryKey;

@Entity(tableName = "events")
public class EventDetails {
    @PrimaryKey(autoGenerate = true)
    @ColumnInfo(name = "ID")
    @NonNull
    private int id;
    @ColumnInfo(name = "eventID")
    private String eventId;

    @ColumnInfo(name = "eventCategoryID")
    private String eventCategoryID;
    @ColumnInfo(name = "eventName")
    private String eventName;
    @ColumnInfo(name = "eventTicket")
    private int eventTicket;
    @ColumnInfo(name = "eventIsActive")
    private boolean isActive;

    public EventDetails(String eventId, String eventCategoryID, String eventName, int eventTicket, boolean isActive) {
        this.eventId = eventId;
        this.eventCategoryID = eventCategoryID;
        this.eventName = eventName;
        this.eventTicket = eventTicket;
        this.isActive = isActive;
    }
    public int getId() {
        return id;
    }
    public void setId(@NonNull int id) {
        this.id = id;
    }

    public String getEventId() {
        return eventId;
    }

    public String getEventCategoryID() {
        return eventCategoryID;
    }

    public String getEventName() {
        return eventName;
    }
    public int getEventTicket() {
        return eventTicket;
    }
    public String getStrEventTicket() {
        return String.valueOf(eventTicket);
    }

    public boolean getIsActive() {
        return isActive;
    }
    public String pr(){
        return "EventDetails{" +
                "eventId='" + eventId + '\'' +
                ", eventCategoryID='" + eventCategoryID + '\'' +
                ", eventName=" + eventName +
                ", eventTicket=" + eventTicket +
                ", isActive=" + isActive +
                '}';
    }

    // Override toString() method to print all properties of the class
    @Override
    public String toString() {
        return "EventDetails{" +
                "eventId='" + eventId + '\'' +
                ", eventCategoryID='" + eventCategoryID + '\'' +
                ", eventName=" + eventName +
                ", eventTicket=" + eventTicket +
                ", isActive=" + isActive +
                '}';
    }
}
