import React, { useState } from "react";

import UploadFile from "./components/UploadFile";
import Results from "./components/Results";
import "./App.css";

function App() {
    const [requestData, setRequestData] = useState({
        beer_can_infos: [
            {
                brand: "Heineken 0.0",
                object_type: "Can",
                number: 10,
            },
            {
                brand: "Heineken Silver",
                object_type: "Can",
                number: 10,
            },
        ],
        beer_carton_infos: [
            {
                brand: "Heineken Silver",
                object_type: "Carton",
                number: 10,
            },
            {
                brand: "Heineken 0.0",
                object_type: "Carton",
                number: 10,
            },
        ],
        beer_person_infos: [
            {
                brand: "Promotion Girl",
                beer_line: "Heineken 0.0",
                object_type: "Person",
                number: 10,
            },
            {
                brand: "Promotion Girl",
                beer_line: "Heineken 0.0",
                object_type: "Person",
                number: 10,
            },
        ],
        beer_posm_infos: [
            {
                brand: "Heineken 0.0",
                beer_line: "",
                object_type: "Billboard",
                number: 10,
            },
            {
                brand: "Heineken Silver",
                beer_line: "",
                object_type: "Billboard",
                number: 10,
            },
        ],
        background: {
            location: "street restaurant",
            activity: "dining",
            atmosphere: ["casual", "welcoming", "bustling"],
            emotion: ["relaxed", "social", "content"],
        },
    });
    return (
        <div>
            <UploadFile setRequestData={setRequestData} />
            {requestData && (
                <Results
                    beer_can_infos={requestData.beer_can_infos}
                    beer_carton_infos={requestData.beer_carton_infos}
                    beer_person_infos={requestData.beer_person_infos}
                    beer_posm_infos={requestData.beer_posm_infos}
                    background={requestData.background}
                />
            )}
        </div>
    );
}

export default App;
