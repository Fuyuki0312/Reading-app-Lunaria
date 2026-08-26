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
import androidx.compose.runtime.setValue

import androidx.compose.runtime.saveable.rememberSaveable

import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp


@Composable
fun LoginScreen(
    onLogin: () -> Unit,
    onRegister: () -> Unit
) {

    var userName by rememberSaveable {
        mutableStateOf("")
    }

    var password by rememberSaveable {
        mutableStateOf("")
    }


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
            value = userName,

            onValueChange = {
                userName = it
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


        Button(
            onClick = {
                onLogin()
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