// App.jsx
import React from 'react';
import styled from 'styled-components';
import { useStore } from './store';
import { FileUpload } from './components/FileUpload';
import { WeatherCharts } from './components/WeatherCharts';

const AppContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #f5f5f5;
`;

const Header = styled.header`
  text-align: center;
  margin-bottom: 2rem;
`;

const App = () => {
  const { weatherData, setWeatherData } = useStore();

  const handleFileUpload = (data) => {
    setWeatherData(data);
  };

  return (
    <AppContainer>
      <Header>
        <h1>Визуализация погодных данных</h1>
        <p>Загрузите JSON файл с данными о погоде</p>
      </Header>
      <FileUpload onFileUpload={handleFileUpload} />
      {weatherData && <WeatherCharts data={weatherData} />}
    </AppContainer>
  );
};

export default App;