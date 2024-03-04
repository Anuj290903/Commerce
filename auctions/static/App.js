import React from 'react';
import { createRoot } from 'react-dom/client';
import Main from './main.jsx'; // Assuming your Main component is in a separate file

// Log a message to verify execution
console.log('Hello from App.js');

// Create a root instance using createRoot and render your Main component
const root = createRoot(document.getElementById('root'));
root.render(<Main />);
