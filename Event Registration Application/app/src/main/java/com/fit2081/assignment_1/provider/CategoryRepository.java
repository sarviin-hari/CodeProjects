package com.fit2081.assignment_1.provider;

import android.app.Application;

import androidx.lifecycle.LiveData;

import com.fit2081.assignment_1.CategoryDetails;

import java.util.List;

public class CategoryRepository {
    private CategoryDAO mCategoryDao;
    private LiveData<List<CategoryDetails>> mAllCategories;
    private LiveData<String> mLocation;
    CategoryRepository(Application application){
        CategoryDatabase db = CategoryDatabase.getDatabase(application);
        mCategoryDao = db.categoryDAO();

        mAllCategories = mCategoryDao.getAllCategories();

    }

    LiveData<List<CategoryDetails>> getmAllCategories(){
        return mAllCategories;
    }

    LiveData<String> getmLocation(String cateId){
        mLocation = mCategoryDao.getmLocation(cateId);
        return mLocation;
    }

    void insert(CategoryDetails category){
        CategoryDatabase.databaseWriterExecutor.execute(() -> mCategoryDao.addCategory((category)));
    }

    void deleteCategory(String category){
        CategoryDatabase.databaseWriterExecutor.execute(() -> mCategoryDao.deleteCategory((category)));
    }

    void delete(CategoryDetails categoryDetails){
        CategoryDatabase.databaseWriterExecutor.execute(() -> mCategoryDao.delete((categoryDetails)));
    }

    void deleteAll(){
        CategoryDatabase.databaseWriterExecutor.execute(() -> mCategoryDao.deleteAllCategories());
    }

    void increaseCounter(String category){
        CategoryDatabase.databaseWriterExecutor.execute(() -> mCategoryDao.increaseCounter((category)));
    }

    void decreaseCounter(String category){
        CategoryDatabase.databaseWriterExecutor.execute(() -> mCategoryDao.decreaseCounter((category)));
    }


    void resetEventCount(){
        CategoryDatabase.databaseWriterExecutor.execute(() -> mCategoryDao.resetEventCount());
    }





}
