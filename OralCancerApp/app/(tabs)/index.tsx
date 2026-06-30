import { WebView } from 'react-native-webview';
import { StyleSheet, View, ActivityIndicator } from 'react-native';
import { useState } from 'react';

export default function HomeScreen() {
  const [loading, setLoading] = useState(true);

  return (
    <View style={styles.container}>
      <WebView 
        source={{ uri: 'https://oralcancer1-production.up.railway.app' }} 
        style={styles.webview}
        onLoadStart={() => setLoading(true)}
        onLoadEnd={() => setLoading(false)}
        allowsFullscreenVideo={true}
        domStorageEnabled={true}
        javaScriptEnabled={true}
        originWhitelist={['*']}
        allowFileAccess={true}
        scalesPageToFit={true}
      />
      {loading && (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#3b82f6" />
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0f172a',
  },
  webview: {
    flex: 1,
  },
  loadingContainer: {
    position: 'absolute',
    left: 0,
    right: 0,
    top: 0,
    bottom: 0,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#0f172a',
  },
});