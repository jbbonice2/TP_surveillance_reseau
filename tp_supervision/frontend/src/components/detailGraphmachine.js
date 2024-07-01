
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
  const timestamps = variableData.map(d => new Date(d.collected_at).toLocaleString());


    // Function to calculate statistics
    const calculateStatistics = (data) => {
      const sum = data.reduce((a, b) => a + b, 0);
      const avg = (sum / data.length) || 0;
      const min = Math.min(...data);
      const max = Math.max(...data);
      const freeAvg = data.length > 0 ? (100 - avg) : 0; // Assuming percentage values for memory
  
      return { avg, freeAvg, min, max };
    };


  const memoryStats = calculateStatistics(memoryData);
  const swapStats = calculateStatistics(swapData);
  const diskStats = calculateStatistics(diskData);
  // const cpuLoadStats = calculateStatistics(cpuLoadData.flat());
  const netSentStats = calculateStatistics(netSentData);
  const netRecvStats = calculateStatistics(netRecvData);
  const cpuTempStats = calculateStatistics(cpuTempData);

  
  // Configurations for ApexCharts
  const memoryChartOptions = {
    chart: {
      type: 'area',
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
    ],
    annotations: {
      yaxis: [
        {
          y: memoryStats.avg,
          borderColor: '#00E396',
          label: {
            borderColor: '#00E396',
            style: {
              color: '#fff',
              background: '#00E396',
            },
            text: `Avg: ${memoryStats.avg.toFixed(2)}`,
          }
        },
        {
          y: memoryStats.min,
          borderColor: '#FEB019',
          label: {
            borderColor: '#FEB019',
            style: {
              color: '#fff',
              background: '#FEB019',
            },
            text: `Min: ${memoryStats.min.toFixed(2)}`,
          }
        },
        {
          y: memoryStats.max,
          borderColor: '#FF4560',
          label: {
            borderColor: '#FF4560',
            style: {
              color: '#fff',
              background: '#FF4560',
            },
            text: `Max: ${memoryStats.max.toFixed(2)}`,
          }
        }
      ]
    },
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.7,
        opacityTo: 0.9,
        stops: [0, 100]
      }
    },
    dataLabels: {
      enabled: false
    },
  };

  const swapChartOptions = {
    chart: {
      type: 'area',
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
    ],
    annotations: {
      yaxis: [
        {
          y: swapStats.avg,
          borderColor: '#00E396',
          label: {
            borderColor: '#00E396',
            style: {
              color: '#fff',
              background: '#00E396',
            },
            text: `Avg: ${swapStats.avg.toFixed(2)}`,
          }
        },
        {
          y: swapStats.min,
          borderColor: '#FEB019',
          label: {
            borderColor: '#FEB019',
            style: {
              color: '#fff',
              background: '#FEB019',
            },
            text: `Min: ${swapStats.min.toFixed(2)}`,
          }
        },
        {
          y: swapStats.max,
          borderColor: '#FF4560',
          label: {
            borderColor: '#FF4560',
            style: {
              color: '#fff',
              background: '#FF4560',
            },
            text: `Max: ${swapStats.max.toFixed(2)}`,
          }
        }
      ]
    },
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.7,
        opacityTo: 0.9,
        stops: [0, 100]
      }
    },
    dataLabels: {
      enabled: false
    },
  };

  const diskChartOptions = {
    chart: {
      type: 'area',
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
    ],
    annotations: {
      yaxis: [
        {
          y: diskStats.avg,
          borderColor: '#00E396',
          label: {
            borderColor: '#00E396',
            style: {
              color: '#fff',
              background: '#00E396',
            },
            text: `Avg: ${diskStats.avg.toFixed(2)}`,
          }
        },
        {
          y: diskStats.min,
          borderColor: '#FEB019',
          label: {
            borderColor: '#FEB019',
            style: {
              color: '#fff',
              background: '#FEB019',
            },
            text: `Min: ${diskStats.min.toFixed(2)}`,
          }
        },
        {
          y: diskStats.max,
          borderColor: '#FF4560',
          label: {
            borderColor: '#FF4560',
            style: {
              color: '#fff',
              background: '#FF4560',
            },
            text: `Max: ${diskStats.max.toFixed(2)}`,
          }
        }
      ]
    },
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.7,
        opacityTo: 0.9,
        stops: [0, 100]
      }
    },
    dataLabels: {
      enabled: false
    },
  };

  const networkChartOptions = {
    chart: {
      type: 'area',
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
    ],
    annotations: {
      yaxis: [
        {
          y: netSentStats.avg,
          borderColor: '#00E396',
          label: {
            borderColor: '#00E396',
            style: {
              color: '#fff',
              background: '#00E396',
            },
            text: `Avg: ${netSentStats.avg.toFixed(2)}`,
          }
        },
        {
          y: netSentStats.min,
          borderColor: '#FEB019',
          label: {
            borderColor: '#FEB019',
            style: {
              color: '#fff',
              background: '#FEB019',
            },
            text: `Min: ${netSentStats.min.toFixed(2)}`,
          }
        },
        {
          y: netSentStats.max,
          borderColor: '#FF4560',
          label: {
            borderColor: '#FF4560',
            style: {
              color: '#fff',
              background: '#FF4560',
            },
            text: `Max: ${netSentStats.max.toFixed(2)}`,
          }
        }
      ]
    },
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.7,
        opacityTo: 0.9,
        stops: [0, 100]
      }
    },
    dataLabels: {
      enabled: false
    },
  };

  const cpuChartOptions = {
    chart: {
      type: 'area',
      height: 350
    },
    dataLabels: {
      enabled: false
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
      type: 'area',
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
    ],
    annotations: {
      yaxis: [
        {
          y: cpuTempStats.avg,
          borderColor: '#00E396',
          label: {
            borderColor: '#00E396',
            style: {
              color: '#fff',
              background: '#00E396',
            },
            text: `Avg: ${cpuTempStats.avg.toFixed(2)}`,
          }
        },
        {
          y: cpuTempStats.min,
          borderColor: '#FEB019',
          label: {
            borderColor: '#FEB019',
            style: {
              color: '#fff',
              background: '#FEB019',
            },
            text: `Min: ${cpuTempStats.min.toFixed(2)}`,
          }
        },
        {
          y: cpuTempStats.max,
          borderColor: '#FF4560',
          label: {
            borderColor: '#FF4560',
            style: {
              color: '#fff',
              background: '#FF4560',
            },
            text: `Max: ${cpuTempStats.max.toFixed(2)}`,
          }
        }
      ]
    },
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.7,
        opacityTo: 0.9,
        stops: [0, 100]
      }
    },
    dataLabels: {
      enabled: false
    },
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
                <Chart options={memoryChartOptions} series={memoryChartOptions.series} type='area' height={350} />
              </div>
              <div className="chart-card">
                <h2>Swap Usage</h2>
                <Chart options={swapChartOptions} series={swapChartOptions.series} type='area' height={350} />
              </div>
              <div className="chart-card">
                <h2>Disk Usage</h2>
                <Chart options={diskChartOptions} series={diskChartOptions.series} type='area' height={350} />
              </div>
              <div className="chart-card">
                <h2>Network Usage</h2>
                <Chart options={networkChartOptions} series={networkChartOptions.series} type='area' height={350} />
              </div>
              <div className="chart-card">
                <h2>CPU Load per Core</h2>
                <Chart options={cpuChartOptions} series={cpuChartOptions.series} type='area' height={350} />
              </div>
              <div className="chart-card">
                <h2>CPU Temperature</h2>
                <Chart options={cpuTempChartOptions} series={cpuTempChartOptions.series} type='area' height={350} />
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






