package com.fit2081.assignment_1.provider;


import android.app.Application;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;

import com.fit2081.assignment_1.EventDetails;

import java.util.List;

public class EventViewModel extends AndroidViewModel {

    private EventRepository mEventRepository;
    private LiveData<List<EventDetails>> mAllEvents;
    private LiveData<String> getmLastEvent;

    public EventViewModel(@NonNull Application application) {
        super(application);
        mEventRepository = new EventRepository(application);
        mAllEvents = mEventRepository.getmAllEvent();
        getmLastEvent = mEventRepository.getmLastEvent();
    }

    // dont let repository handle all the time
    public LiveData<List<EventDetails>> getmAllEvents() {return mAllEvents;}

    public void insert(EventDetails student){
        mEventRepository.insert(student);
    }

    public void deleteEvent(String name){
        mEventRepository.deleteEvents(name);
    }

    public void deleteAll(){
        mEventRepository.deleteAll();
    }

    public void undoSave(){
        mEventRepository.undoSave();
    }

    public LiveData<String> getmLastEvent(){
        return getmLastEvent ;
    }

}
