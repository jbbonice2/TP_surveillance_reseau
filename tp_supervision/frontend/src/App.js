import {BrowserRouter, Routes, Route } from 'react-router-dom'
import Login from './components/login';
import Register from './components/register';
import NotFound from './components/404';
import Home from './components/home';
import Profile from './components/profile';
import Group from './components/groups';
import DetailMachine from './components/detailmachine';
import Listemachine from './components/listemachine';
import React from 'react';
import VarMachine from './components/detailmachineTest';
import DetailGraphMachine from './components/detailGraphmachine';






function App() {
  return (
    <div>
      <BrowserRouter>
        <Routes>
            <Route index element={<Listemachine />} />
            <Route path='/listemachine' element={<Listemachine/>}/>
            <Route path='/register' element={<Register/>} />
            <Route path='/login' element={<Login/>} />
            <Route path='/profile' element={<Profile/>} />
            <Route path='/groups' element={<Group/>} />
            <Route path='/test/:id' element={<VarMachine/>} />
            <Route path="/detailmachine/:id" element={<DetailMachine />} />
            <Route path="/detailgraph/:id" element={<DetailGraphMachine />} />
            {/* <Route path='/profile/:id' element={<Profile/>} />  */}
            <Route path='*' element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;