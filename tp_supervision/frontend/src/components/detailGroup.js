import React, { useState } from 'react';
import { Card } from 'primereact/card';
import { Button } from 'primereact/button';
import axios from 'axios';

const GroupDetailCard = ({ groupDetail }) => {
    const [users, setUsers] = useState(null);
    const [message, setMessage] = useState(null);
    const [message1, setMessage1] = useState(null);
    const [group, setGroup] = useState(groupDetail)
    const [search, setSearch] = useState(null);
    const [selectedUser, setSelectedUser] = useState(null);
    const [selectedUserToDelete, setSelectedUserToDelete] = useState(null)



    const handleChange = (e) => {
        const { name, value } = e.target;
        setGroup(prevState => ({
            ...prevState,
            [name]: value
        }));
    };
    const get_users = async (s) => {
        setMessage(null)
        const token = sessionStorage.getItem('token');
        if (!token) {
            window.location.href = '/login';
        }
        axios.get(`http://localhost:8000/get_users/${token}/${s}`)
            .then((res) => {
                setUsers(res.data);
            })
            .catch((err) => {
                console.log(err);
                setMessage(err?.data?.message);
                setTimeout(() => {
                    setMessage('');
                }, 5000);
            })
    }



  const handleUpdateGroup = async (e) => {
    e.preventDefault();
    try {
        
      const response = await axios.put(`http://localhost:8000/update_detail/${group.id}`, {
        name: group.name,
        description: group.description
      });
      setGroup(response.data);
      setMessage1("Operation reussie !");
      setTimeout(() => {
        setMessage1('');
    }, 5000);
    } catch (error) {
      console.error('Error updating group:', error);
        setMessage(error.message);
        setTimeout(() => {
          setMessage('');
      }, 5000);
    }
  };

  const handleDeleteGroup = async () => {
    try {
        const msg = prompt("Confimer la suppression du groupe (O/N):");
        if (msg === "n" || msg === 'N' || msg === "Non" || msg === "NON") {
            return;
        }
      await axios.delete(`http://localhost:8000/delete_detail/${group.id}`);
      setMessage1('Groupe supprime.');
      setTimeout(() => {
        setMessage1('');
    }, 5000);
    } catch (error) {
      console.error('Error deleting group:', error);
      setMessage(error.message);
      setTimeout(() => {
        setMessage('');
    }, 5000);
    }
  };


    const handleAddUserSubmit = async () => {
        try {
            setMessage(null);
            const token = sessionStorage.getItem('token');
            if (!token) {
                window.location.href = '/login';
                return;
            }
            const response = await axios.put(`http://localhost:8000/add_user_group/${token}`, { user: selectedUser.id, group: group.id });
            setMessage(response.data.message);
            setTimeout(() => {
                setMessage('');
            }, 5000);
        } catch (error) {
            console.error(error);
        }
    };

    const handleDeleteUserSubmit = async () => {
        try {
            setMessage(null);
            const token = sessionStorage.getItem('token');
            if (!token) {
                window.location.href = '/login';
                return;
            }
            const  data = { user: selectedUserToDelete.id, group: group.id };
            console.log(data);
            const response = await axios.delete(`http://localhost:8000/remove_user_from_group/${token}/${selectedUserToDelete.id}/${group.id}`,);
            console.log("user:", response.user , response.group)
            setMessage(response.data.message);
            setTimeout(() => {
                setMessage('');
            }, 5000);

        } catch (error) {
            console.error(error);
        }
    };

    return (
        <Card title={`Group Details - ${group.name}`} className="p-shadow-4">
            <span style={{position:"relative", left:'85%', top:'-12%'}} onClick={handleDeleteGroup} className='btn btn-danger'><i className='bi bi-trash'></i></span>
            <div>
                {message1 && (
                    <h3 style={{color:"violet", fontWeight:"bold"}}>{message1}</h3>
                )}
                <form onSubmit={handleUpdateGroup}>
                    <div>
                        <span className='form-group'>
                            <label htmlFor="name">Nom</label>
                            <input className='form-control' id="name" name='name' onChange={handleChange} type="text" value={group.name}  />
                        </span>
                    </div>
                    <div>
                        <span className="form-groupl">
                            <label htmlFor="description">Description</label>
                            <input className='form-control' id="description"  onChange={handleChange} type="text" value={group.description}  />
                        </span>
                    </div>

                    <button style={{position:"relative", left:'40%', marginTop:"2%", marginBottom:"4%"}} className='btn btn-info'>Enregistrer</button>
                </form>
                
            </div>
            <div className="p-d-flex p-ai-center p-jc-between">
                <Button label="Ajouter un Utilisateur" className="ml-8 mt-2 btn btn-info btn-add-user" data-bs-toggle="modal" data-bs-target="#addUserModal" />
                <Button label="Supprimer un Utilisateur" className="ml-5 mt-2 btn btn-danger btn-remove-user" data-bs-toggle="modal" data-bs-target="#deleteUserModal" />
                <div className="modal fade" id="addUserModal" tabIndex="-1" style={{ "display": "none" }} aria-hidden="true">
                    <div className="modal-dialog modal-dialog-centered">
                        <div className="modal-content">
                            <div className="modal-header">
                                <h5 className="modal-title">Ajouter un utilisateur</h5>
                                <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div className="modal-body">
                                <form>
                                    {message && (
                                        <h3 style={{ color: "violet" }}>{message}</h3>
                                    )}
                                    <div className="form-group">
                                        <input type="text" className="form-control" id="groupName" placeholder="Entrez son nom " value={search} onChange={(e) => { setSearch(e.target.value); get_users(search ? search : null) }} />
                                    </div>
                                    {users?.map((user, index) => (
                                        <span className='text-muted btn' style={{backgroundColor: user === selectedUser ? "blue": ""}} onClick={() => setSelectedUser(user)} key={index}>{user.last_name} {user.first_name}, {user.email}</span>
                                    ))}
                                </form>
                            </div>
                            <div className="modal-footer">
                                <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Fermer</button>
                                <button type="button" className="btn btn-primary" onClick={handleAddUserSubmit}>Enregistrer</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="modal fade" id="deleteUserModal" tabIndex="-1" style={{ "display": "none" }} aria-hidden="true">
                    <div className="modal-dialog modal-dialog-centered">
                        <div className="modal-content">
                            <div className="modal-header">
                                <h5 className="modal-title">Supprimer un utilisateur</h5>
                                <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div className="modal-body">
                                <form>
                                    {message && (
                                        <h3 style={{ color: "violet" }}>{message}</h3>
                                    )}
                                    <div className="form-group">
                                        <input type="text" className="form-control" id="groupName" placeholder="Entrez son nom " value={search} onChange={(e) => { setSearch(e.target.value); get_users(search ? search : null) }} />
                                    </div>
                                    {users &&users.map((user, index) => (
                                        <span className='text-muted btn' style={{backgroundColor: user === selectedUserToDelete ? "blue": ""}} onClick={() => setSelectedUserToDelete(user)} key={index}>{user.last_name} {user.first_name}, {user.email}</span>
                                    ))
                                    // : group.users?.map((user, index)=>(
                                    //     <span className='text-muted btn' onClick={() => setSelectedUserToDelete(user)} key={index}>{user.last_name} {user.first_name}, {user.email}</span>
                                    // ))
                                    }
                                </form>
                            </div>
                            <div className="modal-footer">
                                <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Fermer</button>
                                <button type="button" className="btn btn-danger" onClick={handleDeleteUserSubmit}>Supprimer</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div className="p-pt-3">
                <h5>Membres du Group</h5>
                <ul>
                    {group?.users?.map(user => (
                    
                        <li key={user.id}>{user.first_name} {user.last_name} ({user.email}) 
                            {/* <span className='icon text-danger'><i className='bi bi-trash'></i> </span> */}
                        </li>
                    ))}
                </ul>
            </div>
        </Card>
    );
};

export default GroupDetailCard;
