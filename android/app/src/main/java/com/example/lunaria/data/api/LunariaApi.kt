package com.example.lunaria.data.api

import com.example.lunaria.data.model.book.Book
import com.example.lunaria.data.model.user.UserAccount
import com.example.lunaria.data.model.user.Username
import com.example.lunaria.data.model.user.UsernameAndPreferences

import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface LunariaApi {

    @POST("recommend-books")
    suspend fun recommendBooks(
        @Body request: Username
    ): List<Book>

    @GET("book-brief-info")
    suspend fun getAllBooksFromDatabase(): List<Book>

    @POST("register-user")
    suspend fun registerUserAccount(
        @Body account: UserAccount
    )

    @POST("register-genre-preferences")
    suspend fun registerGenrePreferences(
        @Body genrePreference: UsernameAndPreferences
    )
}