import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import LoginPages from "./pages/LoginPages.jsx";
import Perfil from "./pages/Perfil.jsx";
import CadastroPage from "./pages/CadastroPage.jsx";

const router = createBrowserRouter([
  {
    path: "/",
    element: <LoginPages />,
  },

  {
    path: "/chat",
    element: <App />,
  },

  {
    path: "/perfil",
    element: <Perfil />,
  },

  {
    path: "/cadastro",
    element: <CadastroPage />,
  },
]);

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);
