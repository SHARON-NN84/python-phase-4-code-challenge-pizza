import React, { useState, useEffect } from 'react';

function Pizzas() {
  const [pizzas, setPizzas] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5555/pizzas')
      .then(response => response.json())
      .then(data => setPizzas(data))
      .catch(error => console.error('Error:', error));
  }, []);

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Pizzas</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1rem' }}>
        {pizzas.map(pizza => (
          <div key={pizza.id} style={{ border: '1px solid #ddd', padding: '1rem', borderRadius: '5px' }}>
            <h2>{pizza.name}</h2>
            <p>{pizza.ingredients}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Pizzas;