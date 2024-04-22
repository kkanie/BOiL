import { useEffect, useState } from "react";
import "./App.css";
import axios from "axios";
import { Table } from "./components/Table";
import { Modal } from "./components/Modal";
import cytoscape from 'cytoscape';
import Wynik from './components/Wynik.jsx';
import WynikList from "./components/Wynik.jsx";

<script src="https://unpkg.com/axios/dist/axios.min.js"></script>
function App() {
  const [modalOpen, setModalOpen] = useState(false);
  const [rows, setRows] = useState([]);
  const [wynik, setState] = useState([]);
  


  const generateGraph = (data) => {
    const elements = [];
    const points = new Set(); // Użyjemy zbioru, aby uniknąć duplikatów

    // Dodajemy wierzchołki do zbioru punktów
    data.forEach(row => {
      points.add(row.nastepstwoL);
      points.add(row.nastepstwoP);
    });

    // Tworzymy wierzchołki na podstawie punktów
    points.forEach(point => {
      elements.push({ group: 'nodes', data: { id: `point${point}`, label: `${point}` } });
    });

    // Dodajemy krawędzie na podstawie danych z tabeli
    data.forEach(row => {
      const edgeId = `edge${row.czynnosc}`;
      const label = `${row.czynnosc} (${row.czas_trwania})`; // Dodajemy czas trwania do etykiety krawędzi
      elements.push({ group: 'edges', data: { id: edgeId, source: `point${row.nastepstwoL}`, target: `point${row.nastepstwoP}`, label: label } });
    });

    const cy = cytoscape({
      container: document.getElementById('cy'),
      elements: elements,
      style: [
        {
          selector: 'node',
          style: {
            'background-color': '#69e',
            'label': 'data(label)',
          }
        },
        {
          selector: 'edge',
          style: {
            'width': 1,
            'line-color': '#369',
            'target-arrow-color': '#369',
            'target-arrow-shape': 'triangle',
            'label': 'data(label)',
            'font-size': '14px',
            'color': '#777'
          }
        }
      ],
      layout: {
        name: 'cose',
        nodeRepulsion: 20000000,
        rows: 1,
      }
    });
  };

  useEffect(() => {
    generateGraph(rows);
  }, [rows]);

  const [rowToEdit, setRowToEdit] = useState(null);

  const handleDeleteRow = (targetIndex) => {
    setRows(rows.filter((_, idx) => idx !== targetIndex));
  };

  const handleEditRow = (idx) => {
    setRowToEdit(idx);

    setModalOpen(true);
  }

  const handleSubmit = (newRow) => {
    rowToEdit === null
        ? setRows([...rows, newRow])
        : setRows(
            rows.map((currRow, idx) => {
              if (idx !== rowToEdit) return currRow

              return newRow
            })
        );
  }

  const handleSend = async ()=>{

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/tasks/', rows, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
  
      console.log(response.data);
      // Handle success response here
    } catch (error) {
      console.error('Error:', error);
      // Handle error here
    }
    console.log(rows)
    // // e.preventDefault()
    

    // const response = await fetch('http://127.0.0.1:8000/api/tasks/', {
    //   method: 'POST',
    //   mode: 'no-cors',
    //   body: JSON.stringify(rows),
    //   headers:{
    //       'Content-Type': 'application/json'
    //   }
  // })
  }
  const handleCalculate = async ()=>{
    axios.get(`http://127.0.0.1:8000/api/calculate/`)
      .then(res => {
        const wynik = res.data.tasks;
        console.log(wynik)
      })
  }

//   const handleCalculate = async() =>{
//     // GET request using axios with async/await
//     const response = await axios.get('http://127.0.0.1:8000/api/calculate/');
//     //console.log(response)
//     setWynik([...wynik, response.data.tasks])
//     console.log(wynik)
    
// }

  return (
      <div className="App">
        <div id="cy" style={{width: '80%', height: '600px', margin: 'auto'}}></div>
        <Table rows={rows} deleteRow={handleDeleteRow} editRow={handleEditRow}/>
        <button className="btn" onClick={() => setModalOpen(true)}>Dodaj</button>
        {modalOpen && (<Modal
                closeModal={() => {
                  setModalOpen(false);
                  setRowToEdit(null);
                }}
                onSubmit={handleSubmit}
                defaultValue={rowToEdit !== null && rows[rowToEdit]}
            />
        )}
        <button className="btn" onClick={()=>handleSend()}>Wyślij</button>
        <button className="btn" onClick={()=>handleCalculate()}>Wynik</button>
        <WynikList/>
      </div>
  );
}

export default App;


//trzeba dodac "cos" do strony bo jak sie doda zbyt duzo czynnosci do tabeli to graf
//predzej czy pozniej zniknie

