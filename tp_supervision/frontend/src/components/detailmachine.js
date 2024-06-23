import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import SideBar from "../patials/sidebar";
import NavBar from "../patials/navbar";
import './detailmachines.css';
import { useParams } from 'react-router-dom';

const DetailMachine = () => {
  const { id } = useParams();
  const [machine, setMachine] = useState(null);
  const [variableData, setVariableData] = useState([]);
  const [error, setError] = useState(null);

  const formatMemory = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  useEffect(() => {
    const fetchData = async () => {
      const token = sessionStorage.getItem('token');
      try {
        const response = await axios.get(`http://localhost:8000/machines/${id}/${token}/`);
        setMachine(response.data.data);
        setVariableData(response.data.variable_data);
      } catch (error) {
        setError('Error fetching the machine details!');
        console.error(error);
      }
    };

    fetchData();
  }, [id]);

  if (error) {
    return <div>{error}</div>;
  }

  if (!machine) {
    return <div>Loading...</div>;
  }

  return (
    <>
      <NavBar />
      <SideBar />
      <main id="main" className="main">
        <div className="pagetitle">
          <h1>Machine Details</h1>
          <nav>
            <ol className="breadcrumb">
              <li className="breadcrumb-item"><a href="/">Home</a></li>
              <li className="breadcrumb-item">Pages</li>
              <li className="breadcrumb-item active">Machine Details</li>
            </ol>
          </nav>
        </div>
        {/* <!-- End Page Title --> */}
  
        <section className="section">
          <div>
            <h1>Caractéristiques de la machine</h1>
            <div style={{ marginBottom: '2rem' }}></div> {/* Ajout de l'espace vide */}
            <DataTable value={[machine]}>
              <Column field="node_name" header="Node Name" />
              <Column field="machine_type" header="Type" />
              <Column field="mac_address" header="MAC Address" />
              <Column field="system" header="System" />
              <Column field="machine_architecture" header="Architecture" />
              <Column field="processor" header="Processor" />
              <Column field="cores" header="Cores" />
              <Column field="logical_cores" header="Logical Cores" />
              <Column field="cpu_frequency" header="CPU Frequency (GHz)" />
              <Column field="total_memory" header="Total Memory" body={(rowData) => formatMemory(rowData.total_memory)} />
              <Column field="total_disk" header="Total Disk" body={(rowData) => formatMemory(rowData.total_disk)} />
              <Column field="version" header="Version" />
              <Column field="releases" header="Releases" />
            </DataTable>
          </div>
        </section>
        <section className="section">
          <div>
            <h1>Variable Data</h1>
            <DataTable value={variableData}>
              {/* Ajoutez les colonnes nécessaires pour variableData ici */}
              {/* Par exemple, si variableData contient des objets avec des champs name et value: */}
              <Column field="name" header="Name" />
              <Column field="value" header="Value" />
            </DataTable>
          </div>
        </section>
      </main>
    
      {/* !-- End #main --> */}

      {/* <!-- ======= Footer ======= --> */}
      <footer id="footer" className="footer">
        <div className="copyright">
          &copy; Copyright <strong><span>NiceAdmin</span></strong>. All Rights Reserved
        </div>
        <div className="credits">
          Designed by <a href="https://bootstrapmade.com/">Jbbonice2 && SergeNoah000</a>
        </div>
      </footer>
      <a href="#" className="back-to-top d-flex align-items-center justify-content-center"><i className="bi bi-arrow-up-short"></i></a>
    </>
  );
};

export default DetailMachine;
