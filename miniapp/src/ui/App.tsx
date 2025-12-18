import { useEffect } from "react";
import WebApp from "@twa-dev/sdk";
import PlaceCard from "./PlaceCard";
import SwipeActions from "./SwipeActions";
import "./styles.css";

function App() {
  useEffect(() => {
    WebApp.ready();
  }, []);

  return (
    <div className="app">
      <header>
        <h1>Go Out Today</h1>
        <p>Свайпай места, получай совпадения с друзьями.</p>
      </header>
      <PlaceCard />
      <SwipeActions />
    </div>
  );
}

export default App;
