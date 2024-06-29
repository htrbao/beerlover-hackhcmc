import React, { useState } from "react";

import UploadFile from "./components/UploadFile";
import Results from "./components/Results";
import "./App.css";

function App() {
    const [requestData, setRequestData] = useState()
    return (
        <div>
            <UploadFile />
			<Results />
        </div>
    );
}

export default App;
