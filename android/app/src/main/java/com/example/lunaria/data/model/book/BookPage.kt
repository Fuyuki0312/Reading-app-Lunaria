package com.example.lunaria.data.model.book

import com.google.gson.annotations.SerializedName

data class BookPage(

    @SerializedName("page_num")
    val pageNum: Int,

    @SerializedName("book_id")
    val bookId: Int,

    val content: List<PageContentBlock>
)
