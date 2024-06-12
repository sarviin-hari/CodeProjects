package com.fit2081.assignment_1;

import android.content.SharedPreferences;
import android.os.Bundle;

import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import com.fit2081.assignment_1.provider.CategoryViewModel;
import com.fit2081.assignment_1.provider.EventViewModel;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.lang.reflect.Type;
import java.util.ArrayList;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link FragmentListEvent#newInstance} factory method to
 * create an instance of this fragment.
 */
public class FragmentListEvent extends Fragment {

    RecyclerView recyclerView;
    RecyclerView.LayoutManager layoutManager;
    EventRecyclerAdapter adapter;

    private EventViewModel mEventViewModel;


    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;

    public FragmentListEvent() {
        // Required empty public constructor
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param param1 Parameter 1.
     * @param param2 Parameter 2.
     * @return A new instance of fragment FragmentListEvent.
     */
    // TODO: Rename and change types and number of parameters
    public static FragmentListEvent newInstance(String param1, String param2) {
        FragmentListEvent fragment = new FragmentListEvent();
        Bundle args = new Bundle();
        args.putString(ARG_PARAM1, param1);
        args.putString(ARG_PARAM2, param2);
        fragment.setArguments(args);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {
            mParam1 = getArguments().getString(ARG_PARAM1);
            mParam2 = getArguments().getString(ARG_PARAM2);
        }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
//        // Inflate the layout for this fragment
//        return inflater.inflate(R.layout.fragment_list_event, container, false);
        // Inflate the layout for this fragment
        View rootView = inflater.inflate(R.layout.fragment_list_event, container, false);


        recyclerView = rootView.findViewById(R.id.my_recycler_view_2);
        layoutManager = new LinearLayoutManager(getActivity());  //A RecyclerView.LayoutManager implementation which provides similar functionality to ListView.
        recyclerView.setLayoutManager(layoutManager);   // Also StaggeredGridLayoutManager and GridLayoutManager or a custom Layout manager


        adapter = new EventRecyclerAdapter();
        recyclerView.setAdapter(adapter);

        mEventViewModel = new ViewModelProvider(this).get(EventViewModel.class);
        mEventViewModel.getmAllEvents().observe(getViewLifecycleOwner(), newData -> {
            adapter.setData(newData);
            adapter.notifyDataSetChanged();
        });

//        recyclerView = rootView.findViewById(R.id.my_recycler_view_2);
//
//        layoutManager = new LinearLayoutManager(getActivity());  //A RecyclerView.LayoutManager implementation which provides similar functionality to ListView.
//        recyclerView.setLayoutManager(layoutManager);   // Also StaggeredGridLayoutManager and GridLayoutManager or a custom Layout manager
//
//        SharedPreferences sharedPreferences = requireActivity().getSharedPreferences(KeyStore.FILE_NAME, getActivity().MODE_PRIVATE);
//
//        Gson gson = new Gson();
//        String json = sharedPreferences.getString(KeyStore.EVENT_LIST, null);
//
//        Type type = new TypeToken<ArrayList<EventDetails>>() {}.getType();
//        ArrayList<EventDetails> db = gson.fromJson(json, type);
//
//
//        if (!(db == null)){
//            adapter = new EventRecyclerAdapter();
//            adapter.setData(db);
//            recyclerView.setAdapter(adapter);
//        }

        return rootView;
    }
}