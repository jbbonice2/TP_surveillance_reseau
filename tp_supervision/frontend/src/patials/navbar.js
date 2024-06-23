import React, { useEffect, useState } from 'react';
import axios from 'axios'
const NavBar = ()=>{
  const [userInfo, setUserInfo] = useState(null);
  const [loaded, setLoaded] = useState(false)

  const getUserInfo = async()=>{
    const token = sessionStorage.getItem('token');
    if(!token){
      window.location.href = '/login';
    }
    await axios.post(`http://localhost:8000/user_info/` , {token:token})
    .then((res)=>{
      setUserInfo(res.data)
    })
    .catch((error)=>{
      console.log(error);
    })
  }
  useEffect(()=>{
    if (!loaded ) {
      getUserInfo();
      setLoaded(true);
    }
  });
    return(
        <>
              {/* <!-- ======= Header ======= --> */}
          <header id="header" class="header fixed-top d-flex align-items-center">

            <div class="d-flex align-items-center justify-content-between">
              <a href="/" class="logo d-flex align-items-center">
                <img src="assets/img/logo.png" alt=""/>
                <span class="d-none d-lg-block">MyApp</span>
              </a>
              <i class="bi bi-list toggle-sidebar-btn"></i>
            </div>
            {/* <!-- End Logo --> */}

            <div class="search-bar">
              <form class="search-form d-flex align-items-center" method="POST" action="#">
                <input type="text" name="query" placeholder="Search" title="Enter search keyword"/>
                <button type="submit" title="Search"><i class="bi bi-search"></i></button>
              </form>
            </div>
            {/* <!-- End Search Bar --> */}

            <nav class="header-nav ms-auto">
              <ul class="d-flex align-items-center">

                <li class="nav-item d-block d-lg-none">
                  <a class="nav-link nav-icon search-bar-toggle " href="#">
                    <i class="bi bi-search"></i>
                  </a>
                </li>
                {/* <!-- End Search Icon--> */}

                <li class="nav-item dropdown">

                  <a class="nav-link nav-icon" href="#" data-bs-toggle="dropdown">
                    <i class="bi bi-bell"></i>
                    <span class="badge bg-primary badge-number">1</span>
                  </a>
                  {/* <!-- End Notification Icon --> */}

                  <ul class="dropdown-menu dropdown-menu-end dropdown-menu-arrow notifications">
                    <li class="dropdown-header">
                      VOus avez 1 notification
                      <a href="#"><span class="badge rounded-pill bg-primary p-2 ms-2">Voir tout</span></a>
                    </li>
                    <li>
                      <hr class="dropdown-divider"/>
                    </li>
                  </ul>
                  {/* <!-- End Notification Dropdown Items --> */}

                </li>
                {/* <!-- End Notification Nav --> */}


                <li class="nav-item dropdown pe-3">

                  <a class="nav-link nav-profile d-flex align-items-center pe-0" href="#" data-bs-toggle="dropdown">
                    <img src="assets/img/profile-img.jpg" alt="Profile" class="rounded-circle"/>
                    <span class="d-none d-md-block dropdown-toggle ps-2">{userInfo && userInfo.first_name && userInfo.last_name && (userInfo.first_name+ " " + userInfo.last_name)}</span>
                  </a>
                  {/* <!-- End Profile Iamge Icon --> */}

                  <ul class="dropdown-menu dropdown-menu-end dropdown-menu-arrow profile">
                    <li class="dropdown-header">
                      <h6>{userInfo && userInfo.first_name && userInfo.last_name && (userInfo.first_name+ " " + userInfo.last_name)}</h6>
                      <span>Utilisateur</span>
                    </li>
                    <li>
                      <hr class="dropdown-divider"/>
                    </li>

                    <li>
                      <a class="dropdown-item d-flex align-items-center" href="/profile">
                        <i class="bi bi-person"></i>
                        <span>Mon Profile</span>
                      </a>
                    </li>
                    <li>
                      <hr class="dropdown-divider"/>
                    </li>
                    
                   
                    <li>
                      <a class="dropdown-item d-flex align-items-center" onClick={()=>{sessionStorage.removeItem('token'); window.location.href='/login';}}href="#">
                        <i class="bi bi-box-arrow-right"></i>
                        <span>Deconnexion</span>
                      </a>
                    </li>

                  </ul>
                  {/* <!-- End Profile Dropdown Items --> */}
                </li>
                {/* <!-- End Profile Nav --> */}

              </ul>
            </nav>
            {/* <!-- End Icons Navigation --> */}

          </header>
          {/* <!-- End Header --> */}

        </>
    )
}

export default NavBar;