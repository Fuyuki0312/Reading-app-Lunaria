package com.example.lunaria.data.model.book

data class PageContentBlock(
    val text: String,
    val type: String,
    val align: String,
    val bold: Boolean = false
)