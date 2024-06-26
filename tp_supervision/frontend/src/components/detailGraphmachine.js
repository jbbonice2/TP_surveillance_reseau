
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import SideBar from "../patials/sidebar";
import NavBar from "../patials/navbar";
import './detailgraphmachines.css';
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

  // Extract data for charts
  const memoryData = variableData.map(d => d.memory_percentage);
  const swapData = variableData.map(d => d.swap_used);
  const diskData = variableData.map(d => d.disk_percentage);
  const cpuLoadData = variableData.map(d => d.cpu_load_per_core);
  const netSentData = variableData.map(d => d.net_bytes_sent);
  const netRecvData = variableData.map(d => d.net_bytes_recv);
  const cpuTempData = variableData.map(d => d.cpu_temperature);
  const timestamps = variableData.map(d => new Date(d.collected_at));

  // Configurations for ApexCharts
  const memoryChartOptions = {
    chart: {
      type: 'line',
      height: 350
    },
    xaxis: {
      categories: timestamps
    },
    series: [
      {
        name: 'Memory Usage',
        data: memoryData
      }
    ]
  };

  const swapChartOptions = {
    chart: {
      type: 'line',
      height: 350
    },
    xaxis: {
      categories: timestamps
    },
    series: [
      {
        name: 'Swap Usage',
        data: swapData
      }
    ]
  };

  const diskChartOptions = {
    chart: {
      type: 'line',
      height: 350
    },
    xaxis: {
      categories: timestamps
    },
    series: [
      {
        name: 'Disk Usage',
        data: diskData
      }
    ]
  };

  const networkChartOptions = {
    chart: {
      type: 'line',
      height: 350
    },
    xaxis: {
      categories: timestamps
    },
    series: [
      {
        name: 'Net Bytes Sent',
        data: netSentData
      },
      {
        name: 'Net Bytes Received',
        data: netRecvData
      }
    ]
  };

  const cpuChartOptions = {
    chart: {
      type: 'line',
      height: 350
    },
    xaxis: {
      categories: timestamps
    },
    series: cpuLoadData[0]
      ? cpuLoadData[0].map((_, index) => ({
          name: `CPU Core ${index + 1}`,
          data: cpuLoadData.map(d => d[index])
        }))
      : []
  };

  const cpuTempChartOptions = {
    chart: {
      type: 'line',
      height: 350
    },
    stroke:{
      curve:'smooth',
    },
    xaxis: {
      categories: timestamps
    },
    series: [
      {
        name: 'CPU Temperature',
        data: cpuTempData
      }
    ]
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
              <Column field="total_memory" header="Total Memory" />
              <Column field="total_disk" header="Total Disk" />
              <Column field="version" header="Version" />
              <Column field="releases" header="Releases" />
            </DataTable>
          </div>
        </section>
        
        <section className="section">
          <div>
            <h1>Variable Data</h1>
            <div className="charts-container">
              <div className="chart-card">
                <h2>Memory Usage</h2>
                <Chart options={memoryChartOptions} series={memoryChartOptions.series} type="line" height={350} />
              </div>
              <div className="chart-card">
                <h2>Swap Usage</h2>
                <Chart options={swapChartOptions} series={swapChartOptions.series} type="line" height={350} />
              </div>
              <div className="chart-card">
                <h2>Disk Usage</h2>
                <Chart options={diskChartOptions} series={diskChartOptions.series} type="line" height={350} />
              </div>
              <div className="chart-card">
                <h2>Network Usage</h2>
                <Chart options={networkChartOptions} series={networkChartOptions.series} type="line" height={350} />
              </div>
              <div className="chart-card">
                <h2>CPU Load per Core</h2>
                <Chart options={cpuChartOptions} series={cpuChartOptions.series} type="line" height={350} />
              </div>
              <div className="chart-card">
                <h2>CPU Temperature</h2>
                <Chart options={cpuTempChartOptions} series={cpuTempChartOptions.series} type="line" height={350} />
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

