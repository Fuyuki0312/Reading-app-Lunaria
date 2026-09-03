package com.example.lunaria.ui.screens.login

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.OutlinedTextField
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.runtime.saveable.rememberSaveable

import androidx.compose.material3.Button
import androidx.compose.material3.Checkbox
import androidx.compose.material3.Text

import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope

import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.lunaria.data.api.RetrofitClient
import com.example.lunaria.data.model.user.UsernameAndPreferences
import kotlinx.coroutines.launch



/*
    Note: This screen is built not only to conduct a survey, but also to
          enable users to adjust their surveyed reading preferences.
*/
@Composable
fun GenrePreferenceSurveyScreen(
    username: String,
    initialSelectedGenres: List<String> = emptyList(),
    onFinish: (MutableList<String>) -> Unit
) {

    val predefinedGenres = listOf(
        "Adventure",
        "Comedy",
        "Fantasy",
        "Science Fiction",
        "Mystery",
        "Romance",
        "Romcom",
        "Historical Fiction",
        "Self-help"
    )

    val genres = predefinedGenres + "Others"

    val oldOtherGenre =
        initialSelectedGenres.firstOrNull {
            it !in predefinedGenres
        }

    val selectedGenres = remember(initialSelectedGenres) {

        mutableStateListOf<String>().apply {

            addAll(
                initialSelectedGenres.filter {
                    it in predefinedGenres
                }
            )

            if (oldOtherGenre != null) {
                add("Others")
            }
        }
    }

    var otherGenre by rememberSaveable(
        initialSelectedGenres
    ) {
        mutableStateOf(
            oldOtherGenre ?: ""
        )
    }

    var errorMessage by rememberSaveable {
        mutableStateOf<String?>(null)
    }

    val coroutineScope = rememberCoroutineScope()


    LazyColumn(
        modifier = Modifier.padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {

        item {

            Text(
                text = "What do you enjoy reading?",
                fontSize = 26.sp
            )
        }

        item {

            Text(
                text = "Choose the genres you like so Lunaria can recommend books for you."
            )
        }


        items(genres) { genre ->


            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {

                Checkbox(
                    checked = genre in selectedGenres,

                    onCheckedChange = { isChecked ->

                        if (isChecked) {

                            selectedGenres.add(genre)

                        } else {

                            selectedGenres.remove(genre)
                        }
                    }
                )

                Text(
                    text = genre
                )
            }
        }

        if ("Others" in selectedGenres) {

            item {

                OutlinedTextField(
                    value = otherGenre,

                    onValueChange = {
                        otherGenre = it
                    },

                    label = {
                        Text("Enter another genre")
                    },

                    placeholder = {
                        Text("e.g. Dark Academia")
                    },

                    singleLine = true,

                    modifier = Modifier.fillMaxWidth()
                )
            }
        }

        if (errorMessage != null) {
            item {
                Text(
                    text = errorMessage!!
                )
            }
        }

        item {

            Button(
                onClick = {
                    val finalGenres = selectedGenres
                        .filter { it != "Others" }
                        .toMutableList()

                    if (
                        "Others" in selectedGenres &&
                        otherGenre.isNotBlank()
                    ) {
                        finalGenres.add(otherGenre.trim())
                    }

                    coroutineScope.launch {
                        try {

                            val genrePreferenceToRegister = UsernameAndPreferences(
                                username = username,
                                genres = finalGenres
                            )

                            RetrofitClient.api.registerGenrePreferences(genrePreferenceToRegister)
                            onFinish(finalGenres)
                        } catch (e: Exception) {
                            errorMessage = e.message
                            e.printStackTrace()
                        }
                    }

                },

                enabled =
                    selectedGenres.any { it != "Others" } ||
                        (
                            "Others" in selectedGenres &&
                            otherGenre.isNotBlank()
                        ),

                modifier = Modifier.fillMaxWidth()
            ) {

                Text("Continue")
            }
        }
    }
}