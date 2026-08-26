package com.example.lunaria.data.model.book

import com.google.gson.annotations.SerializedName

data class Book (
    val id: Int,
    val title: String,
    val author: String,

    @SerializedName("published_year")
    val publishedYear: Int,

    val description: String,
    val genres: List<String>
)