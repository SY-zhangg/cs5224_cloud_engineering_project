import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './pages/App';
import SearchResultPage from './pages/SearchResultPage';
import Register from './components/Register';
import LoginPage from './pages/LoginPage';
import Header from './components/header';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css'

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
      <Header />
      <Routes>
        <Route exact path='/' element={<App />}></Route>
        <Route exact path='/search-result-page' element={<SearchResultPage />}></Route>
        <Route exact path='/profile' element={<LoginPage />}></Route>
        <Route path="/register" element={<Register />} />
      </Routes>
    </Router>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
