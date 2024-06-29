import React from "react";
import DetectInfo from "./DetectInfo";
import PieChart from "./PieChart";

import "../styles/Results.css";

const Results = ({
    beer_can_infos,
    beer_carton_infos,
    beer_person_infos,
    background,
}) => {
    console.log(beer_can_infos)
    return (
        <div className="results-container">
            <div className="analyzed-result-container">
                <h1>Analyzed Results</h1>
                <div
                    className="analyzed-result-container"
                    style={{ paddingLeft: "20px" }}>
                    <h2>🍾 Can Statistics</h2>
                    <div className="analyzed-results-list">
                        {beer_can_infos.map((item, index) => (
                            <DetectInfo
                                key={index}
                                beer_line={""}
                                brand={item.brand}
                                object_type={item.object_type}
                                number={item.number}
                            />
                        ))}
                    </div>
                </div>
                <div
                    className="analyzed-result-container"
                    style={{ paddingLeft: "20px" }}>
                    <h2>📦 Carton Statistics</h2>
                    <div className="analyzed-results-list">
                        {beer_carton_infos.map((item, index) => (
                            <DetectInfo
                                key={index}
                                beer_line={""}
                                brand={item.brand}
                                object_type={item.object_type}
                                number={item.number}
                            />
                        ))}
                    </div>
                </div>
                <div
                    className="analyzed-result-container"
                    style={{ paddingLeft: "20px" }}>
                    <h2>👨🏼‍🍳 POSM Statistics</h2>
                    <div className="analyzed-results-list">
                        {beer_person_infos.map((item, index) => (
                            <DetectInfo
                                key={index}
                                beer_line={item.beer_line}
                                brand={item.brand}
                                object_type={item.object_type}
                                number={item.number}
                            />
                        ))}
                    </div>
                </div>
            </div>
            <div className="analyzed-result-container" style={{ height: 400 }}>
                <h1>Distributions</h1>
                <div className="distribution-list" style={{ height: 400 }}>
                    {beer_can_infos !== undefined && beer_can_infos.length > 1 && <PieChart beer_infos={beer_can_infos} />}
                    {beer_carton_infos !== undefined && beer_carton_infos.length > 1 && <PieChart beer_infos={beer_carton_infos} />}
                </div>
            </div>
            <div className="analyzed-result-container">
                <h1>Background</h1>
            </div>
        </div>
    );
};

export default Results;
