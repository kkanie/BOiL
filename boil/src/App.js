import { useState} from "react";

import "./App.css"
import {Table} from "./components/Table";
import {Modal} from "./components/Modal";

function  App(){
    const [modalOpen, setModalOpen] = useState(false);
    const [rows, setRows] = useState([
        {czynnosc: "A", czas_trwania: "2", nastepstwoL: "1", nastepstwoP: "2"},
        {czynnosc: "B", czas_trwania: "4", nastepstwoL: "2", nastepstwoP: "3"},
        {czynnosc: "C", czas_trwania: "2", nastepstwoL: "1", nastepstwoP: "4"},
    ]);

    const [rowToEdit, setRowToEdit] =useState(null);

    const handleDeleteRow = (targetIndex) =>{
        setRows(rows.filter((_, idx) => idx !== targetIndex));
    };

    const handleEditRow = (idx) => {
        setRowToEdit(idx);

        setModalOpen(true);
    }

    const handleSubmit = (newRow) => {
        rowToEdit=== null
            ? setRows([...rows, newRow])
            : setRows(
                rows.map((currRow, idx) =>{
                if(idx !== rowToEdit) return currRow

                return newRow
            })
            );
    }
    return <div className="App">
        <Table rows={rows} deleteRow={handleDeleteRow} editRow={handleEditRow}/>
        <button className="btn" onClick={() => setModalOpen(true)}>Dodaj</button>
        {modalOpen && (<Modal
            closeModal={()=> {
                setModalOpen(false);
                setRowToEdit(null);
            }}
            onSubmit={handleSubmit}
            defaultValue={rowToEdit !== null && rows[rowToEdit]}
            />
            ) }
        <button className="btn">Wyślij</button>
    </div>;
}

export default App;