import { useNavigate } from "react-router-dom";
import { useState } from "react";

function LoginPages() {
   const [email, setEmail] = useState("");
   const [password, setPassword] = useState("");
     
    

  const navigate = useNavigate()
  
    const handleLoginClick = async () => {

      if(!email.trim() || !password.trim()) {
          return alert("Preencha todos os campos."); 
        } 

      try {
        const response = await fetch(
         `${import.meta.env.VITE_USERS_API_URL}/users/login`,
         {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email,
            password,
          }),

         }

        );

        const data = await response.json();

        if (response.ok) {
            console.log(data);

            localStorage.setItem("usuario", JSON.stringify(data.usuario));
            localStorage.setItem("isLogged", "true")


            setEmail("");
            setPassword("");
            navigate("/chat");  
        } else {
          alert(data.message);
        }
      }catch (error) {
        console.error(error);
        alert("Erro ao conectar com a API.");
      }
    
    };

  
  return (
    <div className=" w-screen h-screen  flex items-center justify-center bg-sky-900 p-6">
      <div className="  w-85 h-100 bg-sky-200 rounded-md p-6  space-y-25">
        <input
        type="email"
        placeholder="Digite o seu e-mail"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="mr-2 bg-slate-100 p-2 rounded-md w-75 border "/>

        <input 
        type="password"
        placeholder="Digite a sua senha"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="mr-2 bg-slate-100 p-2 rounded-md w-75 border" />

        <button 
         onClick={()=> {
        

         handleLoginClick ();
          }}
        className="bg-slate-300 p-2 rounded-md w-75 border">Entrar</button>


        <button 
         onClick={() => navigate("/cadastro")}
         className="bg-slate-300 p-2 rounded-md w-75 border">Criar Conta</button>
        
        </div>
      
    </div>
  );
}

export default LoginPages;
