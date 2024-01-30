import logo from './logo.svg';
import './App.css';

import React, { Component } from 'react';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      textValue: '',
      errorMessage: '' 
    };
  }

  handleInputChange = (event) => {
    const value = event.target.value;
    if (value === '' || /^[0-9\b]+$/.test(value)) { 
      this.setState({ textValue: value, errorMessage: '' });
    } else {
      this.setState({ errorMessage: 'Veuillez entrer uniquement des chiffres.' });
    }
  }

  handleSubmit = () => {
    if (this.state.textValue) {
      console.log('Valeur soumise:', this.state.textValue);
      this.setState({ textValue: '', errorMessage: '' }); // Réinitialiser l'état après la soumission
    }
  }
  

  render() {
    return (
      <div className='Header'>

       <div className='Title'>
        <h1>SmartCam</h1>
        </div>
        <div className='Menu'>
        
        <p>Hello world!</p>
        <input
          type="text"
          value={this.state.textValue}
          onChange={this.handleInputChange}
        />
        <button onClick={this.handleSubmit}>Envoyer</button>
        {this.state.errorMessage && <p style={{color: 'red'}}>{this.state.errorMessage}</p>}
        </div>


      </div>
    );
  }
}

export default App;
