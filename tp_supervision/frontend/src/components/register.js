import React, {useEffect, useState, } from "react";
import axios from "axios";
import  ENCRYPTION_KEY  from "../utils/password";
import encryptTextWithKey from "../utils/encryption";


const Register = ()=>{

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [message, setMessage] = useState('');
    const [showMessage, setShowMessage] = useState(false);
    const [loaded , setLoaded] = useState(false);


    const handleSubmit =  async (e)=>{
        e.preventDefault();
        setMessage('')
        setShowMessage(false)
        if( password !== confirmPassword ){
            setMessage("Les deux mot de passe ne correspondent pas");
            setShowMessage(true);
            return;
        }
        const encrypte_p = encryptTextWithKey(password, ENCRYPTION_KEY);
        await axios.post("http://localhost:8000/users/registera/", {
            username: username,
            password: encrypte_p,
            first_name: firstName,
            last_name: lastName
        }).then((res)=>{
            console.log(res);
            if(res.status === 201){
                setMessage("User created successfully");
                window.location = "/Home";
            }
            else if(res.status === 400){
                setMessage("User already exists");
            }
            
           setConfirmPassword('');
           setUsername('');
           setPassword('');
           setFirstName('');
           setLastName('');
           setMessage('');
           window.location = "/login";
        }).catch ((error)=> {
            console.error("Network request failed:", error);
            setMessage('Une erreur s\'est produite');
            // Handle the error, e.g., display an error message to the user
        })
    }

  
    useEffect(()=>{
        document.title = "Enregistrement | MyApp";
        
            setLoaded(true)
    })
    return (
       
               
                <main>
                     {!loaded &&
                    (<>
                        <div class="loading">Loading&#8230;</div>
                        <div class="content"><h3>Patientez ..</h3></div>
                    </>
                )}
                    <div class="container">

                    <section class="section register min-vh-100 d-flex flex-column align-items-center justify-content-center py-4">
                        <div class="container">
                        <div class="row justify-content-center">
                            <div class="col-lg-4 col-md-6 d-flex flex-column align-items-center justify-content-center">

                            <div class="d-flex justify-content-center py-4">
                                <a href="index.html" class="logo d-flex align-items-center w-auto">
                                <img src="assets/img/logo.png" alt=""/>
                                <span class="d-none d-lg-block">MyApp</span>
                                </a>
                            </div>
                            {/* <!-- End Logo --> */}

                            <div class="card mb-3">

                                <div class="card-body">

                                <div class="pt-4 pb-2">
                                    <h5 class="card-title text-center pb-0 fs-4">Enregistrement dans MyApp</h5>
                                    <p class="text-center small">Entrer vos information pour commencer.</p>
                                </div>
                                {message && showMessage && (
                                    <div class="alert alert-warning alert-dismissible fade show" role="alert">
                                        <strong>Erreur</strong>{message}
                                        <span type="button" onClick={()=>{setShowMessage(false)}}class="close" data-dismiss="alert" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                        </span>
                                  </div>
                                )}

                                <form class="row g-3 needs-validation" onSubmit={handleSubmit}novalidate>

                                    <div class="col-12">
                                    <label for="nom" class="form-label">Nom</label>
                                    <div class="input-group has-validation">
                                        
                                        <input value={firstName} onChange={(e)=>{setFirstName(e.target.value)}} type="text" name="nom" class="form-control" id="nom" required/>
                                        <div class="invalid-feedback">Veuillez remplir ce champ.</div>
                                    </div>
                                    </div>

                                    <div class="col-12">
                                    <label for="nom" class="form-label">Prénom</label>
                                    <div class="input-group has-validation">
                                        <input  value={lastName} onChange={(e)=>{setLastName(e.target.value)}}type="text" name="prenom" class="form-control" id="prenom" required/>
                                        <div class="invalid-feedback">Veuillez remplir ce champ.</div>
                                    </div>
                                    </div>

                                    <div class="col-12">
                                    <label for="username" class="form-label">username</label>
                                    <div class="input-group has-validation">
                                        <span class="input-group-text" id="inputGroupPrepend">@</span>
                                        <input value={username} onChange={(e)=>{setUsername(e.target.value)}}  type="text" name="username" class="form-control" id="username"  placeholder="username"required/>
                                        <div class="invalid-feedback">Entrez un username valide.</div>
                                    </div>
                                    </div>

                                    <div class="col-12">
                                    <label for="yourPassword" class="form-label">Mot de passe</label>
                                    <input  value={password} onChange={(e)=>{setPassword(e.target.value)}}type="password" name="password" class="form-control" id="yourPassword" required/>
                                    <div class="invalid-feedback">Veuillez entrer un mot de passe valide</div>
                                    </div>

                                    <div class="col-12">
                                    <label for="yourPassword" class="form-label">Confirmez Mot de passe</label>
                                    <input value={confirmPassword} onChange={(e)=>{setConfirmPassword(e.target.value)}} type="password" name="password" class="form-control" id="yourPassword" required/>
                                    <div class="invalid-feedback">Les deux mots de passes ne correspondent pas.</div>
                                    </div>

                                    
                                    <div class="col-12">
                                    <button class="btn btn-primary w-100" type="submit">Enregistrer</button>
                                    </div>
                                    <div class="col-12">
                                    <p class="small mb-0">Vous avez déjà un compte ? <a href="/login">Connectez-vous.</a></p>
                                    </div>
                                </form>

                                </div>
                            </div>

                            <div class="credits">
                                {/* <!-- All the links in the footer should remain intact. -->
                                <!-- You can delete the links only if you purchased the pro version. -->
                                <!-- Licensing information: https://bootstrapmade.com/license/ -->
                                <!-- Purchase the pro version with working PHP/AJAX contact form: https://bootstrapmade.com/nice-admin-bootstrap-admin-html-template/ --> */}
                                Fait <a href="https://github.com/jbbonice2">Jbbonice2 && SergeNoah000</a>
                            </div>

                            </div>
                        </div>
                        </div>

                    </section>

                    </div>
                </main>

                
    );
};

export default Register;