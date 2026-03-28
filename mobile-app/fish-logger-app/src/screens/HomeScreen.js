import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';

export default function HomeScreen({ navigation }) {
  return (
    <ScrollView style={styles.container}>
      <View style={styles.hero}>
        <Text style={styles.title}>Fish Logger</Text>
        <Text style={styles.subtitle}>
          For researchers and fishers to identify and document fish species
        </Text>
      </View>

      <View style={styles.buttonContainer}>
        <TouchableOpacity
          style={styles.primaryButton}
          onPress={() => navigation.navigate('Camera')}
        >
          <Text style={styles.primaryButtonText}>Take Photo & Identify</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.button}
          onPress={() => navigation.navigate('Submit')}
        >
          <Text style={styles.buttonText}>Submit Catch</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.button}
          onPress={() => navigation.navigate('Database')}
        >
          <Text style={styles.buttonText}>View Database</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.infoSection}>
        <View style={styles.card}>
          <Text style={styles.cardTitle}>For Fishers</Text>
          <Text style={styles.cardText}>
            Photograph your catch and identify species using AI. Works completely offline.
          </Text>
        </View>

        <View style={styles.card}>
          <Text style={styles.cardTitle}>For Researchers</Text>
          <Text style={styles.cardText}>
            Access community-documented fish data. Download complete database for analysis.
          </Text>
        </View>

        <View style={styles.card}>
          <Text style={styles.cardTitle}>Offline First</Text>
          <Text style={styles.cardText}>
            All features work offline. Data syncs automatically when network is available.
          </Text>
        </View>
      </View>

      <View style={styles.speciesSection}>
        <Text style={styles.sectionTitle}>Detectable Species (9)</Text>
        <Text style={styles.speciesText}>• Black Sea Sprat</Text>
        <Text style={styles.speciesText}>• Gilt-Head Bream</Text>
        <Text style={styles.speciesText}>• Hourse Mackerel</Text>
        <Text style={styles.speciesText}>• Red Mullet</Text>
        <Text style={styles.speciesText}>• Red Sea Bream</Text>
        <Text style={styles.speciesText}>• Sea Bass</Text>
        <Text style={styles.speciesText}>• Shrimp</Text>
        <Text style={styles.speciesText}>• Striped Red Mullet</Text>
        <Text style={styles.speciesText}>• Trout</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fafffa',
  },
  hero: {
    backgroundColor: '#e8f5e8',
    padding: 30,
    borderBottomWidth: 3,
    borderBottomColor: '#d4f1d4',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#1a3a1a',
    textAlign: 'center',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: '#2d5a2d',
    textAlign: 'center',
  },
  buttonContainer: {
    padding: 20,
  },
  primaryButton: {
    backgroundColor: '#b8e6b8',
    padding: 18,
    borderWidth: 3,
    borderColor: '#7cb87c',
    marginBottom: 15,
  },
  primaryButtonText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1a3a1a',
    textAlign: 'center',
  },
  button: {
    backgroundColor: '#e8f5e8',
    padding: 15,
    borderWidth: 2,
    borderColor: '#b8e6b8',
    marginBottom: 10,
  },
  buttonText: {
    fontSize: 16,
    color: '#1a3a1a',
    textAlign: 'center',
    fontWeight: '600',
  },
  infoSection: {
    padding: 20,
  },
  card: {
    backgroundColor: '#e8f5e8',
    padding: 20,
    borderWidth: 3,
    borderColor: '#d4f1d4',
    marginBottom: 15,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1a3a1a',
    marginBottom: 8,
  },
  cardText: {
    fontSize: 14,
    color: '#2d5a2d',
    lineHeight: 20,
  },
  speciesSection: {
    padding: 20,
    backgroundColor: '#e8f5e8',
    borderTopWidth: 3,
    borderTopColor: '#d4f1d4',
    marginTop: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1a3a1a',
    marginBottom: 15,
  },
  speciesText: {
    fontSize: 14,
    color: '#2d5a2d',
    paddingVertical: 3,
  },
});
