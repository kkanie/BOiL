import React, {useState} from "react";

import "./Modal.css"
export const Modal = ({closeModal, onSubmit, defaultValue}) => {
    const [formState, setFormState] = useState(defaultValue ||{
        czynnosc: "",
        czas_trwania: "",
        nastepstwoL: "",
        nastepstwoP: "",
    });

    const [errors, setErrors] = useState("")

    const validateForm = () =>{
        if(formState.czynnosc && formState.czas_trwania && formState.nastepstwoP && formState.nastepstwoL){
            setErrors("")
            return true;
        }else{
            let errorFields = [];
            for(const [key, value] of Object.entries(formState)){
                if(!value) {
                    errorFields.push(key);
                }
            }
            setErrors(errorFields.join(", "));
            return false;
        }

    }
    const handleChange = (e) =>{
        setFormState({
            ...formState,
            [e.target.name]: e.target.value
        })
    }

    const handleSubmit = (e) => {
        e.preventDefault();

        if(!validateForm()) return;

        onSubmit(formState)

        closeModal();
    };
    return(
        <div className="modal-container" onClick={(e)=>{
            if(e.target.className === "modal-container") closeModal();
        }}
        >
            <div className="modal">
                <form>
                    <div className="form-group">
                        <label htmlFor="czynnosc">Czynnosc</label>
                        <input name="czynnosc" value={formState.czynnosc} onChange={handleChange}/>
                    </div>
                    <div className="form-group">
                        <label htmlFor="czas_trwania">Czas trwania</label>
                        <input name="czas_trwania" value={formState.czas_trwania} onChange={handleChange}/>
                    </div>
                    <div className="form-group">
                        <label htmlFor="nastepstwoL">Następstwo L</label>
                        <input name="nastepstwoL" value={formState.nastepstwoL} onChange={handleChange}/>
                    </div>
                    <div className="form-group">
                        <label htmlFor="nastepstwoP">Następstwo P</label>
                        <input name="nastepstwoP" value={formState.nastepstwoP} onChange={handleChange}/>
                    </div>
                    {errors && <div className="error">{`Prosze uzupelnic pola: ${errors}`}</div>}
                    <button type="submit" className="btn" onClick={handleSubmit}>Wprowadz</button>
                </form>
            </div>
        </div>
    )
}