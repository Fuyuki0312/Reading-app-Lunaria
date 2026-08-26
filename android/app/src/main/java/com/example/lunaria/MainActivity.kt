package com.example.lunaria

import com.example.lunaria.navigation.AppNavigation


import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.example.lunaria.ui.theme.LunariaTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        enableEdgeToEdge()
        setContent {
            LunariaTheme {
                AppNavigation()
            }
        }
    }
}



