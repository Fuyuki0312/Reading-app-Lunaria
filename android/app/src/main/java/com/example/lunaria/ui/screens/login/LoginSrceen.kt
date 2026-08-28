package com.example.lunaria.ui.screens.login


import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding

import androidx.compose.material3.Button
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton

import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue

import androidx.compose.runtime.saveable.rememberSaveable

import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.lunaria.data.api.RetrofitClient
import com.example.lunaria.data.model.user.Username
import kotlinx.coroutines.launch


@Composable
fun LoginScreen(
    onLogin: (username: String) -> Unit,
    onRegister: () -> Unit,
    allUsername: List<Username>
) {

    var username by rememberSaveable {
        mutableStateOf("")
    }

    var password by rememberSaveable {
        mutableStateOf("")
    }

    var errorMessage by rememberSaveable {
        mutableStateOf<String?>(null)
    }

    val coroutineScope = rememberCoroutineScope()


    Column(
        modifier = Modifier.padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {

        Text(
            text = "🌙 Lunaria",
            fontSize = 32.sp
        )

        Text(
            text = "Welcome back",
            fontSize = 22.sp
        )


        OutlinedTextField(
            value = username,

            onValueChange = {
                username = it
            },

            label = {
                Text("Username")
            },

            singleLine = true,

            modifier = Modifier.fillMaxWidth()
        )


        OutlinedTextField(
            value = password,

            onValueChange = {
                password = it
            },

            label = {
                Text("Password")
            },

            singleLine = true,

            visualTransformation = PasswordVisualTransformation(),

            modifier = Modifier.fillMaxWidth()
        )


        if (errorMessage != null) {
            Text(
                text = errorMessage!!
            )
        }


        Button(
            onClick = {

                if (username.isBlank() || password.isBlank()) {

                    errorMessage = "Username and password cannot be empty."

                } else {
                    var usernameIsFound = false

                    for (tempUsername in allUsername) {
                        if (tempUsername.username == username) {
                            usernameIsFound = true
                            break
                        }
                    }

                    if (usernameIsFound) {
                        coroutineScope.launch {
                            val usernameToSendRequestToBackend = Username(username = username)
                            val account = RetrofitClient.api.getPasswordFromDatabaseByUsername(
                                username = usernameToSendRequestToBackend
                            )

                            if (account.password == password) {
                                onLogin(account.username)
                            } else {
                                errorMessage = "Username or password is incorrect."
                            }
                        }
                    } else {
                        errorMessage = "Username or password is incorrect."
                    }
                }
            },

            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Login")
        }


        TextButton(
            onClick = {
                onRegister()
            },

            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Create an account")
        }
    }
}