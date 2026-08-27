package com.example.lunaria.ui.screens.login


import com.example.lunaria.data.model.user.PreferenceDescription


import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding

import androidx.compose.material3.Button
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text

import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue

import androidx.compose.runtime.saveable.rememberSaveable

import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.lunaria.data.api.RetrofitClient
import kotlinx.coroutines.launch


@Composable
fun PreferenceDescriptionSurveyScreen(
    onFinish: (String) -> Unit,
    username: String
) {

    var preferenceDescription by rememberSaveable {
        mutableStateOf("")
    }

    val coroutineScope = rememberCoroutineScope()

    Column(
        modifier = Modifier.padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {


        Text(
            text = "If there is anything you want Lunaria to know to recommend books for you:",
            fontSize = 26.sp
        )

        OutlinedTextField(
            value = preferenceDescription,

            onValueChange = {
                preferenceDescription = it
            },

            placeholder = {
                Text(
                    "Example: I enjoy fantasy stories with magic, exploration, and mysterious ancient worlds..."
                )
            },

            minLines = 5,
            maxLines = 8,

            modifier = Modifier.fillMaxWidth()
        )

        Button(
            onClick = {

                coroutineScope.launch {

                    val descriptionToRegister = PreferenceDescription(
                            description = preferenceDescription.trim(),
                            username = username
                    )

                    RetrofitClient.api.registerPreferenceDescription(descriptionToRegister)

                    onFinish(preferenceDescription.trim())
                }

            },

            modifier = Modifier.fillMaxWidth()
        ) {

            Text("Finish")
        }
    }
}