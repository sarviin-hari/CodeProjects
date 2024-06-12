package com.fit2081.assignment_1.provider;

import android.content.Context;

import androidx.room.Database;
import androidx.room.Room;
import androidx.room.RoomDatabase;

import com.fit2081.assignment_1.CategoryDetails;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

@Database(entities = {CategoryDetails.class}, version = 4)
public abstract class CategoryDatabase extends RoomDatabase {

    // database name, this is important as data is contained inside a file named "card_database"
    public static final String CATEGORY_DATABASE = "category_database";
    public abstract CategoryDAO categoryDAO();

    // marking the instance as volatile to ensure atomic access to the variable
    private static volatile CategoryDatabase INSTANCE;
    private static final int NUMBER_OF_THREADS = 4;
    static final ExecutorService databaseWriterExecutor =
            Executors.newFixedThreadPool(NUMBER_OF_THREADS);

    /**
     * Since this class is an absract class, to get the database reference we would need
     * to implement a way to get reference to the database.
     *
     * @param context Application of Activity Context
     * @return a reference to the database for read and write operation
     */
    static CategoryDatabase getDatabase(final Context context) {
        if (INSTANCE == null) {
            synchronized (CategoryDatabase.class) {
                if (INSTANCE == null) {
                    INSTANCE = Room.databaseBuilder(context.getApplicationContext(),
                                    CategoryDatabase.class, CATEGORY_DATABASE)
                            .build();
                }
            }
        }
        return INSTANCE;
    }

}