import {BrowserRouter, Routes, Route } from 'react-router-dom'
import Login from './components/login';
import Register from './components/register';
import NotFound from './components/404';
import Home from './components/home';
import Profile from './components/profile';
import Group from './components/groups';


function App() {
  return (
    <div>
      <BrowserRouter>
        <Routes>
            <Route index element={<Home />} />
            <Route path='/Home' element={<Home/>}/>
            <Route path='/register' element={<Register/>} />
            <Route path='/login' element={<Login/>} />
            <Route path='/profile' element={<Profile/>} />
            <Route path='/groups' element={<Group/>} />
            {/* <Route path='/profile/:id' element={<Profile/>} />  */}
            <Route path='*' element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
