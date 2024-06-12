package com.fit2081.assignment_1;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProvider;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import com.fit2081.assignment_1.provider.CategoryViewModel;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link FragmentListCategory#newInstance} factory method to
 * create an instance of this fragment.
 */
public class FragmentListCategory extends Fragment {

    ArrayList<CategoryDetails> categoryDetails = new ArrayList<>();
    RecyclerView recyclerView;
    RecyclerView.LayoutManager layoutManager;
    CategoryRecyclerAdapter adapter;

    private CategoryViewModel mCategoryViewModel;
    List<CategoryDetails> categoryDetailsList;
    String location;


    // TODO: Rename parameter arguments, choose names that match
    // the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
    private static final String ARG_PARAM1 = "param1";
    private static final String ARG_PARAM2 = "param2";

    // TODO: Rename and change types of parameters
    private String mParam1;
    private String mParam2;

    public FragmentListCategory() {
        // Required empty public constructor
    }

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param param1 Parameter 1.
     * @param param2 Parameter 2.
     * @return A new instance of fragment FragmentListCategory.
     */
    // TODO: Rename and change types and number of parameters
    public static FragmentListCategory newInstance(String param1, String param2) {
        FragmentListCategory fragment = new FragmentListCategory();
        Bundle args = new Bundle();
        args.putString(ARG_PARAM1, param1);
        args.putString(ARG_PARAM2, param2);
        fragment.setArguments(args);
        return fragment;
    }

    public CategoryViewModel getmCategoryViewModel() {
        return mCategoryViewModel;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {
            mParam1 = getArguments().getString(ARG_PARAM1);
            mParam2 = getArguments().getString(ARG_PARAM2);
        }

    }

    public CategoryRecyclerAdapter getAdapter() {
        return adapter;
    }

//    public void updateCategoryArray(){
//
////        SharedPreferences sharedPreferences = requireActivity().getSharedPreferences(KeyStore.FILE_NAME, getActivity().MODE_PRIVATE);
////
////        Gson gson = new Gson();
////        String json = sharedPreferences.getString(KeyStore.CATEGORY_LIST, null);
////
////        Type type = new TypeToken<ArrayList<CategoryDetails>>() {}.getType();
////        ArrayList<CategoryDetails> db = gson.fromJson(json, type);
//////        Toast.makeText(getContext(), categoryDetails.size() + " " +  gson.toJson(categoryDetails), Toast.LENGTH_SHORT).show();
////
////        if (json == null){
////            categoryDetails = new ArrayList<CategoryDetails>();
////            adapter.setData(categoryDetails);
////            recyclerView.setAdapter(adapter);
////        }
////        else {
////            categoryDetails = db;
////            adapter.setData(categoryDetails);
////            recyclerView.setAdapter(adapter);
////        }
//
//        adapter = new CategoryRecyclerAdapter();
//        recyclerView.setAdapter(adapter);
//
//        mCategoryViewModel = new ViewModelProvider(this).get(CategoryViewModel.class);
//        mCategoryViewModel.getmAllCategories().observe(getViewLifecycleOwner(), newData -> {
//            adapter.setData(newData);
//            adapter.notifyDataSetChanged();
//        });
//
//    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View rootView = inflater.inflate(R.layout.fragment_list_category, container, false);


        recyclerView = rootView.findViewById(R.id.my_recycler_view);
        layoutManager = new LinearLayoutManager(getActivity());  //A RecyclerView.LayoutManager implementation which provides similar functionality to ListView.
        recyclerView.setLayoutManager(layoutManager);   // Also StaggeredGridLayoutManager and GridLayoutManager or a custom Layout manager


        adapter = new CategoryRecyclerAdapter();
        recyclerView.setAdapter(adapter);

        mCategoryViewModel = new ViewModelProvider(this).get(CategoryViewModel.class);
        mCategoryViewModel.getmAllCategories().observe(getViewLifecycleOwner(), newData -> {
            adapter.setData(newData);
            adapter.notifyDataSetChanged();
        });
        mCategoryViewModel.getmAllCategories().observe(getViewLifecycleOwner(), newData -> {
            categoryDetailsList = newData;
        });

//        SharedPreferences sharedPreferences = requireActivity().getSharedPreferences(KeyStore.FILE_NAME, getActivity().MODE_PRIVATE);
//
//        Gson gson = new Gson();
//        String json = sharedPreferences.getString(KeyStore.CATEGORY_LIST, null);
//
//        Type type = new TypeToken<ArrayList<CategoryDetails>>() {}.getType();
//        ArrayList<CategoryDetails> db = gson.fromJson(json, type);
//
//        if (!(db == null)){
//            categoryDetails = db;
//            adapter = new CategoryRecyclerAdapter();
//            adapter.setData(categoryDetails);
//            recyclerView.setAdapter(adapter);
//        }
//        else{
//            categoryDetails = new ArrayList<>();
//            adapter = new CategoryRecyclerAdapter();
//            adapter.setData(categoryDetails);
//            recyclerView.setAdapter(adapter);
//        }

        return rootView;

    }


}