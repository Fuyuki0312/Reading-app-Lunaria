package com.example.lunaria.navigation

import com.example.lunaria.ui.screens.mainInterface.HomeScreen
import com.example.lunaria.ui.screens.mainInterface.BookDetailScreen
import com.example.lunaria.ui.screens.mainInterface.ExploreScreen
import com.example.lunaria.ui.screens.mainInterface.SettingsScreen
import com.example.lunaria.ui.screens.login.LoginScreen
import com.example.lunaria.ui.screens.login.RegisterScreen
import com.example.lunaria.ui.screens.login.GenrePreferenceSurveyScreen
import com.example.lunaria.ui.screens.login.PreferenceDescriptionSurveyScreen
import com.example.lunaria.data.model.book.Book
import com.example.lunaria.data.model.book.BookID
import com.example.lunaria.data.api.RetrofitClient


import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Search

import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text

import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.remember

import androidx.compose.ui.Modifier

import androidx.navigation3.runtime.entryProvider
import androidx.navigation3.ui.NavDisplay

import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import com.example.lunaria.data.model.user.Username


// ---------- Navigation destinations ----------

data object Home

data object Explore

data object Settings

data object Login

data object Register

data object GenrePreferenceSurvey

data object PreferenceDescriptionSurvey


// ---------- App navigation ----------

@Composable
fun AppNavigation() {

    // | Book recommendation |
    var recommendedBooks by remember {
        mutableStateOf<List<Book>>(emptyList())
    }

    var shouldRecommend by remember {
        mutableStateOf(false)
    } // This is to prevent the LLM from backend to be requested unnecessarily many times
    // Adjust this to true to request the LLM to recommend books


    var errorMessage by remember {
        mutableStateOf<String?>(null)
    }

    // | Screens |
    var isLoggedIn by rememberSaveable {
        mutableStateOf(false)
    }

    val backStack = remember {
        mutableStateListOf<Any>(
            if (isLoggedIn) Home else Login
        )
    }

    val currentScreen = backStack.last()

    // Only show bottom bar and recommend books when a user is at Home or Explore or Settings
    // (when showBottomBar = true)
    val userIsAtMainInterface =
        currentScreen == Home ||
        currentScreen == Explore ||
        currentScreen == Settings


    // | From database |
    var allUsernameFromDatabase by remember {
        mutableStateOf<List<Username>>(emptyList())
    }

    var allBooks by remember {
        mutableStateOf<List<Book>>(emptyList())
    }

    var shouldSearchAllUsername by remember {
        mutableStateOf(true)
    } // search all username at the very moment when users open Lunaria


    // | Login and survey |
    var preferenceDescription by remember {
        mutableStateOf("")
    }


    var username by remember {
        mutableStateOf<String?>(null)
    }

    LaunchedEffect(shouldRecommend) {

        if (shouldRecommend) {
            try {
                val usernameSentToBackend =
                    Username(username = username!!)
                val response = RetrofitClient.api.recommendBooks(usernameSentToBackend)
                recommendedBooks = response

            } catch (e: Exception) {

                errorMessage = e.stackTraceToString()
                e.printStackTrace()
            }

            shouldRecommend = false
        }
    }


    LaunchedEffect(Unit) {
        allBooks = RetrofitClient.api.getAllBooksFromDatabase()
    }


    LaunchedEffect(shouldSearchAllUsername) {
        if (shouldSearchAllUsername){
            allUsernameFromDatabase = RetrofitClient.api.getAllUsernameFromDatabase()
            shouldSearchAllUsername = false
        }
    }


    Scaffold(

        bottomBar = {

            if (userIsAtMainInterface) // Only show bottom bar when a user is at Home or Explore or Settings
            {
                NavigationBar {

                    NavigationBarItem(
                        selected = currentScreen == Home,

                        onClick = {
                            backStack.clear()
                            backStack.add(Home)
                        },

                        icon = {
                            Icon(
                                Icons.Default.Home,
                                contentDescription = "Home"
                            )
                        },

                        label = {
                            Text("Home")
                        }
                    )


                    NavigationBarItem(
                        selected = currentScreen == Explore,

                        onClick = {
                            backStack.clear()
                            backStack.add(Explore)
                        },

                        icon = {
                            Icon(
                                Icons.Default.Search,
                                contentDescription = "Explore"
                            )
                        },

                        label = {
                            Text("Explore")
                        }
                    )


                    NavigationBarItem(
                        selected = currentScreen == Settings,

                        onClick = {
                            backStack.clear()
                            backStack.add(Settings)
                        },

                        icon = {
                            Icon(
                                Icons.Default.AutoAwesome,
                                contentDescription = "Settings"
                            )
                        },

                        label = {
                            Text("Settings")
                        }
                    )
                }
            }
        }

    ) { innerPadding ->

        Box(
            modifier = Modifier.padding(innerPadding)
        ) {

            NavDisplay(

                backStack = backStack,

                entryProvider = entryProvider {


                    entry<Home> {
                        HomeScreen(
                            books = recommendedBooks,
                            username = username!!, // TODO: Hãy lấy username từ login
                            onBookClick = { book ->

                                backStack.add(
                                    BookID(book.id)
                                )
                            }
                        )
                    }

                    entry<BookID> { key ->

                        val book = recommendedBooks.find {
                            it.id == key.bookId
                        }

                        if (book != null) {

                            BookDetailScreen(
                                book = book,

                                onBack = {
                                    backStack.removeLastOrNull()
                                }
                            )

                        } else {

                            Text("Book not found")
                        }
                    }


                    entry<Explore> {
                        ExploreScreen(
                            allBooks = allBooks,
                            onBookClick = { book ->

                                backStack.add(
                                    BookID(book.id)
                                )
                            }
                        )
                    }

                    entry<Settings> {
                        SettingsScreen()
                    }

                    entry<Login> {
                        LoginScreen(
                            onLogin = { usernameToSendToRecommendation ->
                                shouldRecommend = true
                                username = usernameToSendToRecommendation
                                isLoggedIn = true
                                backStack.clear()
                                backStack.add(Home)
                            },
                            onRegister = {
                                backStack.add(Register)
                            },
                            allUsername = allUsernameFromDatabase
                        )
                    }

                    entry<Register> {

                        RegisterScreen(
                            onRegister = { usernameToRegisterGenrePreference ->
                                username = usernameToRegisterGenrePreference
                                isLoggedIn = true
                                backStack.add(GenrePreferenceSurvey)
                            },
                            onBack = {
                                backStack.removeLastOrNull()
                            },
                            allUsername = allUsernameFromDatabase
                        )
                    }

                    entry<GenrePreferenceSurvey> {

                        GenrePreferenceSurveyScreen(
                            username = username!!,
                            onFinish = {
                                backStack.clear()
                                backStack.add(PreferenceDescriptionSurvey)
                            }
                        )
                    }

                    entry<PreferenceDescriptionSurvey> {

                        PreferenceDescriptionSurveyScreen(

                            onFinish = { description ->

                                preferenceDescription = description

                                shouldRecommend = true
                                backStack.clear()
                                backStack.add(Home)
                            },

                            username = username!!
                        )
                    }
                }
            )
        }
    }
}

