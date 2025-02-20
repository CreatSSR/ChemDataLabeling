import React, { useState } from "react";
import axios from "axios";
import { Document, Page } from 'react-pdf';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [pdfUrl, setPdfUrl] = useState("");
  const [reactionInfo, setReactionInfo] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFileUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });
      setPdfUrl(response.data.pdf_path);
      setReactionInfo(response.data.reactions);
    } catch (error) {
      console.error("Error uploading file", error);
    }
  };

  return (
    <div className="App">
      <h1>化学文献标注系统</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleFileUpload}>上传文献</button>

      {reactionInfo && (
        <div>
          <h2>提取的化学反应</h2>
          <pre>{reactionInfo}</pre>
        </div>
      )}

      {pdfUrl && (
        <div>
          <h2>处理后的PDF</h2>
          <Document file={pdfUrl}>
            <Page pageNumber={1} />
          </Document>
        </div>
      )}
    </div>
  );
}

export default App;

