
import foto from "../img/fotoDePerfil.jpg";
import { useSelector } from "react-redux";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { logout } from "../redux/userSlice";


function Perfil() {

  const usuario = useSelector((state) => state.user.user)

  const dispatch = useDispatch();
 
  const handleLogout = () => {
    dispatch(logout());

    localStorage.removeItem("usuario");
    localStorage.removeItem("isLogged");

    Navigate("/");
  }
  

  return (
    <div className="w-screen h-screen flex flex-col items-center justify-center bg-sky-100">
      <h1 className="text-3xl font-bold mb-6">
        Perfil
      </h1>

      <div className="bg-slate-100 p-6 rounded-lg shadow-md w-1/2 h-[80%]">
        <img
          src={foto}
          alt="Foto de perfil"
          title="Sua foto"
          className="w-40 h-40 rounded-full object-cover mx-auto"
        />

        <div className="space-y-4 mt-6">
          <div className="bg-sky-200 p-4 rounded-xl">
            <p>Nome: {usuario?.name}</p>
          </div>

          <div className="bg-sky-200 p-4 rounded-xl">
            <p>Email: {usuario?.email}</p>
          </div>

          <div className="bg-sky-200 p-4 rounded-xl">
            <p>Cargo:{usuario?.role}</p>  
          </div>

          <div>
            <button className="bg-sky-300 p-4 rounded-xl" onClick={handleLogout}>Sair</button>
            </div>
        </div>
      </div>
    </div>
  );
}

export default Perfil;