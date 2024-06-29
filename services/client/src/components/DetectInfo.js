import React from "react";
import "../styles/DetectInfo.css";

const DetectInfo = ({brand, beer_line, object_type, number}) => {
    return (
        <div className="detect-info-container">
            <div className="info-title-container">
                <p style={{fontSize: "25px", fontWeight: "bold"}}>{brand}</p>
                <p>{beer_line}</p>
            </div>
            <div className="data-info-container">
                <p style={{fontSize: "55px", fontWeight: "bold"}}>{number}</p>
                <p style={{marginBottom: "15px"}}>{object_type}/Image</p>
            </div>
        </div>
    )
}

export default DetectInfo;