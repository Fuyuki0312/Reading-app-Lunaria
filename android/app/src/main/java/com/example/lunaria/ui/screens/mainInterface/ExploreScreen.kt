package com.example.lunaria.ui.screens.mainInterface

import com.example.lunaria.data.model.book.Book


import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.Icon
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.Button
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.ui.unit.dp

import androidx.compose.ui.Modifier
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable

@Composable
fun ExploreScreen(
    allBooks: List<Book>,
    onBookClick: (Book) -> Unit
) {

    var searchText by rememberSaveable {
        mutableStateOf("")
    }

    var searchQuery by rememberSaveable {
        mutableStateOf("")
    }


    val searchedBooks =
        if (searchQuery.isBlank()) {
            emptyList<Book>()
        } else {
            searchBook(allBooks = allBooks, query = searchQuery)
        }


    LazyColumn {

        item {

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                OutlinedTextField(
                    value = searchText,

                    onValueChange = {
                        searchText = it
                    },

                    placeholder = {
                        Text("Search for a book...")
                    },

                    leadingIcon = {
                        Icon(
                            Icons.Default.Search,
                            contentDescription = "Search"
                        )
                    },

                    singleLine = true,

                    modifier = Modifier.weight(1f)
                    )

                Button(
                    onClick = {
                        searchQuery = searchText
                    }
                ) {
                    Text("Search")
                }
            }
        }

        items(searchedBooks) { book ->

            BookCard(
                book = book,
                onClick = {
                    onBookClick(book)
                }
            )

        }
    }
}

 // TODO: Use this fun
fun searchBook (allBooks: List<Book>, query: String): MutableList<Book> {

    val filtered_books = mutableListOf<Book>()

    for (book in allBooks) {

        if (book.title.contains(query, ignoreCase = true)) {
            filtered_books.add(book)
        }

    }

    return filtered_books
}