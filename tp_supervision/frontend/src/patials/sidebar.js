import React from "react";


const SideBar =()=>{
    return (
        <>
              {/* <!-- ======= Sidebar ======= --> */}
            <aside id="sidebar" class="sidebar">

                <ul class="sidebar-nav" id="sidebar-nav">

                <li class="nav-item">
                    <a class="nav-link collapsed" href="/">
                    <i class="bi bi-grid"></i>
                    <span>Accueil</span>
                    </a>
                </li>
                <li class="nav-item">
                    <a class="nav-link collapsed" data-bs-target="#charts-nav" data-bs-toggle="collapse" href="#">
                    <i class="bi bi-bar-chart"></i><span>Groupes</span><i class="bi bi-chevron-down ms-auto"></i>
                    </a>
                    <ul id="charts-nav" class="nav-content collapse " data-bs-parent="#sidebar-nav">
                    <li>
                        <a href="/groups">
                        <i class="bi bi-circle"></i><span>Liste</span>
                        </a>
                    </li>
                    <li>
                        <a href="#">
                        <i class="bi bi-circle"></i><span>Ajout</span>
                        </a>
                    </li>
                    
                    </ul>
                </li>

      


                </ul>

            </aside>
            {/* <!-- End Sidebar--> */}

        </>

    );
};

export default SideBar;