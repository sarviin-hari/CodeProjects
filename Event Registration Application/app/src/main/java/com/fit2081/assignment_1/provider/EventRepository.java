//package com.fit2081.assignment_1.provider;
//
//public class EventRepository {
//}


package com.fit2081.assignment_1.provider;

import android.app.Application;

import androidx.lifecycle.LiveData;

import com.fit2081.assignment_1.EventDetails;

import java.util.List;

public class EventRepository {
    private EventDAO mEventDao;
    private LiveData<List<EventDetails>> mAllEvent;
    private LiveData<String> mLastEvent;

    EventRepository(Application application){
        EventDatabase db = EventDatabase.getDatabase(application);
        mEventDao = db.eventDAO();
        mAllEvent = mEventDao.getAllEvents();
        mLastEvent = mEventDao.getLastEvent();

    }

    LiveData<List<EventDetails>> getmAllEvent(){
        return mAllEvent;
    }

    LiveData<String> getmLastEvent(){
        return mLastEvent;
    }


    void insert(EventDetails event){
        EventDatabase.databaseWriterExecutor.execute(() -> mEventDao.addEvent((event)));
    }

    void deleteEvents(String event){
        EventDatabase.databaseWriterExecutor.execute(() -> mEventDao.deleteEvent((event)));
    }

    void deleteAll(){
        EventDatabase.databaseWriterExecutor.execute(() -> mEventDao.deleteAllEvents());
    }

    void undoSave(){
        EventDatabase.databaseWriterExecutor.execute(() -> mEventDao.undoSave());
    }


}
