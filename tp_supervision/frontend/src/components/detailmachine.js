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
        setMachine(response.data); // Assuming data is an array with a single machine object
        setVariableData(response.data.data);
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
  
        <section className="section">
          <div>
            <h1>Caractéristiques de la machine</h1>
            <div style={{ marginBottom: '2rem' }}></div>
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
              <Column field="id" header="ID" />
              <Column field="used_memory" header="Used Memory" />
              <Column field="memory_percentage" header="Memory Percentage" />
              <Column field="swap_used" header="Swap Used" />
              <Column field="disk_percentage" header="Disk Percentage" />
              <Column field="cpu_load_per_core" header="CPU Load per Core" body={(rowData) => rowData.cpu_load_per_core.join(', ')} />
              <Column field="net_bytes_sent" header="Net Bytes Sent" />
              <Column field="net_bytes_recv" header="Net Bytes Received" />
              <Column field="active_processes" header="Active Processes" />
              <Column field="gpu_usage_percentage" header="GPU Usage Percentage" />
              <Column field="cpu_temperature" header="CPU Temperature" />
              <Column field="collected_at" header="Collected At" />
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

export default DetailMachine;
