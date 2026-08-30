package com.example.lunaria.ui.screens.mainInterface

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.ListItem
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier


@Composable
fun SettingsScreen(
    onAdjustReadingPreferences: () -> Unit
) {

    Column {

        Text("Settings")

        HorizontalDivider()

        ListItem(
            headlineContent = {
                Text("Adjust your reading preferences")
            },

            supportingContent = {
                Text("Change your favorite genres and preference description")
            },

            modifier = Modifier
                .fillMaxWidth()
                .clickable {
                    onAdjustReadingPreferences()
                }
        )

        HorizontalDivider()
    }
}