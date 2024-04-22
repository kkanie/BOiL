import React from 'react';
import axios from 'axios';

export default class WynikList extends React.Component {
  state = {
    wynik: []
  }

  componentDidMount() {
    axios.get(`http://127.0.0.1:8000/api/calculate/`)
      .then(res => {
        const wynik = res.data.tasks;
        this.setState({ wynik });
      })
      .catch(error => {
        // Handle error
        console.error('Error fetching data:', error);
      });
  }

  render() {
    const criticalTasks = this.state.wynik.filter(wynik => wynik.is_critical);
    console.log(criticalTasks)
    return (
      <div>
        <h1>Wyniki</h1>
      <ul>
        {
          this.state.wynik.map(wynik =>
              <li key={wynik.id}>{wynik.id}, {wynik.ES}, {wynik.LS}, {wynik.slack}</li>
            )
        }
      </ul>
      <h1>Ścieżka krytyczna</h1>
      <ul>
        {
          this.state.wynik.filter(wynik => wynik.is_critical).map(wynik =>
              <li key={wynik.id}>{wynik.id}</li>
            )
        }
      </ul>
      </div>
    )
  }
}