// src/components/BulkUpdate.js

import React, { useState } from 'react';

const BulkUpdate = () => {
  const [formData, setFormData] = useState({
    updateType: '',
    updateValue: '',
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Replace with your form submission logic (e.g., API call)
    console.log('Bulk update submitted:', formData);
    // Reset form fields after submission
    setFormData({
      updateType: '',
      updateValue: '',
    });
  };

  return (
    <div>
      <h2>Bulk Update Employees</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Update Type:
          <input type="text" name="updateType" value={formData.updateType} onChange={handleChange} />
        </label>
        <br />
        <label>
          Update Value:
          <input type="text" name="updateValue" value={formData.updateValue} onChange={handleChange} />
        </label>
        <br />
        <button type="submit">Bulk Update</button>
      </form>
    </div>
  );
};

export default BulkUpdate;
