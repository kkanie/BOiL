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
  }

  render() {
    return (
      <ul>
        {
          this.state.wynik
            .map(wynik =>
              <li key={wynik.id}>{wynik.desc}</li>
            )
        }
      </ul>
    )
  }
}