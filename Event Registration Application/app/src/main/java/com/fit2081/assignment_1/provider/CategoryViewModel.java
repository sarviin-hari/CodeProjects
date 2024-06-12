package com.fit2081.assignment_1.provider;




import android.app.Application;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;

import com.fit2081.assignment_1.CategoryDetails;

import java.util.List;

public class CategoryViewModel extends AndroidViewModel {

    private CategoryRepository mCategoryRepository;
    private LiveData<List<CategoryDetails>> mAllCategories;
    private LiveData<String> mLocation;

    public CategoryViewModel(@NonNull Application application) {
        super(application);
        mCategoryRepository = new CategoryRepository(application);
        mAllCategories = mCategoryRepository.getmAllCategories();
//        mLocation = mCategoryRepository.getmLocation(String cateId);

    }

    // dont let repository handle all the time
    public LiveData<List<CategoryDetails>> getmAllCategories() {
//        Toast.makeText(getApplication(),  "Mere list" +  mAllCategories.getValue(), Toast.LENGTH_SHORT).show();
        return mAllCategories;
    }

    public LiveData<String> getmLocation(String cateId) {
//        Toast.makeText(getApplication(),  "Mere list" +  mAllCategories.getValue(), Toast.LENGTH_SHORT).show();
        mLocation = mCategoryRepository.getmLocation(cateId);
        return mLocation;
    }

    public void insert(CategoryDetails student){
        mCategoryRepository.insert(student);
    }

    public void deleteCategory(String name){
        mCategoryRepository.deleteCategory(name);
    }
    public void delete(CategoryDetails categoryDetails){
        mCategoryRepository.delete(categoryDetails);
    }

    public void increaseCounter(String name){

        mCategoryRepository.increaseCounter(name);
    }

    public void decreaseCounter(String name){

        mCategoryRepository.decreaseCounter(name);
    }


    public void resetEventCount(){
        mCategoryRepository.resetEventCount();
    }



    public void deleteAll(){
        mCategoryRepository.deleteAll();
    }

//    public LiveData<String> getLastCategory(){
//        return mLastCat;
//    }



}