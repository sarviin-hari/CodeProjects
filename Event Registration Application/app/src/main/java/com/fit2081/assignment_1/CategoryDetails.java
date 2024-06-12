package com.fit2081.assignment_1;

import androidx.room.Entity;

import androidx.annotation.NonNull;
import androidx.room.ColumnInfo;
import androidx.room.Entity;
import androidx.room.PrimaryKey;


@Entity(tableName = "categories")
public class CategoryDetails {
    @PrimaryKey(autoGenerate = true)
    @ColumnInfo(name = "ID")
    @NonNull
    private int id;
    @ColumnInfo(name = "categoryID")
    private String categoryId;
    @ColumnInfo(name = "categoryName")
    private String categoryName;
    @ColumnInfo(name = "categoryEventCount")
    private int eventCount;
    @ColumnInfo(name = "categoryIsActive")
    private boolean isActive;
    @ColumnInfo(name = "categoryLocation")
    private String location;

    private int initialEventCount;

    public CategoryDetails(String categoryId, String categoryName, int eventCount, boolean isActive, String location) {
        this.categoryId = categoryId;
        this.categoryName = categoryName;
        this.eventCount = eventCount;
        this.isActive = isActive;
        this.initialEventCount = eventCount;
        this.location = location;
    }



    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public int getId() {
        return id;
    }

    public void setId(@NonNull int id) {
        this.id = id;
    }

    public int getInitialEventCount() {
        return initialEventCount;
    }

    public void resetEventCount() {
        eventCount = initialEventCount;
    }

    public void increaseCounter(){
        eventCount += 1;
    }

    public boolean decreaseCounter(){
        eventCount -= 1;
        return eventCount == 0;
    }

    public void setCategoryId(String categoryId) {
        this.categoryId = categoryId;
    }

    public void setCategoryName(String categoryName) {
        this.categoryName = categoryName;
    }

    public void setActive(boolean active) {
        isActive = active;
    }

    public void setInitialEventCount(int initialEventCount) {
        this.initialEventCount = initialEventCount;
    }

    public int getEventCount() {
        return eventCount;
    }

    public String getCategoryId() {
        return categoryId;
    }

    public String getCategoryName() {
        return categoryName;
    }

//    public String getEventCount() {
//        return String.valueOf(eventCount);
//    }

    public void setEventCount(int eventCount) {
        this.eventCount = eventCount;
    }
    public boolean getIsActive(){
        return isActive;
    }
//    public String getisActive() {
//        if (isActive){
//            return "True";
//        }
//        return "False";
//    }


    // Override toString() method to print all properties of the class
    @Override
    public String toString() {
        return "CategoryDetails{" +
                "categoryId='" + categoryId + '\'' +
                ", categoryName='" + categoryName + '\'' +
                ", eventCount=" + eventCount +
                ", isActive=" + isActive +
                '}';
    }


}
