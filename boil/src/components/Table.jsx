import React from "react";

import "./Table.css";
import {BsFillPencilFill, BsFillTrashFill} from "react-icons/bs";

export const Table = ({rows, deleteRow, editRow}) => {
    return (<div className="table-wrapper">
        <table className="table">
            <thead>
            <tr>
                <th>Czynnosc</th>
                <th>Czas trwania</th>
                <th>Następstwo zdarzeń: L</th>
                <th>Następstwo zdarzeń: P</th>
                <th>Akcje</th>
            </tr>
            </thead>
            <tbody>
            {
                rows.map((row, idx) => {
                    return <tr key={idx}>
                        <td>{row.czynnosc}</td>
                        <td>{row.czas_trwania}</td>
                        <td>{row.nastepstwoL}</td>
                        <td>{row.nastepstwoP}</td>
                        <td>
                        <span className="actions">
                            <BsFillTrashFill className="delete-btn" onClick={() => deleteRow(idx)}/>
                            <BsFillPencilFill onClick={() => editRow(idx)}/>
                        </span>
                        </td>
                    </tr>
                })
            }
            </tbody>
        </table>
    </div>)
};