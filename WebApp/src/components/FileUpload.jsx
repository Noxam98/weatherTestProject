// components/FileUpload.jsx
import React from 'react';
import styled from 'styled-components';

const UploadContainer = styled.div`
  padding: 2rem;
  border: 2px dashed #ccc;
  border-radius: 8px;
  text-align: center;
  margin-bottom: 2rem;
`;

const UploadButton = styled.button`
  padding: 0.5rem 1rem;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 1rem;
  
  &:hover {
    background-color: #357abd;
  }
`;

const ErrorMessage = styled.div`
  color: #ff4444;
  margin-top: 1rem;
  font-size: 0.9rem;
`;

export const FileUpload = ({ onFileUpload }) => {
  const handleFileInput = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const data = JSON.parse(e.target.result);
        onFileUpload(data);
      } catch (error) {
        alert('Ошибка при чтении файла');
      }
    };
    reader.readAsText(file);
  };

  return (
    <UploadContainer>
      <h3>Загрузите JSON файл с данными о погоде</h3>
      <input
        type="file"
        accept=".json"
        onChange={handleFileInput}
        style={{ display: 'none' }}
        id="fileInput"
      />
      <UploadButton onClick={() => document.getElementById('fileInput').click()}>
        Выбрать файл
      </UploadButton>
    </UploadContainer>
  );
};