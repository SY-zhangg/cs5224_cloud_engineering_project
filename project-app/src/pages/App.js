import React from "react";
import '../css/App.css';

function App() {
  React.useEffect(() => {
    fetch("https://test-vedhika.d186pebvqnkz8n.amplifyapp.com/setup/", {
      method: 'POST',
      ReferrerPolicy: "origin-when-cross-origin",
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome</h1>
        Please navigate through the nav bar on top.
      </header>
    </div>
  );
}

export default App;