// import React, { useEffect, useState } from 'react';
// import axios from 'axios';
// import { DataTable } from 'primereact/datatable';
// import { Column } from 'primereact/column';
// import SideBar from "../patials/sidebar";
// import NavBar from "../patials/navbar";
// import './detailgraphmachines.css';
// import { useParams } from 'react-router-dom';
// import { ProgressSpinner } from 'primereact/progressspinner';
// import 'primereact/resources/themes/saga-blue/theme.css';
// import 'primereact/resources/primereact.min.css';
// import 'primeicons/primeicons.css';
// import Chart from 'react-apexcharts';

// // Utility function to calculate statistics
// const calculateStatistics = (data) => {
//   if (!data.length) return { average: 0, min: 0, max: 0 };
//   const sum = data.reduce((acc, value) => acc + value, 0);
//   const average = sum / data.length;
//   const min = Math.min(...data);
//   const max = Math.max(...data);
//   return { average, min, max };
// };

// const DetailGraphMachine = () => {
//   const { id } = useParams();
//   const [machine, setMachine] = useState(null);
//   const [variableData, setVariableData] = useState([]);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     const fetchData = async () => {
//       const token = sessionStorage.getItem('token');
//       try {
//         const response = await axios.get(`http://localhost:8000/machines/${id}/${token}/`);
//         setMachine(response.data);
//         setVariableData(response.data.data);
//       } catch (error) {
//         setError('Error fetching the machine details!');
//         console.error(error);
//       }
//     };
//     fetchData();
//   }, [id]);

