import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Provider as ReduxProvider } from 'react-redux';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { store } from './store';
import { theme } from './theme';
import LoginScreen from './screens/LoginScreen';
import DashboardScreen from './screens/DashboardScreen';
import AlertsScreen from './screens/AlertsScreen';
import TeamsScreen from './screens/TeamsScreen';
import UsersScreen from './screens/UsersScreen';
import ReportsScreen from './screens/ReportsScreen';
import SettingsScreen from './screens/SettingsScreen';
import PrivateRoute from './components/PrivateRoute';

const Stack = createNativeStackNavigator();

const App: React.FC = () => {
  return (
    <ReduxProvider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <NavigationContainer>
          <Stack.Navigator
            initialRouteName="Login"
            screenOptions={{
              headerStyle: {
                backgroundColor: theme.palette.primary.main,
              },
              headerTintColor: theme.palette.primary.contrastText,
              headerTitleStyle: {
                fontWeight: 'bold',
              },
            }}
          >
            <Stack.Screen
              name="Login"
              component={LoginScreen}
              options={{ headerShown: false }}
            />
            <Stack.Screen
              name="Dashboard"
              component={PrivateRoute(DashboardScreen)}
              options={{ title: 'Dashboard' }}
            />
            <Stack.Screen
              name="Alerts"
              component={PrivateRoute(AlertsScreen)}
              options={{ title: 'Alerts' }}
            />
            <Stack.Screen
              name="Teams"
              component={PrivateRoute(TeamsScreen)}
              options={{ title: 'Teams' }}
            />
            <Stack.Screen
              name="Users"
              component={PrivateRoute(UsersScreen)}
              options={{ title: 'Users' }}
            />
            <Stack.Screen
              name="Reports"
              component={PrivateRoute(ReportsScreen)}
              options={{ title: 'Reports' }}
            />
            <Stack.Screen
              name="Settings"
              component={PrivateRoute(SettingsScreen)}
              options={{ title: 'Settings' }}
            />
          </Stack.Navigator>
        </NavigationContainer>
      </ThemeProvider>
    </ReduxProvider>
  );
};

export default App; 