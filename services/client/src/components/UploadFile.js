import React, { useState } from 'react'
import axios from 'axios';

import ProgressBar from './ProgressBar';
import DropArea from './DropArea';
import '../styles/UploadFile.css';

const UploadFile = ({setRequestData}) => {
    const [fileName, setFileName] = useState()
    const [image, setImage] = useState()
    const [progressBar, setProgressBar] = useState(0)

    const handleFile = async (event) => {
        const file = event.target.files[0];

        const formdata = new FormData();
        setImage(setImage(URL.createObjectURL(file)))
        setFileName(file.name)
        formdata.append('file', file);

        await axios.post('https://80b1-85-238-208-71.ngrok-free.app/upload', formdata, {
            headers: {
                'Content-Type': 'multipart/form-data'
            },
            progress: (progressEvent) => {
                const { loaded, total } = progressEvent;
                console.log(loaded, total)
                const percent = Math.floor((loaded * 100) / total);
                console.log(percent)
                setProgressBar(percent)
            },
            onUploadProgress: (progressEvent) => {
                const { loaded, total } = progressEvent;
                console.log(loaded, total)
                const percent = Math.floor((loaded * 100) / total);
                console.log(percent)
                setProgressBar(percent)
            },
        }).then(res => {
            setImage(URL.createObjectURL(file))
            setRequestData(res.results)
        }).catch(err => {
            console.log(err)
        })
    }

    return (
        <div className='upload-file-container'>
            <div className='image-and-drag'>
            {
                image ? (
                    <img src={image} className='upload-image' alt=''/>
                ) : (
                    <DropArea/>
                )
            }
            </div>
            <div className='upload-btn-container'>

                <input type="file" id="actual-btn" onChange={handleFile} hidden/>
                <label for="actual-btn">+ Add Document</label>

                <br></br>
                {
                    (progressBar > 0) &&
                    <div className='progressbar'>
                        <ProgressBar fileName={fileName} progressBar={progressBar}></ProgressBar>
                    </div>
                }
            </div>
        </div>
    )
}

export default UploadFile;