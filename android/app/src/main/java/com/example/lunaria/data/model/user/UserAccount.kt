package com.example.lunaria.data.model.user

import com.google.gson.annotations.SerializedName


data class UserAccount(
    val username: String,
    val password: String,

    @SerializedName("genre_preferences")
    val genrePreference: List<String> = mutableListOf()
)
