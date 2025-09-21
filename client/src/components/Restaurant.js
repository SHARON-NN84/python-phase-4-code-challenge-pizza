import React, { useState, useEffect } from 'react';

function Restaurants() {
  const [restaurants, setRestaurants] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5555/restaurants')
      .then(response => response.json())
      .then(data => setRestaurants(data))
      .catch(error => console.error('Error:', error));
  }, []);

  const handleDelete = (id) => {
    fetch(`http://localhost:5555/restaurants/${id}`, {
      method: 'DELETE'
    })
    .then(response => {
      if (response.ok) {
        setRestaurants(restaurants.filter(restaurant => restaurant.id !== id));
      } else {
        console.error('Failed to delete restaurant');
      }
    })
    .catch(error => console.error('Error:', error));
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Restaurants</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1rem' }}>
        {restaurants.map(restaurant => (
          <div key={restaurant.id} style={{ border: '1px solid #ddd', padding: '1rem', borderRadius: '5px' }}>
            <h2>{restaurant.name}</h2>
            <p>{restaurant.address}</p>
            <button 
              onClick={() => handleDelete(restaurant.id)}
              style={{ backgroundColor: '#dc3545', color: 'white', border: 'none', padding: '0.5rem 1rem', borderRadius: '3px' }}
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Restaurants;