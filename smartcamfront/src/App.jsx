import React, { Component } from 'react';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      textValue: '',
      errorMessage: '',
      allData: [] // Initialisation d'un état pour stocker toutes les données
    };
  }

  componentDidMount() {
    this.getAllData(); // Appeler getAllData lorsque le composant est monté
  }

  handleInputChange = (event) => {
    const value = event.target.value;
    if (value === '' || /^[0-9\b]+$/.test(value)) {
      this.setState({ textValue: value, errorMessage: '' });
    } else {
      this.setState({ errorMessage: 'Veuillez entrer uniquement des chiffres.' });
    }
  }

  handleSubmit = async () => {
    if (this.state.textValue) {
      console.log('Valeur soumise:', this.state.textValue);
      await this.postTemperature(this.state.textValue);
      this.setState({ textValue: '', errorMessage: '' });
    }
  }

  postTemperature = async (temperature) => {
    console.log('temperature en envoi:', temperature);
    try {
      const response = await fetch('http://192.168.1.52:5000/sendtemperature', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          temperature: temperature
        }),
      });
      const data = await response.json();
      console.log('Réponse du serveur:', data);
      this.getAllData(); // Rafraîchir les données après l'envoi
    } catch (error) {
      console.error('Erreur lors de l\'envoi de la température', error);
      this.setState({ errorMessage: 'Erreur lors de l\'envoi de la température.' });
    }
  }

  getAllData = async () => {
    console.log('Récupération de toutes les données');
    try {
      const response = await fetch('http://192.168.1.52:5000/getdata', {
        method: 'GET',
      });
      const data = await response.json();
      console.log('Réponse du serveur:', data);
      this.setState({ allData: data }); 
    } catch (error) {
      console.error('Erreur lors de la récupération des données', error);
      this.setState({ errorMessage: 'Erreur lors de la récupération des données.' });
    }
  }

  render() {
    return (
      <div className='Header'>
        <div className='Title'>
          <h1>SmartCam</h1>
        </div>
        <div className='Textetemp'>
          <p>Choose your temperature</p>
        </div>
        <div className='Menu'>
          <input
            type="text"
            value={this.state.textValue}
            onChange={this.handleInputChange}
          />
          <button onClick={this.handleSubmit}>Envoyer</button>
          {this.state.errorMessage && <p style={{color: 'red'}}>{this.state.errorMessage}</p>}
        </div>

        <div className='AllData'>
        <h2>All Data</h2>
        {this.state.allData.map((item, index) => (
          
          <div className='rectangle'>
          <div key={index}>
            <p>ID: {item[0]} - people: {item[1]} - Temperature: {item[2]} - Light: {item[3]} - Date: {item[4]}</p>
          </div>
          </div>
        ))}
      </div>
      </div>
    );
  }
}

export default App;
