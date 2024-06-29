import React from "react";
import DetectInfo from "./DetectInfo";
import PieChart from "./PieChart";

import "../styles/Results.css";

const Results = () => {
    let beer_infos = [
        {
            brand: "Heineken",
            beer_line: "Silver",
            object_type: "Can",
            number: 10,
        },
        {
            brand: "Heineken",
            beer_line: "Silver",
            object_type: "Can",
            number: 10,
        },
        {
            brand: "Heineken",
            beer_line: "Silver",
            object_type: "Can",
            number: 10,
        },
        {
            brand: "Heineken",
            beer_line: "Silver",
            object_type: "Can",
            number: 10,
        },
        {
            brand: "Heineken",
            beer_line: "Silver",
            object_type: "Can",
            number: 10,
        },
        {
            brand: "Heineken",
            beer_line: "Silver",
            object_type: "Can",
            number: 10,
        },
        {
            brand: "Heineken",
            beer_line: "Silver",
            object_type: "Can",
            number: 10,
        },
        {
            brand: "Heineken",
            beer_line: "Silver",
            object_type: "Can",
            number: 10,
        },
        {
            brand: "Heineken",
            beer_line: "Silver",
            object_type: "Can",
            number: 10,
        },
        {
            brand: "Heineken",
            beer_line: "Silver",
            object_type: "Can",
            number: 10,
        },
        {
            brand: "Heineken",
            beer_line: "Silver",
            object_type: "Can",
            number: 10,
        },
        {
            brand: "Heineken",
            beer_line: "Silver",
            object_type: "Can",
            number: 10,
        },
        {
            brand: "Heineken",
            beer_line: "Silver",
            object_type: "Can",
            number: 10,
        },
        {
            brand: "Heineken",
            beer_line: "Silver",
            object_type: "Can",
            number: 10,
        },
        {
            brand: "Heineken",
            beer_line: "Silver",
            object_type: "Can",
            number: 10,
        },
        {
            brand: "Heineken",
            beer_line: "Silver",
            object_type: "Can",
            number: 10,
        },
    ];
    return (
        <div className="results-container">
            <div className="analyzed-result-container">
                <h1>Analyzed Results</h1>
                <div className="analyzed-results-list">
                    {beer_infos.map((item, index) => (
                        <DetectInfo
                            key={index}
                            brand={item.brand}
                            beer_line={item.beer_line}
                            object_type={item.object_type}
                            number={item.number}
                        />
                    ))}
                </div>
            </div>
            <div className="analyzed-result-container" style={{ height: 400 }}>
                <h1>Distributions</h1>
                <div className="distribution-list" style={{ height: 400 }}>
                    <PieChart />
                    <PieChart />
                </div>
            </div>
        </div>
    );
};

export default Results;
