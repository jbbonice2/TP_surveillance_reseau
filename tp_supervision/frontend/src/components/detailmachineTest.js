import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import SideBar from "../patials/sidebar";
import NavBar from "../patials/navbar";
import './detailmachines.css';
import { useParams } from 'react-router-dom';
import { ProgressSpinner } from 'primereact/progressspinner';
import 'primereact/resources/themes/saga-blue/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';

const VarMachine = () => {
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
        const response = await axios.get(`http://localhost:8000/variabledata/${id}/${token}/`);
        setMachine(response.data); // Assuming data is an array with a single machine object
        setVariableData(response.data.variabledata_set        );
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
    return <div><ProgressSpinner/></div>;
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
  
        <section className="section">
          <div>
            <h1>Caractéristiques de la machine</h1>
            <div style={{ marginBottom: '2rem' }}></div>
            <DataTable value={[machine]} >
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
            <DataTable value={variableData} rowsPerPageOptions={[5, 10, 25, 50]} paginator rows={12} className="p-datatable-gridlines">
              {/* <Column field="machine" header="Machine" body={(rowData) => rowData.machine.name} /> Assuming machine has a 'name' field */}
              <Column field="mac_address" header="MAC Address" />
              <Column field="battery_percentage" header="Battery Percentage" />
              <Column field="uptime" header="Uptime" body={(rowData) => `${rowData.uptime} s`} />
              <Column field="boot_time" header="Boot Time" body={(rowData) => new Date(rowData.boot_time).toLocaleString()} />
              <Column field="shutdown_time" header="Shutdown Time" body={(rowData) => rowData.shutdown_time ? new Date(rowData.shutdown_time).toLocaleString() : 'N/A'} />
              <Column field="collected_at" header="Collected At" body={(rowData) => new Date(rowData.collected_at).toLocaleString()} />
            </DataTable>
          </div>
        </section>
      </main>
    
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

export default VarMachine;
