import React, { useState } from 'react';

const AddEmployee = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    department: '',
    position: '',
    employer: '',
    year_started: '',
  });
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Submitting form data:', formData);

    try {
      const response = await fetch('http://localhost:8000/api/employees/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user: {
            username: formData.username,
            email: formData.email,
            first_name: formData.first_name,
            last_name: formData.last_name,
          },
          department: formData.department,
          position: formData.position,
          employer: formData.employer,
          year_started: formData.year_started,
        }),
      });

      console.log('Server response:', response);

      if (response.ok) {
        setIsSubmitted(true);
        setFormData({
          username: '',
          email: '',
          first_name: '',
          last_name: '',
          department: '',
          position: '',
          employer: '',
          year_started: '',
        });
        setTimeout(() => {
          setIsSubmitted(false);
        }, 3000);
      } else {
        const errorData = await response.json();
        console.error('Server error:', errorData);
        setError('Failed to add employee. Please try again.');
        setTimeout(() => {
          setError(null);
        }, 3000);
      }
    } catch (error) {
      console.error('Error adding employee:', error);
      setError('Failed to add employee. Please try again.');
      setTimeout(() => {
        setError(null);
      }, 3000);
    }
  };

  return (
    <div>
      <h2>Add Employee</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Username:
          <input type="text" name="username" value={formData.username} onChange={handleChange} />
        </label>
        <br />
        <label>
          Email:
          <input type="email" name="email" value={formData.email} onChange={handleChange} />
        </label>
        <br />
        <label>
          First Name:
          <input type="text" name="first_name" value={formData.first_name} onChange={handleChange} />
        </label>
        <br />
        <label>
          Last Name:
          <input type="text" name="last_name" value={formData.last_name} onChange={handleChange} />
        </label>
        <br />
        <label>
          Department:
          <input type="text" name="department" value={formData.department} onChange={handleChange} />
        </label>
        <br />
        <label>
          Position:
          <input type="text" name="position" value={formData.position} onChange={handleChange} />
        </label>
        <br />
        <label>
          Employer:
          <input type="text" name="employer" value={formData.employer} onChange={handleChange} />
        </label>
        <br />
        <label>
          Year Started:
          <input type="text" name="year_started" value={formData.year_started} onChange={handleChange} />
        </label>
        <br />
        <button type="submit">Add Employee</button>
      </form>
      {isSubmitted && <p style={{ color: 'green' }}>Employee added successfully!</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default AddEmployee;