//   if (error) {
//     return <div>{error}</div>;
//   }

//   if (!machine) {
//     return <div><ProgressSpinner/></div>;
//   }

//   const memoryData = variableData.map(d => d.memory_percentage);
//   const cpuLoadData = variableData.map(d => d.cpu_load_per_core);
//   const cpuTempData = variableData.map(d => d.cpu_temperature);
//   const swapData = variableData.map(d => d.swap_used);
//   const diskData = variableData.map(d => d.disk_percentage);
//   const netSentData = variableData.map(d => d.net_bytes_sent / 1024); // Convert bytes to KB
//   const netRecvData = variableData.map(d => d.net_bytes_recv / 1024); // Convert bytes to KB
//   const timestamps = variableData.map(d => new Date(d.collected_at).toLocaleString());

//   const memoryStats = calculateStatistics(memoryData);
//   const swapStats = calculateStatistics(swapData);
//   const diskStats = calculateStatistics(diskData);
//   const cpuLoadStats = calculateStatistics(cpuLoadData.flat());
//   const netSentStats = calculateStatistics(netSentData);
//   const netRecvStats = calculateStatistics(netRecvData);
//   const cpuTempStats = calculateStatistics(cpuTempData);

//   const chartOptions = (title, stats) => ({
//     chart: {
//       type: 'area',
//       height: 350,
//       toolbar: {
//         show: true
//       }
//     },
//     stroke: {
//       curve: 'smooth'
//     },
//     fill: {
//       type: 'gradient',
//       gradient: {
//         shade: 'dark',
//         type: "vertical",
//         shadeIntensity: 0.5,
//         gradientToColors: undefined,
//         inverseColors: true,
//         opacityFrom: 0.7,
//         opacityTo: 0.3,
//         stops: [0, 90, 100]
//       }
//     },
//     xaxis: {
//       categories: timestamps
//     },
//     title: {
//       text: `${title}`,
//       align: 'left'
//     },
//     annotations: stats ? {
//       yaxis: [{
//         y: stats?.average,
//         borderColor: '#00E396',
//         label: {
//           borderColor: '#00E396',
//           style: {
//             color: '#fff',
//             background: '#00E396'
//           },
//           text: `Average: ${stats?.average?.toFixed(2)}`
//         }
//       }, {
//         y: stats.min,
//         borderColor: '#FEB019',
//         label: {
//           borderColor: '#FEB019',
//           style: {
//             color: '#fff',
//             background: '#FEB019'
//           },
//           text: `Min: ${stats.min}`
//         }
//       }, {
//         y: stats.max,
//         borderColor: '#FF4560',
//         label: {
//           borderColor: '#FF4560',
//           style: {
//             color: '#fff',
//             background: '#FF4560'
//           },
//           text: `Max: ${stats.max}`
//         }
//       }]
//     } : {}
//   });

