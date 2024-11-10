// components/WeatherCharts.jsx
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import styled from 'styled-components';

const ChartsContainer = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  padding: 1rem;
  
  @media (max-width: 1200px) {
    grid-template-columns: 1fr;
  }
`;

const ChartWrapper = styled.div`
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
`;

export const WeatherCharts = ({ data }) => {
  if (!data || !data.daily_statistics) return null;

  const prepareChartData = () => {
    return Object.entries(data.daily_statistics).map(([date, stats]) => ({
      date,
      // Temperature
      tempMin: stats.temperature.min,
      tempMax: stats.temperature.max,
      tempAvg: stats.temperature.avg,
      // Humidity
      humidityMin: stats.humidity.min,
      humidityMax: stats.humidity.max,
      humidityAvg: stats.humidity.avg,
      // Pressure
      pressureMin: stats.pressure.min,
      pressureMax: stats.pressure.max,
      pressureAvg: stats.pressure.avg,
      // Wind Speed
      windMin: stats.wind_speed.min,
      windMax: stats.wind_speed.max,
      windAvg: stats.wind_speed.avg,
    }));
  };

  const chartData = prepareChartData();

  return (
    <ChartsContainer>
      <ChartWrapper>
        <h3>Температура</h3>
        <LineChart width={500} height={300} data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis domain={['dataMin - 1', 'dataMax + 1']} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="tempMin" stroke="#8884d8" name="Мин" />
          <Line type="monotone" dataKey="tempMax" stroke="#82ca9d" name="Макс" />
          <Line type="monotone" dataKey="tempAvg" stroke="#ffc658" name="Средняя" />
        </LineChart>
      </ChartWrapper>

      <ChartWrapper>
        <h3>Влажность</h3>
        <LineChart width={500} height={300} data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis domain={[0, 100]} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="humidityMin" stroke="#8884d8" name="Мин" />
          <Line type="monotone" dataKey="humidityMax" stroke="#82ca9d" name="Макс" />
          <Line type="monotone" dataKey="humidityAvg" stroke="#ffc658" name="Средняя" />
        </LineChart>
      </ChartWrapper>

      <ChartWrapper>
        <h3>Давление</h3>
        <LineChart width={500} height={300} data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis domain={['dataMin - 1', 'dataMax + 1']} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="pressureMin" stroke="#8884d8" name="Мин" />
          <Line type="monotone" dataKey="pressureMax" stroke="#82ca9d" name="Макс" />
          <Line type="monotone" dataKey="pressureAvg" stroke="#ffc658" name="Средняя" />
        </LineChart>
      </ChartWrapper>

      <ChartWrapper>
        <h3>Скорость ветра</h3>
        <LineChart width={500} height={300} data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis domain={['dataMin - 1', 'dataMax + 1']} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="windMin" stroke="#8884d8" name="Мин" />
          <Line type="monotone" dataKey="windMax" stroke="#82ca9d" name="Макс" />
          <Line type="monotone" dataKey="windAvg" stroke="#ffc658" name="Средняя" />
        </LineChart>
      </ChartWrapper>
    </ChartsContainer>
  );
};