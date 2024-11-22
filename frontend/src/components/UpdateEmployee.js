import React, { useState, useEffect } from 'react';
import axios from 'axios';

const UpdateEmployee = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [formData, setFormData] = useState({
    user: {
      username: '',
      first_name: '',
      last_name: '',
    },
    employer: '',
    position: '',
    department: '',
    year_started: '',
    year_left: '',
  });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [employeeId, setEmployeeId] = useState(null);

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleSearchSubmit = async (e) => {
    e.preventDefault();
    if (!searchQuery) {
      setError('Search query cannot be empty.');
      return;
    }
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/employees/by-employer/', {
        params: { username: searchQuery }
      });
      const employee = response.data;
      console.log('Fetched Employee:', employee); // Debug log
      setFormData({
        user: {
          username: employee.user.username || '',
          first_name: employee.user.first_name || '',
          last_name: employee.user.last_name || '',
        },
        employer: employee.employer || '',
        position: employee.position || '',
        department: employee.department || '',
        year_started: employee.year_started || '',
        year_left: employee.year_left || '',
      });
      setEmployeeId(employee.id);
      setMessage('Employee found.');
      setError('');
    } catch (error) {
      setError(error.response ? error.response.data.error : 'Error fetching employee.');
      setMessage('');
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name.startsWith('user.')) {
      const userField = name.split('.')[1];
      setFormData(prevFormData => ({
        ...prevFormData,
        user: {
          ...prevFormData.user,
          [userField]: value,
        },
      }));
    } else {
      setFormData(prevFormData => ({
        ...prevFormData,
        [name]: value,
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!employeeId) {
      setError('No employee selected for update.');
      return;
    }
    try {
      await axios.put(`http://127.0.0.1:8000/api/employees/${employeeId}/`, formData);
      setMessage('Employee updated successfully.');
      setError('');
    } catch (error) {
      setError(error.response ? error.response.data.error : 'Error updating employee.');
      setMessage('');
    }
  };

  useEffect(() => {
    if (message || error) {
      const timer = setTimeout(() => {
        setMessage('');
        setError('');
      }, 3000);

      return () => clearTimeout(timer);
    }
  }, [message, error]);

  return (
    <div>
      <h1>Update Employee</h1>
      <form onSubmit={handleSearchSubmit}>
        <input
          type="text"
          name="searchQuery"
          value={searchQuery}
          onChange={handleSearchChange}
          placeholder="Search by employer username"
        />
        <button type="submit">Search</button>
      </form>
      {message && <p>{message}</p>}
      {error && <p>{error}</p>}
      {employeeId && (
        <div>
          <h2>Edit Employee Details</h2>
          <form onSubmit={handleSubmit}>
            <label>
              Username:
              <input
                type="text"
                name="user.username"
                value={formData.user.username}
                onChange={handleChange}
                placeholder="Username"
              />
            </label>
            <label>
              First Name:
              <input
                type="text"
                name="user.first_name"
                value={formData.user.first_name}
                onChange={handleChange}
                placeholder="First Name"
              />
            </label>
            <label>
              Last Name:
              <input
                type="text"
                name="user.last_name"
                value={formData.user.last_name}
                onChange={handleChange}
                placeholder="Last Name"
              />
            </label>
            <label>
              Employer:
              <input
                type="text"
                name="employer"
                value={formData.employer}
                onChange={handleChange}
                placeholder="Employer"
              />
            </label>
            <label>
              Position:
              <input
                type="text"
                name="position"
                value={formData.position}
                onChange={handleChange}
                placeholder="Position"
              />
            </label>
            <label>
              Department:
              <input
                type="text"
                name="department"
                value={formData.department}
                onChange={handleChange}
                placeholder="Department"
              />
            </label>
            <label>
              Year Started:
              <input
                type="number"
                name="year_started"
                value={formData.year_started}
                onChange={handleChange}
                placeholder="Year Started"
              />
            </label>
            <label>
              Year Left:
              <input
                type="number"
                name="year_left"
                value={formData.year_left}
                onChange={handleChange}
                placeholder="Year Left"
              />
            </label>
            <button type="submit">Update</button>
          </form>
        </div>
      )}
    </div>
  );
};

export default UpdateEmployee;
