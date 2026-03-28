import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import HomeScreen from './src/screens/HomeScreen';
import CameraScreen from './src/screens/CameraScreen';
import IdentifyScreen from './src/screens/IdentifyScreen';
import SubmitScreen from './src/screens/SubmitScreen';
import DatabaseScreen from './src/screens/DatabaseScreen';
import { DatabaseProvider } from './src/context/DatabaseContext';

const Stack = createStackNavigator();

export default function App() {
  return (
    <DatabaseProvider>
      <NavigationContainer>
        <StatusBar style="dark" />
        <Stack.Navigator
          initialRouteName="Home"
          screenOptions={{
            headerStyle: {
              backgroundColor: '#d4f1d4',
            },
            headerTintColor: '#1a3a1a',
            headerTitleStyle: {
              fontWeight: 'bold',
            },
          }}
        >
          <Stack.Screen 
            name="Home" 
            component={HomeScreen}
            options={{ title: 'Fish Logger' }}
          />
          <Stack.Screen 
            name="Camera" 
            component={CameraScreen}
            options={{ title: 'Take Photo' }}
          />
          <Stack.Screen 
            name="Identify" 
            component={IdentifyScreen}
            options={{ title: 'Identify Fish' }}
          />
          <Stack.Screen 
            name="Submit" 
            component={SubmitScreen}
            options={{ title: 'Submit Catch' }}
          />
          <Stack.Screen 
            name="Database" 
            component={DatabaseScreen}
            options={{ title: 'Database' }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </DatabaseProvider>
  );
}
