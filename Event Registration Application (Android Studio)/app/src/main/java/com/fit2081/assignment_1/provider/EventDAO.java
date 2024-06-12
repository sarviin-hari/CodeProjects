package com.fit2081.assignment_1.provider;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Insert;
import androidx.room.Query;

import com.fit2081.assignment_1.EventDetails;

import java.util.List;
@Dao
public interface EventDAO {
    @Query("select * from events")
    LiveData<List<EventDetails>> getAllEvents();

    @Query("select * from events where eventID=:evID")
    List<EventDetails> getEvent(String evID);

    @Insert
    void addEvent(EventDetails event);
    @Query("delete from events where eventID=:evID")
    void deleteEvent(String evID);
    @Query(("delete from events"))
    void deleteAllEvents();

    @Query("SELECT eventCategoryID FROM events WHERE id = (SELECT MAX(id) FROM events)")
    LiveData<String> getLastEvent();
    @Query(("delete from events where id = (select max(id) from events)"))
    void undoSave();


}
