import React from "react";
import DetectInfo from "./DetectInfo";
import PieChart from "./PieChart";

import "../styles/Results.css";

const Results = ({
    beer_can_infos,
    beer_carton_infos,
    beer_person_infos,
    beer_posm_infos,
    background,
    base64_img,
    description,
    label_color,
    font_color,
}) => {
    console.log(beer_can_infos);
    return (
        <div className="results-container">
            <div className="analyzed-result-container">
                <h1>Analyzed Results</h1>
                <div
                    className="analyzed-result-container"
                    style={{ paddingLeft: "20px" }}>
                    <h2>🍾 Bottle Statistics</h2>
                    <div className="analyzed-results-list">
                        {beer_can_infos &&
                            beer_can_infos.map((item, index) => (
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
                        {beer_carton_infos &&
                            beer_carton_infos.map((item, index) => (
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
                    <h2>👫 People Statistics</h2>
                    <div className="analyzed-results-list">
                        {beer_person_infos &&
                            beer_person_infos.map((item, index) => (
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
                <div
                    className="analyzed-result-container"
                    style={{ paddingLeft: "20px" }}>
                    <h2>♺ POSM Statistics</h2>
                    <div className="analyzed-results-list">
                        {beer_posm_infos &&
                            beer_posm_infos.map((item, index) => (
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
                    {beer_can_infos !== undefined &&
                        beer_can_infos.length > 1 && (
                            <PieChart beer_infos={beer_can_infos} />
                        )}
                    {beer_carton_infos !== undefined &&
                        beer_carton_infos.length > 1 && (
                            <PieChart beer_infos={beer_carton_infos} />
                        )}
                </div>
            </div>
            <div
                className="analyzed-result-container"
                style={{ flexDirection: "row" }}>
                <h1>Background</h1>
                <div className="analyzed-results-list">
                    <div
                        className="background-results-container"
                        style={{ marginLeft: "4%", marginTop: "10px" }}>
                        <h4
                            style={{
                                width: "fit-content",
                                backgroundColor: "#f8f8f8",
                                borderRadius: "10px",
                                marginTop: "-10px",
                                paddingLeft: "5px",
                                paddingRight: "5px",
                            }}>
                            Activity and Location
                        </h4>
                        <p style={{ alignItems: "center", paddingLeft: "20%" }}>
                            {background.activity
                                ? background.activity + " at"
                                : ""}{" "}
                            {background.location}
                        </p>
                    </div>
                    <div
                        className="background-results-container"
                        style={{ marginLeft: "4%", marginTop: "10px" }}>
                        <h4
                            style={{
                                width: "fit-content",
                                backgroundColor: "#f8f8f8",
                                borderRadius: "10px",
                                marginTop: "-10px",
                                paddingLeft: "5px",
                                paddingRight: "5px",
                            }}>
                            Atmosphere
                        </h4>
                        <p style={{ alignItems: "center", paddingLeft: "20%" }}>
                            {background.atmosphere.length > 0 &&
                                background.atmosphere[0]}{" "}
                            {background.atmosphere.length > 1 && (
                                <span>&#183;</span>
                            )}{" "}
                            {background.atmosphere.length > 1 &&
                                background.atmosphere[1]}{" "}
                            {background.atmosphere.length > 2 && (
                                <span>&#183;</span>
                            )}{" "}
                            {background.atmosphere.length > 2 &&
                                background.atmosphere[2]}
                        </p>
                    </div>
                    <div
                        className="background-results-container"
                        style={{ marginLeft: "4%", marginTop: "10px" }}>
                        <h4
                            style={{
                                width: "fit-content",
                                backgroundColor: "#f8f8f8",
                                borderRadius: "10px",
                                marginTop: "-10px",
                                paddingLeft: "5px",
                                paddingRight: "5px",
                            }}>
                            Emotions
                        </h4>
                        <p style={{ alignItems: "center", paddingLeft: "20%" }}>
                            {background.emotion.length > 0 &&
                                background.emotion[0]}{" "}
                            {background.emotion.length > 1 && (
                                <span>&#183;</span>
                            )}{" "}
                            {background.emotion.length > 1 &&
                                background.emotion[1]}{" "}
                            {background.emotion.length > 2 && (
                                <span>&#183;</span>
                            )}{" "}
                            {background.emotion.length > 2 &&
                                background.emotion[2]}
                        </p>
                    </div>
                </div>
            </div>
            <div className="analyzed-result-container">
                <h1>Processed Image</h1>
                <div className="analyzed-results-list">
                    <div className="image-and-drag">
                        {base64_img && (
                            <div>
                                <img
                                    src={"data:image/png;base64," + base64_img}
                                    className="upload-image"
                                    alt=""
                                />
                                <div className="analyzed-results-list">
                                {label_color &&
                                    label_color.map((item, index) => (
                                        <p
                                            key={index}
                                            style={{
                                                color: `rgb(${font_color[index][0]}, ${font_color[index][1]}, ${font_color[index][2]})`,
                                            }}>
                                            <strong>{item}</strong>
                                        </p>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                    <p style={{width:"600px"}}>{description}</p>
                </div>
            </div>
        </div>
    );
};

export default Results;
