package com.fleetsmart.conductor.ui.navigation

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.fleetsmart.conductor.ui.screens.*
import com.fleetsmart.conductor.ui.theme.AppColors
import androidx.compose.ui.unit.dp

sealed class Screen(val route: String, val title: String, val icon: ImageVector) {
    object Login : Screen("login", "Login", Icons.Default.Lock)
    object Routes : Screen("routes", "Rutas", Icons.Default.List)
    object ActiveRoute : Screen("active_route", "Ruta Activa", Icons.Default.Map)
    object Incidents : Screen("incidents", "Incidencias", Icons.Default.Warning)
    object Profile : Screen("profile", "Perfil", Icons.Default.Person)
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun FleetDriverApp(
    onIniciarRuta: () -> Unit,
    onDetenerRuta: () -> Unit
) {
    val navController = rememberNavController()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentDestination = navBackStackEntry?.destination
    val currentRoute = currentDestination?.route

    // Función para navegar de forma segura
    fun navigateToTab(route: String) {
        navController.navigate(route) {
            popUpTo(navController.graph.findStartDestination().id) {
                saveState = true
            }
            launchSingleTop = true
            restoreState = true
        }
    }

    // LÓGICA DE VISIBILIDAD DE BARRAS
    // Ocultamos barras en Login y en ActiveRoute
    val showBars = currentRoute != Screen.Login.route && currentRoute != Screen.ActiveRoute.route

    Scaffold(
        modifier = Modifier.fillMaxSize(),
        containerColor = AppColors.Background,
        topBar = {
            if (showBars) {
                TopAppBar(
                    title = { Text("FleetSmart") },
                    colors = TopAppBarDefaults.topAppBarColors(
                        containerColor = AppColors.Card,
                        titleContentColor = AppColors.Foreground
                    ),
                    actions = {
                        IconButton(onClick = { navigateToTab(Screen.Profile.route) }) {
                            Surface(
                                shape = MaterialTheme.shapes.small,
                                color = AppColors.Primary,
                                modifier = Modifier.size(40.dp)
                            ) {
                                Box(contentAlignment = androidx.compose.ui.Alignment.Center) {
                                    Text(
                                        text = "CM",
                                        style = MaterialTheme.typography.labelMedium,
                                        color = AppColors.PrimaryForeground
                                    )
                                }
                            }
                        }
                    }
                )
            }
        },
        bottomBar = {
            if (showBars) {
                NavigationBar(
                    containerColor = AppColors.Card,
                    contentColor = AppColors.Foreground
                ) {
                    val items = listOf(
                        Screen.Routes,
                        Screen.Incidents,
                        Screen.Profile
                    )

                    items.forEach { screen ->
                        val selected = currentDestination?.hierarchy?.any {
                            it.route == screen.route
                        } == true

                        NavigationBarItem(
                            icon = { Icon(screen.icon, contentDescription = screen.title) },
                            label = { Text(screen.title, style = MaterialTheme.typography.labelSmall) },
                            selected = selected,
                            onClick = { navigateToTab(screen.route) },
                            colors = NavigationBarItemDefaults.colors(
                                selectedIconColor = AppColors.Primary,
                                selectedTextColor = AppColors.Primary,
                                indicatorColor = AppColors.Primary.copy(alpha = 0.1f),
                                unselectedIconColor = AppColors.MutedForeground,
                                unselectedTextColor = AppColors.MutedForeground
                            )
                        )
                    }
                }
            }
        }
    ) { paddingValues ->
        NavigationGraph(
            navController = navController,
            onIniciarRuta = onIniciarRuta,
            onDetenerRuta = onDetenerRuta,
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        )
    }
}

@Composable
fun NavigationGraph(
    navController: NavHostController,
    onIniciarRuta: () -> Unit,
    onDetenerRuta: () -> Unit,
    modifier: Modifier = Modifier
) {
    NavHost(
        navController = navController,
        startDestination = Screen.Login.route,
        modifier = modifier
    ) {
        // --- PANTALLA DE LOGIN ---
        composable(Screen.Login.route) {
            LoginScreen(
                onLoginSuccess = {
                    // Al loguearse, vamos a rutas y borramos el login del historial (backstack)
                    // para que al dar "atrás" no vuelva al login.
                    navController.navigate(Screen.Routes.route) {
                        popUpTo(Screen.Login.route) { inclusive = true }
                    }
                }
            )
        }

        composable(Screen.Routes.route) {
            MyRoutesScreen(
                onStartRoute = { _ ->
                    onIniciarRuta() // 🚀 INICIAMOS EL GPS AQUÍ
                    navController.navigate(Screen.ActiveRoute.route)
                }
            )
        }

        composable(Screen.ActiveRoute.route) {
            ActiveRouteScreen(
                onBack = {
                    onDetenerRuta() // 🛑 DETENEMOS EL GPS AL SALIR DE LA RUTA
                    navController.popBackStack()
                }
            )
        }

        composable(Screen.Incidents.route) {
            ReportIncidentScreen()
        }

        composable(Screen.Profile.route) {
            ProfileScreen()
        }
    }
}