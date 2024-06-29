import React from "react";
import "../styles/DropArea.css";
import image_icon from "../assets/image-icon.png";

const DropArea = () => {
    return (
        <div style={{ textAlign: "center" }}>
            <div className="circle large">
                <div className="circle medium">
                    <div className="circle small">
                        <div className="circle tiny">
                            <img className="icon" src={image_icon} alt="icon" />
                        </div>
                    </div>
                </div>
            </div>
            <p style={{ fontWeight: "bold", marginBottom: "-10px" }}>
                Drag and drop to upload your files here
            </p>
            <p style={{ fontSize: "small", opacity: "40%" }}>
                JPEG, EPS, PNG, TFF
            </p>
        </div>
    );
};

export default DropArea;
