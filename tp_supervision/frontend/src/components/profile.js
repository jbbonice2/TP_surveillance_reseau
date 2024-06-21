import React, { useEffect, useState } from "react";
import NavBar from '../patials/navbar';
import SideBar from '../patials/sidebar';
import axios from "axios";
import encryptTextWithKey from "../utils/encryption";
import ENCRYPTION_KEY from "../utils/password";


const Profile = ()=>{
    const [userInfo, setUserInfo]  = useState(null);
    const [loaded, setLoaded] = useState(false);
    const [image_profile, setImageProfile] = useState();
    const [newPassword, setnewPassword] = useState(null);
    const [currentPassword, setcurrentPassword] = useState(null);
    const [renewPassword, setrenewPassword] = useState(null);
    const [showMessage, setShowMessage] = useState(false);
    const [message, setMessage] = useState(false);



    const [loading, setLoading] = useState(false);
    const [totalRecords, setTotalRecords] = useState(0);
    const [selectedGroups, setSelectedGroups] = useState([]); 


    const handleChange = (e) => {
        const { name, value } = e.target;
        setUserInfo(prevState => ({
            ...prevState,
            [name]: value
        }));
    };
    const handleUserInfo = async()=>{
        const token = sessionStorage.getItem('token');
        if(!token){
            window.location.href = '/login';
        }
        // console.log(actualUser);
        axios.post(`http://localhost:8000/user_info/`, 
           
             {token:token})
             .then((response) => {
                setUserInfo(response.data);
                
              })
              .catch((err) => {
                console.error( err);
              });
    };


    // Fonction pour mettre à jour le profil utilisateur
const updateUserProfile = async ( formData) => {
    const token = sessionStorage.getItem('token');
        if(!token){
            window.location.href = '/login';
        }
        // Construire l'URL avec l'ID de l'utilisateur
    const url = `http://localhost:8000/user_update/${token}/`;

    // Envoi de la requête POST avec Axios
     await axios.put(url, formData)
     .then((res)=>{
        setUserInfo(res.data);
     })
     .catch((err)=>{
        console.log(err);
     })
        
};

    // Fonction pour mettre à jour le profil utilisateur
    const userDelete = async ( ) => {
        const token = sessionStorage.getItem('token');
            if(!token){
                window.location.href = '/login';
            }
            // Construire l'URL avec l'ID de l'utilisateur
        const url = `http://localhost:8000/user_delete/${token}/`;
    
        // Envoi de la requête POST avec Axios
         await axios.delete(url)
         .then((res)=>{
            setUserInfo(res.data);
            window.location.href = '/login';
         })
         .catch((err)=>{
            console.log(err);
         })
            
    };
    

      // Fonction pour mettre à jour le profil utilisateur
      const changepassword = async (e ) => {
        e.preventDefault();
        setMessage('')
        setShowMessage(false)
        if( renewPassword !== newPassword ){
            setMessage("Les deux mot de passe ne correspondent pas");
            setShowMessage(true);
            return;
        }
        const token = sessionStorage.getItem('token');
            if(!token){
                window.location.href = '/login';
            }
            const encrypte_p = encryptTextWithKey(currentPassword, ENCRYPTION_KEY);
            const encrypte_n = encryptTextWithKey(newPassword, ENCRYPTION_KEY);

            const data = {
                currentpassword: encrypte_p,
                newpassword: encrypte_n,
            };
        

            // Construire l'URL avec l'ID de l'utilisateur
        const url = `http://localhost:8000/change_password/${token}/`;
    
        // Envoi de la requête POST avec Axios
         await axios.put(url, data)
         .then((res)=>{
            setMessage(res.data.message);
            setShowMessage(true);
            setnewPassword('');
            setcurrentPassword('');
            setrenewPassword('');
         })
         .catch((err)=>{
            console.log(err);
         })
            
    };
    

// Gestionnaire de soumission du formulaire
const handleSubmit = (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    formData.append("image_profile", image_profile)
    updateUserProfile( formData)
        .then(data => {
            handleUserInfo();
        })
        .catch(error => {
            console.log(error);
        });
};

    useEffect(()=>{
        if (!loaded) {
        handleUserInfo();
        setLoaded(true);
        }
        
    }, [loaded]);
    return(
        <>
            <NavBar/>
            <SideBar />
            <main id="main" class="main">

                
            {userInfo ? (
                <>
                <section class="section profile">
                <div class="row">
                    <div class="col-xl-4">

                    <div class="card">
                        <div class="card-body profile-card pt-4 d-flex flex-column align-items-center">

                        <img src={userInfo && userInfo.first_name && userInfo.last_name && (userInfo.first_name+ " " + userInfo.last_name)} style={{maxWidth:'100%'}}  alt="Profile" class="rounded-circle" />
                        <h2>{userInfo && userInfo.first_name && userInfo.last_name && (userInfo.first_name+ " " + userInfo.last_name)}</h2>
                        {/* <h3></h3>
                        <div class="social-links mt-2">
                            <a href={""} target="blank" class="twitter ml-2"><i class="bi bi-twitter"></i></a>
                            <a href={""} target="blank" class="facebook"><i class="bi bi-facebook"></i></a>
                            <a href={""} target="blank" class="instagram"><i class="bi bi-instagram"></i></a>
                            <a href={""} target="blank" class="linkedin"><i class="bi bi-linkedin"></i></a>
                            
                        </div> */}
                        </div>
                    </div>

                    </div>

                    <div class="col-xl-8">

                    <div class="card">
                        <div class="card-body pt-3">
                        {/* <!-- Bordered Tabs --> */}
                        <ul class="nav nav-tabs nav-tabs-bordered" role="tablist">

                            <li class="nav-item" role="presentation">
                            <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#profile-overview" aria-selected="false" role="tab" tabindex="-1">Informations</button>
                            </li>

                            <li class="nav-item" role="presentation">
                            <button class="nav-link " data-bs-toggle="tab" data-bs-target="#profile-edit" aria-selected="true"  role="tab">Editer Profile</button>
                            </li>

                            <li class="nav-item" role="presentation">
                            <button class="nav-link" data-bs-toggle="tab" data-bs-target="#settings" aria-selected="false" role="tab"  tabindex="-1">Permissions</button>
                            </li>

                            <li class="nav-item" role="presentation">
                            <button class="nav-link" data-bs-toggle="tab" data-bs-target="#profile-change-password" aria-selected="false" role="tab"   tabindex="-1">Changer Mot de passe</button>
                            </li>

                        </ul>
                        <div class="tab-content pt-2">

                            <div class="tab-pane fade profile-overview active show" id="profile-overview" role="tabpanel">
                            

                            <h5 class="card-title"> Details du Profil</h5>

                            <div class="row">
                                <div class="col-lg-3 col-md-4 label ">Nom </div>
                                <div class="col-lg-9 col-md-8">{userInfo && userInfo.first_name  && (userInfo.first_name)}</div>
                            </div>

                            <div class="row">
                                <div class="col-lg-3 col-md-4 label">Prenom</div>
                                <div class="col-lg-9 col-md-8">{userInfo && userInfo.last_name  && (userInfo.last_name)}</div>
                            </div>

                            <div class="row">
                                <div class="col-lg-3 col-md-4 label">Email</div>
                                <div class="col-lg-9 col-md-8">{userInfo && userInfo.email  && (userInfo.email)}</div>
                            </div>

                           
                            </div>

                            <div class="tab-pane fade profile-edit pt-3 " id="profile-edit" role="tabpanel">

                            {/* <!-- Profile Edit Form --> */}
                            <form  onSubmit={handleSubmit} >
                                <div class="row mb-3">
                                <label for="profileImage" class="col-md-4 col-lg-3 col-form-label">Profile Image</label>
                                <div class="col-md-8 col-lg-9">
                                    <img src="" alt="Profile"/>
                                    <div class="pt-2">
                                        <input type="file" id="profile_image_data" name="profile_image_data" onChange={(e)=>{setImageProfile(e.target.files[0])}} style={{display:"none"}}/>
                                    <span onClick={()=>{document.querySelector("#profile_image_data").click()}} class="btn btn-primary btn-sm" title="Upload new profile image"><i class="bi bi-upload"></i></span>
                                    <span  class="btn btn-danger btn-sm" title="Remove my profile image"><i class="bi bi-trash"></i></span>
                                    </div>
                                </div>
                                </div>

                                <div class="row mb-3">
                                <label for="last_name" class="col-md-4 col-lg-3 col-form-label">Nom</label>
                                <div class="col-md-8 col-lg-9">
                                    <input name="last_name" value={userInfo.last_name} onChange={handleChange} type="text" class="form-control" id="last_name"   />
                                </div>
                                </div>

                                <div class="row mb-3">
                                <label for="first_name" class="col-md-4 col-lg-3 col-form-label">Prenom</label>
                                <div class="col-md-8 col-lg-9">
                                    <input name="first_name" class="form-control" id="first_name"   onChange={handleChange}  value={userInfo.first_name}  />
                                </div>
                                </div>

                                <div class="row mb-3">
                                <label for="email" class="col-md-4 col-lg-3 col-form-label">Email</label>
                                <div class="col-md-8 col-lg-9">
                                    <input name="email" type="email" class="form-control"  value={userInfo.email} onChange={handleChange}    id="email" />
                                </div>
                                </div>


                                <div class="text-center">
                                <button type="submit" class="btn btn-primary">Enregistrer</button>
                                </div>
                            </form>
                            {/* <!-- End Profile Edit Form --> */}

                            </div>

                            <div class="tab-pane fade pt-3" id="settings" role="tabpanel">

                            {/* <!-- Settings Form --> */}
                            <form>

                                <div class="row mb-3">
                                <label for="fullName" class="col-md-4 col-lg-3 col-form-label">Email Notifications</label>
                                <div class="col-md-8 col-lg-9">
                                    <div class="form-check">
                                    <input class="form-check-input" type="checkbox" id="changesMade" checked=""/>
                                    <label class="form-check-label" for="changesMade">
                                        Changes made to your account
                                    </label>
                                    </div>
                                    <div class="form-check">
                                    <input class="form-check-input" type="checkbox" id="newProducts" checked=""/>
                                    <label class="form-check-label" for="newProducts">
                                        Information on new products and services
                                    </label>
                                    </div>
                                    <div class="form-check">
                                    <input class="form-check-input" type="checkbox" id="proOffers"/>
                                    <label class="form-check-label" for="proOffers">
                                        Marketing and promo offers
                                    </label>
                                    </div>
                                    <div class="form-check">
                                    <input class="form-check-input" type="checkbox" id="securityNotify" checked="" disabled=""/>
                                    <label class="form-check-label" for="securityNotify">
                                        Security alerts
                                    </label>
                                    </div>
                                </div>
                                </div>

                                <div class="text-center">
                                <button type="submit" class="btn btn-primary">Save Changes</button>
                                </div> 
                            </form>
                            <hr/>
                        
                            <div class="text-center">
                                <button onClick={()=>{userDelete()}} className="btn btn-danger">Supprimer compte</button>
                                </div>
                          
                            {/* <!-- End settings Form --> */}

                            </div>

                            <div class="tab-pane fade pt-3" id="profile-change-password" role="tabpanel">
                            {/* <!-- Change Password Form --> */}
                            <form onSubmit={changepassword}>
                                {message && showMessage &&(<>
                                <h3 className="text-danger">{message}</h3>
                                </>)}
                                <div class="row mb-3">
                                <label for="currentPassword" class="col-md-4 col-lg-3 col-form-label">Mot de passe actuel</label>
                                <div class="col-md-8 col-lg-9">
                                    <input name="password" type="password"  value={currentPassword} onChange={(e)=>{setcurrentPassword(e.target.value)}} class="form-control" id="currentPassword"/>
                                </div>
                                </div>

                                <div class="row mb-3">
                                <label for="newPassword" class="col-md-4 col-lg-3 col-form-label">Nouveau mot de passe</label>
                                <div class="col-md-8 col-lg-9">
                                    <input name="newpassword" type="password"  value={newPassword} onChange={(e)=>{setnewPassword(e.target.value)}} class="form-control" id="newPassword"/>
                                </div>
                                </div>

                                <div class="row mb-3">
                                <label for="renewPassword" class="col-md-4 col-lg-3 col-form-label">Confirmer mot de passe</label>
                                <div class="col-md-8 col-lg-9">
                                    <input name="renewpassword" type="password" value={renewPassword} onChange={(e)=>{setrenewPassword(e.target.value)}} class="form-control" id="renewPassword"/>
                                </div>
                                </div>

                                <div class="text-center">
                                <button type="submit" class="btn btn-primary">Changer Mot de passe</button>
                                </div>
                            </form>
                            {/* <!-- End Change Password Form --> */}

                            </div>

                        </div>
                        {/* <!-- End Bordered Tabs --> */}

                        </div>
                    </div>

                    </div>
                </div>
                </section>
                </>
            ):
            (
                <div style={{marginLeft:'50%', marginTop:'20%', marginBottom:'20%' , width:'40%', height:'40%'}}> <div  class="spinner-grow text-secondary"  role="status">
                    <span class="visually-hidden">Loading...</span>
                </div></div>
            )} 

                </main>
             {/* <Footer/> */}
        </>
    );
};

export default Profile;