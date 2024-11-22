// src/App.js

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import AddEmployee from './components/AddEmployee';
import UpdateEmployee from './components/UpdateEmployee';
import BulkUpdate from './components/BulkUpdate';
import SearchEmployees from './components/SearchEmployees'; // Import SearchEmployees component

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/add-employee" element={<AddEmployee />} />
        <Route path="/update-employee/:id" element={<UpdateEmployee />} />
        <Route path="/bulk-update" element={<BulkUpdate />} />
        <Route path="/search" element={<SearchEmployees />} /> {/* Route for SearchEmployees component */}
      </Routes>
    </Router>
  );
}

export default App;
