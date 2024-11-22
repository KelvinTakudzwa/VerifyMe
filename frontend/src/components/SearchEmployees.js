import React, { useState } from 'react';

const SearchEmployees = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [error, setError] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(`http://localhost:8000/api/employees/search/?q=${searchTerm}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setSearchResults(data); // Assuming API returns an array of matching employees
      } else {
        setError('Failed to fetch search results.');
      }
    } catch (error) {
      console.error('Error searching for employees:', error);
      setError('Error searching for employees. Please try again.');
    }
  };

  return (
    <div>
      <h2>Search Employees</h2>
      <form onSubmit={handleSearch}>
        <label>
          Search Term:
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </label>
        <button type="submit">Search</button>
      </form>

      <div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {searchResults.length > 0 ? (
          <ul>
            {searchResults.map((employee) => (
              <li key={employee.id}>
                {employee.user.username} - {employee.position}
              </li>
            ))}
          </ul>
        ) : (
          <p>No employees found.</p>
        )}
      </div>
    </div>
  );
};

export default SearchEmployees;
