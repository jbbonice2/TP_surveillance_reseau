import React, { useEffect, useState } from "react";
import encryptTextWithKey from "../utils/encryption";
import ENCRYPTION_KEY from "../utils/password";
import axios from 'axios';



const Login = ()=>{
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const [showMessage, setShowMessage] = useState(false);
    
        
    const handleSubmit = async (e)=>{
        e.preventDefault();
        setMessage('');
        const encrypte_p = encryptTextWithKey(password, ENCRYPTION_KEY);
       await axios.post(`http://localhost:8000/users/login`, {
            username: username,
            password: encrypte_p
    }).then((res)=>{
        console.log(res.data);
        sessionStorage.setItem('token', res.data.token);
        setUsername('');
        setPassword('');
        window.location.href = '/';
        }).catch((err)=>{
            console.log(err);
            setMessage("Username or password incorrect");
    }); 
    };
    
  

    useEffect(()=>{
        document.title = "Connexion | MyApp ";

    })
    return (
       
       
          
           <>

                <main>
                    <div class="container">

                    <section class="section register min-vh-100 d-flex flex-column align-items-center justify-content-center py-4">
                        <div class="container">
                        <div class="row justify-content-center">
                            <div class="col-lg-4 col-md-6 d-flex flex-column align-items-center justify-content-center">

                            <div class="d-flex justify-content-center py-4">
                                <a href="/" class="logo d-flex align-items-center w-auto">
                                <img src="assets/img/logo.png" alt=""/>
                                <span class="d-none d-lg-block">MyApp</span>
                                </a>
                            </div>
                            {/* <!-- End Logo --> */}

                            <div class="card mb-3">

                                <div class="card-body">

                                <div class="pt-4 pb-2">
                                    <h5 class="card-title text-center pb-0 fs-4">Connectez-vous à votre compte</h5>
                                    <p class="text-center small">Entrez votre adresse mail et votre mot de passe</p>
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
                                    <label for="yourUsername" class="form-label">Username</label>
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
                                    <div class="form-check">
                                        <input class="form-check-input" type="checkbox" name="remember" value="true" id="rememberMe"/>
                                        <label class="form-check-label" for="rememberMe">Se souvenir de moi.</label>
                                    </div>
                                    </div>
                                    <div class="col-12">
                                    <button class="btn btn-primary w-100" type="submit">Connexion</button>
                                    </div>
                                    <div class="col-12">
                                    <p class="small mb-0">Pas de compte ? <a href="/register">Créez-en un</a></p>
                                    </div>
                                </form>

                                </div>
                            </div>

                            <div class="credits">
                              
                                Designed by <a href="https://bootstrapmade.com/">Jbbonice2 && SergeNoah000</a>
                            </div>

                            </div>
                        </div>
                        </div>

                    </section>

                    </div>
                </main>
                

                <a href="#" class="back-to-top d-flex align-items-center justify-content-center"><i class="bi bi-arrow-up-short"></i></a>

               
            </>
           
    );
};

export default Login;