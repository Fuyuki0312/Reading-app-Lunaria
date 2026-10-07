package com.example.lunaria.ui.screens.mainInterface.bookScreens


import com.example.lunaria.data.api.RetrofitClient
import com.example.lunaria.data.model.book.BookPage
import com.example.lunaria.data.model.book.PageContentBlock

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding

import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll

import androidx.compose.material3.Button
import androidx.compose.material3.Text

import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue

import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Text
import androidx.compose.ui.unit.dp


@Composable
fun ReadingScreen(
    bookId: Int,
    onBack: () -> Unit
) {

    var pages by remember {
        mutableStateOf<List<BookPage>>(emptyList())
    }

    var currentPageIndex by remember {
        mutableIntStateOf(0)
    }

    var errorMessage by remember {
        mutableStateOf<String?>(null)
    }

    LaunchedEffect(bookId) {

        try {

            pages =
                RetrofitClient.api.getBookPages(bookId)

        } catch (e: Exception) {

            errorMessage = e.message
            e.printStackTrace()
        }
    }

    if (pages.isEmpty()) {
        Text("Loading...")
        return
    }

    val currentPage = pages[currentPageIndex]

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp)
            .verticalScroll(rememberScrollState())
    ) {
        for (block in currentPage.content) {
            Text(
                text = block.text
            )
        }
    }
}