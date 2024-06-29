import React from "react";
import '../styles/ProgressBar.css';
import image_icon from '../assets/image-icon.png'

const ProgressBar = ({fileName, progressBar}) => {
    const preprocess = (fileName) => {
        if(fileName.length > 20) {
            fileName = fileName.substring(0, 15) + '...' + fileName.substring(fileName.length - 5, fileName.length);
        }
        return fileName
    }
    return (
        <div className="upload-progress-bar">
            <div className="custom-progressBar" style={{justifyContent:"flex-start", marginBottom:"-30px", gap:"5px"}}>
                <img className="icon" src={image_icon} alt="icon" style={{width:"5%"}}/>
                <p>{preprocess(fileName)}</p>
            </div>
            <div className="custom-progressBar">
                <progress color="#000" value={progressBar} max="100"/>
                <p>{progressBar}%</p>
            </div>
        </div>
    )
}

export default ProgressBar;