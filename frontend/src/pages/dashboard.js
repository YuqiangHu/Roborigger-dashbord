import Layout from '../components/layout';
import { useState } from "react";

import { FileUploader } from "react-drag-drop-files";
const fileTypes = ["CSV"];
const uploadmessagefile = new FormData();
const pdfprogressform = new FormData();
var current = new Date();
var title=current.getTime();
var outputlink="http://localhost:8000/setup/generatePdf/?title="+title;


export default function App() {
  
  const [ messagefile, setmessagefile ] = useState();
  const handleChangemsg = (file) => {
    setmessagefile(file[0]);
  }
  const upload = () => {
    uploadmessagefile.append('title', title);
    uploadmessagefile.append('file', messagefile, messagefile.name);
    fetch('http://127.0.0.1:8000/uploadfile/', {
      method: 'POST',
      body: uploadmessagefile
    })
    .then( res => {console.log("uploadmessagefile",res);
      var x = document.getElementById("btnmakeplot");
      x.style.display = "block";
    })
    .catch(error => alert(error))
  } 
  const pdfprogress = () => {
    var x = document.getElementById("btnmakeplot");
    x.innerHTML = "Creating Plots....";
    pdfprogressform.append('title', title);
    pdfprogressform.append('csvfile', messagefile.name);
    fetch('http://127.0.0.1:8000/processs/', {
      method: 'POST',
      body: pdfprogressform
    })
    .then( res => {console.log("pdfprogressform",res);
    })
    .catch(error => alert(error))


    fetch('http://127.0.0.1:8000/setup/makepdf/', {
      method: 'POST',
      body: pdfprogressform
    })
    .then( res => {alert("Plots Created");
    var x = document.getElementById("btnmakeplot");
    x.innerHTML = "Plots Created";
    var x = document.getElementById("btnmakepdf");
    x.href = outputlink;
    x.style.display = "block";  
    })
    .catch(error => alert(error))

  } 
  return (
    <Layout title='' content='Dashboard page'>
    
    <div class="panel panel-default">

    <div class="panel-body">
    
    <div className="App" class="panel-body">
        <h2>Upload Message CSV file</h2>
            <FileUploader
                multiple={true}
                handleChange={handleChangemsg}
                name="messagefile"
                types={fileTypes}
            />
            <p>{messagefile ?  `File name: ${messagefile.name}` : "No file uploaded" }</p>
            
            <div class="d-grid gap-2">
            <button onClick={() => upload()} class="btn btn-primary btn-block">Upload Data File</button>
            <button id="btnmakeplot" style={{display:"none"}} onClick={() => pdfprogress()} class="btn btn-warning btn-block">Create Plots</button>
            <a id="btnmakepdf" style={{display:"none"}} href="/" class="btn btn-success btn-block">Create PDF</a>
      </div>
    </div>
  </div>

    </div>







   
        </Layout>
  );}
