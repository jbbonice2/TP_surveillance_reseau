import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useTable } from 'react-table';
import SideBar from '../partials/sidebar';
import NavBar from '../partials/navbar';

const DataTable = ({ columns, data }) => {
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable({ columns, data });

  return (
    <table {...getTableProps()} className="table">
      <thead>
        {headerGroups.map(headerGroup => (
          <tr {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map(column => (
              <th {...column.getHeaderProps()}>{column.render('Header')}</th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody {...getTableBodyProps()}>
        {rows.map(row => {
          prepareRow(row);
          return (
            <tr {...row.getRowProps()}>
              {row.cells.map(cell => (
                <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
              ))}
            </tr>
          );
        })}
      </tbody>
    </table>
  );
};

const Home = () => {
  const [machines, setMachines] = useState([]);
  const [variableData, setVariableData] = useState([]);
  const token = c1098c68d61f15fda542e1ae3953b838425c91d4;  // Replace with actual token

  useEffect(() => {
    const fetchMachines = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/machines/?token=${token}`);
        setMachines(response.data);
      } catch (error) {
        console.error('Error fetching machines:', error);
      }
    };

    const fetchVariableData = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/variable_data/?token=${token}`);
        setVariableData(response.data);
      } catch (error) {
        console.error('Error fetching variable data:', error);
      }
    };

    fetchMachines();
    fetchVariableData();
  }, [token]);

  const machineColumns = [
    { Header: 'ID', accessor: 'id' },
    { Header: 'Name', accessor: 'name' },
    { Header: 'Type', accessor: 'type' },
    // Add more columns as necessary
  ];

  const variableDataColumns = [
    { Header: 'Machine ID', accessor: 'machine_id' },
    { Header: 'Variable Name', accessor: 'variable_name' },
    { Header: 'Value', accessor: 'value' },
    // Add more columns as necessary
  ];

  return (
    <>
      <NavBar />
      <SideBar />
      <main id="main" className="main">
        <div className="pagetitle">
          <h1>Machine Data</h1>
          <nav>
            <ol className="breadcrumb">
              <li className="breadcrumb-item"><a href="index.html">Home</a></li>
              <li className="breadcrumb-item">Pages</li>
              <li className="breadcrumb-item active">Machine Data</li>
            </ol>
          </nav>
        </div>
        <section className="section">
          <div className="row">
            <div className="col-lg-6">
              <div className="card">
                <div className="card-body">
                  <h5 className="card-title">Machines</h5>
                  <DataTable columns={machineColumns} data={machines} />
                </div>
              </div>
            </div>
            <div className="col-lg-6">
              <div className="card">
                <div className="card-body">
                  <h5 className="card-title">Variable Data</h5>
                  <DataTable columns={variableDataColumns} data={variableData} />
                </div>
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

export default Home;

