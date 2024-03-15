import React, { Component } from 'react';
import { Line } from 'react-chartjs-2';
import './App.css';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

class App extends Component {
  constructor(props) {
    super(props);
    const savedTemperatureData = JSON.parse(localStorage.getItem('temperatureData')) || [];
    this.state = {
      textValue: '',
      errorMessage: '',
      allData: [], // Initialisation d'un état pour stocker toutes les données
      chauffageState: 'NO', // Ajout d'un nouvel état pour le chauffage
      chauffageState2: 'YES',
      currentTemperature: 'N/A', // Ajout pour la température actuelle
      isPersonPresent: false, // Ajout pour la présence de personne
      temperatureData: savedTemperatureData,
    };
    
  }

  toggleChauffage = async () => {
    const newState = this.state.chauffageState === 'NO' ? 'YES' :'YES';
    this.setState({ chauffageState: newState });
    await this.postChauffageState(newState);
  };

  postChauffageState = async (state) => {
    try {
      const response = await fetch('http://172.20.10.5:5000/sendchauffage', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          chauffage: state
        }),
      });
      const data = await response.json();
      console.log('Réponse du serveur:', data);
    } catch (error) {
      console.error('Erreur lors de l\'envoi de l\'état du chauffage', error);
      this.setState({ errorMessage: 'Erreur lors de l\'envoi de l\'état du chauffage.' });
    }
  };
  toggleChauffage2 = async () => {
    const newState = this.state.chauffageState2 === 'YES' ? 'NO' :'NO';
    this.setState({ chauffageState2: newState });
    await this.postChauffageState2(newState);
  }
  postChauffageState2 = async (state) => {
    try {
      const response = await fetch('http://172.20.10.5:5000/sendchauffage', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          chauffage: state
        }),
      });
      const data = await response.json();
      console.log('Réponse du serveur:', data);
    }
    catch (error) {
      console.error('Erreur lors de l\'envoi de l\'état du chauffage', error);
      this.setState({ errorMessage: 'Erreur lors de l\'envoi de l\'état du chauffage.' });
    }
  };

  getTemperatureData = async () => {
    try {
      const response = await fetch('http://172.20.10.5:5000/getiftemp');
      const data = await response.json();
  
      // Mettre à jour directement currentTemperature avec la valeur obtenue
      this.setState({
        currentTemperature: parseFloat(data.temperature).toFixed(1) // Arrondi à une décimale
      });
  
      // Ajoutez également cette nouvelle donnée à temperatureData pour le graphique, si nécessaire
      const newTemperatureData = {
        date: new Date().toLocaleString(), // Date et heure actuelles pour l'exemple
        temperature: data.temperature,
      };
      this.setState(prevState => ({
        temperatureData: [...prevState.temperatureData, newTemperatureData],
      }));
  
      // Sauvegarde dans localStorage pour persistance
      localStorage.setItem('temperatureData', JSON.stringify(this.state.temperatureData));
  
    } catch (error) {
      console.error('Erreur lors de la récupération des données de température', error);
      this.setState({ errorMessage: 'Erreur lors de la récupération des données de température.' });
    }
  };
  
  
  

  
  componentDidMount() {
    this.getAllData(); // Appeler getAllData lorsque le composant est monté
    this.getPresenceData(); // Appeler getPresenceData également lors du montage
    this.dataInterval = setInterval(this.getAllData, 10000); // Récupérer toutes les données toutes les 10 secondes
    this.presenceInterval = setInterval(this.getPresenceData, 2000); // Vérifier la présence toutes les 5 secondes
    this.tempInterval = setInterval(this.getTemperatureData, 3000); // Par exemple, toutes les 10 secondes
  }
  
  componentWillUnmount() {
    clearInterval(this.dataInterval); // Nettoyer l'intervalle pour getAllData
    clearInterval(this.presenceInterval); // Nettoyer l'intervalle pour getPresenceData
    clearInterval(this.tempInterval);
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
      const response = await fetch('http://172.20.10.5:5000/sendtemperature', {
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
      const response = await fetch('http://172.20.10.5:5000/getdata', {
        method: 'GET',
      });
      const data = await response.json();
      console.log('Réponse du serveur:', data);
      this.setState({ allData: data });
      if (data.length > 0) {
        const latestData = data[data.length - 1]; // Supposons que le dernier élément contient les dernières infos
        this.setState({
          currentTemperature: parseFloat(latestData[2]).toFixed(1), // Arrondi à une décimale
          isPersonPresent: latestData[1] > 0,
        });
      }
    } catch (error) {
      console.error('Erreur lors de la récupération des données', error);
      this.setState({ errorMessage: 'Erreur lors de la récupération des données.' });
    }
  }
  
  getPresenceData = async () => {
    try {
      const response = await fetch('http://172.20.10.5:5000/getifdetect', {
        method: 'GET',
      });
      const data = await response.json();
      console.log('Réponse de présence du serveur:', data);
  
      // Mettre à jour l'état de la présence en fonction de la réponse
      this.setState({
        isPersonPresent: data.detection > 0, // Supposons que 'detection' retourne 1 pour présence, 0 sinon
      });
    } catch (error) {
      console.error('Erreur lors de la récupération de la présence', error);
      this.setState({ errorMessage: 'Erreur lors de la récupération des données de présence.' });
    }
  }
  resetGraph = () => {
    this.setState({ temperatureData: [] }); // Réinitialiser les données de température
    localStorage.removeItem('temperatureData'); // Optionnel: Supprimer de localStorage pour une réinitialisation persistante
  };
  
  render() {
    const data = {
      labels: this.state.temperatureData.map(item => item.date),
      datasets: [{
        label: 'Temperature',
        data: this.state.temperatureData.map(item => item.temperature),
        fill: false,
        backgroundColor: 'rgb(255, 0, 0,0.9)',
        borderColor: 'rgba(255, 0, 0, 0.4)',
      }],
    };
  
  
    const options = {
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: 'white', // Définir la couleur de la grille de l'axe Y en blanc
          },
          ticks: {
            color: 'white', // Définir la couleur des labels de l'axe Y en blanc
          }
        },
        x: {
          grid: {
            color: 'white', // Définir la couleur de la grille de l'axe X en blanc
          },
          ticks: {
            color: 'rgba(128, 128, 128, 1)', // Définir la couleur des labels de l'axe X en blanc
          }
        }
      },
      plugins: {
        legend: {
          labels: {
            color: 'white' // Définir la couleur des labels de la légende en blanc
          }
        },
        tooltip: {
          titleColor: 'white', // Couleur du titre du tooltip
          bodyColor: 'white', // Couleur du corps du tooltip
          footerColor: 'white', // Couleur du pied de page du tooltip
        }
      }
    };
    

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
          <div className='buttonSend'>
          <button onClick={this.handleSubmit}>Send</button>
          </div>
          {this.state.errorMessage && <p style={{color: 'red'}}>{this.state.errorMessage}</p>}
        </div>
        <div className="buttonsContainer">
        <button onClick={this.toggleChauffage}>Start Heating</button>
        <button onClick={this.toggleChauffage2}>Stop Heating</button>
      </div>


        <div className='infoBlocks'>
        <div className='temperatureBlock'>
        <h3>Current Temperature</h3>
        <p>{this.state.currentTemperature}°C</p>
      </div>

          <div className='presenceBlock'>
            <h3>Occuped Room</h3>
            <p>{this.state.isPersonPresent ? 'Yes' : 'No'}</p>
          </div>
        </div>

        <div className='chartContainer'>
          <h2>Evolution of temperature</h2>
          <Line data={data} options={options} />
        </div>
        <div className='resetButtonContainer'>
        <button onClick={this.resetGraph}>Reset data graph</button>
        </div>



        <div className='AllData'>
        <h2>All Data</h2>
        {this.state.allData.map((item, index) => (
          
          <div className='rectangle'>
          <div key={index}>
            <p>ID: {item[0]} - Occuped: {item[1]} - Temperature: {item[2]} -Humidity: {item[3]} Light: {item[4]} -Heating: {item[5]} -Date: {item[6]}</p>
          </div>
          </div>
        ))}
      </div>
      </div>
    );
  }
}

export default App;
