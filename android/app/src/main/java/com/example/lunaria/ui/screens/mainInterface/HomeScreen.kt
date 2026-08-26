package com.example.lunaria.ui.screens.mainInterface

import com.example.lunaria.data.model.book.Book


import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding

import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items

import androidx.compose.material3.Card
import androidx.compose.material3.Text

import androidx.compose.runtime.Composable

import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun HomeScreen(
    books: List<Book>,
    username: String,
    onBookClick: (Book) -> Unit
) {


    LazyColumn(
        modifier = Modifier.padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {

        item {
            Text(
                text = "🌙 Lunaria",
                fontSize = 28.sp
            )
        }

        item {
            Text(
                text = "Discover Books",
                fontSize = 20.sp
            )
        }

        items(books) { book ->

            BookCard(
                book = book,
                onClick = {
                    onBookClick(book)
                }
            )
        }
    }
}


@Composable
fun BookCard(
    book: Book,
    onClick: () -> Unit
) {

    Card(
        modifier = Modifier.fillMaxWidth(),
        onClick = onClick
    ) {

        Column(
            modifier = Modifier.padding(16.dp)
        ) {

            Text(
                text = book.title,
                fontSize = 20.sp
            )

            Text(
                text = "by ${book.author}",
                fontSize = 14.sp
            )
        }
    }
}