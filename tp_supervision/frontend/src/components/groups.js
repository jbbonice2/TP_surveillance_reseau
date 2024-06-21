import React, { useEffect, useState } from "react";
import axios from "axios";
import NavBar from "../patials/navbar";
import SideBar from "../patials/sidebar";
import GroupDetailCard from './detailGroup'; 

import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';

const Group =()=>{

  const [groupName, setGroupName] = useState('');
  const [descriptionGroup, setDescriptionGroup] = useState('');
  const [message, setMessage] = useState(null);
  const [loaded, setLoaded] = useState(false);
  const [groups, setGroups] = useState();
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [showUpdateModal, setShowUpdateModal] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);

  const truncateDescription = (description) => {
    const maxLength = 10;
    if (description.length > maxLength) {
      return `${description.substring(0, maxLength)}...`;
    }
    return description;
  };

  const handleUpdateGroup = async () => {
    try {
      const response = await axios.put(`http://localhost:8000/update_detail/${selectedGroup.id}`, {
        name: groupName,
        description: descriptionGroup
      });
      const updatedData = groups.map(group => (group.id === selectedGroup.id ? response.data : group));
      setGroups(updatedData);
      setGroupName(''); // Réinitialiser les champs après la mise à jour
      setDescriptionGroup('');
      setShowUpdateModal(false); // Fermer le modal après la mise à jour
      console.log('Group updated:', response.data);
    } catch (error) {
      console.error('Error updating group:', error);
        setMessage(error.message);
        setTimeout(() => {
          setMessage('');
      }, 5000);
    }  };

  const handleDeleteGroup = async () => {
    try {
      await axios.delete(`http://localhost:8000/delete_detail/${selectedGroup.id}`);
      const updatedData = groups.filter(group => group.id !== selectedGroup.id);
      setGroups(updatedData);
      setSelectedGroup(null);
      console.log('Group deleted successfully');
    } catch (error) {
      console.error('Error deleting group:', error);
      setMessage(error.message);
      setTimeout(() => {
        setMessage('');
    }, 5000);
    }
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    setMessage(null);
    const token = sessionStorage.getItem('token');
    try {
      const response = await axios.post(`http://localhost:8000/groups/${token}/`, {
        name: groupName,
        description: descriptionGroup
      });
      setMessage(response.data.message);
      setShowAddModal(false); // Fermer le modal après l'ajout
      setGroupName('');
      setDescriptionGroup('');
    } catch (error) {
      console.error('Erreur lors de l\'envoi du formulaire :', error);
      setMessage(error.message);
      setTimeout(() => {
        setMessage('');
    }, 5000);
    };
  }

  const getGroups = async () => {
    setMessage(null);
    const token = sessionStorage.getItem('token');
    try {
      const response = await axios.get(`http://localhost:8000/get_all_groups/${token}`);
      console.log(response.data); 
      setGroups(response.data);
    } catch (error) {
      console.error('Erreur lors de l\'envoi du formulaire :', error);
      setMessage(error.message);
      setTimeout(() => {
        setMessage('');
    }, 5000);
    };
  }

  useEffect(()=>{
    if(!loaded){
      getGroups();
      setLoaded(true);
    }
  }, []); // <-- Dépendance vide pour exécuter une seule fois

  return(
    <>
      <NavBar/>
      <SideBar/>
      <main id="main" className="main">

        <div className="pagetitle">
          <h1>Gestion des groupes</h1>
          <nav>
            <ol className="breadcrumb">
              <li className="breadcrumb-item"><a href="/">Accueil</a></li>
            </ol>
            <span title="Creer un nouveau groupe" style={{"position":"relative", left:'90%'}} className="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#addModal"><i className="bi bi-plus "></i>Ajouter</span>


            <div className="modal fade" id="addModal" tabIndex="-1" style={{"display":"none"}} aria-hidden="true">
              <div className="modal-dialog modal-dialog-centered">
                <div className="modal-content">
                  <div className="modal-header">
                    <h5 className="modal-title">Ajouter un groupe</h5>
                    <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                  </div>
                  <div className="modal-body">
                    <form>
                      {message && (
                        <h3 style={{color:"violet", fontWeight:"bold"}}>{message}</h3>
                      )}
                      <div className="form-group">
                        <label htmlFor="groupName">Nom du groupe</label>
                        <input type="text" className="form-control" id="groupName" placeholder="Entrez le nom du groupe" value={groupName} onChange={(e) => setGroupName(e.target.value)} />
                      </div>
                      <div className="form-group">
                        <label htmlFor="descriptionGroup">Description du groupe</label>
                        <textarea className="form-control" id="descriptionGroup" name="descriptionGroup" placeholder="Description du groupe" value={descriptionGroup} onChange={(e) => setDescriptionGroup(e.target.value)}></textarea>
                      </div>
                    </form>
                  </div>
                  <div className="modal-footer">
                    <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Fermer</button>
                    <button type="button" className="btn btn-primary" onClick={handleFormSubmit}>Enregistrer</button>
                  </div>
                </div>
              </div>
            </div>

          </nav>
        </div>
        {/* <!-- End Page Title --> */}

        <section className="section">
          <div className="row">
            <div className="col-lg-6">
              <div className="card">
                <DataTable value={groups} selectionMode="single" selection={selectedGroup} onSelectionChange={(e) => setSelectedGroup(e.value)}>
                  <Column  headerStyle={{ width: '3rem' }} />
                  <Column field="id" header="ID" sortable />
                  <Column field="name" header="Nom" sortable />
                  <Column field="description" header="Description" body={rowData => truncateDescription(rowData.description)} />
                  <Column field="created_at" header="Date creation"   body={(rowData) => {
                    return new Date(rowData.created_at).toLocaleString('fr-FR', {
                      day: 'numeric',
                      month: 'numeric',
                      year: 'numeric',
                      // hour: '2-digit',
                      // minute: '2-digit'
                    });
                  }}sortable />
                  <Column field="users_count" header="Nombres d'utilisateurs" sortable />
                  {/* <Column header="Actions" body={(rowData) => (
                    <div className="d-flex justify-content-between">
                      <button className="btn btn-sm btn-primary" onClick={() => {
                        setSelectedGroup(rowData);
                        setGroupName(rowData.name);
                        setDescriptionGroup(rowData.description);
                        setShowUpdateModal(true);
                      }}>Modifier</button>
                      <button className="ml-1 btn btn-sm btn-danger" onClick={() => handleDeleteGroup(rowData)}>Supprimer</button>
                    </div>
                  )} /> */}
                </DataTable>
              </div>
            </div>

            <div className="col-lg-6">
              <div className="card">
                <div className="card-body">
                  <h5 className="card-title">Details du groupe</h5>
                  {selectedGroup && (
                    <div className="p-col">
                      <GroupDetailCard groupDetail={selectedGroup} />
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Modal pour la modification */}
        <div className={`modal fade ${showUpdateModal ? 'show' : ''}`} style={{ display: showUpdateModal ? 'block' : 'none' }} id="updateModal" tabIndex="-1" aria-labelledby="updateModalLabel" aria-hidden={!showUpdateModal}>
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title" id="updateModalLabel">Modifier le groupe</h5>
                <button type="button" className="btn-close" onClick={() => setShowUpdateModal(false)}></button>
              </div>
              <div className="modal-body">
                <form>
                  <div className="form-group">
                    <label htmlFor="updateGroupName">Nom du groupe</label>
                    <input type="text" className="form-control" id="updateGroupName" value={groupName} onChange={(e) => setGroupName(e.target.value)} />
                  </div>
                  <div className="form-group">
                    <label htmlFor="updateDescriptionGroup">Description du groupe</label>
                    <textarea className="form-control" id="updateDescriptionGroup" value={descriptionGroup} onChange={(e) => setDescriptionGroup(e.target.value)}></textarea>
                  </div>
                </form>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => setShowUpdateModal(false)}>Fermer</button>
                <button type="button" className="btn btn-primary" onClick={handleUpdateGroup}>Enregistrer</button>
              </div>
            </div>
          </div>
        </div>

      </main>
      {/* !-- End #main --> */}

      {/* <!-- ======= Footer ======= --> */}
      <footer id="footer" className="footer">
        <div className="copyright">
          &copy; Copyright <strong><span>MyAPp</span></strong>. All Rights Reserved
        </div>
        <div className="credits">
          Designed by <a href="https://bootstrapmade.com/">Jbbonice2 && SergeNoah000</a>
        </div>
      </footer>
      {/* <!-- End Footer --> */}

      <a href="#" className="back-to-top d-flex align-items-center justify-content-center"><i className="bi bi-arrow-up-short"></i></a>

    </>
  );
};

export default Group;
