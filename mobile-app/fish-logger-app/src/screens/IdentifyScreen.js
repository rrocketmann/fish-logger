import React, { useState } from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity, ActivityIndicator, ScrollView } from 'react-native';
import axios from 'axios';

const SERVER_URL = 'http://100.118.217.22:5002';

export default function IdentifyScreen({ route, navigation }) {
  const { photoUri } = route.params;
  const [identifying, setIdentifying] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const identifyFish = async () => {
    setIdentifying(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('fish_image', {
        uri: photoUri,
        type: 'image/jpeg',
        name: 'photo.jpg'
      });

      const response = await axios.post(`${SERVER_URL}/api/identify`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResults(response.data.predictions);
    } catch (err) {
      setError('Unable to identify. Please check your connection or try again later.');
      console.error(err);
    } finally {
      setIdentifying(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.imageContainer}>
        <Image source={{ uri: photoUri }} style={styles.image} />
      </View>

      {!results && !identifying && (
        <TouchableOpacity
          style={styles.identifyButton}
          onPress={identifyFish}
        >
          <Text style={styles.identifyButtonText}>Identify This Fish</Text>
        </TouchableOpacity>
      )}

      {identifying && (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#b8e6b8" />
          <Text style={styles.loadingText}>Analyzing image...</Text>
        </View>
      )}

      {error && (
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>{error}</Text>
          <Text style={styles.offlineNote}>
            Note: AI identification requires internet connection. You can still submit the catch with "Unknown" species.
          </Text>
        </View>
      )}

      {results && (
        <View style={styles.resultsContainer}>
          <Text style={styles.resultsTitle}>Top 5 Predictions</Text>
          {results.map((result, index) => (
            <View key={index} style={styles.predictionItem}>
              <View style={styles.progressBarContainer}>
                <View 
                  style={[styles.progressBar, { width: `${result.probability * 100}%` }]} 
                />
              </View>
              <View style={styles.predictionInfo}>
                <Text style={styles.speciesName}>{result.species}</Text>
                <Text style={styles.probability}>{(result.probability * 100).toFixed(1)}%</Text>
              </View>
            </View>
          ))}

          <TouchableOpacity
            style={styles.submitButton}
            onPress={() => navigation.navigate('Submit', { 
              photoUri, 
              suggestedSpecies: results[0].species 
            })}
          >
            <Text style={styles.submitButtonText}>Submit This Catch</Text>
          </TouchableOpacity>
        </View>
      )}

      <TouchableOpacity
        style={styles.backButton}
        onPress={() => navigation.goBack()}
      >
        <Text style={styles.backButtonText}>Take Another Photo</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fafffa',
  },
  imageContainer: {
    backgroundColor: '#e8f5e8',
    padding: 20,
    borderBottomWidth: 3,
    borderBottomColor: '#d4f1d4',
  },
  image: {
    width: '100%',
    height: 300,
    resizeMode: 'contain',
    borderWidth: 2,
    borderColor: '#b8e6b8',
  },
  identifyButton: {
    margin: 20,
    backgroundColor: '#b8e6b8',
    padding: 18,
    borderWidth: 3,
    borderColor: '#7cb87c',
  },
  identifyButtonText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1a3a1a',
    textAlign: 'center',
  },
  loadingContainer: {
    padding: 40,
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 15,
    fontSize: 16,
    color: '#2d5a2d',
  },
  errorContainer: {
    margin: 20,
    padding: 20,
    backgroundColor: '#ffd4d4',
    borderWidth: 2,
    borderColor: '#ffb3b3',
  },
  errorText: {
    fontSize: 16,
    color: '#4a0000',
    marginBottom: 10,
  },
  offlineNote: {
    fontSize: 14,
    color: '#4a0000',
  },
  resultsContainer: {
    margin: 20,
    padding: 20,
    backgroundColor: '#e8f5e8',
    borderWidth: 3,
    borderColor: '#d4f1d4',
  },
  resultsTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1a3a1a',
    marginBottom: 20,
  },
  predictionItem: {
    backgroundColor: '#fff',
    padding: 15,
    borderWidth: 2,
    borderColor: '#b8e6b8',
    marginBottom: 10,
  },
  progressBarContainer: {
    height: 30,
    backgroundColor: '#fafffa',
    borderWidth: 2,
    borderColor: '#d4f1d4',
    marginBottom: 10,
  },
  progressBar: {
    height: '100%',
    backgroundColor: '#b8e6b8',
  },
  predictionInfo: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  speciesName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1a3a1a',
  },
  probability: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2d5a2d',
  },
  submitButton: {
    marginTop: 20,
    backgroundColor: '#b8e6b8',
    padding: 15,
    borderWidth: 3,
    borderColor: '#7cb87c',
  },
  submitButtonText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1a3a1a',
    textAlign: 'center',
  },
  backButton: {
    margin: 20,
    backgroundColor: '#e8f5e8',
    padding: 15,
    borderWidth: 2,
    borderColor: '#b8e6b8',
  },
  backButtonText: {
    fontSize: 16,
    color: '#1a3a1a',
    textAlign: 'center',
    fontWeight: '600',
  },
});
