// import React, { useEffect, useState } from 'react';
// import { DataTable } from 'primereact/datatable';
// import { Column } from 'primereact/column';
// import 'primereact/resources/themes/lara-light-indigo/theme.css';
// import 'primereact/resources/primereact.min.css';
// import 'primeicons/primeicons.css';

// function MyDataTable() {
//   const [data, setData] = useState([]);

//   useEffect(() => {
//     fetch('/donnees.json')
//       .then(response => response.json())
//       .then(data => setData(data))
//       .catch(error => console.error('Erreur lors de la récupération des données !', error));
//   }, []);

//   return (
//     <div className="container">
//       <h2 className="text-center mb-4">Tableau de données</h2>
//       <DataTable value={data} responsiveLayout="stack" breakpoint="960px">
//         {/* <Column field="id" header="ID" sortable></Column>
//         <Column field="machine_id" header="ID Machine" sortable></Column> */}
//         <Column field="timestamp" header="Timestamp" sortable>
//           {rowData => new Date(rowData.timestamp).toLocaleString()}
//         </Column>
//         <Column field="used_memory" header="Mémoire utilisée" sortable></Column>
//         <Column field="memory_percentage" header="Pourcentage de mémoire" sortable></Column>
//         <Column field="cached_memory" header="Mémoire mise en cache" sortable></Column>
//         <Column field="swap_total" header="Total du swap" sortable></Column>
//         <Column field="swap_used" header="Swap utilisé" sortable></Column>
//         <Column field="swap_percentage" header="Pourcentage de swap" sortable></Column>
//         <Column field="used_disk" header="Disque utilisé" sortable></Column>
//         <Column field="disk_percentage" header="Pourcentage de disque" sortable></Column>
//         <Column field="cpu_load_per_core" header="Charge CPU par cœur" sortable></Column>
//         <Column field="net_bytes_sent" header="Octets réseau envoyés" sortable></Column>
//         <Column field="net_bytes_recv" header="Octets réseau reçus" sortable></Column>
//         <Column field="active_processes" header="Processus actifs" sortable></Column>
//       </DataTable>
//     </div>
//   );
// }

// export default MyDataTable;import React, { useEffect, useState } from 'react';
import React, { useEffect, useState } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import './datatable.css';

function CustomDataTable() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('/donnees.json') // Assurez-vous de spécifier correctement l'URL de votre fichier JSON
      .then(response => response.json())
      .then(data => setData(data))
      .catch(error => console.error('Erreur lors de la récupération des données !', error));
  }, []);

  const dateBodyTemplate = (rowData) => {
    return new Date(rowData.timestamp).toLocaleString();
  };

  const sizeBodyTemplate = (size) => {
    if (size < 1024) return `${size} B`;
    else if (size < 1048576) return `${(size / 1024).toFixed(2)} KB`;
    else if (size < 1073741824) return `${(size / 1048576).toFixed(2)} MB`;
    else return `${(size / 1073741824).toFixed(2)} GB`;
  };

  return (
    <div className="datatable-container">
      <h2 className="text-center mb-4">Tableau de Données Variables</h2>
      <DataTable value={data} responsiveLayout="scroll" className="p-datatable-custom">
        {/* <Column field="id" header="ID" sortable></Column>
        <Column field="machine_id" header="ID Machine" sortable></Column> */}
        <Column field="timestamp" header="Timestamp" body={dateBodyTemplate} sortable></Column>
        <Column field="used_memory" header="Mémoire utilisée" body={(rowData) => sizeBodyTemplate(rowData.used_memory)} sortable></Column>
        <Column field="memory_percentage" header="Pourcentage de mémoire" sortable></Column>
        <Column field="cached_memory" header="Mémoire mise en cache" body={(rowData) => sizeBodyTemplate(rowData.cached_memory)} sortable></Column>
        <Column field="swap_total" header="Total du swap" body={(rowData) => sizeBodyTemplate(rowData.swap_total)} sortable></Column>
        <Column field="swap_used" header="Swap utilisé" body={(rowData) => sizeBodyTemplate(rowData.swap_used)} sortable></Column>
        <Column field="swap_percentage" header="Pourcentage de swap" sortable></Column>
        <Column field="used_disk" header="Disque utilisé" body={(rowData) => sizeBodyTemplate(rowData.used_disk)} sortable></Column>
        <Column field="disk_percentage" header="Pourcentage de disque" sortable></Column>
        <Column field="cpu_load_per_core" header="Charge CPU par cœur" sortable></Column>
        <Column field="net_bytes_sent" header="Octets réseau envoyés" body={(rowData) => sizeBodyTemplate(rowData.net_bytes_sent)} sortable></Column>
        <Column field="net_bytes_recv" header="Octets réseau reçus" body={(rowData) => sizeBodyTemplate(rowData.net_bytes_recv)} sortable></Column>
        <Column field="active_processes" header="Processus actifs" sortable></Column>
      </DataTable>
    </div>
  );
}

export default CustomDataTable;
