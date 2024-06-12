package com.fit2081.assignment_1.provider;

import androidx.lifecycle.LiveData;
import androidx.room.Dao;
import androidx.room.Delete;
import androidx.room.Insert;
import androidx.room.Query;

import com.fit2081.assignment_1.CategoryDetails;

import java.util.List;
@Dao
public interface CategoryDAO {
    @Query("select * from categories")
    LiveData<List<CategoryDetails>> getAllCategories();
    @Query("select categoryLocation from categories where categoryID=:catID")
    LiveData<String> getmLocation(String catID);

//    @Query("select * from categories where categoryID=:catID")
//    List<CategoryDetails> getCategory(String catID);

    @Insert
    void addCategory(CategoryDetails category);
    @Query("delete from categories where lower(categoryID)=lower(:catID)")
    void deleteCategory(String catID);

    @Delete
    void delete(CategoryDetails categoryDetails);

    @Query(("delete from categories"))
    void deleteAllCategories();

    @Query("SELECT categoryID FROM categories WHERE id = (SELECT MAX(id) FROM categories)")
    LiveData<String> getLastCategory();
    @Query(("update categories set categoryEventCount = categoryEventCount + 1 where lower(categoryID) = lower(:catID)"))
    void increaseCounter(String catID);

    @Query(("update categories set categoryEventCount = categoryEventCount - 1 where lower(categoryID) = lower(:catID)"))
    void decreaseCounter(String catID);


    @Query(("update categories set categoryEventCount = initialEventCount"))
    void resetEventCount();

}
