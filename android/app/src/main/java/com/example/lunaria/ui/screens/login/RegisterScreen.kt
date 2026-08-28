package com.example.lunaria.ui.screens.login


import com.example.lunaria.data.api.RetrofitClient


import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.lunaria.data.model.user.UserAccount
import androidx.compose.runtime.rememberCoroutineScope
import com.example.lunaria.data.model.user.Username
import kotlinx.coroutines.launch


@Composable
fun RegisterScreen(
    onRegister: (String) -> Unit,
    onBack: () -> Unit,
    allUsername: List<Username>
) {

    var username by rememberSaveable {
        mutableStateOf("")
    }

    var password by rememberSaveable {
        mutableStateOf("")
    }

    var confirmPassword by rememberSaveable {
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
            text = "Create your Lunaria account",
            fontSize = 26.sp
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
            visualTransformation = PasswordVisualTransformation(),
            singleLine = true,
            modifier = Modifier.fillMaxWidth()
        )

        OutlinedTextField(
            value = confirmPassword,
            onValueChange = {
                confirmPassword = it
            },
            label = {
                Text("Confirm password")
            },
            visualTransformation = PasswordVisualTransformation(),
            singleLine = true,
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

                } else if (password != confirmPassword) {

                    errorMessage = "Passwords do not match."

                } else {

                    var usernameIsAvailable = true
                    for (usernameFromList in allUsername) {
                        if (username == usernameFromList.username)
                            usernameIsAvailable = false
                    } // this for loop checks if the current username is already taken in database

                    if (usernameIsAvailable) {
                        errorMessage = null

                        coroutineScope.launch {
                            try {
                                val account = UserAccount(username = username, password = password)
                                RetrofitClient.api.registerUserAccount(account = account)

                                onRegister(username)
                            } catch (e: Exception) {

                                errorMessage = e.message
                                e.printStackTrace()
                            }
                        }
                    }

                    else {
                        errorMessage = "This username is already taken."
                    }
                }

            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Register")
        }


        TextButton(
            onClick = {
                onBack()
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Back to login")
        }
    }
}