import React from "react";
import SideBar from "../patials/sidebar";
import NavBar from "../patials/navbar";

const Home = ()=>{
    return (
        <>
           

            <NavBar/>
            <SideBar/>
            <main id="main" class="main">

                <div class="pagetitle">
                <h1>Blank Page</h1>
                <nav>
                    <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="index.html">Home</a></li>
                    <li class="breadcrumb-item">Pages</li>
                    <li class="breadcrumb-item active">Blank</li>
                    </ol>
                </nav>
                </div>
                {/* <!-- End Page Title --> */}

                <section class="section">
                <div class="row">
                    <div class="col-lg-6">

                    <div class="card">
                        <div class="card-body">
                        <h5 class="card-title">Example Card</h5>
                        <p>This is an examle page with no contrnt. You can use it as a starter for your custom pages.</p>
                        </div>
                    </div>

                    </div>

                    <div class="col-lg-6">

                    <div class="card">
                        <div class="card-body">
                        <h5 class="card-title">Example Card</h5>
                        <p>This is an examle page with no contrnt. You can use it as a starter for your custom pages.</p>
                        </div>
                    </div>

                    </div>
                </div>
                </section>

            </main>
                {/* !-- End #main --> */}

            {/* <!-- ======= Footer ======= --> */}
            <footer id="footer" class="footer">
                <div class="copyright">
                &copy; Copyright <strong><span>NiceAdmin</span></strong>. All Rights Reserved
                </div>
                <div class="credits">
                {/* <!-- All the links in the footer should remain intact. -->
                <!-- You can delete the links only if you purchased the pro version. -->
                <!-- Licensing information: https://bootstrapmade.com/license/ -->
                <!-- Purchase the pro version with working PHP/AJAX contact form: https://bootstrapmade.com/nice-admin-bootstrap-admin-html-template/ --> */}
                Designed by <a href="https://bootstrapmade.com/">Jbbonice2 && SergeNoah000</a>
                </div>
            </footer>
            {/* <!-- End Footer --> */}

            <a href="#" class="back-to-top d-flex align-items-center justify-content-center"><i class="bi bi-arrow-up-short"></i></a>

        </>
    );
};

export default Home;