//   const charts = [
//     { title: "Memory Usage", data: memoryData, stats: memoryStats },
//     {
//       title: "CPU Load per Core",
//       data: cpuLoadData[0]
//         ? cpuLoadData[0].map((_, index) => ({
//             name: `CPU Core ${index + 1}`,
//             data: cpuLoadData.map(d => d[index])
//           }))
//         : [],
//       stats: cpuLoadStats
//     },
//     { title: "CPU Temperature", data: cpuTempData, stats: cpuTempStats },
//     {
//       title: "Network Usage",
//       data: [
//         { name: 'Net Bytes Sent (KB)', data: netSentData },
//         { name: 'Net Bytes Received (KB)', data: netRecvData }
//       ],
//       stats:netRecvStats // { send: netSentStats, recv: netRecvStats }
//     },
//     { title: "Swap Usage", data: swapData, stats: swapStats },
//     { title: "Disk Usage", data: diskData, stats: diskStats },
//   ];

//   return (
//     <>
//       <NavBar />
//       <SideBar />
//       <main id="main" className="main">
//         <div className="pagetitle">
//           <h1>Machine Details</h1>
//           <nav>
//             <ol className="breadcrumb">
//               <li className="breadcrumb-item"><a href="/">Home</a></li>
//               <li className="breadcrumb-item">Pages</li>
//               <li className="breadcrumb-item active">Machine Details</li>
//             </ol>
//           </nav>
//         </div>
  
//         <section className="section">
//           <div>
//             <h1>Caractéristiques de la machine</h1>
//             <div style={{ marginBottom: '2rem' }}></div>
//             <DataTable value={[machine]} >
//               <Column field="node_name" header="Node Name" />
//               <Column field="machine_type" header="Type" />
//               <Column field="mac_address" header="MAC Address" />
//               <Column field="system" header="System" />
//               <Column field="machine_architecture" header="Architecture" />
//               <Column field="processor" header="Processor" />
//               <Column field="cores" header="Cores" />
//               <Column field="logical_cores" header="Logical Cores" />
//               <Column field="cpu_frequency" header="CPU Frequency (GHz)" />
//               <Column field="total_memory" header="Total Memory" />
//               <Column field="total_disk" header="Total Disk" />
//               <Column field="version" header="Version" />
//               <Column field="releases" header="Releases" />
//             </DataTable>
//           </div>
//         </section>
        
//         <section className="section">
//           <div>
//             <h1>Variable Data</h1>
//             <div className="charts-container">
//               {charts.map((chart, index) => (
//                 <div key={index} className="chart-card">
//                   <h2>{chart.title}</h2>
//                   <Chart
//                     options={chartOptions(chart.title, chart.stats)}
//                     series={chart.title === "Network Usage" ? chart.data : [{ name: chart.title, data: chart.data }]}
//                     type='area'
//                     height={350}
//                   />
//                   <div className="stats">
//                     {chart.stats && (
//                       <>
//                         <p>Average: {chart.stats?.average.toFixed(2)}</p>
//                         <p>Min: {chart.stats.min}</p>
//                         <p>Max: {chart.stats.max}</p>
//                       </>
//                     )}
//                   </div>
//                 </div>
//               ))}
//             </div>
//           </div>
//         </section>
//       </main>
  
//       <footer id="footer" className="footer">
//         <div className="copyright">
//           &copy; Copyright <strong><span>NiceAdmin</span></strong>. All Rights Reserved
//         </div>
//         <div className="credits">
//           Designed by <a href="https://github.com/SergeNoah000">Jbbonice2 && SergeNoah000</a>
//         </div>
//       </footer>
//       <a href="#" className="back-to-top d-flex align-items-center justify-content-center"><i className="bi bi-arrow-up-short"></i></a>
//     </>
//   );
// };

// export default DetailGraphMachine;


