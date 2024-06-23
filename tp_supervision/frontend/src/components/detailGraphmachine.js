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
import Chart from 'react-apexcharts';

const DetailGraphMachine = () => {
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
    return <div><ProgressSpinner/></div>;
  }

  const memoryOptions = {
    chart: {
      type: 'line',
      height: 350
    },
    series: [{
      name: 'Memory Usage',
      data: variableData.map(data => data.memory_percentage)
    }],
    xaxis: {
      categories: variableData.map(data => data.collected_at)
    }
  };

  const swapOptions = {
    chart: {
      type: 'line',
      height: 350
    },
    series: [{
      name: 'Swap Usage',
      data: variableData.map(data => data.swap_percentage)
    }],
    xaxis: {
      categories: variableData.map(data => data.collected_at)
    }
  };

  const diskOptions = {
    chart: {
      type: 'line',
      height: 350
    },
    series: [{
      name: 'Disk Usage',
      data: variableData.map(data => data.disk_percentage)
    }],
    xaxis: {
      categories: variableData.map(data => data.collected_at)
    }
  };

  const networkOptions = {
    chart: {
      type: 'line',
      height: 350
    },
    series: [
      {
        name: 'Net Bytes Sent',
        data: variableData.map(data => data.net_bytes_sent)
      },
      {
        name: 'Net Bytes Received',
        data: variableData.map(data => data.net_bytes_recv)
      }
    ],
    xaxis: {
      categories: variableData.map(data => data.collected_at)
    }
  };

  const getCpuLoadSeries = () => {
    const series = [];
    if (variableData.length > 0) {
      const numCores = variableData[0].cpu_load_per_core.length;
      for (let i = 0; i < numCores; i++) {
        series.push({
          name: `Core ${i + 1} Load`,
          data: variableData.map(data => data.cpu_load_per_core[i])
        });
      }
      series.push({
        name: 'Average CPU Load',
        data: variableData.map(data => data.cpu_load_per_core.reduce((a, b) => a + b, 0) / numCores)
      });
    }
    return series;
  };

  const cpuOptions = {
    chart: {
      type: 'line',
      height: 350
    },
    series: getCpuLoadSeries(),
    xaxis: {
      categories: variableData.map(data => data.collected_at)
    }
  };

  const temperatureOptions = {
    chart: {
      type: 'line',
      height: 350
    },
    series: [{
      name: 'CPU Temperature',
      data: variableData.map(data => data.cpu_temperature)
    }],
    xaxis: {
      categories: variableData.map(data => data.collected_at)
    }
  };

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
            <div className="charts">
              <div className="chart">
                <h3>Memory Usage</h3>
                <Chart options={memoryOptions} series={memoryOptions.series} type="line" height={350} />
              </div>
              <div className="chart">
                <h3>Swap Usage</h3>
                <Chart options={swapOptions} series={swapOptions.series} type="line" height={350} />
              </div>
              <div className="chart">
                <h3>Disk Usage</h3>
                <Chart options={diskOptions} series={diskOptions.series} type="line" height={350} />
              </div>
              <div className="chart">
                <h3>Network Usage</h3>
                <Chart options={networkOptions} series={networkOptions.series} type="line" height={350} />
              </div>
              <div className="chart">
                <h3>CPU Load</h3>
                <Chart options={cpuOptions} series={cpuOptions.series} type="line" height={350} />
              </div>
              <div className="chart">
                <h3>CPU Temperature</h3>
                <Chart options={temperatureOptions} series={temperatureOptions.series} type="line" height={350} />
              </div>
            </div>
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

export default DetailGraphMachine;
