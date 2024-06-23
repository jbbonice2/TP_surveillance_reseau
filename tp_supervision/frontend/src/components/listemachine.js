import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { DropdownButton, Dropdown, ButtonGroup } from 'react-bootstrap';
import SideBar from "../patials/sidebar";
import NavBar from "../patials/navbar";
import 'primereact/resources/themes/saga-blue/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import './listemachines.css';
import { useNavigate } from 'react-router-dom';

const Listemachine = () => {
  const [machines, setMachines] = useState([]);
  const navigate = useNavigate(); // Utilisation de useNavigate pour la navigation

  const formatMemory = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  useEffect(() => {
    const fetchMachines = async () => {
      try {
        const token = sessionStorage.getItem('token');
        if (!token) {
          console.error('Token not found in session storage');
          return;
        }

        const response = await axios.get(`http://localhost:8000/machines/${token}/`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        setMachines(response.data || []);
      } catch (error) {
        console.error('Error fetching machines:', error);
      }
    };

    fetchMachines();
  }, []);

  // Fonction pour gérer la redirection vers la page de détails
  const redirectToDetails = (id) => {
    navigate(`/detailmachine/${id}`);
  };

  return (
    <>
      <NavBar />
      <SideBar />
      <main id="main" className="main">
        <div className="pagetitle">
          <h1>Machines</h1>
          <nav>
            <ol className="breadcrumb">
              <li className="breadcrumb-item"><a href="index.html">Home</a></li>
              <li className="breadcrumb-item">Pages</li>
              <li className="breadcrumb-item active">Machines</li>
            </ol>
          </nav>
        </div>
        <section className="section">
          <div className="datatable-container">
            <h2 className="datatable-title">Machines présentes dans le réseau</h2>
            <DataTable value={machines} paginator rows={10} className="p-datatable-custom" header="Liste des machines">
              <Column field="node_name" header="Node Name" sortable />
              <Column field="machine_type" header="Type" sortable />
              <Column field="mac_address" header="MAC Address" sortable />
              <Column field="system" header="System" sortable />
              <Column field="machine_architecture" header="Architecture" sortable />
              <Column field="processor" header="Processor" sortable />
              <Column field="cores" header="Cores" sortable />
              <Column field="logical_cores" header="Logical Cores" sortable />
              <Column field="cpu_frequency" header="CPU Frequency (GHz)" sortable />
              <Column field="total_memory" header="Total Memory" sortable body={(rowData) => formatMemory(rowData.total_memory)} />
              <Column field="total_disk" header="Total Disk" sortable body={(rowData) => formatMemory(rowData.total_disk)} />
              <Column field="version" header="Version" sortable />
              <Column field="releases" header="Releases" sortable />
              <Column
                header="Actions"
                body={(rowData) => (
                  <DropdownButton
                    as={ButtonGroup}
                    key="dropdown-basic-button"
                    id={`dropdown-button-drop-${rowData.id}`} // Use rowData.id for unique ID
                    title="Actions"
                  >
                    <Dropdown.Item onClick={() => redirectToDetails(rowData.id)}>details en table</Dropdown.Item>
                    <Dropdown.Item onClick={() => redirectToDetails(rowData.id)}>Charge</Dropdown.Item>
                    <Dropdown.Item onClick={() => navigate(`/detailgraph/${rowData.id}`)}>Details en graphe</Dropdown.Item>
                  </DropdownButton>
                )}
              />
            </DataTable>
          </div>
        </section>
      </main>
      <footer id="footer" className="footer">
        <div className="copyright">
          &copy; Copyright <strong><span>NiceAdmin</span></strong>. All Rights Reserved
        </div>
        <div className="credits">
          Designed by <a href="https://bootstrapmade.com/">Jbbonice2 & SergeNoah000</a>
        </div>
      </footer>
      <a href="#" className="back-to-top d-flex align-items-center justify-content-center">
        <i className="bi bi-arrow-up-short"></i>
      </a>
    </>
  );
};

export default Listemachine;
