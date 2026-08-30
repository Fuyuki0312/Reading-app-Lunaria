package com.example.lunaria.ui.screens.mainInterface

import com.example.lunaria.data.model.book.Book


import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding

import androidx.compose.material3.Button
import androidx.compose.material3.Text

import androidx.compose.runtime.Composable

import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp


@Composable
fun BookDetailScreen(
    book: Book,
    onBack: () -> Unit
) {

    Column(
        modifier = Modifier
            .padding(24.dp)
            .verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {

        // Title
        Text(
            text = book.title,
            fontSize = 28.sp
        )

        // Author
        Text(
            text = "Author: ${book.author}",
            fontSize = 16.sp
        )

        // Genres
        val genres = book.genres.joinToString(", ")
        
        Text(
            text = "Genres: $genres",
            fontSize = 16.sp
        )

        // Published year
        Text(
            text = "Published: ${book.publishedYear}",
            fontSize = 16.sp
        )

        // Description
        Text(
            text = "Description",
            fontSize = 20.sp
        )

        Text(
            text = book.description,
            fontSize = 16.sp
        )

        // Back button
        Button(
            onClick = onBack,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Back")
        }
    }
}
