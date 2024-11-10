import { create } from 'zustand';

export const useStore = create((set) => ({
  weatherData: null,
  setWeatherData: (data) => set({ weatherData: data }),
}));